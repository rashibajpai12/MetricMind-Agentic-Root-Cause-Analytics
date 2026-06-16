import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
import google.generativeai as genai

st.set_page_config(page_title="MetricMind", layout="wide")

st.title("MetricMind: Agentic Root-Cause Analytics Engine")

st.markdown("""
Ask business questions in natural language.  
MetricMind generates SQL, runs analysis, detects failures, and produces evidence-backed insights.
""")

root_cause = pd.read_csv("metricmind_root_cause_results.csv")
revenue = pd.read_csv("metricmind_monthly_revenue.csv")

con = duckdb.connect()
con.register("sales", root_cause)

api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

question = st.text_input(
    "Ask a business question",
    "Why did revenue drop?"
)
question = st.text_input(
    "Ask a business question",
    "Why did revenue drop?"
)
if st.button("Analyze"):

    st.subheader("1. User Question")
    st.write(question)

    st.subheader("2. SQL Generation Agent")

    if model is None:
        st.error("Gemini API key is missing. Add GEMINI_API_KEY in Streamlit secrets.")
        st.stop()

    sql_prompt = f"""
You are a SQL generation agent.

Table name: sales

Columns:
{list(root_cause.columns)}

User question:
{question}

Generate one safe DuckDB SQL query only.
Do not use DROP, DELETE, UPDATE, INSERT, ALTER.
Return only SQL, no explanation.
"""

    sql_query = model.generate_content(sql_prompt).text.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    st.subheader("Generated SQL")
    st.code(sql_query, language="sql")

    st.subheader("3. Failure Detection Agent")

    blocked_words = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]

    if any(word in sql_query.upper() for word in blocked_words):
        st.error("Unsafe SQL detected. Query blocked.")
        st.stop()

    try:
        result = con.execute(sql_query).fetchdf()
    except Exception as e:
        st.error("SQL execution failed.")
        st.write(e)
        st.stop()

    if result.empty:
        st.warning("No matching data found for this question.")
        st.stop()

    st.success("SQL executed successfully.")

    st.subheader("4. SQL Result")
    st.dataframe(result, use_container_width=True)

    if {"category", "revenue_change", "region"}.issubset(result.columns):
        st.subheader("Revenue Impact Chart")

        fig = px.bar(
            result,
            x="category",
            y="revenue_change",
            color="region",
            title="Revenue Change by Category"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("5. Evidence Verification + Insight Agent")

    insight_prompt = f"""
You are MetricMind, an evidence-backed analytics agent.

User question:
{question}

SQL query:
{sql_query}

SQL result:
{result.to_string()}

Generate:
1. Main finding
2. Evidence from the SQL result
3. Possible business reason
4. Recommended action
5. Confidence level

Rules:
- Use only the SQL result.
- Do not invent numbers.
- Keep it crisp.
"""

    insight = model.generate_content(insight_prompt).text
    st.markdown(insight)

    verification_prompt = f"""
Check if the insight is supported by the SQL result.

Insight:
{insight}

SQL Result:
{result.to_string()}

Give:
1. Evidence Score out of 10
2. Unsupported claims if any
"""

    verification = model.generate_content(verification_prompt).text

    st.subheader("Evidence Verification")
    st.write(verification)

    st.download_button(
        label="Download Insight Report",
        data=insight,
        file_name="metricmind_v2_report.txt",
        mime="text/plain"
    )
