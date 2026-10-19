import requests
import xml.etree.ElementTree as ET

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

r = requests.get("https://blinkit.com/sitemaps/categories.xml", headers=headers, timeout=10)
print("Categories xml status:", r.status_code)
root = ET.fromstring(r.content)
namespaces = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs = [elem.text for elem in root.findall('.//sm:loc', namespaces)]
print(f"Total category URLs in categories.xml: {len(locs)}")

for l in locs[:25]:
    print(l)
