import requests
import csv
import os
import re
import time

# 저장 경로
os.makedirs("output", exist_ok=True)
OUTPUT = "output/raw_terms_reddit.csv"

# 타겟 서브레딧 리스트
SUBREDDITS = ["Slang", "GenZ", "InternetSlang", "UrbanDictionary"]

# 가짜 헤더 (이거 없으면 레딧이 차단함)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def clean_text(text):
    return text.replace("\n", " ").strip() if text else ""

def fetch_reddit_data(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=50"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            print(f"⚠️ Failed to fetch r/{subreddit}: {res.status_code}")
            return []
        
        data = res.json()
        posts = data.get("data", {}).get("children", [])
        extracted = []
        
        for post in posts:
            p_data = post["data"]
            title = clean_text(p_data.get("title", ""))
            selftext = clean_text(p_data.get("selftext", ""))
            
            # 간단한 필터링: 제목이 너무 길면 슬랭 단어가 아닐 확률 높음
            # 혹은 "What does X mean?" 패턴 추출 로직을 넣을 수도 있음
            term_candidate = title
            definition_candidate = selftext
            
            # 제목이 'What implies...' 또는 'Meaning of...' 형태면 정제 (예시 로직)
            match = re.search(r"meaning of ['\"]?([\w\s\-]+)['\"]?", title, re.IGNORECASE)
            if match:
                term_candidate = match.group(1)

            extracted.append([
                term_candidate,
                f"[Title] {title} [Body] {definition_candidate[:200]}...", # 문맥을 정의로 저장
                f"Reddit (r/{subreddit})",
                "en", # 레딧은 주로 영어
                "Global"
            ])
            
        return extracted
        
    except Exception as e:
        print(f"❌ Error fetching r/{subreddit}: {e}")
        return []

def run():
    all_rows = []
    print("🚀 Reddit Crawling Start...")
    for sub in SUBREDDITS:
        rows = fetch_reddit_data(sub)
        all_rows.extend(rows)
        time.sleep(1) # 매너 딜레이

    # 파일 저장
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # 헤더 추가 (Dedup에서 읽을 때 헷갈리지 않게)
        writer.writerow(["term", "definition", "source", "language", "country"])
        writer.writerows(all_rows)
    
    print(f"✅ Reddit crawling finished. {len(all_rows)} terms saved.")

if __name__ == "__main__":
    run()
