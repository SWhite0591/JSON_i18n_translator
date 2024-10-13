from json_handler import load_json_ordered, save_json_ordered
from translation_comparator import find_missing_translations
from translator import translate_missing_keys
from collections import OrderedDict
import os
from config import REQUIREMENTS_FILE_FORMAT, SYSTEM_PROMPT_PATH, TRANSLATE_CHUNK_SIZE
from api.deepseek_api import DeepSeekAPI

def process_translation(api, en_data, target_data, target_language, locale_path, retranslate_keys=None):
    # Load system prompt and requirements files
    with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    requirements_file = os.path.join(locale_path, REQUIREMENTS_FILE_FORMAT.format(lang=target_language))
    requirements = ""
    if os.path.exists(requirements_file):
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements = f.read()

    # Find missing translations
    missing_translations = find_missing_translations(en_data, target_data)
    print(f"Missing translations: {len(missing_translations)}")

    # Add keys to be retranslated to missing_translations
    if retranslate_keys:
        for key in retranslate_keys:
            retranslate_data = get_nested_value(en_data, key)
            if retranslate_data is not None:
                if isinstance(retranslate_data, (dict, OrderedDict)):
                    nested_retranslate = find_missing_translations(retranslate_data, {}, key)
                    missing_translations.update(nested_retranslate)
                else:
                    missing_translations[key] = retranslate_data
        print(f"Total translations to process: {len(missing_translations)}")

    if not missing_translations:
        print("No missing translations or keys to retranslate. Skipping translation process.")
        return target_data

    missing_chunks = [dict(list(missing_translations.items())[i:i+TRANSLATE_CHUNK_SIZE]) for i in range(0, len(missing_translations), TRANSLATE_CHUNK_SIZE)]

    translated_data = {}
    for chunk in missing_chunks:
        # Translate missing keys for each chunk
        chunk_translated = translate_missing_keys(api, chunk, system_prompt, requirements, target_language)
        # Merge chunk translations into translated_data
        translated_data.update(chunk_translated)

    # Merge translations
    merged_data, untranslated_keys = merge_translations_ordered(en_data, target_data, translated_data, retranslate_keys)

    if untranslated_keys:
        print(f"Warning: The following keys were not translated: {', '.join(untranslated_keys)}")

    return merged_data

def merge_translations_ordered(en_data, target_data, translated_data, retranslate_keys=None, prefix=''):
    result = OrderedDict()
    untranslated_keys = []
    
    for key, value in en_data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, OrderedDict):
            nested_target = target_data.get(key, OrderedDict())
            nested_result, nested_untranslated = merge_translations_ordered(
                value, nested_target, translated_data, retranslate_keys, full_key
            )
            result[key] = nested_result
            untranslated_keys.extend(nested_untranslated)
        else:
            if full_key in translated_data:
                result[key] = translated_data[full_key]
            elif key in target_data and (not retranslate_keys or full_key not in retranslate_keys):
                result[key] = target_data[key]
            else:
                if full_key in translated_data:
                    result[key] = translated_data[full_key]
                else:
                    result[key] = value  # Use English text as default
                    untranslated_keys.append(full_key)

    return result, untranslated_keys

def get_full_key(data, key, prefix=''):
    
    for k, v in data.items():
        current_key = f"{prefix}.{k}" if prefix else k
        if k == key:
            return current_key
        if isinstance(v, dict):
            result = get_full_key(v, key, current_key)
            if result:
                return result
    return None

def get_nested_value(data, key):
    keys = key.split('.')
    value = data
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return None
    return value

def set_nested_value(data, key, value):
    keys = key.split('.')
    for k in keys[:-1]:
        if k not in data:
            data[k] = {}
        data = data[k]
    data[keys[-1]] = value
