import requests
import csv

LANGS = {
    "ko": "Korean_slang",
    "ja": "Japanese_slang",
    "fr": "French_slang",
    "de": "German_slang",
    "ru": "Russian_slang",
    "es": "Spanish_slang",
    "pt": "Portuguese_slang",
    "it": "Italian_slang"
}

OUTPUT = "output/raw_terms_wiktionary.csv"

def run():
    rows = []
    for lang, category in LANGS.items():
        url = f"https://en.wiktionary.org/wiki/Category:{category}"
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            continue

        for line in res.text.split('title="'):
            if '"' in line:
                term = line.split('"')[0]
                if len(term) < 2:
                    continue
                rows.append([
                    term,
                    "Slang term listed on Wiktionary",
                    "Wiktionary",
                    lang,
                    lang.upper()
                ])

    with open(OUTPUT, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

if __name__ == "__main__":
    run()
