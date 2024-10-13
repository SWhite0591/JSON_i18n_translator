from collections import OrderedDict

def find_missing_translations(en_data, target_data, path=""):
    missing_translations = {}
    for key, value in en_data.items():
        current_path = f"{path}.{key}" if path else key
        if key not in target_data:
            if isinstance(value, (dict, OrderedDict)):
                nested_missing = find_missing_translations(value, {}, current_path)
                missing_translations.update(nested_missing)
            else:
                missing_translations[current_path] = value
        elif isinstance(value, (dict, OrderedDict)) and isinstance(target_data[key], (dict, OrderedDict)):
            nested_missing = find_missing_translations(value, target_data[key], current_path)
            missing_translations.update(nested_missing)
    return missing_translations