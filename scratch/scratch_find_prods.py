import json

with open("blinkit_sample_state.json", "r", encoding="utf-8") as f:
    state = json.load(f)

# Search recursively for product objects
def find_product_dicts(obj, depth=0):
    products = []
    if depth > 10:
        return products
    if isinstance(obj, dict):
        # Check if this dict looks like a product
        if any(k in obj for k in ['product_id', 'productId', 'product_name', 'productName', 'mrp', 'price', 'inventory']):
            products.append(obj)
        for k, v in obj.items():
            products.extend(find_product_dicts(v, depth+1))
    elif isinstance(obj, list):
        for item in obj:
            products.extend(find_product_dicts(item, depth+1))
    return products

prods = find_product_dicts(state)
print("Potential product dicts found:", len(prods))
if prods:
    print("Sample prod keys:", list(prods[0].keys()))
    # print sample
    sample = {k: prods[0][k] for k in list(prods[0].keys())[:10]}
    print("Sample prod:", json.dumps(sample, indent=2))
else:
    # Check categories
    cats = state.get('data', {}).get('categories', {})
    print("Categories list length:", len(cats.get('list', [])))
    if cats.get('list'):
        print("Sample cat:", cats['list'][0])
