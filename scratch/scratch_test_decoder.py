import requests
from bs4 import BeautifulSoup
import json

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

if target_script:
    # Print what comes around column 538205
    idx = target_script.find("window.grofers.PRELOADED_STATE = ") + len("window.grofers.PRELOADED_STATE = ")
    # test raw json parse using raw_decode
    decoder = json.JSONDecoder()
    obj, end_pos = decoder.raw_decode(target_script[idx:])
    print("Successfully parsed via raw_decode! Consumed characters:", end_pos)
    print("Top keys:", list(obj.keys()))
    # check what was after end_pos
    after = target_script[idx + end_pos : idx + end_pos + 100]
    print("Text after json object:", repr(after))
