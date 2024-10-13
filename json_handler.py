import json
import re
from collections import OrderedDict

def load_json_ordered(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=OrderedDict)

def save_json_ordered(file_path, data, ensure_ascii=True):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=ensure_ascii, indent=2)