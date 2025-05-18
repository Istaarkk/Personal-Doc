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
    elif file_name.startswith("SOC-"):
        return "SOC"
    elif file_name.startswith("indicator-"):
        return "indicator"
    return "unknown"


def is_valid_string(value):
    if not value or not isinstance(value, str):
        return False
    return any(value.startswith(keyword) for keyword in VALID_KEYWORDS)


def get_referenced_files(data, source_file):
    references = {
        "playbook": defaultdict(set),
        "automation": defaultdict(set),
        "layout": defaultdict(set),
        "SOC": defaultdict(set),
        "indicator": defaultdict(set)
    }

    reference_keys = {
        "playbook": {"playbookId", "name"},
        "automation": {"scriptId"},
        "layout": {"fieldId"},
        "SOC": {"SOC-"},
        "indicator": {"indicator-"}
    }

    def recursive_search(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, str) and is_valid_string(value):
                    for ref_type, keys in reference_keys.items():
                        if key in keys or any(value.startswith(prefix) for prefix in keys):
                            references[ref_type][value].add(source_file)
                else:
                    recursive_search(value)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item)

    recursive_search(data)
    return references


def crawl(starting_file, all_files, id_index):
    visited = set()
    to_visit = [starting_file]

    discovered_files = set()
    object_usage = {
        "playbook": defaultdict(set),
        "automation": defaultdict(set),
        "layout": defaultdict(set),
        "SOC": defaultdict(set),
        "indicator": defaultdict(set)
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
        discovered_files.add(current)

        references = get_referenced_files(data, current)

        for ref_type, objects in references.items():
            for obj_id, sources in objects.items():
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

                object_usage[ref_type][obj_id].update(sources)

                if matched_file and matched_file not in visited and matched_file not in to_visit:
                    to_visit.append(matched_file)

    return discovered_files, object_usage


def convert_sets(obj):
    if isinstance(obj, dict):
        return {k: convert_sets(v) for k, v in obj.items()}
    elif isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, list):
        return [convert_sets(i) for i in obj]
    else:
        return obj


def main():
    starting_files = [
        "incidenttype-SOC-Default.json",
        "playbook-SOC-Module-Context.yml",
        "layoutscontainer-Report.json",
        "automation-StopScheduledTask.yml"
    ]

    all_files = list_all_files()
    id_index = build_id_index(all_files)

    results_by_source = {}
    summary = {
        "playbook": defaultdict(set),
        "automation": defaultdict(set),
        "layout": defaultdict(set),
        "SOC": defaultdict(set),
        "indicator": defaultdict(set)
    }

    for file in starting_files:
        if file not in all_files:
            print(f"Error: file {file} not found")
            continue

        discovered, usage = crawl(file, all_files, id_index)
        results_by_source[file] = discovered

        for obj_type in summary:
            for obj_id, files in usage[obj_type].items():
                summary[obj_type][obj_id].update(files)

    output = {
        "results_by_source": convert_sets(results_by_source),
        "object_references": convert_sets(summary)
    }

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    with open(os.path.join(OUTPUT_PATH, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print("✅ Résultat exporté vers summary.json")


if __name__ == "__main__":
    main()
