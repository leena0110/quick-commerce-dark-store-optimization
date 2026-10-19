import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

r = requests.get("https://blinkit.com/robots.txt", headers=headers, timeout=10)
print("Status:", r.status_code)
print(r.text)
