import streamlit as st
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="MetricMind",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("MetricMind: Agentic Root-Cause Analytics Engine")

st.markdown("""
Analyze business metric changes using
root-cause analytics and AI-generated insights.
""")

# -----------------------------
# User Input
# -----------------------------
question = st.text_input(
    "Ask a business question",
    "Why did revenue drop?"
)

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("Analyze"):

    st.subheader("Business Question")
    st.write(question)

    # -------------------------
    # Root Cause Results
    # -------------------------
    st.subheader("Root Cause Results")

    root_cause = pd.read_csv(
        "metricmind_root_cause_results.csv"
    )

    st.dataframe(
        root_cause,
        use_container_width=True
    )

    # -------------------------
    # Revenue Trend Data
    # -------------------------
    st.subheader("Revenue Trend Data")

    revenue = pd.read_csv(
        "metricmind_monthly_revenue.csv"
    )

    st.dataframe(
        revenue,
        use_container_width=True
    )

    # -------------------------
    # Final Report
    # -------------------------
    st.subheader("Final Verified Report")

    with open(
        "metricmind_final_report.txt",
        "r",
        encoding="utf-8"
    ) as f:
        report = f.read()

    st.markdown(report)

    # -------------------------
    # Download Report
    # -------------------------
    st.download_button(
        label="Download Final Report",
        data=report,
        file_name="metricmind_report.txt",
        mime="text/plain"
    )
