import os
import json
import yaml
import re
from collections import defaultdict

# Chemins d'entrée et de sortie
INPUT_PATH = "/home/m.da-cruz/soar/"
OUTPUT_PATH = "/home/m.da-cruz/result/"

# Mots-clés valides
VALID_KEYWORDS = ("SOC", "incident", "field", "playbook", "automation", "layout", "indicator")


def list_all_files():
    return [
        f for f in os.listdir(INPUT_PATH)
        if f.endswith((".json", ".yml", ".yaml"))
    ]


def load_file(file_name):
    try:
        with open(os.path.join(INPUT_PATH, file_name), "r", encoding="utf-8") as file:
            if file_name.endswith(".json"):
                return json.load(file)
            return yaml.safe_load(file)
    except (FileNotFoundError, json.JSONDecodeError, yaml.YAMLError) as e:
        print(f"Erreur lors du chargement de {file_name} : {e}")
        return None


def normalize_name(value):
    return re.sub(r"[^a-zA-Z0-9_-]", '', value).lower()


def build_id_index(all_files):
    index = {}

    def add_by_pattern(obj, file):
        if isinstance(obj, dict):
            for val in obj.values():
                add_by_pattern(val, file)
        elif isinstance(obj, list):
            for item in obj:
                add_by_pattern(item, file)
        elif isinstance(obj, str):
            norm = normalize_name(obj)
            if norm.startswith(("soc-", "incidentfield-", "widget-")):
                index[norm] = file

    for file in all_files:
        data = load_file(file)
        if not isinstance(data, dict):
            continue
        if "id" in data:
            index[normalize_name(data["id"])] = file
        if "name" in data:
            index[normalize_name(data["name"])] = file
        add_by_pattern(data, file)

    return index


def categorize_file(file_name):
    if file_name.startswith("playbook-"):
        return "playbook"
    elif file_name.startswith("automation-"):
        return "automation"
    elif file_name.startswith("layoutscontainer-"):
        return "layout"
    elif file_name.startswith("SOC-") or file_name.startswith("incidenttype-SOC"):
        return "SOC"
    elif file_name.startswith("indicator-"):
        return "indicator"
    return "unknown"


def is_valid_string(value):
    if not value or not isinstance(value, str):
        return False
    return any(value.startswith(keyword) for keyword in VALID_KEYWORDS)


def extract_from_type_incident(data, all_inputs):
    type_used = set()

    def recurse(obj):
        if isinstance(obj, dict):
            if "extractAsIsIndicatorTypeId" in obj and isinstance(obj["extractAsIsIndicatorTypeId"], str):
                type_used.add(obj["extractAsIsIndicatorTypeId"])
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

    recurse(data)
    all_inputs["type_used"].update(type_used)
    return all_inputs


def extract_from_layout(data, all_inputs):
    layout_used = set()

    def recurse(obj):
        if isinstance(obj, dict):
            if "fieldId" in obj and isinstance(obj["fieldId"], str):
                layout_used.add(obj["fieldId"])
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

    recurse(data)
    all_inputs["layout_used"].update(layout_used)
    return all_inputs


def extract_from_playbook(data, all_inputs):
    playbook_used = set()

    def recurse(obj):
        if isinstance(obj, dict):
            if "name" in obj and is_valid_string(obj["name"]):
                playbook_used.add(obj["name"])
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

    recurse(data)
    all_inputs["playbook_used"].update(playbook_used)
    return all_inputs


def extract_from_automation(data, all_inputs):
    automation_used = set()

    def recurse(obj):
        if isinstance(obj, dict):
            if "scriptId" in obj and is_valid_string(obj["scriptId"]):
                automation_used.add(obj["scriptId"])
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

    recurse(data)
    all_inputs["automation_used"].update(automation_used)
    return all_inputs


def extract_from_incident_field(data):
    results = set()

    def recurse(obj):
        if isinstance(obj, dict):
            if "cliName" in obj and isinstance(obj["cliName"], str):
                results.add(obj["cliName"])
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

    recurse(data)
    return results


def get_referenced_files(data):
    referenced = {
        "playbook": set(),
        "automation": set(),
        "layout": set(),
        "SOC": set(),
        "indicator": set()
    }

    referenced_keys = {
        "playbook": {"playbookId", "name"},
        "Type": {"extractAsIsIndicatorTypeId"},
        "automation": {"scriptId"},
        "layout": {"fieldId"},
        "SOC": {"SOC-"},
        "indicator": {"indicator-"}
    }

    def recursive_search(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str) and is_valid_string(value):
                    for ref_type, keys in referenced_keys.items():
                        if key in keys or any(value.startswith(prefix) for prefix in keys):
                            referenced[ref_type].add(value)
                else:
                    recursive_search(value)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item)

    recursive_search(data)
    return referenced


def crawl(starting_file):
    all_files = list_all_files()
    if starting_file not in all_files:
        print(f"Error: file {starting_file} is unknown")
        return {}, {}

    id_index = build_id_index(all_files)
    visited = set()
    to_visit = [starting_file]

    discovered_files = {cat: set() for cat in ["playbook", "automation", "layout", "SOC", "indicator", "unknown"]}
    all_inputs = {
        "playbook_used": set(),
        "layout_used": set(),
        "automation_used": set(),
        "field_used": set(),
        "type_used": set()
    }

    while to_visit:
        current = to_visit.pop(0)
        if current in visited:
            continue
        visited.add(current)

        data = load_file(current)
        if not data:
            continue

        category = categorize_file(current)
        if category == "layout":
            extract_from_layout(data, all_inputs)
        elif category == "playbook":
            extract_from_playbook(data, all_inputs)
        elif category == "automation":
            extract_from_automation(data, all_inputs)
        elif category == "SOC":
            extract_from_type_incident(data, all_inputs)
        elif category == "indicator":
            all_inputs["field_used"].update(extract_from_incident_field(data))

        refs = get_referenced_files(data)
        if not refs or not isinstance(refs, dict):
            continue

        for ref_type, ids in refs.items():
            for obj_id in ids:
                norm_id = normalize_name(obj_id)
                matched_file = id_index.get(norm_id)

                if not matched_file:
                    prefix = {
                        "playbook": "playbook-",
                        "layout": "layout-",
                        "automation": "automation-",
                        "SOC": "SOC-",
                        "indicator": "indicator-"
                    }.get(ref_type, "")
                    matched_file = id_index.get(prefix + norm_id)

                if matched_file and matched_file not in visited and matched_file not in to_visit:
                    to_visit.append(matched_file)
                    discovered_files[categorize_file(matched_file)].add(matched_file)

    for file in to_visit:
        discovered_files[categorize_file(file)].add(file)

    return discovered_files, all_inputs


def main():
    starting_files = [
        "incidenttype-SOC-Default.json",
        "playbook-SOC-Module-Context.yml",
        "layoutscontainer-Report.json",
        "automation-StopScheduledTask.yml"
    ]

    all_files = list_all_files()
    id_index = build_id_index(all_files)
    final_results = []

    global_usage_tracker = {
        "playbook": defaultdict(set),
        "automation": defaultdict(set),
        "layout": defaultdict(set),
        "SOC": defaultdict(set),
        "incident_fields": defaultdict(set),
    }

    for file in starting_files:
        if file not in all_files:
            print(f"[ERREUR] Fichier {file} non trouvé.")
            continue

        discovered_files, all_inputs = crawl(file)

        for obj_type in global_usage_tracker:
            for obj_id in all_inputs.get(f"{obj_type}_used", []):
                global_usage_tracker[obj_type][obj_id].add(file)

        used_objects = {
            "playbook": sorted(all_inputs["playbook_used"]),
            "automation": sorted(all_inputs["automation_used"]),
            "layout": sorted(all_inputs["layout_used"]),
            "SOC": sorted(all_inputs["type_used"]),
            "incident_fields": sorted(all_inputs["field_used"]),
        }

        unresolved = {
            key: [obj_id for obj_id in used_objects[key] if normalize_name(obj_id) not in id_index]
            for key in ["playbook", "automation", "layout", "SOC"]
        }

        final_results.append({
            "source_file": file,
            "used": used_objects,
            "unresolved": unresolved,
            "discovered_files": {
                key: sorted(list(val)) for key, val in discovered_files.items()
            }
        })

    usage_summary = {
        key: {obj: len(files) for obj, files in usage_map.items()}
        for key, usage_map in global_usage_tracker.items()
    }

    output = {
        "results_by_source": final_results,
        "usage_summary": usage_summary
    }

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    output_file = os.path.join(OUTPUT_PATH, "xsoar_crawl_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n Résultats enregistrés dans : {output_file}")


if __name__ == "__main__":
    main()
