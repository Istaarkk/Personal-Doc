import os
import json
import yaml
import re
from collections import defaultdict, deque
from typing import Dict, Set, List, Any, Optional, Tuple

class XSOARCrawler:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        
        # Patterns pour identifier les différents types d'objets
        self.object_patterns = {
            'playbook': [
                r'playbook-(.+)\.ya?ml',
                r'.*playbook.*\.ya?ml'
            ],
            'automation': [
                r'automation-(.+)\.ya?ml',
                r'script-(.+)\.ya?ml'
            ],
            'incident_type': [
                r'incidenttype-(.+)\.json',
                r'SOC-(.+)\.json'
            ],
            'incident_field': [
                r'incidentfield-(.+)\.json',
                r'field-(.+)\.json'
            ],
            'layout': [
                r'layoutscontainer-(.+)\.json',
                r'layout-(.+)\.json'
            ],
            'widget': [
                r'widget-(.+)\.json'
            ],
            'indicator_type': [
                r'reputation-(.+)\.json',
                r'indicator-(.+)\.json'
            ],
            'classifier': [
                r'classifier-(.+)\.json'
            ],
            'mapper': [
                r'mapper-(.+)\.json'
            ]
        }
        
        # Chemins dans les objets où chercher les références
        self.reference_paths = {
            'playbook_references': [
                ['tasks', '*', 'task', 'playbookId'],
                ['tasks', '*', 'task', 'scriptId'],
                ['tasks', '*', 'task', 'script'],
                ['tasks', '*', 'scriptarguments', '*'],
                ['configuration', '*', 'defaultvalue'],
                ['inputs', '*', 'value'],
                ['outputs', '*', 'contextPath']
            ],
            'automation_references': [
                ['script', 'commands', '*', 'name'],
                ['configuration', '*', 'defaultvalue'],
                ['args', '*', 'defaultValue'],
                ['outputs', '*', 'contextPath']
            ],
            'field_references': [
                ['layouts', '*', 'sections', '*', 'fields', '*', 'fieldId'],
                ['layouts', '*', 'tabs', '*', 'sections', '*', 'fields', '*', 'fieldId'],
                ['fields', '*', 'fieldId'],
                ['extractSettings', '*', 'fieldCliName'],
                ['cliName'],
                ['name']
            ],
            'layout_references': [
                ['layout', 'sections', '*', 'fields', '*', 'fieldId'],
                ['layout', 'tabs', '*', 'sections', '*', 'fields', '*', 'fieldId'],
                ['detailsV2', 'tabs', '*', 'sections', '*', 'fields', '*', 'fieldId']
            ]
        }
        
        self.file_index = {}
        self.id_to_file = {}
        self.dependencies = defaultdict(set)
        self.reverse_dependencies = defaultdict(set)
        
    def load_file(self, file_path: str) -> Optional[Dict]:
        """Charge un fichier JSON ou YAML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.endswith('.json'):
                    return json.load(f)
                else:
                    return yaml.safe_load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de {file_path}: {e}")
            return None
    
    def normalize_id(self, obj_id: str) -> str:
        """Normalise un ID pour la recherche"""
        if not obj_id:
            return ""
        return re.sub(r'[^a-zA-Z0-9_-]', '', str(obj_id)).lower()
    
    def identify_object_type(self, filename: str) -> str:
        """Identifie le type d'objet basé sur le nom de fichier"""
        for obj_type, patterns in self.object_patterns.items():
            for pattern in patterns:
                if re.match(pattern, filename, re.IGNORECASE):
                    return obj_type
        return 'unknown'
    
    def extract_object_id(self, data: Dict, filename: str) -> str:
        """Extrait l'ID principal d'un objet"""
        # Priorité aux champs ID standards
        for id_field in ['id', 'name', 'commonfields.id']:
            if '.' in id_field:
                # Navigation dans les objets imbriqués
                keys = id_field.split('.')
                value = data
                try:
                    for key in keys:
                        value = value[key]
                    if value:
                        return str(value)
                except (KeyError, TypeError):
                    continue
            elif id_field in data and data[id_field]:
                return str(data[id_field])
        
        # Fallback sur le nom de fichier
        return filename.replace('.json', '').replace('.yml', '').replace('.yaml', '')
    
    def get_value_by_path(self, data: Any, path: List[str]) -> List[Any]:
        """Récupère les valeurs selon un chemin donné, supportant les wildcards"""
        results = []
        
        def recursive_get(obj: Any, remaining_path: List[str]):
            if not remaining_path:
                if obj and isinstance(obj, str) and obj.strip():
                    results.append(obj)
                return
            
            current_key = remaining_path[0]
            rest_path = remaining_path[1:]
            
            if current_key == '*':
                # Wildcard - itérer sur tous les éléments
                if isinstance(obj, dict):
                    for value in obj.values():
                        recursive_get(value, rest_path)
                elif isinstance(obj, list):
                    for item in obj:
                        recursive_get(item, rest_path)
            else:
                # Clé spécifique
                if isinstance(obj, dict) and current_key in obj:
                    recursive_get(obj[current_key], rest_path)
        
        recursive_get(data, path)
        return results
    
    def extract_references_from_object(self, data: Dict, obj_type: str) -> Set[str]:
        """Extrait toutes les références d'un objet selon son type"""
        references = set()
        
        # Références spécifiques au type
        if obj_type in self.reference_paths:
            for path in self.reference_paths[obj_type]:
                values = self.get_value_by_path(data, path)
                references.update(values)
        
        # Recherche générale dans tout l'objet
        references.update(self._deep_extract_references(data))
        
        # Nettoyer et filtrer les références
        cleaned_refs = set()
        for ref in references:
            if ref and isinstance(ref, str) and len(ref.strip()) > 2:
                cleaned_refs.add(ref.strip())
        
        return cleaned_refs
    
    def _deep_extract_references(self, obj: Any, depth: int = 0) -> Set[str]:
        """Extraction récursive de toutes les références potentielles"""
        if depth > 10:  # Limite de profondeur pour éviter les boucles infinies
            return set()
        
        references = set()
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                # Clés qui indiquent généralement des références
                reference_keys = {
                    'playbookid', 'scriptid', 'fieldid', 'automationid',
                    'playbook', 'script', 'field', 'automation',
                    'name', 'id', 'cliname', 'type'
                }
                
                if key.lower() in reference_keys and isinstance(value, str):
                    references.add(value)
                
                # Recherche récursive
                references.update(self._deep_extract_references(value, depth + 1))
                
        elif isinstance(obj, list):
            for item in obj:
                references.update(self._deep_extract_references(item, depth + 1))
        
        elif isinstance(obj, str) and len(obj) > 2:
            # Patterns pour identifier les références dans les chaînes
            patterns = [
                r'!([A-Za-z][A-Za-z0-9_-]*)',  # Commandes Demisto
                r'\$\{([^}]+)\}',  # Variables
                r'incident\.([a-zA-Z_][a-zA-Z0-9_]*)',  # Champs d'incident
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, obj)
                references.update(matches)
        
        return references
    
    def build_indexes(self):
        """Construit les index de fichiers et d'IDs"""
        print("Construction des index...")
        
        for filename in os.listdir(self.input_path):
            if not filename.endswith(('.json', '.yml', '.yaml')):
                continue
            
            file_path = os.path.join(self.input_path, filename)
            data = self.load_file(file_path)
            
            if not data:
                continue
            
            obj_type = self.identify_object_type(filename)
            obj_id = self.extract_object_id(data, filename)
            
            # Index principal
            self.file_index[filename] = {
                'path': file_path,
                'type': obj_type,
                'id': obj_id,
                'data': data
            }
            
            # Index ID vers fichier
            normalized_id = self.normalize_id(obj_id)
            self.id_to_file[normalized_id] = filename
            
            # Variantes d'ID possibles
            id_variants = [
                obj_id,
                obj_id.lower(),
                f"{obj_type}-{obj_id}",
                filename.replace('.json', '').replace('.yml', '').replace('.yaml', '')
            ]
            
            for variant in id_variants:
                if variant:
                    self.id_to_file[self.normalize_id(variant)] = filename
    
    def resolve_reference(self, ref: str) -> Optional[str]:
        """Résout une référence vers un nom de fichier"""
        normalized_ref = self.normalize_id(ref)
        
        # Recherche directe
        if normalized_ref in self.id_to_file:
            return self.id_to_file[normalized_ref]
        
        # Recherche avec préfixes
        prefixes = ['playbook-', 'automation-', 'script-', 'incidentfield-', 'widget-', 'layout-']
        for prefix in prefixes:
            variant = f"{prefix}{normalized_ref}"
            if variant in self.id_to_file:
                return self.id_to_file[variant]
        
        # Recherche partielle
        for indexed_id, filename in self.id_to_file.items():
            if normalized_ref in indexed_id or indexed_id in normalized_ref:
                return filename
        
        return None
    
    def crawl_dependencies(self, start_files: List[str]) -> Dict:
        """Crawl des dépendances à partir des fichiers de départ"""
        print(f"Début du crawl à partir de {len(start_files)} fichiers...")
        
        results = {}
        visited = set()
        queue = deque(start_files)
        
        while queue:
            current_file = queue.popleft()
            
            if current_file in visited:
                continue
            
            if current_file not in self.file_index:
                print(f"Fichier non trouvé: {current_file}")
                continue
            
            visited.add(current_file)
            file_info = self.file_index[current_file]
            
            print(f"Analyse de {current_file} ({file_info['type']})...")
            
            # Extraire les références
            references = self.extract_references_from_object(
                file_info['data'], 
                file_info['type']
            )
            
            resolved_deps = set()
            unresolved_deps = set()
            
            for ref in references:
                resolved_file = self.resolve_reference(ref)
                if resolved_file:
                    resolved_deps.add(resolved_file)
                    self.dependencies[current_file].add(resolved_file)
                    self.reverse_dependencies[resolved_file].add(current_file)
                    
                    # Ajouter à la queue si pas encore visité
                    if resolved_file not in visited and resolved_file not in queue:
                        queue.append(resolved_file)
                else:
                    unresolved_deps.add(ref)
            
            results[current_file] = {
                'type': file_info['type'],
                'id': file_info['id'],
                'resolved_dependencies': sorted(list(resolved_deps)),
                'unresolved_references': sorted(list(unresolved_deps)),
                'all_references': sorted(list(references))
            }
        
        return results
    
    def generate_summary(self, results: Dict) -> Dict:
        """Génère un résumé des résultats"""
        summary = {
            'total_files_analyzed': len(results),
            'by_type': defaultdict(int),
            'dependency_graph': dict(self.dependencies),
            'reverse_dependencies': dict(self.reverse_dependencies),
            'most_referenced': [],
            'unresolved_summary': defaultdict(set)
        }
        
        # Comptage par type
        for file_data in results.values():
            summary['by_type'][file_data['type']] += 1
        
        # Fichiers les plus référencés
        ref_counts = [(file, len(refs)) for file, refs in self.reverse_dependencies.items()]
        summary['most_referenced'] = sorted(ref_counts, key=lambda x: x[1], reverse=True)[:10]
        
        # Résumé des références non résolues
        for file_data in results.values():
            for unresolved in file_data['unresolved_references']:
                summary['unresolved_summary'][file_data['type']].add(unresolved)
        
        # Convertir les sets en listes pour la sérialisation JSON
        summary['unresolved_summary'] = {
            k: sorted(list(v)) for k, v in summary['unresolved_summary'].items()
        }
        
        return summary
    
    def run(self, start_files: List[str]):
        """Point d'entrée principal"""
        print("=== XSOAR Dependency Crawler ===")
        
        # Construction des index
        self.build_indexes()
        print(f"Index construit: {len(self.file_index)} fichiers trouvés")
        
        # Crawl des dépendances
        results = self.crawl_dependencies(start_files)
        
        # Génération du résumé
        summary = self.generate_summary(results)
        
        # Sauvegarde des résultats
        output_data = {
            'metadata': {
                'start_files': start_files,
                'total_files_found': len(self.file_index),
                'total_files_analyzed': len(results)
            },
            'results': results,
            'summary': summary
        }
        
        os.makedirs(self.output_path, exist_ok=True)
        output_file = os.path.join(self.output_path, 'xsoar_dependencies.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Résultats sauvegardés dans: {output_file}")
        self.print_summary(summary)
    
    def print_summary(self, summary: Dict):
        """Affiche un résumé des résultats"""
        print("\n=== RÉSUMÉ ===")
        print(f"Fichiers analysés: {summary['total_files_analyzed']}")
        
        print("\nPar type:")
        for obj_type, count in summary['by_type'].items():
            print(f"  {obj_type}: {count}")
        
        print("\nFichiers les plus référencés:")
        for file, count in summary['most_referenced'][:5]:
            print(f"  {file}: {count} références")
        
        print("\nRéférences non résolues par type:")
        for obj_type, refs in summary['unresolved_summary'].items():
            if refs:
                print(f"  {obj_type}: {len(refs)} références")


def main():
    # Configuration
    INPUT_PATH = "/home/m.da-cruz/soar/"
    OUTPUT_PATH = "/home/m.da-cruz/result/"
    
    # Fichiers de départ
    start_files = [
        "incidenttype-SOC-Default.json",
        "playbook-SOC-Module-Context.yml",
        "layoutscontainer-Report.json",
        "automation-StopScheduledTask.yml"
    ]
    
    # Lancement du crawler
    crawler = XSOARCrawler(INPUT_PATH, OUTPUT_PATH)
    crawler.run(start_files)


if __name__ == "__main__":
    main()
