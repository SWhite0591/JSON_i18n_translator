import argparse
from json_handler import load_json_ordered, save_json_ordered
from api.siliconflow_api import SiliconFlowAPI
import os
from translation_processor import process_translation
from api.deepseek_api import DeepSeekAPI

def main():
    parser = argparse.ArgumentParser(description="JSON Language Pack Translator")
    parser.add_argument("locale_path", help="Path to the locale directory")
    parser.add_argument("--api", choices=["siliconflow", "deepseek"], default="deepseek", help="Choose API to use")
    parser.add_argument("--retranslate", nargs="+", help="Keys to force retranslation, e.g. 'a.b.c' 'd.e.f'")
    
    args = parser.parse_args()

    # Load English JSON file
    en_path = os.path.join(args.locale_path, "en.json")
    en_data = load_json_ordered(en_path)

    # Initialize the API based on user choice
    if args.api == "siliconflow":
        api = SiliconFlowAPI()
    elif args.api == "deepseek":
        api = DeepSeekAPI()

    # Process all JSON files in the locale directory
    for filename in os.listdir(args.locale_path):
        if filename.endswith(".json") and filename != "en.json":
            target_language = filename.split(".")[0]
            target_path = os.path.join(args.locale_path, filename)
            
            print(f"\nProcessing {target_language} translations...")
            
            # Load target JSON file
            target_data = load_json_ordered(target_path)

            # Process translation
            merged_data = process_translation(api, en_data, target_data, target_language, args.locale_path, args.retranslate)

            # Save updated target data
            save_json_ordered(target_path, merged_data, ensure_ascii=False)

            print(f"Updated translations saved to {target_path}")

    print("\nAll translations have been processed and updated.")

if __name__ == "__main__":
    main()

# Usage: python3 main.py path/to/locale --api deepseek --retranslate a.b.c d.e.f
