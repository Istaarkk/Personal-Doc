import os
import json
import yaml
import re
from collections import defaultdict, deque
from typing import Dict, Set, List, Any, Optional, Tuple, Iterable
from pathlib import Path

# -------------------------------------------------------------
# XSOAR Crawler — version "+grep -rni" (réduction des faux positifs)
# -------------------------------------------------------------
# Objectifs de cette version :
#  1) Séparer clairement les vraies dépendances d'objets XSOAR
#     (playbooks, scripts/automations, intégrations, types, champs, layouts,
#      widgets, classifiers, mappers, reports)
#     de toutes les autres références (context paths, champs incident, commandes,
#     valeurs par défaut, etc.) pour réduire les faux positifs.
#  2) Implémenter un "grep -rni" natif en Python pour confirmer l'usage réel
#     des objets dans la codebase (avec numéros de ligne, insensible à la casse,
#     récursif, filtres d'exclusion).
#  3) Ne retenir dans l'inventaire final que les objets non natifs ET utilisés
#     (au moins une occurrence hors de leur fichier de définition et hors /Tests...).
# -------------------------------------------------------------


def _is_binary_file(path: Path, blocksize: int = 1024) -> bool:
    try:
        with open(path, 'rb') as f:
            chunk = f.read(blocksize)
        if b"\0" in chunk:
            return True
        # Heuristique simple : si + de 30% d'octets sont > 0x7F, probable binaire
        if chunk:
            high = sum(1 for b in chunk if b > 0x7F)
            return high / len(chunk) > 0.30
        return False
    except Exception:
        return True


def _safe_load_yaml_or_json(file_path: Path) -> Optional[Dict[str, Any]]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        if not text.strip():
            return None
        if file_path.suffix.lower() == '.json':
            try:
                return json.loads(text)
            except Exception:
                return None
        else:
            try:
                data = yaml.safe_load(text)
                return data if isinstance(data, dict) else None
            except Exception:
                return None
    except Exception:
        return None


class XSOARCrawler:
    def __init__(self, input_path: str, output_path: str, *, custom_only: bool = True, used_only: bool = True):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.custom_only = custom_only
        self.used_only = used_only

        # -------------------------------
        # Détection stricte des fichiers
        # -------------------------------
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

        # Extraction ciblée des dépendances (objets uniquement)
        self.dependency_extractors = {
            'playbook': self._extract_playbook_object_deps,
            'automation': self._extract_automation_object_deps,
            'integration': self._extract_integration_object_deps,
            'incident_type': self._extract_incident_type_object_deps,
            'incident_field': self._extract_field_object_deps,
            'layout': self._extract_layout_object_deps,
            'widget': self._extract_widget_object_deps,
            'classifier': self._extract_classifier_object_deps,
            'mapper': self._extract_mapper_object_deps,
            'report': self._extract_report_object_deps,
        }

        # Références non-objets (pour info diagnostics, pas comptées comme deps)
        self.soft_ref_extractors = {
            'playbook': self._extract_playbook_soft_refs,
            'automation': self._extract_automation_soft_refs,
            'integration': self._extract_integration_soft_refs,
            'incident_type': self._extract_incident_type_soft_refs,
            'incident_field': self._extract_field_soft_refs,
            'layout': self._extract_layout_soft_refs,
            'widget': self._extract_widget_soft_refs,
            'classifier': self._extract_classifier_soft_refs,
            'mapper': self._extract_mapper_soft_refs,
            'report': self._noop_soft_refs,
        }

        # Filtrage du bruit (agressif)
        self.noise_filters = {
            'common_words': {
                'and', 'or', 'not', 'if', 'then', 'else', 'true', 'false',
                'yes', 'no', 'admin', 'user', 'system', 'default', 'custom',
                'new', 'old', 'temp', 'tmp', 'test', 'demo', 'example', 'none',
            },
            'system_commands': {
                'Print', 'Set', 'GetIncident', 'CreateIncident', 'CloseIncident',
                'AddEvidence', 'DeleteContext', 'ExecuteCommand'
            },
            'min_length': 3,
            'max_length': 120,
            'invalid_chars': r'[<>"\'"'"'`()\[\]{}]'
        }

        # Dossiers/Extensions ignorés pour le grep et pour la détection d'usage
        self.ignore_dirs = {
            '.git', '.idea', '.vscode', '__pycache__', '.pytest_cache', '.tox', '.eggs',
            'dist', 'build', 'node_modules', 'venv', 'env', 'Tests', 'TestPlaybooks'
        }
        self.allowed_grep_exts = {
            '.yml', '.yaml', '.json', '.md', '.py', '.ps1', '.sh', '.js', '.ts', '.tsx'
        }

        # Heuristique "natif"
        self.native_path_markers = [
            '/Packs/Base/', '/Packs/Legacy/', '/Packs/CommonPlaybooks/',
            '/Packs/CommonTypes/', '/Packs/CommonScripts/'
        ]
        self.native_id_prefixes = ['DBot', 'Builtin', 'Common.']

        self.object_registry: Dict[str, Dict[str, Any]] = {}
        self.file_registry: Dict[str, str] = {}
        self.statistics = defaultdict(int)

        # Usages trouvés via grep: key -> [occurrences]
        self.usage_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    # -------------------------
    # Identification / Registre
    # -------------------------
    def identify_object_type(self, filename: str) -> Optional[str]:
        filename_lower = filename.lower()
        for obj_type, config in self.object_patterns.items():
            if not any(filename_lower.endswith(ext) for ext in config['file_extensions']):
                continue
            for pattern in config['patterns']:
                if re.match(pattern, filename, re.IGNORECASE):
                    return obj_type
        return None

    def _get_nested_value(self, data: Dict, field_path: str) -> Any:
        keys = field_path.split('.')
        current = data
        try:
            for key in keys:
                current = current[key]
            return current
        except Exception:
            return None

    def extract_object_id(self, data: Dict, obj_type: str, filename: str) -> str:
        config = self.object_patterns.get(obj_type, {})
        id_fields = config.get('id_fields', ['id', 'name'])
        for field_path in id_fields:
            value = self._get_nested_value(data, field_path)
            if isinstance(value, str) and value.strip():
                return value.strip()
        # fallback: enlever le préfixe pattern si possible
        base_name = filename
        for pattern in config.get('patterns', []):
            m = re.match(pattern, filename, re.IGNORECASE)
            if m and m.groups():
                base_name = m.group(1)
                break
        return Path(base_name).stem

    def _is_native_object(self, obj: Dict[str, Any]) -> bool:
        if not self.custom_only:
            return False
        path = obj.get('path', '')
        obj_id = obj.get('id', '')
        for marker in self.native_path_markers:
            if marker in path:
                return True
        return any(str(obj_id).startswith(p) for p in self.native_id_prefixes)

    def build_registry(self) -> None:
        if not self.input_path.exists():
            raise FileNotFoundError(f"Répertoire d'entrée non trouvé: {self.input_path}")
        files_found = 0
        files_processed = 0
        for file_path in self.input_path.rglob('*'):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in ['.json', '.yml', '.yaml']:
                continue
            files_found += 1
            obj_type = self.identify_object_type(file_path.name)
            if not obj_type:
                self.statistics['unknown_type'] += 1
                continue
            data = _safe_load_yaml_or_json(file_path)
            if not isinstance(data, dict):
                self.statistics['load_errors'] += 1
                continue
            obj_id = self.extract_object_id(data, obj_type, file_path.name)
            unique_key = f"{obj_type}:{obj_id}"
            if unique_key in self.object_registry:
                self.statistics['duplicates'] += 1
                continue
            record = {
                'id': obj_id,
                'type': obj_type,
                'filename': file_path.name,
                'path': str(file_path),
                'data': data,
            }
            if self._is_native_object(record):
                self.statistics['native_skipped'] += 1
                continue
            self.object_registry[unique_key] = record
            self.file_registry[file_path.name] = unique_key
            files_processed += 1
            self.statistics[f'type_{obj_type}'] += 1
        self.statistics['files_found'] = files_found
        self.statistics['files_indexed'] = files_processed

    # ------------------
    # Filtrage de chaîne
    # ------------------
    def is_valid_reference(self, ref: str) -> bool:
        if not isinstance(ref, str):
            return False
        ref = ref.strip()
        if not ref:
            return False
        if len(ref) < self.noise_filters['min_length'] or len(ref) > self.noise_filters['max_length']:
            return False
        if re.search(self.noise_filters['invalid_chars'], ref):
            return False
        if ref.lower() in self.noise_filters['common_words']:
            return False
        if ref in self.noise_filters['system_commands']:
            return False
        # Bruit typique à ignorer
        exclude_patterns = [
            r'^\d+$',                  # nombres
            r'^[a-f0-9-]{36}$',         # UUID
            r'^\$\{.*\}$',           # variables non résolues
            r'^https?://',              # URLs
            r'^\w+@\w+\.',           # emails
            r'\s',                     # espaces multiples -> éviter les phrases
        ]
        for p in exclude_patterns:
            if re.search(p, ref, re.IGNORECASE):
                return False
        return True

    # ----------------------------------------
    # Extraction DEPENDANCES (objets uniquement)
    # ----------------------------------------
    def _extract_playbook_object_deps(self, data: Dict) -> Set[str]:
        deps = set()
        tasks = data.get('tasks', {}) or {}
        for t in tasks.values():
            task = (t or {}).get('task', {}) or {}
            # Sous-playbooks
            pbid = task.get('playbookId')
            if isinstance(pbid, str) and self.is_valid_reference(pbid):
                deps.add(pbid)
            # Scripts/Automations
            for k in ('scriptId',):
                val = task.get(k)
                if isinstance(val, str) and self.is_valid_reference(val):
                    deps.add(val)
            # Certains exports utilisent 'script' avec un nom, éviter les commandes (!cmd)
            sc = task.get('script')
            if isinstance(sc, str) and not sc.strip().startswith('!') and self.is_valid_reference(sc):
                deps.add(sc)
        return deps

    def _extract_automation_object_deps(self, data: Dict) -> Set[str]:
        deps = set()
        # Automations peuvent appeler d'autres automations via 'script' dans code YAML (rare)
        # On reste conservateur: on NE compte PAS les context paths ni les commandes d'intégration.
        return deps

    def _extract_integration_object_deps(self, data: Dict) -> Set[str]:
        # Une intégration ne dépend normalement pas d'autres objets XSOAR (ses commands ne sont pas des deps)
        return set()

    def _extract_incident_type_object_deps(self, data: Dict) -> Set[str]:
        deps = set()
        pbid = data.get('playbookId')
        if isinstance(pbid, str) and self.is_valid_reference(pbid):
            deps.add(pbid)
        return deps

    def _extract_field_object_deps(self, data: Dict) -> Set[str]:
        # Un champ peut référencer un script (validation/trigger) -> dépendance d'automation
        deps = set()
        sc = data.get('script')
        if isinstance(sc, str) and self.is_valid_reference(sc):
            deps.add(sc)
        return deps

    def _extract_layout_object_deps(self, data: Dict) -> Set[str]:
        # Layouts référencent des champs (pas des objets). Pas de deps strictes d'objets.
        return set()

    def _extract_widget_object_deps(self, data: Dict) -> Set[str]:
        # Un widget peut référencer un script custom
        deps = set()
        sc = data.get('script')
        if isinstance(sc, str) and self.is_valid_reference(sc):
            deps.add(sc)
        return deps

    def _extract_classifier_object_deps(self, data: Dict) -> Set[str]:
        # Classifier: pas de deps d'objets (mappe des valeurs brutes)
        return set()

    def _extract_mapper_object_deps(self, data: Dict) -> Set[str]:
        # Mapper: pas de deps d'objets
        return set()

    def _extract_report_object_deps(self, data: Dict) -> Set[str]:
        # Report: peut référencer des widgets -> considérer comme deps
        deps = set()
        widgets = data.get('widgets', []) or []
        for w in widgets:
            if isinstance(w, dict):
                wname = w.get('id') or w.get('name')
                if isinstance(wname, str) and self.is_valid_reference(wname):
                    deps.add(wname)
        return deps

    # ----------------------------------------------------
    # Extraction SOFT REFS (contexte/champs/commandes/etc.)
    # ----------------------------------------------------
    def _extract_playbook_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        refs = {'context_paths': set(), 'incident_fields': set(), 'commands': set()}
        tasks = data.get('tasks', {}) or {}
        for t in tasks.values():
            task = (t or {}).get('task', {}) or {}
            for k in ('script',):
                sc = task.get(k)
                if isinstance(sc, str) and sc.strip().startswith('!'):
                    # Ex: "!integration-command" => commande d'intégration
                    refs['commands'].add(sc.strip()[1:])
            # context paths dans outputs/nexttasks/conditions (conservateur)
        # Inputs/outputs (contextPath)
        for sec in ('inputs', 'outputs'):
            for it in data.get(sec, []) or []:
                if isinstance(it, dict):
                    cp = it.get('contextPath')
                    if isinstance(cp, str) and '.' in cp:
                        refs['context_paths'].add(cp)
        return refs

    def _extract_automation_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        refs = {'context_paths': set(), 'incident_fields': set(), 'commands': set()}
        script_data = data.get('script', {}) or {}
        for dep in script_data.get('depends_on', []) or []:
            if isinstance(dep, dict) and isinstance(dep.get('name'), str):
                refs['commands'].add(dep['name'])
        # Arguments par défaut incident.xxx -> champs
        for arg in (data.get('args') or []):
            if isinstance(arg, dict):
                dv = arg.get('defaultValue')
                if isinstance(dv, str) and dv.startswith('incident.'):
                    refs['incident_fields'].add(dv.replace('incident.', '', 1))
        return refs

    def _extract_integration_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        refs = {'context_paths': set(), 'incident_fields': set(), 'commands': set()}
        script_data = data.get('script', {}) or {}
        for cmd in script_data.get('commands', []) or []:
            if isinstance(cmd, dict):
                name = cmd.get('name')
                if isinstance(name, str):
                    refs['commands'].add(name)
                for out in cmd.get('outputs', []) or []:
                    if isinstance(out, dict):
                        cp = out.get('contextPath')
                        if isinstance(cp, str) and '.' in cp:
                            refs['context_paths'].add(cp)
        return refs

    def _extract_incident_type_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        refs = {'context_paths': set(), 'incident_fields': set(), 'commands': set()}
        pps = data.get('preProcessingScript')
        if isinstance(pps, str):
            refs['incident_fields'].update(re.findall(r'incident\.(\w+)', pps))
        return refs

    def _extract_field_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        refs = {'context_paths': set(), 'incident_fields': set(), 'commands': set()}
        validation = data.get('validation', {}) or {}
        for v in validation.values():
            if isinstance(v, str):
                refs['incident_fields'].update(re.findall(r'incident\.(\w+)', v))
        return refs

    def _extract_layout_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        refs = {'context_paths': set(), 'incident_fields': set(), 'commands': set()}
        def grab(sections: Iterable[Dict[str, Any]]):
            for s in sections:
                if isinstance(s, dict):
                    for f in s.get('fields', []) or []:
                        if isinstance(f, dict) and isinstance(f.get('fieldId'), str):
                            refs['incident_fields'].add(f['fieldId'])
        layout = data.get('layout', {}) or {}
        if isinstance(layout.get('sections'), list):
            grab(layout['sections'])
        for tab in layout.get('tabs', []) or []:
            if isinstance(tab, dict) and isinstance(tab.get('sections'), list):
                grab(tab['sections'])
        details_v2 = data.get('detailsV2', {}) or {}
        for tab in details_v2.get('tabs', []) or []:
            if isinstance(tab, dict) and isinstance(tab.get('sections'), list):
                grab(tab['sections'])
        return refs

    def _extract_widget_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        refs = {'context_paths': set(), 'incident_fields': set(), 'commands': set()}
        q = data.get('query')
        if isinstance(q, str):
            refs['incident_fields'].update(re.findall(r'incident\.(\w+)', q))
        return refs

    def _extract_classifier_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        refs = {'context_paths': set(), 'incident_fields': set(), 'commands': set()}
        mapping = data.get('mapping', {}) or {}
        for v in mapping.values():
            if isinstance(v, str):
                # valeurs brutes mappées vers types
                pass
        return refs

    def _extract_mapper_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        refs = {'context_paths': set(), 'incident_fields': set(), 'commands': set()}
        mapping = data.get('mapping', {}) or {}
        for fm in mapping.values():
            if isinstance(fm, dict):
                for name in fm.keys():
                    if isinstance(name, str):
                        refs['incident_fields'].add(name)
        return refs

    def _noop_soft_refs(self, data: Dict) -> Dict[str, Set[str]]:
        return {'context_paths': set(), 'incident_fields': set(), 'commands': set()}

    # ---------------------------
    # Résolution par ID / Approx
    # ---------------------------
    def resolve_dependency(self, ref: str) -> Optional[str]:
        if not self.is_valid_reference(ref):
            return None
        ref_norm = ref.strip()
        # 1) ID exact
        for key, obj in self.object_registry.items():
            if obj['id'] == ref_norm:
                return key
        # 2) Essais avec préfixes fréquents
        type_prefixes = {
            'playbook': ['playbook-'],
            'automation': ['automation-', 'script-'],
            'incident_field': ['incidentfield-', 'field-'],
            'layout': ['layoutscontainer-', 'layout-'],
            'widget': ['widget-'],
            'incident_type': ['incidenttype-']
        }
        for obj_type, prefixes in type_prefixes.items():
            base_key = f"{obj_type}:{ref_norm}"
            if base_key in self.object_registry:
                return base_key
            for p in prefixes:
                cand = f"{obj_type}:{p}{ref_norm}"
                if cand in self.object_registry:
                    return cand
        # 3) Correspondance partielle assez longue
        low = ref_norm.lower()
        if len(low) >= 4:
            for key, obj in self.object_registry.items():
                oid = str(obj['id']).lower()
                if low in oid or oid in low:
                    return key
        return None

    # -------------------------------
    # GREP -rni (implémentation Python)
    # -------------------------------
    def _build_search_terms(self, obj_key: str) -> List[str]:
        obj = self.object_registry[obj_key]
        oid = obj['id']
        terms = {oid}
        # Ajouter version "sans préfixe"
        for pref in ['playbook-', 'automation-', 'script-', 'incidenttype-', 'incidentfield-',
                     'field-', 'layoutscontainer-', 'layout-', 'widget-', 'reputation-', 'indicator-']:
            if oid.startswith(pref):
                terms.add(oid[len(pref):])
        # Nom affiché alternatif
        data = obj.get('data', {}) or {}
        alt = None
        if obj['type'] == 'integration':
            alt = data.get('display') or data.get('name')
        elif obj['type'] in ('automation', 'playbook'):
            alt = data.get('name')
        elif obj['type'] in ('incident_type', 'incident_field', 'layout', 'widget', 'classifier', 'mapper', 'report'):
            alt = data.get('name') or data.get('id')
        if isinstance(alt, str) and alt.strip():
            terms.add(alt.strip())
        # Nom de fichier sans extension
        terms.add(Path(obj['filename']).stem)
        # Nettoyage
        terms = {t for t in terms if self.is_valid_reference(str(t))}
        return sorted(terms, key=lambda s: (-len(s), s))  # longs d'abord

    def _compile_patterns(self, terms: List[str]) -> Tuple[re.Pattern, re.Pattern]:
        # Pattern 1: clé explicite (YAML/JSON) ex: playbookId: NAME | scriptId: NAME | script: NAME
        joined = '|'.join(re.escape(t) for t in terms)
        keynames = r'(?:playbookId|scriptId|script|id|classifierId|mapperId|layout|incidenttype|type|widget)'
        p1 = re.compile(fr'(?i)\b{keynames}\s*:\s*(?:"|\')?\s*(?:{joined})\b')
        # Pattern 2: occurrence générique avec délimiteurs (pour .py/.md/etc.)
        p2 = re.compile(fr'(?i)(?<![\w-])(?:{joined})(?![\w-])')
        return p1, p2

    def _should_skip_path(self, path: Path) -> bool:
        parts = {p for p in path.parts}
        if any(d in parts for d in self.ignore_dirs):
            return True
        if path.suffix.lower() not in self.allowed_grep_exts:
            return True
        if _is_binary_file(path):
            return True
        try:
            if path.stat().st_size > 2 * 1024 * 1024:  # 2MB
                return True
        except Exception:
            return True
        return False

    def grep_rni_for_object(self, obj_key: str) -> List[Dict[str, Any]]:
        obj = self.object_registry[obj_key]
        own_path = Path(obj['path']).resolve()
        terms = self._build_search_terms(obj_key)
        p1, p2 = self._compile_patterns(terms)
        out: List[Dict[str, Any]] = []
        for path in self.input_path.rglob('*'):
            if not path.is_file():
                continue
            if self._should_skip_path(path):
                continue
            # Éviter le propre fichier de l'objet
            try:
                if path.resolve() == own_path:
                    continue
            except Exception:
                pass
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for idx, line in enumerate(f, start=1):
                        if p1.search(line) or p2.search(line):
                            # ignorer probablement les commentaires simples
                            striped = line.strip()
                            if striped.startswith('#') or striped.startswith('//'):
                                continue
                            out.append({
                                'file': str(path),
                                'line': idx,
                                'text': line.rstrip('\n')
                            })
            except Exception:
                continue
        return out

    # -------------------------------
    # Analyse dépendances + usages
    # -------------------------------
    def analyze(self, start_files: Optional[List[str]] = None) -> Dict[str, Any]:
        # 1) Registre
        self.build_registry()
        if not self.object_registry:
            return {'error': 'Aucun objet XSOAR custom détecté.'}

        # 2) Dépendances (graph restreint à objets)
        results: Dict[str, Dict[str, Any]] = {}
        processed = set()
        queue = deque()
        if start_files:
            for name in start_files:
                uk = self.file_registry.get(name)
                if uk:
                    queue.append(uk)
        else:
            queue.extend(self.object_registry.keys())

        level = 0
        while queue and level < 10:
            level += 1
            for _ in range(len(queue)):
                uk = queue.popleft()
                if uk in processed:
                    continue
                processed.add(uk)
                obj = self.object_registry[uk]
                extractor = self.dependency_extractors.get(obj['type'])
                soft_extractor = self.soft_ref_extractors.get(obj['type'], self._noop_soft_refs)
                hard_deps = extractor(obj['data']) if extractor else set()
                resolved = {}
                unresolved = []
                for dep in hard_deps:
                    rk = self.resolve_dependency(dep)
                    if rk:
                        resolved[rk] = {
                            'id': self.object_registry[rk]['id'],
                            'type': self.object_registry[rk]['type'],
                            'filename': self.object_registry[rk]['filename'],
                        }
                        if rk not in processed:
                            queue.append(rk)
                    else:
                        unresolved.append(dep)
                soft_refs = soft_extractor(obj['data'])
                results[uk] = {
                    'object': {'id': obj['id'], 'type': obj['type'], 'filename': obj['filename']},
                    'dependencies': resolved,               # OBJETS uniquement
                    'unresolved': sorted(unresolved),       # candidats objets non résolus
                    'soft_refs': {
                        'context_paths': sorted(soft_refs.get('context_paths', set())),
                        'incident_fields': sorted(soft_refs.get('incident_fields', set())),
                        'commands': sorted(soft_refs.get('commands', set())),
                    },
                    'dependency_count': len(resolved),
                    'analysis_level': level
                }

        # 3) GREP usages pour chaque objet
        for uk in self.object_registry.keys():
            occ = self.grep_rni_for_object(uk)
            # Filtrer encore: ignorer occurrences sous /Tests/ et doublons par (f,l)
            seen = set()
            filtered = []
            for o in occ:
                p = Path(o['file'])
                if any(d in set(p.parts) for d in self.ignore_dirs):
                    continue
                key = (o['file'], o['line'])
                if key in seen:
                    continue
                seen.add(key)
                filtered.append(o)
            self.usage_index[uk] = filtered

        # 4) Option: ne garder que les objets "utilisés"
        used_keys = set(self.object_registry.keys())
        if self.used_only:
            used_keys = {uk for uk, occ in self.usage_index.items() if len(occ) > 0}

        # 5) Construction du rapport
        analysis_results = {uk: v for uk, v in results.items() if uk in used_keys}
        report = self._make_report(analysis_results, used_keys)
        return {
            'analysis_results': analysis_results,
            'report': report,
            'usage_index': self.usage_index,
            'stats': dict(self.statistics),
        }

    def _make_report(self, analysis_results: Dict[str, Any], used_keys: Set[str]) -> Dict[str, Any]:
        type_stats = defaultdict(lambda: {'count': 0, 'with_deps': 0, 'avg_deps': 0.0})
        reverse_deps = defaultdict(set)
        dep_graph = {}
        total_deps = 0
        for uk, res in analysis_results.items():
            t = res['object']['type']
            c = res['dependency_count']
            type_stats[t]['count'] += 1
            type_stats[t]['with_deps'] += 1 if c > 0 else 0
            total_deps += c
            dep_graph[uk] = list(res['dependencies'].keys())
            for dk in res['dependencies'].keys():
                reverse_deps[dk].add(uk)
        for t, s in type_stats.items():
            if s['count']:
                s['avg_deps'] = round(sum(analysis_results[k]['dependency_count'] for k in analysis_results if analysis_results[k]['object']['type'] == t) / s['count'], 2)
        most_ref = sorted(((k, len(v)) for k, v in reverse_deps.items()), key=lambda x: x[1], reverse=True)[:10]
        out = {
            'summary': {
                'total_custom_objects_indexed': len(self.object_registry),
                'total_custom_objects_used': len(used_keys),
                'total_dependencies_found': total_deps,
            },
            'statistics_by_type': dict(type_stats),
            'most_referenced_objects': [
                {
                    'key': k,
                    'object': self.object_registry.get(k, {}).get('id', 'Unknown'),
                    'type': self.object_registry.get(k, {}).get('type', 'Unknown'),
                    'reference_count': n
                } for k, n in most_ref
            ],
            'dependency_graph': dep_graph,
            'reverse_dependencies': {k: sorted(list(v)) for k, v in reverse_deps.items()},
        }
        return out

    # ----------------
    # Export des rapports
    # ----------------
    def save_outputs(self, results: Dict[str, Any]) -> None:
        self.output_path.mkdir(parents=True, exist_ok=True)
        detailed = self.output_path / 'xsoar_dependencies_detailed.json'
        with open(detailed, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        summary = self.output_path / 'xsoar_dependencies_summary.json'
        with open(summary, 'w', encoding='utf-8') as f:
            json.dump(results.get('report', {}), f, indent=2, ensure_ascii=False)
        # CSV (uniquement vraies deps d'objets + non résolus + occurrences grep consolidées)
        csv_path = self.output_path / 'xsoar_dependencies_report.csv'
        self._save_csv(csv_path, results['analysis_results'])
        # Usages détaillés (grep)
        usages_path = self.output_path / 'xsoar_usages_grep.json'
        with open(usages_path, 'w', encoding='utf-8') as f:
            json.dump(self.usage_index, f, indent=2, ensure_ascii=False)

    def _save_csv(self, path: Path, analysis_results: Dict[str, Any]) -> None:
        import csv
        with open(path, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, delimiter=';')
            w.writerow(['Objet Parent','Type Parent','Statut Parent','Objet Fils','Type Fils','Statut Fils','Nombre References','Contexte'])
            # Dépendances résolues
            for pk, res in analysis_results.items():
                p = res['object']
                for ck, cinfo in res['dependencies'].items():
                    ctx = f"{cinfo['id']} référencé par {p['id']}"
                    w.writerow([p['id'], p['type'], 'Trouvé', cinfo['id'], cinfo['type'], 'Trouvé', 1, ctx])
            # Non résolues (candidats objets)
            for pk, res in analysis_results.items():
                p = res['object']
                for u in res['unresolved']:
                    ctx = f"{u} non résolu dans {p['id']}"
                    w.writerow([p['id'], p['type'], 'Trouvé', u, 'Inconnu', 'Non trouvé', 1, ctx])

    # ---------------
    # Entrée principale
    # ---------------
    def run(self, start_files: Optional[List[str]] = None) -> None:
        results = self.analyze(start_files)
        if 'error' in results:
            print('❌', results['error'])
            return
        self.save_outputs(results)
        self.print_summary(results['report'])

    def print_summary(self, report: Dict[str, Any]) -> None:
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DE L'ANALYSE (custom & utilisés)")
        print("="*60)
        s = report['summary']
        print(f"Objets custom indexés: {s['total_custom_objects_indexed']}")
        print(f"Objets custom utilisés: {s['total_custom_objects_used']}")
        print(f"Dépendances (objets) trouvées: {s['total_dependencies_found']}")
        print("\nPar type:")
        for t, st in report['statistics_by_type'].items():
            print(f"  - {t:15} -> {st['count']} utilisés, {st['with_deps']} avec deps, moy {st['avg_deps']} dép/objet")
        if report['most_referenced_objects']:
            print("\nObjets les plus référencés:")
            for item in report['most_referenced_objects'][:5]:
                print(f"  * {item['object']} ({item['type']}) -> {item['reference_count']} références")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='XSOAR Crawler (avec grep -rni)')
    parser.add_argument('-i', '--input', required=True, help='Racine de la codebase XSOAR')
    parser.add_argument('-o', '--output', required=True, help='Dossier de sortie pour les rapports')
    parser.add_argument('--all', action='store_true', help='Inclure aussi les objets non utilisés (désactive used_only)')
    parser.add_argument('--include-native', action='store_true', help='Inclure les objets natifs (désactive custom_only)')
    parser.add_argument('--start', nargs='*', help='Analyser à partir de fichiers précis (noms exacts)')
    args = parser.parse_args()

    crawler = XSOARCrawler(
        input_path=args.input,
        output_path=args.output,
        custom_only=not args.include_native,
        used_only=not args.all,
    )
    crawler.run(start_files=args.start)
