import requests
from bs4 import BeautifulSoup
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://blinkit.com/cn/dairy-breakfast/cid/14/922"
r = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')

found_state = None
for s in soup.find_all('script'):
    txt = s.text or ""
    if "window.grofers.PRELOADED_STATE" in txt:
        # Extract the json part
        match = re.search(r'window\.grofers\.PRELOADED_STATE\s*=\s*(\{.*?\});\s*(?:window|\n|</script>)', txt, re.DOTALL)
        if match:
            raw_json = match.group(1)
            try:
                found_state = json.loads(raw_json)
                print("Successfully parsed Blinkit PRELOADED_STATE!")
            except Exception as e:
                print("JSON parse error:", e)
                # Try finding json up to end
                idx = txt.find("window.grofers.PRELOADED_STATE = ") + len("window.grofers.PRELOADED_STATE = ")
                end_idx = txt.rfind("};") + 1
                try:
                    found_state = json.loads(txt[idx:end_idx])
                    print("Successfully parsed via rfind!")
                except Exception as e2:
                    print("rfind JSON parse error:", e2)

if found_state:
    print("State Top Keys:", list(found_state.keys()))
    if 'data' in found_state:
        print("Data Keys:", list(found_state['data'].keys()))
        # Check layout or page data
        for k in found_state['data']:
            val = found_state['data'][k]
            if isinstance(val, dict):
                print(f"Key {k} is dict with keys:", list(val.keys())[:10])
            elif isinstance(val, list):
                print(f"Key {k} is list with length:", len(val))
    # Write sample to inspect
    with open("blinkit_sample_state.json", "w", encoding="utf-8") as f:
        json.dump(found_state, f, indent=2)
    print("Saved blinkit_sample_state.json")
