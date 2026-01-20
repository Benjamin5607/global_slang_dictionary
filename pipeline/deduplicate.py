import os
import pandas as pd
import csv

# 모든 소스 파일 정의
SOURCE_FILES = [
    "output/raw_terms_urban.csv",
    "output/raw_terms_wiktionary.csv",
    "output/raw_terms_reddit.csv",        # 추가됨
    "output/raw_terms_github_lists.csv"   # 추가됨
]

os.makedirs("output", exist_ok=True)

dfs = []
for path in SOURCE_FILES:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            # 헤더가 있는 파일들이므로 header=0 (기본값) 사용
            # on_bad_lines='skip' : CSV 형식이 꼬인 라인은 쿨하게 버림 (파이프라인 멈춤 방지)
            df = pd.read_csv(path, on_bad_lines='skip')
            
            # 컬럼 이름 강제 통일 (만약 소스마다 헤더가 다르다면 여기서 rename 필요)
            # 현재 모든 크롤러가 ["term", "definition", "source", "language", "country"] 순서로 저장한다고 가정
            if df.shape[1] >= 5:
                df.columns = ["term", "definition", "source", "language", "country"]
                dfs.append(df)
        except Exception as e:
            print(f"⚠️ Error reading {path}: {e}")
    else:
        print(f"⚠️ Skipping missing/empty file: {path}")

if not dfs:
    print("❌ No data found across all sources!")
    exit(0) # 실패 처리는 하지 말고 종료

# 통합
full_df = pd.concat(dfs, ignore_index=True)

# 정규화 (특수문자 제거, 소문자 변환)
full_df["normalized"] = full_df["term"].astype(str).str.lower().str.replace(r"[^a-z0-9]", "", regex=True)

# 중복 제거 (정규화된 단어 + 언어 조합이 같으면 제거)
# keep='first' -> 먼저 수집된(리스트 앞쪽 파일) 소스를 우선함
# 만약 Reddit(최신)을 우선하고 싶으면 dfs 순서를 바꾸거나 sort_values를 쓰면 됨
full_df = full_df.drop_duplicates(subset=["normalized", "language"], keep='first')

# 결과 저장
full_df.to_csv("output/raw_terms_clean.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)
print(f"🎉 Total merged terms: {len(full_df)}")
