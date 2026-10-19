import json
from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://blinkit.com/cn/bread-pav/cid/14/953"
session = requests.Session()
r = session.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')

target_script = None
for s in soup.find_all('script'):
    txt = s.text or ""
    if "window.grofers.PRELOADED_STATE" in txt:
        target_script = txt
        break

idx = target_script.find("window.grofers.PRELOADED_STATE = ") + len("window.grofers.PRELOADED_STATE = ")
decoder = json.JSONDecoder()
state, _ = decoder.raw_decode(target_script[idx:])

def extract_from_state(state, source_url):
    records = []
    
    # In blinkit state, products are stored in snippets with common_attributes, or in widget objects
    def walk(obj):
        if isinstance(obj, dict):
            # Check if this node has product info
            # Format 1: common_attributes
            ca = obj.get('common_attributes')
            if ca and isinstance(ca, dict) and ca.get('name') and ca.get('product_id'):
                # Extract variant text from surrounding obj if available
                variant_txt = None
                if 'variant' in obj:
                    v = obj['variant']
                    variant_txt = v.get('text') if isinstance(v, dict) else str(v)
                elif 'unit' in obj:
                    variant_txt = str(obj['unit'])
                
                # Check normal price
                price_val = ca.get('price')
                mrp_val = ca.get('mrp')
                
                records.append({
                    'source_product_id': str(ca.get('product_id')),
                    'product_name': ca.get('name'),
                    'brand': ca.get('brand'),
                    'variant': variant_txt,
                    'displayed_price': price_val,
                    'original_price': mrp_val,
                    'inventory': ca.get('inventory'),
                    'availability_status': ca.get('state'),
                    'category': ca.get('l0_category'),
                    'subcategory': ca.get('l1_category') or ca.get('ptype'),
                    'rating': ca.get('rating')
                })
            
            # Format 2: cart_item or snippet
            for k, v in obj.items():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)
                
    walk(state)
    return records

items = extract_from_state(state, url)
print(f"Extracted {len(items)} items")
# Deduplicate
unique = {it['source_product_id']: it for it in items}.values()
print(f"Unique products: {len(unique)}")
for u in list(unique)[:8]:
    print(u)
