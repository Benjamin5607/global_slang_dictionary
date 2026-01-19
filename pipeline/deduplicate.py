import os
import pandas as pd

urban_csv = "output/raw_terms_urban.csv"
wiki_csv  = "output/raw_terms_wiktionary.csv"
os.makedirs("output", exist_ok=True)

dfs = []
for path in [urban_csv, wiki_csv]:
    if os.path.exists(path):
        if os.path.getsize(path) > 0:  # 비어있는 파일 건너뛰기
            df = pd.read_csv(path)
            dfs.append(df)
        else:
            print(f"⚠️ CSV is empty, skipping: {path}")
    else:
        print(f"⚠️ CSV not found, skipping: {path}")

if not dfs:
    print("❌ No data found in any CSV, exiting...")
    exit(1)  # 데이터가 없으면 workflow 중단

df = pd.concat(dfs, ignore_index=True)

# 컬럼명
if df.shape[1] == 5:
    df.columns = ["term", "definition", "source", "language", "country"]

# 중복 제거
df["normalized"] = df["term"].str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
df = df.drop_duplicates(subset=["normalized", "language"])

df.to_csv("output/raw_terms_clean.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)
print("✅ raw_terms_clean.csv 생성 완료:", len(df), "개 항목")
