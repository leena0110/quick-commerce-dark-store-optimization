import requests
import xml.etree.ElementTree as ET

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

r = requests.get("https://blinkit.com/sitemap.xml", headers=headers, timeout=10)
print("Sitemap status:", r.status_code)
root = ET.fromstring(r.content)
# sitemaps have namespace
namespaces = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs = [elem.text for elem in root.findall('.//sm:loc', namespaces)]
print(f"Total sitemaps found: {len(locs)}")
for l in locs[:20]:
    print(l)
