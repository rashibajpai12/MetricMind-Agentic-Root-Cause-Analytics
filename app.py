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

    st.subheader("Root Cause Results
