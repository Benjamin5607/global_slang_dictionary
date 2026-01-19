import os
import pandas as pd

# =====================
# 1️⃣ Crawlers CSV 경로
urban_csv = "output/raw_terms_urban.csv"
wiki_csv  = "output/raw_terms_wiktionary.csv"
os.makedirs("output", exist_ok=True)
# =====================

# 2️⃣ 각 CSV 읽기
dfs = []
for path in [urban_csv, wiki_csv]:
    if os.path.exists(path):
        df = pd.read_csv(path)
        dfs.append(df)
    else:
        print(f"⚠️ CSV not found, skipping: {path}")

# 3️⃣ 합치기
if dfs:
    df = pd.concat(dfs, ignore_index=True)
else:
    raise FileNotFoundError("No raw_terms CSV found!")

# 4️⃣ 컬럼 이름 설정 (헤더 없는 경우 대비)
if df.shape[1] == 5:
    df.columns = ["term", "definition", "source", "language", "country"]

# 5️⃣ 정규화 + 중복 제거
df["normalized"] = df["term"].str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
df = df.drop_duplicates(subset=["normalized", "language"])

# 6️⃣ 최종 CSV 저장
df.to_csv("output/raw_terms_clean.csv", index=False, encoding="utf-8")

print(f"✅ raw_terms_clean.csv 생성 완료: {len(df)}개 항목")
