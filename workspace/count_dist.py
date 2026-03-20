import json
with open('results/inner_monologue_dataset.json', encoding='utf-8') as f:
    data = json.load(f)
from collections import Counter
counts = Counter(d.get('behavior_type') for d in data)
print("Behavior types:", counts)

cat_counts = Counter(d.get('resistance_parent') for d in data if d.get('behavior_type') == 'resistance')
print("Parents:", cat_counts)
