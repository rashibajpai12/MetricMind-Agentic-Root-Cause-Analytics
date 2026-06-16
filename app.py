import streamlit as st

st.set_page_config(page_title="MetricMind", layout="wide")

st.title("MetricMind: Agentic Root-Cause Analytics Engine")

st.write("""
MetricMind investigates why a business metric changed using:
SQL-backed analysis, root-cause detection, Gemini insight generation,
and evaluator-agent verification.
""")

question = st.text_input("Ask a business question", "Why did revenue drop?")

if st.button("Analyze"):
    st.subheader("Agent Workflow")
    st.write("Planner Agent → Root-Cause Engine → Gemini Insight Agent → Evaluator Agent → Final Report")

    st.subheader("Final Verified Report")
    st.write("Upload your final_report.txt logic here in V2.")
