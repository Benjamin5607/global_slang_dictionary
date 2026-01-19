import pandas as pd

df = pd.read_csv("output/raw_terms.csv", header=None)
df.columns = ["term", "definition", "source", "language", "country"]

df["normalized"] = df["term"].str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
df = df.drop_duplicates(subset=["normalized", "language"])

df.to_csv("output/raw_terms_clean.csv", index=False)
