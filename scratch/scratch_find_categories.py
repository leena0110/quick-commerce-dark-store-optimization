import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

r = requests.get("https://blinkit.com/", headers=headers, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')

links = soup.find_all('a', href=True)
category_links = set()
for a in links:
    href = a['href']
    if '/cn/' in href:
        category_links.add(href if href.startswith('http') else 'https://blinkit.com' + href)

print(f"Found {len(category_links)} category links:")
for c in sorted(list(category_links))[:25]:
    print(c)
