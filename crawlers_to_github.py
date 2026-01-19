import pandas as pd
from github import Github

# =====================
# 1. Crawlers CSV 경로
CSV_PATH = "output/raw_terms_clean.csv"  # Crawlers 결과 CSV
# =====================

# =====================
# 2. GitHub 설정
GITHUB_TOKEN = "GH_PAT"  # GitHub PAT
REPO_NAME = "global_slang_dictionary"       # Crawlers Repo 이름
# =====================

# CSV 읽기
df = pd.read_csv(CSV_PATH)
csv_content = df.to_csv(index=False, encoding="utf-8")

# GitHub 연결
g = Github(GITHUB_TOKEN)
repo = g.get_user().get_repo(REPO_NAME)

# GitHub 업데이트
try:
    file = repo.get_contents(CSV_PATH)
    repo.update_file(file.path, "Update raw_terms", csv_content, file.sha)
    print(f"✅ CSV updated in GitHub: {CSV_PATH}")
except:
    repo.create_file(CSV_PATH, "Create raw_terms", csv_content)
    print(f"✅ CSV created in GitHub: {CSV_PATH}")
