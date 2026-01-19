import os
import pandas as pd
from github import Github

# =====================
# Crawlers 결과 경로
OUTPUT = "output/raw_terms_clean.csv"
os.makedirs("output", exist_ok=True)
# =====================

# 예시 DataFrame (실제로는 Urban Dictionary, Wiktionary Crawlers에서 생성된 CSV 읽으면 됨)
df_urban = pd.read_csv("output/raw_terms_urban.csv")
df_wiki = pd.read_csv("output/raw_terms_wiktionary.csv")
df = pd.concat([df_urban, df_wiki], ignore_index=True)

# 중복 제거
df.drop_duplicates(subset=["term"], inplace=True)

# 최종 CSV 저장
df.to_csv(OUTPUT, index=False, encoding="utf-8")

# =====================
# GitHub 업로드
GITHUB_TOKEN = os.getenv("GH_PAT")
REPO_NAME = "Benjamin5607/global_slang_dictionary"  # 변경 필요
FILE_PATH = OUTPUT  # 그대로 output/raw_terms_clean.csv
# =====================

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

try:
    file = repo.get_contents(FILE_PATH)
    repo.update_file(file.path, "Update raw_terms_clean.csv", open(FILE_PATH, "r", encoding="utf-8").read(), file.sha)
    print(f"✅ CSV updated in GitHub: {FILE_PATH}")
except:
    repo.create_file(FILE_PATH, "Create raw_terms_clean.csv", open(FILE_PATH, "r", encoding="utf-8").read())
    print(f"✅ CSV created in GitHub: {FILE_PATH}")
