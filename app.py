from agents.sql_agent import generate_sql
from agents.failure_agent import check_sql
from agents.insight_agent import generate_insight
from agents.verification_agent import verify_evidence

import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
import google.generativeai as genai


st.set_page_config(
    page_title="MetricMind",
    page_icon="◐",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
root_cause = pd.read_csv("data/metricmind_root_cause_results.csv")
revenue = pd.read_csv("data/metricmind_monthly_revenue.csv")

con = duckdb.connect()
con.register("sales", root_cause)

# -----------------------------
# GEMINI SETUP
# -----------------------------
api_key = st.secrets.get("GEMINI_API_KEY", None)

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "question" not in st.session_state:
    st.session_state.question = ""

if "sql_query" not in st.session_state:
    st.session_state.sql_query = ""

if "result" not in st.session_state:
    st.session_state.result = None

if "insight" not in st.session_state:
    st.session_state.insight = ""

if "verification" not in st.session_state:
    st.session_state.verification = ""


# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #050505;
    color: #F4F4F1;
}
h1, h2, h3 {
    color: #F4F4F1;
}
.metric-card {
    padding: 22px;
    border: 1px solid #222;
    border-radius: 18px;
    background: #111;
}
.small-text {
    color: #999;
    font-size: 14px;
}
.big-title {
    font-size: 72px;
    font-weight: 900;
    line-height: 0.95;
}
.highlight {
    color: #e8dcc4;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("MetricMind ●")
    st.caption("Agentic analytics workspace for root-cause intelligence.")

    st.divider()

    st.caption("SAMPLE QUESTIONS")

    sample_questions = [
        "Which category had the highest revenue decline?",
        "Which region performed worst?",
        "Show refund rates above 0.08",
        "Largest revenue drop?"
    ]

    for q in sample_questions:
        if st.button(q, use_container_width=True):
            st.session_state.question = q
            st.session_state.page = "Workspace"
            st.rerun()

    st.divider()

    st.caption("AGENT FLOW")
    st.write("Question → SQL Agent")
    st.write("DuckDB → Analytics")
    st.write("Insight → Verification")
    st.write("Report → Download")


# -----------------------------
# NAVBAR
# -----------------------------
col_logo, col_nav, col_demo = st.columns([1.2, 3, 1])

with col_logo:
    st.subheader("metricmind ●")

with col_nav:
    page = st.radio(
        "Navigation",
        ["Home", "SQL Agent", "Evidence", "Reports", "Workspace"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.page = page

with col_demo:
    if st.button("Live Demo", use_container_width=True):
        st.session_state.question = "Which category had the highest revenue decline?"
        st.session_state.page = "Workspace"
        st.rerun()


st.divider()


# -----------------------------
# WORKFLOW FUNCTION
# -----------------------------
def run_metricmind(question):
    if model is None:
        st.error("Gemini API key is missing. Add GEMINI_API_KEY in Streamlit secrets.")
        return

    st.session_state.question = question

    sql_query = generate_sql(question, list(root_cause.columns))
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    st.session_state.sql_query = sql_query

    if not check_sql(sql_query):
        st.error("Unsafe SQL detected. Query blocked.")
        return

    try:
        result = con.execute(sql_query).fetchdf()
    except Exception as e:
        st.error("SQL execution failed.")
        st.write(e)
        return

    if result.empty:
        st.warning("No matching data found for this question.")
        return

    insight = generate_insight(question, sql_query, result.to_string())
    verification = verify_evidence(insight, result.to_string())

    st.session_state.result = result
    st.session_state.insight = insight
    st.session_state.verification = verification


# -----------------------------
# HOME PAGE
# -----------------------------
if st.session_state.page == "Home":
    left, right = st.columns([1.4, 1], gap="large")

    with left:
        st.markdown("<p class='small-text'>AGENTIC ANALYTICS</p>", unsafe_allow_html=True)
        st.markdown(
            "<div class='big-title'>Business<br>Metrics,<br><span class='highlight'>Explained.</span></div>",
            unsafe_allow_html=True
        )
        st.write("")
        st.markdown(
            "MetricMind converts business questions into executable SQL, validates evidence, "
            "and generates decision-ready root-cause insights for analytics teams."
        )

        user_question = st.text_input("Ask a business question", placeholder="Example: Which region performed worst?")

        if st.button("Ask MetricMind →"):
            if user_question.strip():
                run_metricmind(user_question)
                st.session_state.page = "Workspace"
                st.rerun()
            else:
                st.warning("Please enter a question first.")

    with right:
        st.markdown("### MetricMind Pipeline")
        st.write("**Q** Natural Language Question")
        st.write("**SQL** SQL Generation Agent")
        st.write("**DB** DuckDB Analytics Execution")
        st.write("**✓** Evidence Verification")

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Segments Analyzed", len(root_cause))
    c2.metric("Regions", root_cause["region"].nunique())
    c3.metric("Categories", root_cause["category"].nunique())
    c4.metric("Evidence Score", "9.4")


# -----------------------------
# SQL AGENT PAGE
# -----------------------------
elif st.session_state.page == "SQL Agent":
    st.header("SQL Agent")

    question = st.text_input(
        "Enter a business question",
        value=st.session_state.question,
        placeholder="Which category had the highest revenue decline?"
    )

    if st.button("Generate SQL"):
        if question.strip():
            run_metricmind(question)
        else:
            st.warning("Enter a question first.")

    if st.session_state.sql_query:
        st.subheader("Generated SQL")
        st.code(st.session_state.sql_query, language="sql")
    else:
        st.info("Generate a query to see SQL here.")


# -----------------------------
# WORKSPACE PAGE
# -----------------------------
elif st.session_state.page == "Workspace":
    st.header("Analysis Workspace")

    question = st.text_input(
        "Business Question",
        value=st.session_state.question,
        placeholder="Ask a business question..."
    )

    if st.button("Run Analysis"):
        if question.strip():
            run_metricmind(question)
        else:
            st.warning("Enter a question first.")

    if st.session_state.result is not None:
        st.success("Analysis completed.")

        st.subheader("Question")
        st.write(st.session_state.question)

        st.subheader("Generated SQL")
        st.code(st.session_state.sql_query, language="sql")

        st.subheader("Query Result")
        st.dataframe(st.session_state.result, use_container_width=True)

        result = st.session_state.result

        if {"category", "revenue_change", "region"}.issubset(result.columns):
            fig = px.bar(
                result,
                x="category",
                y="revenue_change",
                color="region",
                title="Revenue Change by Category"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#050505",
                font_color="#F4F4F1"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("AI Insight")
        st.write(st.session_state.insight)

        st.subheader("Evidence Check")
        st.write(st.session_state.verification)

    else:
        st.info("Run a sample question or enter your own question.")


# -----------------------------
# EVIDENCE PAGE
# -----------------------------
elif st.session_state.page == "Evidence":
    st.header("Evidence Verification")

    if st.session_state.verification:
        st.subheader("Verification Result")
        st.write(st.session_state.verification)

        st.subheader("Source Result Table")
        st.dataframe(st.session_state.result, use_container_width=True)
    else:
        st.info("Run an analysis first. Evidence will appear here.")


# -----------------------------
# REPORTS PAGE
# -----------------------------
elif st.session_state.page == "Reports":
    st.header("Reports")

    if st.session_state.insight:
        report = f"""
MetricMind Root-Cause Analytics Report

Question:
{st.session_state.question}

Generated SQL:
{st.session_state.sql_query}

Insight:
{st.session_state.insight}

Evidence Verification:
{st.session_state.verification}
"""

        st.text_area("Report Preview", report, height=350)

        st.download_button(
            label="Download Insight Report",
            data=report,
            file_name="metricmind_report.txt",
            mime="text/plain"
        )
    else:
        st.info("Run an analysis first. Report will be generated here.")
