import json

with open("blinkit_sample_state.json", "r", encoding="utf-8") as f:
    state = json.load(f)

def extract_products(state):
    extracted = []
    
    def walk(obj):
        if isinstance(obj, dict):
            # A product item in blinkit layout usually has 'identity' with an 'id', 'name', 'normal_price'
            if 'product_id' in obj or ('identity' in obj and 'name' in obj and 'normal_price' in obj):
                # Extract clean fields
                pid = obj.get('product_id') or obj.get('identity', {}).get('id')
                name = obj.get('name', {}).get('text') if isinstance(obj.get('name'), dict) else obj.get('name')
                brand = obj.get('brand_name') or obj.get('brand')
                variant = obj.get('variant', {}).get('text') if isinstance(obj.get('variant'), dict) else obj.get('variant')
                
                # Price extraction
                price_text = obj.get('normal_price', {}).get('text') if isinstance(obj.get('normal_price'), dict) else str(obj.get('normal_price', ''))
                # Offer or mrp
                mrp_text = ""
                if 'offer' in obj and isinstance(obj['offer'], dict):
                    mrp_text = obj['offer'].get('text', '')
                elif 'mrp' in obj:
                    mrp_text = str(obj['mrp'])
                
                inventory = obj.get('inventory')
                is_sold_out = obj.get('is_sold_out', False)
                rating = obj.get('rating', {}).get('value') if isinstance(obj.get('rating'), dict) else obj.get('rating')
                merchant_id = obj.get('merchant_id')
                
                if pid and name:
                    extracted.append({
                        "product_id": str(pid),
                        "product_name": name,
                        "brand": brand,
                        "variant": variant,
                        "price_raw": price_text,
                        "mrp_raw": mrp_text,
                        "inventory": inventory,
                        "is_sold_out": is_sold_out,
                        "rating": rating,
                        "merchant_id": merchant_id
                    })
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(state)
    return extracted

prods = extract_products(state)
# Deduplicate by product_id
unique_prods = {p['product_id']: p for p in prods}.values()
print(f"Extracted {len(prods)} product instances, {len(unique_prods)} unique products!")

for p in list(unique_prods)[:10]:
    print(p)
