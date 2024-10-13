import json
import re

from api.openrouter_api import OpenRouterAPI

def print_translations(translated_data, missing_translations, prefix=''):
    print("---------Translations-----------")
    for key, value in translated_data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        original_value = missing_translations.get(key, "N/A")
        
        if isinstance(value, dict):
            print_translations(value, original_value, full_key)
        else:
            print(f"KEY:{full_key}")
            print(f"{original_value}")
            print(f"{value}")
            print("")
    print("--------------------")

def translate_missing_keys(model_api, missing_translations, system_prompt, requirements, target_language):
    # Convert missing translations to JSON
    json_input = json.dumps(missing_translations, ensure_ascii=False)
    
    # Update system prompt to instruct the model to work with JSON
    json_system_prompt = f"{system_prompt}\n Translation to target language: {target_language}."
    
    # Call the API once with the JSON input
    translated_json = model_api.translate(json_input, json_system_prompt, requirements)
    
    # Remove extra escaping
    translated_json = re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'', translated_json)

    try:
        # Parse the JSON string into a Python dictionary
        translated_dict = json.loads(translated_json)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Problematic JSON string: {translated_json}")
        raise

    # print_translations(translated_dict, missing_translations)

    # Return the translated dictionary
    return translated_dict