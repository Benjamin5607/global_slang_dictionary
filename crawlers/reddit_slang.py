import praw
import csv

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_SECRET",
    user_agent="slang-db"
)

SUBREDDITS = [
    "slang",
    "linguistics",
    "korea",
    "japan",
    "thailand",
    "vietnam"
]

OUTPUT = "output/raw_terms.csv"

def run():
    rows = []
    for sub in SUBREDDITS:
        for post in reddit.subreddit(sub).hot(limit=50):
            if len(post.title.split()) <= 3:
                rows.append([
                    post.title,
                    post.selftext[:300],
                    f"Reddit:{sub}",
                    "unknown",
                    "online"
                ])

    with open(OUTPUT, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

if __name__ == "__main__":
    run()
