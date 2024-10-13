from json_handler import load_json_ordered, save_json_ordered
from translation_comparator import find_missing_translations
from translator import translate_missing_keys
from collections import OrderedDict
import os
from config import REQUIREMENTS_FILE_FORMAT, SYSTEM_PROMPT_PATH, TRANSLATE_CHUNK_SIZE
from api.deepseek_api import DeepSeekAPI

def process_translation(api, en_data, target_data, target_language, locale_path):
    # Load system prompt
    with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    # Try to load requirements file
    requirements_file = os.path.join(locale_path, REQUIREMENTS_FILE_FORMAT.format(lang=target_language))
    requirements = ""
    if os.path.exists(requirements_file):
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements = f.read()

    # Find missing translations
    missing_translations = find_missing_translations(en_data, target_data)
    print(f"Missing translations: {len(missing_translations)}")

    if not missing_translations:
        print("No missing translations. Skipping translation process.")
        return target_data

    missing_chunks = [dict(list(missing_translations.items())[i:i+TRANSLATE_CHUNK_SIZE]) for i in range(0, len(missing_translations), TRANSLATE_CHUNK_SIZE)]

    translated_data = {}
    for chunk in missing_chunks:
        # Translate missing keys for each chunk
        chunk_translated = translate_missing_keys(api, chunk, system_prompt, requirements, target_language)
        # Merge chunk translations into translated_data
        translated_data.update(chunk_translated)

    # print("Translated data:")
    # print(translated_data)

    # Merge translations
    merged_data, untranslated_keys = merge_translations_ordered(en_data, target_data, translated_data)

    if untranslated_keys:
        print(f"警告：以下键未被翻译: {', '.join(untranslated_keys)}")

    return merged_data

def merge_translations_ordered(en_data, target_data, translated_data, prefix=''):
    result = OrderedDict()
    untranslated_keys = []
    
    for key, value in en_data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, OrderedDict):
            
            nested_target = target_data.get(key, OrderedDict())
            nested_result, nested_untranslated = merge_translations_ordered(value, nested_target, translated_data, full_key)
            result[key] = nested_result
            untranslated_keys.extend(nested_untranslated)
        else:
            
            if key in target_data:
                result[key] = target_data[key]
            elif full_key in translated_data:
                result[key] = translated_data[full_key]
            elif key in translated_data:
                result[key] = translated_data[key]
            else:
                result[key] = value  # 使用英文原文作为默认值
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

def check_untranslated_keys(missing_translations, translated_data):
    untranslated = []
    for key in missing_translations:
        if key not in translated_data:
            untranslated.append(key)
    return untranslated