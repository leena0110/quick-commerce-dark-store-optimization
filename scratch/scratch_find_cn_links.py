import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://blinkit.com/cn/dairy-breakfast/cid/14/922"
r = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('a', href=True)
cn_links = set()
for a in links:
    href = a['href']
    if '/cn/' in href:
        full = href if href.startswith('http') else 'https://blinkit.com' + href
        cn_links.add((full, a.get_text(strip=True)))

print(f"Total /cn/ links found: {len(cn_links)}")
for l, text in sorted(list(cn_links)):
    print(f"{text} -> {l}")
