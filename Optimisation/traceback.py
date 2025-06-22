import os
import json
import yaml
import re
from collections import defaultdict, deque
from typing import Dict, Set, List, Any, Optional, Tuple
from pathlib import Path

class XSOARCrawler:
    def __init__(self, input_path: str, output_path: str):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        
        # Configuration des patterns d'objets XSOAR avec validation stricte
        self.object_patterns = {
            'playbook': {
                'patterns': [r'playbook-(.+)\.ya?ml$', r'.*[Pp]laybook.*\.ya?ml$'],
                'id_fields': ['id', 'name', 'commonfields.id'],
                'file_extensions': ['.yml', '.yaml']
            },
            'automation': {
                'patterns': [r'automation-(.+)\.ya?ml$', r'script-(.+)\.ya?ml$'],
                'id_fields': ['commonfields.id', 'name', 'id'],
                'file_extensions': ['.yml', '.yaml']
            },
            'integration': {
                'patterns': [r'integration-(.+)\.ya?ml$'],
                'id_fields': ['commonfields.id', 'display', 'name'],
                'file_extensions': ['.yml', '.yaml']
            },
            'incident_type': {
                'patterns': [r'incidenttype-(.+)\.json$', r'SOC-(.+)\.json$'],
                'id_fields': ['id', 'name', 'cliName'],
                'file_extensions': ['.json']
            },
            'incident_field': {
                'patterns': [r'incidentfield-(.+)\.json$', r'field-(.+)\.json$'],
                'id_fields': ['id', 'name', 'cliName'],
                'file_extensions': ['.json']
            },
            'layout': {
                'patterns': [r'layoutscontainer-(.+)\.json$', r'layout-(.+)\.json$'],
                'id_fields': ['id', 'name', 'group'],
                'file_extensions': ['.json']
            },
            'widget': {
                'patterns': [r'widget-(.+)\.json$'],
                'id_fields': ['id', 'name'],
                'file_extensions': ['.json']
            },
            'indicator_type': {
                'patterns': [r'reputation-(.+)\.json$', r'indicator-(.+)\.json$'],
                'id_fields': ['id', 'details'],
                'file_extensions': ['.json']
            },
            'classifier': {
                'patterns': [r'classifier-(.+)\.json$'],
                'id_fields': ['id', 'name', 'brandName'],
                'file_extensions': ['.json']
            },
            'mapper': {
                'patterns': [r'mapper-(.+)\.json$'],
                'id_fields': ['id', 'name', 'brandName'],
                'file_extensions': ['.json']
            },
            'report': {
                'patterns': [r'report-(.+)\.json$'],
                'id_fields': ['id', 'name'],
                'file_extensions': ['.json']
            }
        }
        
        # Système de filtrage avancé pour extraire les vraies dépendances
        self.dependency_extractors = {
            'playbook': self._extract_playbook_dependencies,
            'automation': self._extract_automation_dependencies,
            'integration': self._extract_integration_dependencies,
            'incident_type': self._extract_incident_type_dependencies,
            'incident_field': self._extract_field_dependencies,
            'layout': self._extract_layout_dependencies,
            'widget': self._extract_widget_dependencies,
            'classifier': self._extract_classifier_dependencies,
            'mapper': self._extract_mapper_dependencies
        }
        
        # Filtres pour éliminer les faux positifs
        self.noise_filters = {
            'common_words': {
                'and', 'or', 'not', 'if', 'then', 'else', 'true', 'false',
                'yes', 'no', 'admin', 'user', 'system', 'default', 'custom',
                'new', 'old', 'temp', 'tmp', 'test', 'demo', 'example'
            },
            'system_commands': {
                'Print', 'Set', 'GetIncident', 'CreateIncident', 'CloseIncident',
                'AddEvidence', 'DeleteContext', 'ExecuteCommand', 'Print'
            },
            'min_length': 3,
            'max_length': 100,
            'invalid_chars': r'[<>"\'\`\(\)\[\]{}]'
        }
        
        self.object_registry = {}  # ID unique -> objet XSOAR
        self.file_registry = {}    # filename -> metadata
        self.dependencies = defaultdict(set)
        self.statistics = defaultdict(int)
    
    def load_file(self, file_path: Path) -> Optional[Dict]:
        """Charge un fichier avec gestion d'erreur robuste"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() == '.json':
                    data = json.load(f)
                else:
                    data = yaml.safe_load(f)
                return data if isinstance(data, dict) else None
        except Exception as e:
            print(f"⚠️  Erreur chargement {file_path.name}: {e}")
            self.statistics['load_errors'] += 1
            return None
    
    def identify_object_type(self, filename: str) -> Optional[str]:
        """Identification stricte du type d'objet"""
        filename_lower = filename.lower()
        
        for obj_type, config in self.object_patterns.items():
            # Vérifier l'extension
            if not any(filename_lower.endswith(ext) for ext in config['file_extensions']):
                continue
                
            # Vérifier les patterns
            for pattern in config['patterns']:
                if re.match(pattern, filename, re.IGNORECASE):
                    return obj_type
        
        return None
    
    def extract_object_id(self, data: Dict, obj_type: str, filename: str) -> str:
        """Extraction de l'ID avec priorité selon le type d'objet"""
        config = self.object_patterns.get(obj_type, {})
        id_fields = config.get('id_fields', ['id', 'name'])
        
        for field_path in id_fields:
            value = self._get_nested_value(data, field_path)
            if value and isinstance(value, str) and len(value.strip()) > 0:
                return value.strip()
        
        # Fallback : nom de fichier sans extension et préfixe
        base_name = filename
        for pattern in config.get('patterns', []):
            match = re.match(pattern, filename, re.IGNORECASE)
            if match and match.groups():
                base_name = match.group(1)
                break
        
        return Path(base_name).stem
    
    def _get_nested_value(self, data: Dict, field_path: str) -> Any:
        """Récupère une valeur dans un objet imbriqué"""
        keys = field_path.split('.')
        current = data
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError, AttributeError):
            return None
    
    def is_valid_reference(self, ref: str) -> bool:
        """Filtre strict pour valider une référence"""
        if not ref or not isinstance(ref, str):
            return False
        
        ref = ref.strip()
        
        # Filtres de base
        if len(ref) < self.noise_filters['min_length'] or len(ref) > self.noise_filters['max_length']:
            return False
        
        # Caractères invalides
        if re.search(self.noise_filters['invalid_chars'], ref):
            return False
        
        # Mots communs à exclure
        if ref.lower() in self.noise_filters['common_words']:
            return False
        
        # Commandes système connues
        if ref in self.noise_filters['system_commands']:
            return False
        
        # Patterns à exclure
        exclude_patterns = [
            r'^\d+$',  # Nombres seuls
            r'^[a-f0-9-]{36}$',  # UUIDs
            r'^\$\{.*\}$',  # Variables non résolues
            r'^https?://',  # URLs
            r'^\w+@\w+\.',  # Emails
        ]
        
        for pattern in exclude_patterns:
            if re.match(pattern, ref, re.IGNORECASE):
                return False
        
        return True
    
    # Extracteurs spécialisés par type d'objet
    
    def _extract_playbook_dependencies(self, data: Dict) -> Set[str]:
        """Extraction des dépendances de playbook"""
        deps = set()
        
        # Sous-playbooks
        tasks = data.get('tasks', {})
        for task_data in tasks.values():
            task_info = task_data.get('task', {})
            
            # Playbook ID direct
            if 'playbookId' in task_info:
                deps.add(task_info['playbookId'])
            
            # Script/Automation ID
            if 'scriptId' in task_info:
                deps.add(task_info['scriptId'])
            
            # Script name dans task
            if 'script' in task_info and isinstance(task_info['script'], str):
                deps.add(task_info['script'])
        
        # Inputs et outputs
        for section in ['inputs', 'outputs']:
            items = data.get(section, [])
            for item in items:
                if isinstance(item, dict):
                    # Context paths
                    if 'contextPath' in item:
                        deps.add(item['contextPath'])
        
        return {dep for dep in deps if self.is_valid_reference(dep)}
    
    def _extract_automation_dependencies(self, data: Dict) -> Set[str]:
        """Extraction des dépendances d'automation"""
        deps = set()
        
        # Script dependencies
        script_data = data.get('script', {})
        
        # Commandes utilisées
        if 'depends_on' in script_data:
            for dep in script_data['depends_on']:
                if isinstance(dep, dict) and 'name' in dep:
                    deps.add(dep['name'])
        
        # Arguments avec références
        args = data.get('args', [])
        for arg in args:
            if isinstance(arg, dict) and 'defaultValue' in arg:
                default_val = arg['defaultValue']
                if isinstance(default_val, str) and default_val.startswith('incident.'):
                    field_name = default_val.replace('incident.', '')
                    deps.add(field_name)
        
        return {dep for dep in deps if self.is_valid_reference(dep)}
    
    def _extract_integration_dependencies(self, data: Dict) -> Set[str]:
        """Extraction des dépendances d'intégration"""
        deps = set()
        
        # Configuration par défaut
        config = data.get('configuration', [])
        for config_item in config:
            if isinstance(config_item, dict) and 'defaultvalue' in config_item:
                deps.add(config_item['defaultvalue'])
        
        # Commandes et leurs outputs
        script_data = data.get('script', {})
        commands = script_data.get('commands', [])
        for cmd in commands:
            if isinstance(cmd, dict):
                # Context outputs
                outputs = cmd.get('outputs', [])
                for output in outputs:
                    if isinstance(output, dict) and 'contextPath' in output:
                        deps.add(output['contextPath'])
        
        return {dep for dep in deps if self.is_valid_reference(dep)}
    
    def _extract_incident_type_dependencies(self, data: Dict) -> Set[str]:
        """Extraction des dépendances de type d'incident"""
        deps = set()
        
        # Playbook par défaut
        if 'playbookId' in data:
            deps.add(data['playbookId'])
        
        # Champs pré-définis
        predefined_fields = data.get('preProcessingScript', '')
        if predefined_fields:
            # Extraction des noms de champs depuis le script
            field_matches = re.findall(r'incident\.(\w+)', predefined_fields)
            deps.update(field_matches)
        
        return {dep for dep in deps if self.is_valid_reference(dep)}
    
    def _extract_field_dependencies(self, data: Dict) -> Set[str]:
        """Extraction des dépendances de champ d'incident"""
        deps = set()
        
        # Scripts associés
        if 'script' in data:
            deps.add(data['script'])
        
        # Champs liés dans les validations
        validation = data.get('validation', {})
        if isinstance(validation, dict):
            for key, value in validation.items():
                if isinstance(value, str) and 'incident.' in value:
                    field_refs = re.findall(r'incident\.(\w+)', value)
                    deps.update(field_refs)
        
        return {dep for dep in deps if self.is_valid_reference(dep)}
    
    def _extract_layout_dependencies(self, data: Dict) -> Set[str]:
        """Extraction des dépendances de layout"""
        deps = set()
        
        def extract_fields_from_sections(sections):
            for section in sections:
                if isinstance(section, dict):
                    fields = section.get('fields', [])
                    for field in fields:
                        if isinstance(field, dict) and 'fieldId' in field:
                            deps.add(field['fieldId'])
        
        # Layout principal
        layout = data.get('layout', {})
        if 'sections' in layout:
            extract_fields_from_sections(layout['sections'])
        
        # Tabs
        if 'tabs' in layout:
            for tab in layout['tabs']:
                if isinstance(tab, dict) and 'sections' in tab:
                    extract_fields_from_sections(tab['sections'])
        
        # Details V2
        details_v2 = data.get('detailsV2', {})
        if 'tabs' in details_v2:
            for tab in details_v2['tabs']:
                if isinstance(tab, dict) and 'sections' in tab:
                    extract_fields_from_sections(tab['sections'])
        
        return {dep for dep in deps if self.is_valid_reference(dep)}
    
    def _extract_widget_dependencies(self, data: Dict) -> Set[str]:
        """Extraction des dépendances de widget"""
        deps = set()
        
        # Queries et données
        query = data.get('query', '')
        if query:
            # Extraction des champs depuis les requêtes
            field_matches = re.findall(r'incident\.(\w+)', query)
            deps.update(field_matches)
        
        # Script personnalisé
        if 'script' in data:
            deps.add(data['script'])
        
        return {dep for dep in deps if self.is_valid_reference(dep)}
    
    def _extract_classifier_dependencies(self, data: Dict) -> Set[str]:
        """Extraction des dépendances de classifier"""
        deps = set()
        
        # Mapping vers les types d'incidents
        mapping = data.get('mapping', {})
        for incident_type in mapping.values():
            if isinstance(incident_type, str):
                deps.add(incident_type)
        
        return {dep for dep in deps if self.is_valid_reference(dep)}
    
    def _extract_mapper_dependencies(self, data: Dict) -> Set[str]:
        """Extraction des dépendances de mapper"""
        deps = set()
        
        # Mapping des champs
        mapping = data.get('mapping', {})
        for field_mapping in mapping.values():
            if isinstance(field_mapping, dict):
                for field_name in field_mapping.keys():
                    deps.add(field_name)
        
        return {dep for dep in deps if self.is_valid_reference(dep)}
    
    def build_registry(self):
        """Construction du registre unifié des objets XSOAR"""
        print("🔍 Construction du registre des objets XSOAR...")
        
        if not self.input_path.exists():
            raise FileNotFoundError(f"Répertoire d'entrée non trouvé: {self.input_path}")
        
        files_found = 0
        files_processed = 0
        
        for file_path in self.input_path.rglob('*'):
            if not file_path.is_file() or file_path.suffix.lower() not in ['.json', '.yml', '.yaml']:
                continue
            
            files_found += 1
            obj_type = self.identify_object_type(file_path.name)
            
            if not obj_type:
                self.statistics['unknown_type'] += 1
                continue
            
            data = self.load_file(file_path)
            if not data:
                continue
            
            obj_id = self.extract_object_id(data, obj_type, file_path.name)
            unique_key = f"{obj_type}:{obj_id}"
            
            # Vérification de doublons
            if unique_key in self.object_registry:
                print(f"⚠️  Doublon détecté: {unique_key}")
                self.statistics['duplicates'] += 1
                continue
            
            # Enregistrement de l'objet
            self.object_registry[unique_key] = {
                'id': obj_id,
                'type': obj_type,
                'filename': file_path.name,
                'path': str(file_path),
                'data': data,
                'dependencies': set()
            }
            
            self.file_registry[file_path.name] = unique_key
            files_processed += 1
            self.statistics[f'type_{obj_type}'] += 1
        
        print(f"📊 Registre construit: {files_processed}/{files_found} fichiers traités")
        print(f"   Types trouvés: {dict((k, v) for k, v in self.statistics.items() if k.startswith('type_'))}")
    
    def resolve_dependency(self, ref: str, source_type: str) -> Optional[str]:
        """Résolution intelligente des dépendances"""
        if not self.is_valid_reference(ref):
            return None
        
        ref_normalized = ref.strip()
        
        # Recherche directe par ID
        for unique_key, obj_data in self.object_registry.items():
            if obj_data['id'] == ref_normalized:
                return unique_key
        
        # Recherche avec préfixes courants
        type_prefixes = {
            'playbook': ['playbook-'],
            'automation': ['automation-', 'script-'],
            'incident_field': ['incidentfield-', 'field-'],
            'layout': ['layoutscontainer-', 'layout-'],
            'widget': ['widget-'],
            'incident_type': ['incidenttype-']
        }
        
        for obj_type, prefixes in type_prefixes.items():
            for prefix in prefixes:
                test_key = f"{obj_type}:{ref_normalized}"
                if test_key in self.object_registry:
                    return test_key
                
                # Test avec préfixe
                prefixed_ref = f"{prefix}{ref_normalized}"
                test_key = f"{obj_type}:{prefixed_ref}"
                if test_key in self.object_registry:
                    return test_key
        
        # Recherche floue (correspondance partielle)
        for unique_key, obj_data in self.object_registry.items():
            obj_id = obj_data['id'].lower()
            ref_lower = ref_normalized.lower()
            
            if ref_lower in obj_id or obj_id in ref_lower:
                if len(ref_lower) > 3:  # Éviter les correspondances trop courtes
                    return unique_key
        
        return None
    
    def analyze_dependencies(self, start_objects: List[str]) -> Dict:
        """Analyse complète des dépendances"""
        print(f"🔗 Analyse des dépendances à partir de {len(start_objects)} objets...")
        
        results = {}
        processed = set()
        queue = deque()
        
        # Initialisation de la queue
        for start_obj in start_objects:
            if start_obj in self.file_registry:
                unique_key = self.file_registry[start_obj]
                queue.append(unique_key)
            else:
                print(f"⚠️  Objet de départ non trouvé: {start_obj}")
        
        level = 0
        while queue and level < 10:  # Limite de profondeur
            current_level_size = len(queue)
            level += 1
            
            print(f"   Niveau {level}: {current_level_size} objets à analyser")
            
            for _ in range(current_level_size):
                if not queue:
                    break
                    
                unique_key = queue.popleft()
                
                if unique_key in processed:
                    continue
                
                processed.add(unique_key)
                obj_data = self.object_registry[unique_key]
                
                # Extraction des dépendances selon le type
                extractor = self.dependency_extractors.get(obj_data['type'])
                if extractor:
                    raw_deps = extractor(obj_data['data'])
                else:
                    raw_deps = set()
                
                # Résolution des dépendances
                resolved_deps = {}
                unresolved_deps = []
                
                for dep in raw_deps:
                    resolved_key = self.resolve_dependency(dep, obj_data['type'])
                    if resolved_key:
                        target_obj = self.object_registry[resolved_key]
                        resolved_deps[resolved_key] = {
                            'id': target_obj['id'],
                            'type': target_obj['type'],
                            'filename': target_obj['filename']
                        }
                        
                        # Ajouter à la queue pour analyse ultérieure
                        if resolved_key not in processed:
                            queue.append(resolved_key)
                    else:
                        unresolved_deps.append(dep)
                
                # Enregistrement des résultats
                results[unique_key] = {
                    'object': {
                        'id': obj_data['id'],
                        'type': obj_data['type'],
                        'filename': obj_data['filename']
                    },
                    'dependencies': resolved_deps,
                    'unresolved': sorted(unresolved_deps),
                    'dependency_count': len(resolved_deps),
                    'analysis_level': level
                }
                
                self.statistics['objects_analyzed'] += 1
        
        print(f"✅ Analyse terminée: {len(results)} objets analysés sur {level} niveaux")
        return results
    
    def generate_report(self, analysis_results: Dict) -> Dict:
        """Génération d'un rapport complet"""
        print("📋 Génération du rapport...")
        
        # Statistiques par type
        type_stats = defaultdict(lambda: {'count': 0, 'has_dependencies': 0, 'avg_deps': 0})
        dependency_graph = {}
        reverse_deps = defaultdict(set)
        
        total_deps = 0
        for unique_key, result in analysis_results.items():
            obj_type = result['object']['type']
            dep_count = result['dependency_count']
            
            type_stats[obj_type]['count'] += 1
            type_stats[obj_type]['has_dependencies'] += 1 if dep_count > 0 else 0
            total_deps += dep_count
            
            # Graphe de dépendances
            dependency_graph[unique_key] = list(result['dependencies'].keys())
            
            # Dépendances inverses
            for dep_key in result['dependencies'].keys():
                reverse_deps[dep_key].add(unique_key)
        
        # Calcul des moyennes
        for obj_type, stats in type_stats.items():
            if stats['count'] > 0:
                deps_sum = sum(analysis_results[k]['dependency_count'] 
                             for k in analysis_results.keys() 
                             if analysis_results[k]['object']['type'] == obj_type)
                stats['avg_deps'] = round(deps_sum / stats['count'], 2)
        
        # Objets les plus référencés
        most_referenced = sorted(
            [(key, len(refs)) for key, refs in reverse_deps.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Compilation des références non résolues
        all_unresolved = defaultdict(set)
        for result in analysis_results.values():
            obj_type = result['object']['type']
            for unresolved in result['unresolved']:
                all_unresolved[obj_type].add(unresolved)
        
        report = {
            'summary': {
                'total_objects_analyzed': len(analysis_results),
                'total_dependencies_found': total_deps,
                'total_unresolved': sum(len(refs) for refs in all_unresolved.values()),
                'analysis_coverage': f"{len(analysis_results)}/{len(self.object_registry)} objets"
            },
            'statistics_by_type': dict(type_stats),
            'most_referenced_objects': [
                {
                    'key': key,
                    'object': self.object_registry[key]['id'] if key in self.object_registry else 'Unknown',
                    'reference_count': count
                }
                for key, count in most_referenced
            ],
            'dependency_graph': dependency_graph,
            'reverse_dependencies': {k: list(v) for k, v in reverse_deps.items()},
            'unresolved_by_type': {k: sorted(list(v)) for k, v in all_unresolved.items()},
            'processing_statistics': dict(self.statistics)
        }
        
        return report
    
    def generate_csv_report(self, analysis_results: Dict) -> str:
        """Génère un rapport CSV avec le format demandé"""
        import csv
        from io import StringIO
        
        print("📊 Génération du rapport CSV...")
        
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer, delimiter=';')
        
        # En-têtes CSV
        writer.writerow([
            'Objet Parent',
            'Type Parent', 
            'Statut Parent',
            'Objet Fils',
            'Type Fils',
            'Statut Fils',
            'Nombre References',
            'Contexte'
        ])
        
        # Comptage des références (objet fils -> combien de fois référencé)
        reference_count = defaultdict(int)
        parent_child_map = defaultdict(list)
        
        # Première passe : compter les références
        for parent_key, result in analysis_results.items():
            parent_obj = result['object']
            
            for child_key, child_info in result['dependencies'].items():
                reference_count[child_key] += 1
                parent_child_map[child_key].append({
                    'parent_key': parent_key,
                    'parent_obj': parent_obj
                })
        
        # Génération des lignes CSV
        processed_relationships = set()
        
        for child_key, parents_list in parent_child_map.items():
            if child_key not in self.object_registry:
                continue
                
            child_obj = self.object_registry[child_key]
            child_name = child_obj['id']
            child_type = child_obj['type']
            child_status = "Trouvé"
            total_references = reference_count[child_key]
            
            for parent_info in parents_list:
                parent_obj = parent_info['parent_obj']
                parent_name = parent_obj['id']
                parent_type = parent_obj['type']
                parent_status = "Trouvé"
                
                # Éviter les doublons
                relationship_key = f"{parent_name}#{child_name}"
                if relationship_key in processed_relationships:
                    continue
                processed_relationships.add(relationship_key)
                
                # Contexte de la relation
                context = f"{child_name} trouvé {total_references} fois --> dans {parent_name}"
                
                writer.writerow([
                    parent_name,
                    parent_type,
                    parent_status,
                    child_name,
                    child_type,
                    child_status,
                    total_references,
                    context
                ])
        
        # Ajout des références non trouvées
        for parent_key, result in analysis_results.items():
            parent_obj = result['object']
            parent_name = parent_obj['id']
            parent_type = parent_obj['type']
            
            for unresolved_ref in result['unresolved']:
                context = f"{unresolved_ref} non trouvé --> dans {parent_name}"
                
                writer.writerow([
                    parent_name,
                    parent_type,
                    "Trouvé",
                    unresolved_ref,
                    "Inconnu",
                    "Non trouvé",
                    1,
                    context
                ])
        
        return csv_buffer.getvalue()

    def run(self, start_files: List[str]):
        """Point d'entrée principal du crawler"""
        print("🚀 === XSOAR Dependency Crawler - Version Améliorée ===")
        
        try:
            # Construction du registre
            self.build_registry()
            
            if not self.object_registry:
                print("❌ Aucun objet XSOAR trouvé dans le répertoire d'entrée")
                return
            
            # Analyse des dépendances
            analysis_results = self.analyze_dependencies(start_files)
            
            if not analysis_results:
                print("❌ Aucune dépendance analysée")
                return
            
            # Génération du rapport
            report = self.generate_report(analysis_results)
            
            # Sauvegarde
            self.output_path.mkdir(parents=True, exist_ok=True)
            
            # Rapport détaillé JSON
            detailed_output = {
                'metadata': {
                    'start_files': start_files,
                    'input_path': str(self.input_path),
                    'analysis_timestamp': str(Path.cwd() / 'timestamp'),
                    'total_objects_registry': len(self.object_registry)
                },
                'analysis_results': analysis_results,
                'report': report
            }
            
            output_file = self.output_path / 'xsoar_dependencies_detailed.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(detailed_output, f, indent=2, ensure_ascii=False, default=str)
            
            # Rapport résumé JSON
            summary_file = self.output_path / 'xsoar_dependencies_summary.json'
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            
            # Rapport CSV
            csv_content = self.generate_csv_report(analysis_results)
            csv_file = self.output_path / 'xsoar_dependencies_report.csv'
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_content)
            
            print(f"\n✅ Résultats sauvegardés:")
            print(f"   📄 Rapport détaillé: {output_file}")
            print(f"   📋 Rapport résumé: {summary_file}")
            print(f"   📊 Rapport CSV: {csv_file}")
            
            self.print_summary(report)
            
        except Exception as e:
            print(f"❌ Erreur durant l'exécution: {e}")
            raise
    
    def print_summary(self, report: Dict):
        """Affichage du résumé"""
        print("\n" + "="*50)
        print("📊 RÉSUMÉ DE L'ANALYSE")
        print("="*50)
        
        summary = report['summary']
        print(f"Objets analysés: {summary['total_objects_analyzed']}")
        print(f"Dépendances trouvées: {summary['total_dependencies_found']}")
        print(f"Références non résolues: {summary['total_unresolved']}")
        print(f"Couverture: {summary['analysis_coverage']}")
        
        print(f"\n📈 STATISTIQUES PAR TYPE:")
        for obj_type, stats in report['statistics_by_type'].items():
            print(f"  {obj_type:<15}: {stats['count']} objets, "
                  f"{stats['has_dependencies']} avec dépendances, "
                  f"moy. {stats['avg_deps']} dép/objet")
        
        print(f"\n🔗 OBJETS LES PLUS RÉFÉRENCÉS:")
        for item in report['most_referenced_objects'][:5]:
            print(f"  {item['object']:<30}: {item['reference_count']} références")
        
        if report['unresolved_by_type']:
            print(f"\n⚠️  RÉFÉRENCES NON RÉSOLUES PAR TYPE:")
            for obj_type, refs in report['unresolved_by_type'].items():
                if refs:
                    print(f"  {obj_type}: {len(refs)} références")
                    # Afficher quelques exemples
                    for ref in refs[:3]:
                        print(f"    - {ref}")
                    if len(refs) > 3:
                        print(f"
