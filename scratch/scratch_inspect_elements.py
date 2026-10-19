import requests
from bs4 import BeautifulSoup
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. Investigate Blinkit HTML
print("--- Investigating Blinkit HTML ---")
r_b = requests.get("https://blinkit.com/cn/dairy-breakfast/cid/14/922", headers=headers, timeout=15)
soup_b = BeautifulSoup(r_b.text, 'html.parser')
# find all scripts
scripts = soup_b.find_all('script')
print(f"Blinkit total script tags: {len(scripts)}")
for idx, s in enumerate(scripts):
    txt = s.text or ""
    if "window.__PRELOADED_STATE__" in txt or "window.__INITIAL_STATE__" in txt or "props" in txt or "products" in txt:
        print(f"Script {idx} has relevant state! length: {len(txt)}")
        print(txt[:300])

# Look for product cards / text in Blinkit
product_divs = soup_b.find_all(attrs={"data-test-id": True})
print(f"Blinkit data-test-id count: {len(product_divs)}")
for d in product_divs[:5]:
    print("Test ID:", d.get("data-test-id"), "Text:", d.get_text()[:100])

# 2. Investigate JioMart HTML
print("\n--- Investigating JioMart HTML ---")
r_j = requests.get("https://www.jiomart.com/c/groceries/dairy-bakery/dairy/62", headers=headers, timeout=15)
soup_j = BeautifulSoup(r_j.text, 'html.parser')
# search for product cards
cards = soup_j.find_all('div', class_=re.compile(r'product|card|item', re.I))
print(f"JioMart matching card tags: {len(cards)}")
# Let's check classes on jio mart
links = soup_j.find_all('a', href=re.compile(r'/p/groceries/'))
print(f"JioMart product links found: {len(links)}")
for l in links[:5]:
    print("Link:", l.get('href'), "Text:", l.get_text(strip=True)[:100])

# Check robots.txt for both
print("\n--- Checking robots.txt ---")
for site in ["https://blinkit.com/robots.txt", "https://www.jiomart.com/robots.txt", "https://www.bigbasket.com/robots.txt"]:
    try:
        rob = requests.get(site, headers=headers, timeout=10)
        print(f"\nRobots.txt for {site} (status {rob.status_code}):")
        lines = [ln for ln in rob.text.split('\n') if 'User-agent' in ln or 'Disallow' in ln][:15]
        print('\n'.join(lines))
    except Exception as e:
        print(f"Error checking {site}: {e}")
