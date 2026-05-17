
import json
import re
import os

summary_path = r'C:\Projects\Dashboard\4. Blueprint\Books\Better_Version_Summary.json'
dossier_path = r'C:\Projects\Dashboard\4. Blueprint\Books\Better_Version_Master_Dossier.md'

with open(summary_path, 'r', encoding='utf-8') as f:
    summary_data = json.load(f)

base_names = [i['base_name'] for i in summary_data]

book_summaries = {}
current_title = None
tree_labels = []
in_tree = False

with open(dossier_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('### '):
            if current_title:
                book_summaries[current_title] = ' '.join(tree_labels)
            
            m = re.match(r'### \d+\. (.*)', line.strip())
            if m:
                current_title = m.group(1).strip()
            else:
                current_title = line.strip()[4:].strip()
            tree_labels = []
            in_tree = False
        elif '**Concept tree:**' in line:
            in_tree = True
        elif in_tree:
            if '```' in line:
                if tree_labels: in_tree = False
                continue
            m = re.search(r'\"label\": \"(.*?)\"', line)
            if m:
                label = m.group(1)
                if not label.startswith('[Item'):
                    tree_labels.append(label)

if current_title:
    book_summaries[current_title] = ' '.join(tree_labels)

final_list = []
for bn in base_names:
    s = book_summaries.get(bn)
    if not s:
        for k, v in book_summaries.items():
            if bn in k or k in bn:
                s = v
                break
    final_list.append({'title': bn, 'summary_labels': s or ''})

with open('books_data.json', 'w', encoding='utf-8') as f:
    json.dump(final_list, f, ensure_ascii=False, indent=2)
