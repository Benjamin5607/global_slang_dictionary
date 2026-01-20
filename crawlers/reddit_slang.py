import requests
import csv
import os
import time
import random

os.makedirs("output", exist_ok=True)
OUTPUT = "output/raw_terms_reddit.csv"

# 🔥 여기가 은어의 광산임 (성적, 데이팅, 게임, 밈)
SUBREDDITS = [
    "Slang",            # 일반 슬랭
    "GenZ",             # 1020세대 용어
    "InternetSlang",    # 인터넷 용어
    "UrbanDictionary",  # 어반딕셔너리 토론
    "OutOfTheLoop",     # 유행어 질문 (설명 굿)
    "NoStupidQuestions",# 질문
    "Tinder",           # 데이팅/성적 은어 (FWB, ONS 등)
    "ExplainLikeImFive",# 밈 설명
    "Twitch",           # 게임/인방 용어
    "Fanfiction",       # 19금/팬픽 용어 (오메가버스 등)
    "EnglishLearning"   # 외국인이 물어보는 슬랭
]

# 봇 차단 방지용 가짜 헤더 (필수!)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def clean_text(text):
    if not text: return ""
    return text.replace("\n", " ").replace('"', '').strip()

def fetch_reddit_data(subreddit):
    # new.json 대신 hot.json을 섞어서 인기 있는(검증된) 슬랭 수집
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        
        # 429 Too Many Requests 방지
        if res.status_code == 429:
            print(f"⏳ Rate limited on r/{subreddit}. Waiting...")
            time.sleep(5)
            return []
            
        if res.status_code != 200:
            print(f"⚠️ Failed to fetch r/{subreddit}: Status {res.status_code}")
            return []
        
        data = res.json()
        posts = data.get("data", {}).get("children", [])
        extracted = []
        
        for post in posts:
            p_data = post["data"]
            
            # 1. 제목(Title) 가져오기
            title = clean_text(p_data.get("title", ""))
            
            # 2. 본문(Selftext) 가져오기 (없으면 제목으로 대체)
            selftext = clean_text(p_data.get("selftext", ""))
            if not selftext: 
                selftext = title
            
            # 3. 스티키(공지사항) 제외
            if p_data.get("stickied"): 
                continue

            # 🔥 필터링 로직 완화:
            # 이전에는 "What does X mean?"만 찾았는데, 이제는 그냥 제목을 슬랭 후보로 둡니다.
            # (나중에 AI가 슬랭인지 아닌지 판단하는 게 훨씬 정확함)
            
            # 데이터가 너무 길면(장문글) 본문 앞부분만 자름
            context = f"[Title] {title} [Context] {selftext[:300]}..."

            extracted.append([
                title,   # term 후보 (나중에 AI가 정제함)
                context, # definition (문맥)
                f"Reddit (r/{subreddit})",
                "en",    # 레딧은 99% 영어 기반
                "Global"
            ])
            
        print(f"✅ r/{subreddit}: {len(extracted)} posts collected.")
        return extracted
        
    except Exception as e:
        print(f"❌ Error fetching r/{subreddit}: {e}")
        return []

def run():
    all_rows = []
    print("🚀 Reddit Crawling Start (Deep Dive Mode)...")
    
    for sub in SUBREDDITS:
        rows = fetch_reddit_data(sub)
        all_rows.extend(rows)
        # 봇 탐지 피하기 위해 랜덤 딜레이 (1~3초)
        time.sleep(random.uniform(1, 3))

    with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "definition", "source", "language", "country"])
        writer.writerows(all_rows)
    
    print(f"🎉 Reddit crawling finished. Total {len(all_rows)} potential terms saved.")

if __name__ == "__main__":
    run()
