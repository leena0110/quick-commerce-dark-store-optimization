import requests
from bs4 import BeautifulSoup
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. Investigate JioMart
print("--- Investigating JioMart ---")
try:
    r = requests.get("https://www.jiomart.com/c/groceries/dairy-bakery/dairy/62", headers=headers, timeout=15)
    print("JioMart Dairy status:", r.status_code, "Length:", len(r.content))
    soup = BeautifulSoup(r.text[:500000], 'html.parser')
    # Search for product cards or JSON-LD
    scripts = soup.find_all('script', type='application/ld+json')
    print("JioMart JSON-LD found:", len(scripts))
    for s in scripts[:3]:
        print("Sample LD-JSON:", s.text[:200])
except Exception as e:
    print("JioMart error:", e)

# 2. Investigate Blinkit
print("\n--- Investigating Blinkit ---")
try:
    r = requests.get("https://blinkit.com/cn/dairy-breakfast/cid/14/922", headers=headers, timeout=15)
    print("Blinkit Category status:", r.status_code, "Length:", len(r.content))
    soup = BeautifulSoup(r.text, 'html.parser')
    # check next data
    next_data = soup.find('script', id='__NEXT_DATA__')
    if next_data:
        print("Blinkit NEXT_DATA found! Length:", len(next_data.text))
        data = json.loads(next_data.text)
        print("Keys:", list(data.keys()))
        print("Page props keys:", list(data.get('props', {}).get('pageProps', {}).keys()))
    else:
        print("No NEXT_DATA found on Blinkit")
except Exception as e:
    print("Blinkit error:", e)

# 3. Investigate DMart Ready
print("\n--- Investigating DMart Ready ---")
try:
    r = requests.get("https://www.dmart.in/category/dairy-1", headers=headers, timeout=15)
    print("DMart status:", r.status_code, "Length:", len(r.content))
    soup = BeautifulSoup(r.text, 'html.parser')
    next_data = soup.find('script', id='__NEXT_DATA__')
    if next_data:
        print("DMart NEXT_DATA found! Length:", len(next_data.text))
except Exception as e:
    print("DMart error:", e)
