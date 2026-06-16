import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MetricMind",
    layout="wide"
)

st.title("MetricMind: Agentic Root-Cause Analytics Engine")

st.markdown("""
Analyze business metric changes using
root-cause analytics and AI-generated insights.
""")

question = st.text_input(
    "Ask a business question",
    "Why did revenue drop?"
)

if st.button("Analyze"):

    st.subheader("Business Question")
    st.write(question)

  st.subheader("Root Cause Results")

root_cause = pd.read_csv(
    "metricmind_root_cause_results.csv"
)

st.dataframe(
    root_cause,
    use_container_width=True
)

st.subheader("Final Verified Report")

with open(
    "metricmind_final_report.txt",
    "r",
    encoding="utf-8"
) as f:
    report = f.read()

st.markdown(report)
