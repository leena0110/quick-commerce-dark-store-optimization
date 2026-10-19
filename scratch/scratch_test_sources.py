import requests
import json
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

candidates = [
    ("Blinkit Homepage", "https://blinkit.com/"),
    ("Blinkit Categories API / Search", "https://blinkit.com/v1/layout/search?q=milk"),
    ("BigBasket Homepage", "https://www.bigbasket.com/"),
    ("BigBasket Product API", "https://www.bigbasket.com/listing-svc/v2/products?type=pc&slug=fruits-vegetables"),
    ("JioMart Grocery", "https://www.jiomart.com/c/groceries/2"),
    ("JioMart Category API", "https://www.jiomart.com/catalogsearch/result?q=milk"),
    ("Zepto Web", "https://www.zeptonow.com/"),
    ("DMart Ready", "https://www.dmart.in/"),
    ("Amazon Fresh India", "https://www.amazon.in/alm/storefront?almBrandId=ctnow")
]

results = []
for name, url in candidates:
    try:
        r = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        results.append({
            "name": name,
            "url": url,
            "status_code": r.status_code,
            "content_type": r.headers.get("content-type", ""),
            "length": len(r.content),
            "final_url": r.url
        })
    except Exception as e:
        results.append({
            "name": name,
            "url": url,
            "error": str(e)
        })

print(json.dumps(results, indent=2))
