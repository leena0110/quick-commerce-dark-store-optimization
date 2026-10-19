import json

# Load state
import requests
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
r = requests.get("https://blinkit.com/cn/bread-pav/cid/14/953", headers=headers, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')
for s in soup.find_all('script'):
    txt = s.text or ""
    if "window.grofers.PRELOADED_STATE" in txt:
        idx = txt.find("window.grofers.PRELOADED_STATE = ") + len("window.grofers.PRELOADED_STATE = ")
        state, _ = json.JSONDecoder().raw_decode(txt[idx:])
        break

def find_pid(obj, target_id="757807"):
    if isinstance(obj, dict):
        if obj.get('product_id') == target_id or obj.get('identity', {}).get('id') == target_id:
            print("FOUND PARENT DICT KEYS:", list(obj.keys()))
            if 'variant' in obj:
                print("Variant in obj:", obj['variant'])
            if 'unit' in obj:
                print("Unit in obj:", obj['unit'])
            if 'display_name' in obj:
                print("Display name in obj:", obj['display_name'])
        for k, v in obj.items():
            find_pid(v, target_id)
    elif isinstance(obj, list):
        for item in obj:
            find_pid(item, target_id)

find_pid(state, "757807")
