import requests
import csv
import os
import time
import random
from fake_useragent import UserAgent  # 신분 위조 전문가

os.makedirs("output", exist_ok=True)
OUTPUT = "output/raw_terms_reddit.csv"

# 타겟 서브레딧
SUBREDDITS = [
    "Slang", "GenZ", "InternetSlang", "UrbanDictionary",
    "OutOfTheLoop", "NoStupidQuestions", "Tinder",
    "ExplainLikeImFive", "Twitch", "Fanfiction", "EnglishLearning"
]

def clean_text(text):
    if not text: return ""
    return text.replace("\n", " ").replace('"', '').strip()

def get_random_header():
    # 매번 다른 브라우저인 척 위장
    try:
        ua = UserAgent()
        user_agent = ua.random
    except:
        # 라이브러리 실패 시 비상용 하드코딩 헤더
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    return {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }

def fetch_reddit_data(subreddit):
    # www.reddit.com 대신 old.reddit.com이나 gateway 등을 쓸 수도 있지만
    # JSON 엔드포인트에 헤더만 잘 속이면 뚫림
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=40"
    
    headers = get_random_header()
    
    try:
        # ⚠️ 중요: 봇 탐지 피하기 위해 타임아웃 넉넉히
        res = requests.get(url, headers=headers, timeout=15)
        
        # 429 (Too Many Requests) -> 잠깐 쉬었다 가기
        if res.status_code == 429:
            print(f"⏳ Rate limited on r/{subreddit}. Cooling down 10s...")
            time.sleep(10)
            return []

        if res.status_code != 200:
            print(f"⚠️ Failed to fetch r/{subreddit}: Status {res.status_code}")
            # 403이 뜨면 한 번 더 시도 (다른 User-Agent로)
            if res.status_code == 403:
                print("🔄 403 detected. Retrying with new identity...")
                time.sleep(2)
                headers = get_random_header()
                res = requests.get(url, headers=headers, timeout=15)
                if res.status_code != 200: return []
            else:
                return []
        
        data = res.json()
        posts = data.get("data", {}).get("children", [])
        extracted = []
        
        for post in posts:
            p_data = post["data"]
            
            # 스티키(공지) 제외
            if p_data.get("stickied"): continue
            
            title = clean_text(p_data.get("title", ""))
            selftext = clean_text(p_data.get("selftext", ""))
            
            # 본문 없으면 제목 사용
            if not selftext: selftext = title
            
            # 데이터 정제
            context = f"[Title] {title} [Context] {selftext[:300]}..."

            extracted.append([
                title, 
                context, 
                f"Reddit (r/{subreddit})", 
                "en", 
                "Global"
            ])
            
        print(f"✅ r/{subreddit}: {len(extracted)} posts collected.")
        return extracted
        
    except Exception as e:
        print(f"❌ Error fetching r/{subreddit}: {e}")
        return []

def run():
    all_rows = []
    print("🚀 Reddit Crawling Start (Stealth Mode)...")
    
    for sub in SUBREDDITS:
        rows = fetch_reddit_data(sub)
        all_rows.extend(rows)
        # 봇 탐지 피하기 위해 3~7초 랜덤 대기 (사람인 척)
        sleep_time = random.uniform(3, 7)
        time.sleep(sleep_time)

    # 데이터 저장
    if all_rows:
        with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["term", "definition", "source", "language", "country"])
            writer.writerows(all_rows)
        print(f"🎉 Reddit crawling finished. Total {len(all_rows)} terms saved.")
    else:
        print("⚠️ No data collected. Reddit might be blocking aggressive requests.")

if __name__ == "__main__":
    run()
