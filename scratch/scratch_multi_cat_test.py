import requests
from bs4 import BeautifulSoup
import json
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

test_categories = [
    ("Dairy", "https://blinkit.com/cn/milk/cid/14/922"),
    ("Bakery", "https://blinkit.com/cn/bread-pav/cid/14/953"),
    ("Snacks", "https://blinkit.com/cn/namkeen-snacks/cid/1237/29"),
    ("Vegetables", "https://blinkit.com/cn/fresh-vegetables/cid/1487/1489")
]

all_extracted = []

for cat_name, url in test_categories:
    print(f"\nFetching {cat_name}: {url} ...")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"Status: {r.status_code}, Length: {len(r.content)}")
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for PRELOADED_STATE
        found = False
        for s in soup.find_all('script'):
            txt = s.text or ""
            if "window.grofers.PRELOADED_STATE" in txt:
                idx = txt.find("window.grofers.PRELOADED_STATE = ") + len("window.grofers.PRELOADED_STATE = ")
                end_idx = txt.rfind("};") + 1
                state = json.loads(txt[idx:end_idx])
                found = True
                
                # Walk state and find all snippet / card dicts
                def walk(obj):
                    if isinstance(obj, dict):
                        # check common_attributes or click_map
                        c_attr = obj.get('common_attributes') or obj.get('click_map')
                        if c_attr and isinstance(c_attr, dict) and ('product_id' in c_attr or 'name' in c_attr):
                            pid = c_attr.get('product_id')
                            name = c_attr.get('name')
                            brand = c_attr.get('brand')
                            price = c_attr.get('price')
                            mrp = c_attr.get('mrp')
                            inv = c_attr.get('inventory')
                            state_val = c_attr.get('state')
                            l0 = c_attr.get('l0_category')
                            l1 = c_attr.get('l1_category')
                            
                            # Also check stepper or variant if available
                            variant = None
                            if 'stepper_data_v2' in obj:
                                pass
                            
                            if pid and name:
                                all_extracted.append({
                                    "target_category": cat_name,
                                    "product_id": str(pid),
                                    "product_name": name,
                                    "brand": brand,
                                    "price": price,
                                    "mrp": mrp,
                                    "inventory": inv,
                                    "availability": state_val,
                                    "l0_category": l0,
                                    "l1_category": l1,
                                    "url": url
                                })
                        for v in obj.values():
                            walk(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            walk(item)
                
                walk(state)
                break
        if not found:
            print("No state found!")
    except Exception as e:
        print("Error:", e)
    time.sleep(1)

print(f"\nTotal extracted across categories: {len(all_extracted)}")
# Deduplicate by product_id
unique = {p['product_id']: p for p in all_extracted}.values()
print(f"Total unique products: {len(unique)}")
for u in list(unique)[:15]:
    print(u)
