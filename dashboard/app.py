import streamlit as st
import pandas as pd

st.set_page_config(page_title="Slang & Slur Monitor", layout="wide")

df = pd.read_csv("output/enriched_terms.csv")

st.title("🌍 Multilingual Slang & Slur Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Terms", len(df))
col2.metric("Slurs (Severity ≥4)", len(df[df["severity"] >= 4]))
col3.metric("Languages", df["language"].nunique())

st.subheader("Filter")
lang = st.multiselect("Language", df["language"].unique())
severity = st.slider("Severity", 1, 5, (1, 5))

filtered = df
if lang:
    filtered = filtered[filtered["language"].isin(lang)]
filtered = filtered[
    (filtered["severity"] >= severity[0]) &
    (filtered["severity"] <= severity[1])
]

st.dataframe(filtered, use_container_width=True)

st.subheader("🔥 High Risk Terms")
st.dataframe(
    filtered.sort_values("severity", ascending=False).head(20),
    use_container_width=True
)
