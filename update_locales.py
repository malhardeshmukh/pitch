import json
import re

def replace_text(text):
    text = re.sub(r'\bProduct\b', 'Model', text)
    text = re.sub(r'\bproduct\b', 'model', text)
    text = re.sub(r'\bProducts\b', 'Models', text)
    text = re.sub(r'\bproducts\b', 'models', text)
    text = re.sub(r'\bUsed\b', 'Preowned', text)
    text = re.sub(r'\bused\b', 'preowned', text)
    text = re.sub(r'\bCatalog\b', 'Models', text)
    return text

def walk_and_replace(obj):
    if isinstance(obj, dict):
        return {k: walk_and_replace(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [walk_and_replace(v) for v in obj]
    elif isinstance(obj, str):
        return replace_text(obj)
    return obj

with open('c:\\pitch\\locales\\en.default.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract comments and JSON
comments = []
json_lines = []
in_json = False
for line in lines:
    if line.strip().startswith('{') and not in_json:
        in_json = True
    if not in_json:
        comments.append(line)
    else:
        # Strip trailing comments for json parsing if any simple ones exist
        json_lines.append(line)

json_str = ''.join(json_lines)

# Remove single line comments which are not valid JSON
json_str = re.sub(r'^\s*//.*$', '', json_str, flags=re.MULTILINE)

try:
    data = json.loads(json_str)
    new_data = walk_and_replace(data)
    
    with open('c:\\pitch\\locales\\en.default.json', 'w', encoding='utf-8') as f:
        f.write(''.join(comments))
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    print('Updated en.default.json')
except Exception as e:
    print('Error:', e)
