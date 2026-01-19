# 파일명: crawlers_to_github.py
import os
import pandas as pd
from github import Github

# =====================
# Crawlers CSV 경로
OUTPUT = "output/raw_terms.csv"
os.makedirs("output", exist_ok=True)  # 폴더 없으면 생성
# =====================

# Crawlers 결과 DataFrame 예시
# 실제로는 urban_dictionary.py 등에서 DataFrame 가져오도록 수정
df = pd.DataFrame([
    ["slang1", "definition1", "en"],
    ["slang2", "definition2", "en"]
])
df.to_csv(OUTPUT, index=False, encoding="utf-8")

# =====================
# GitHub 업로드
GITHUB_TOKEN = os.getenv("GH_PAT")  # GitHub Secret
REPO_NAME = "global_slang_dictionary"
FILE_PATH = OUTPUT  # 그대로 output/raw_terms.csv
# =====================

g = Github(GITHUB_TOKEN)
repo = g.get_user().get_repo(REPO_NAME)

try:
    file = repo.get_contents(FILE_PATH)
    repo.update_file(file.path, "Update raw_terms", open(FILE_PATH, "r", encoding="utf-8").read(), file.sha)
    print(f"✅ CSV updated in GitHub: {FILE_PATH}")
except:
    repo.create_file(FILE_PATH, "Create raw_terms", open(FILE_PATH, "r", encoding="utf-8").read())
    print(f"✅ CSV created in GitHub: {FILE_PATH}")
