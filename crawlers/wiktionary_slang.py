import requests
import csv
import os
from bs4 import BeautifulSoup # pip install beautifulsoup4 필요

os.makedirs("output", exist_ok=True)
OUTPUT = "output/raw_terms_wiktionary.csv"

LANGS = {
    "ko": "Korean_slang",
    "ja": "Japanese_slang",
    "fr": "French_slang",
    "en": "English_slang"
    # 필요한 언어 더 추가
}

def run():
    print("🚀 Wiktionary Crawling Start...")
    rows = []
    headers = {
        "User-Agent": "GlobalSlangBot/1.0 (MyContactInfo)"
    }

    for lang, category in LANGS.items():
        url = f"https://en.wiktionary.org/wiki/Category:{category}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code != 200:
                continue
            
            soup = BeautifulSoup(res.text, "html.parser")
            
            # Wiktionary 카테고리 페이지의 단어 목록 div 찾기
            # 보통 mw-category-group 클래스 안에 li로 들어있음
            category_groups = soup.find_all("div", class_="mw-category-group")
            
            for group in category_groups:
                links = group.find_all("a")
                for link in links:
                    term = link.get_text()
                    if term:
                        rows.append([
                            term,
                            f"Slang term listed in Wiktionary ({category})",
                            "Wiktionary",
                            lang,
                            lang.upper()
                        ])
        except Exception as e:
            print(f"❌ Error in {lang}: {e}")

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "definition", "source", "language", "country"])
        writer.writerows(rows)
        
    print(f"✅ Wiktionary finished. {len(rows)} terms saved.")

if __name__ == "__main__":
    run()
