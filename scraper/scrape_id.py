import requests, json, os, re
from bs4 import BeautifulSoup
from links import URLS

HEADERS = {"User-Agent": "Mozilla/5.0"}

def clean(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'Baca juga.*', '', text, flags=re.I)
    return text.strip()

def scrape(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script","style","nav","footer","aside"]):
        tag.decompose()

    blocks = []
    for tag in soup.find_all(["p","h1","h2","h3","li"]):
        t = clean(tag.get_text())
        if len(t) > 50:
            blocks.append(t)

    return {"url": url, "content": "\n".join(blocks)}

def main():
    os.makedirs("data/raw", exist_ok=True)
    data = []

    for url in URLS:
        print("Scraping:", url)
        data.append(scrape(url))

    with open("data/raw/kuku_dataset.json","w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

    print("✅ Scraping selesai")

if __name__ == "__main__":
    main()
