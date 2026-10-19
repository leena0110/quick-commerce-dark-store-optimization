import json

with open("blinkit_sample_state.json", "r", encoding="utf-8") as f:
    state = json.load(f)

cats = state.get('data', {}).get('categories', {}).get('list', [])
print(f"Total categories in list: {len(cats)}")

for c in cats:
    print(f"Cat ID: {c.get('id')}, Name: {c.get('name')}, Slug: {c.get('slug')}")
    sub_cats = c.get('sub_categories') or c.get('subcategories') or []
    if sub_cats:
        print(f"  Subcategories ({len(sub_cats)}): {[s.get('name') for s in sub_cats[:3]]}")
