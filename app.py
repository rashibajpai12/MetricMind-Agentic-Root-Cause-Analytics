import streamlit as st
import pandas as pd

from utils.database import load_data
from agents.schema_agent import get_schema
from agents.sql_agent import generate_sql
from agents.sql_validator import validate_sql
from agents.insight_agent import generate_insight
from agents.root_cause_agent import analyze_root_cause
from agents.recommendation_agent import generate_recommendations
from agents.evidence_agent import verify_evidence
from agents.visualization_agent import create_chart

st.set_page_config(page_title="MetricMind", layout="wide")

df, con = load_data()
schema = get_schema(df)

if "history" not in st.session_state:
    st.session_state.history = []

st.title("MetricMind")
st.caption("Agentic Root-Cause Analytics Engine")

tabs = st.tabs([
    "Workspace",
    "SQL Agent",
    "Visualization",
    "Insight",
    "Root Cause",
    "Recommendations",
    "Evidence",
    "Report"
])

with tabs[0]:
    st.header("Ask MetricMind")

    sample = st.selectbox(
        "Try a sample question",
        [
            "",
            "Which category generated the highest revenue?",
            "Which region had the lowest profit?",
            "Show monthly revenue trend.",
            "Which category has the highest refund rate?",
            "Which customer segment is most profitable?",
            "Find products with high revenue but low profit.",
            "Why is profit declining in the North region?",
            "Compare revenue by region and category.",
            "Which category needs urgent attention?",
            "What are the top business risks?"
        ]
    )

    question = st.text_input("Enter your business question", value=sample)

    if st.button("Run Analysis"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            with st.spinner("MetricMind is thinking..."):
                sql = generate_sql(question, schema)
                safe, message = validate_sql(sql)

                if not safe:
                    st.error(message)
                    st.code(sql, language="sql")
                else:
                    try:
                        result = con.execute(sql).fetchdf()

                        insight = generate_insight(question, result.to_string())
                        root_cause = analyze_root_cause(question, result.to_string())
                        recommendations = generate_recommendations(question, result.to_string(), root_cause)
                        evidence = verify_evidence(insight, result.to_string())

                        st.session_state.latest = {
                            "question": question,
                            "sql": sql,
                            "result": result,
                            "insight": insight,
                            "root_cause": root_cause,
                            "recommendations": recommendations,
                            "evidence": evidence
                        }

                        st.session_state.history.append(st.session_state.latest)
                        st.success("Analysis complete.")

                    except Exception as e:
                        st.error("SQL execution failed.")
                        st.write(e)
                        st.code(sql, language="sql")

    if "latest" in st.session_state:
        latest = st.session_state.latest

        st.subheader("Result")
        st.dataframe(latest["result"], use_container_width=True)

        chart = create_chart(latest["result"])
        if chart:
            st.plotly_chart(chart, use_container_width=True)

        st.subheader("Executive Insight")
        st.write(latest["insight"])

with tabs[1]:
    st.header("SQL Agent")
    if "latest" in st.session_state:
        st.code(st.session_state.latest["sql"], language="sql")
    else:
        st.info("Run analysis first.")

with tabs[2]:
    st.header("Visualization")
    if "latest" in st.session_state:
        chart = create_chart(st.session_state.latest["result"])
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("No suitable chart found.")
    else:
        st.info("Run analysis first.")

with tabs[3]:
    st.header("Insight Agent")
    if "latest" in st.session_state:
        st.write(st.session_state.latest["insight"])
    else:
        st.info("Run analysis first.")

with tabs[4]:
    st.header("Root Cause Agent")
    if "latest" in st.session_state:
        st.write(st.session_state.latest["root_cause"])
    else:
        st.info("Run analysis first.")

with tabs[5]:
    st.header("Recommendation Agent")
    if "latest" in st.session_state:
        st.write(st.session_state.latest["recommendations"])
    else:
        st.info("Run analysis first.")

with tabs[6]:
    st.header("Evidence Verification")
    if "latest" in st.session_state:
        st.write(st.session_state.latest["evidence"])
    else:
        st.info("Run analysis first.")

with tabs[7]:
    st.header("Executive Report")

    if "latest" in st.session_state:
        latest = st.session_state.latest

        report = f"""
METRICMIND EXECUTIVE REPORT

Question:
{latest['question']}

Generated SQL:
{latest['sql']}

Result:
{latest['result'].to_string()}

Insight:
{latest['insight']}

Root Cause:
{latest['root_cause']}

Recommendations:
{latest['recommendations']}

Evidence:
{latest['evidence']}
"""

        st.text_area("Report Preview", report, height=500)

        st.download_button(
            "Download Report",
            data=report,
            file_name="metricmind_report.txt",
            mime="text/plain"
        )
    else:
        st.info("Run analysis first.")
