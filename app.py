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

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #030303;
    color: #F4F4F1;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 1320px;
    padding: 1.6rem 3rem 3rem 3rem;
}

[data-testid="stSidebar"] {
    background: #050505;
    border-right: 1px solid rgba(255,255,255,0.08);
}

.side-brand {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.04em;
    margin-bottom: 8px;
}

.side-sub {
    color: #8F8F8F;
    font-size: 14px;
    margin-bottom: 34px;
    line-height: 1.7;
}

.side-section {
    margin-top: 32px;
    margin-bottom: 14px;
    color: #777;
    font-size: 11px;
    letter-spacing: 0.24em;
    text-transform: uppercase;
}

.side-pill {
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.025);
    border-radius: 999px;
    padding: 11px 14px;
    margin-bottom: 10px;
    color: #D7D7D7;
    font-size: 13px;
    line-height: 1.45;
}

.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 70px;
}

.logo {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.04em;
}

.nav-links {
    display: flex;
    gap: 30px;
    color: #B8B8B8;
    font-size: 14px;
    font-weight: 600;
}

.sign-btn {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 999px;
    padding: 11px 20px;
    color: #F5F5F5;
    background: rgba(255,255,255,0.04);
}

.hero {
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 34px;
    align-items: center;
    min-height: 360px;
    margin-bottom: 30px;
}

.eyebrow {
    display: flex;
    align-items: center;
    gap: 16px;
    color: #747474;
    font-size: 11px;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    margin-bottom: 28px;
}

.eyebrow-line {
    width: 32px;
    height: 1px;
    background: #787878;
}

.hero-title {
    font-size: clamp(58px, 6vw, 92px);
    font-weight: 820;
    letter-spacing: -0.07em;
    line-height: 0.94;
    max-width: 760px;
    color: #F2F2EE;
}

.hero-title span {
    color: #E9DEC8;
}

.hero-desc {
    margin-top: 28px;
    max-width: 640px;
    color: #A7ACB8;
    font-size: 18px;
    line-height: 1.65;
    font-weight: 500;
}

.hero-actions {
    display: flex;
    gap: 14px;
    margin-top: 34px;
}

.action-primary, .action-secondary {
    border-radius: 999px;
    padding: 13px 23px;
    font-size: 14px;
    font-weight: 700;
    display: inline-block;
}

.action-primary {
    border: 1px solid rgba(255,255,255,0.16);
    background: rgba(255,255,255,0.055);
    color: #F4F4F1;
}

.action-secondary {
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.025);
    color: #F4F4F1;
}

/* Compact agent visual */
.agent-card-visual {
    border: 1px solid rgba(255,255,255,0.09);
    background: radial-gradient(circle at top right, rgba(232,221,200,0.10), transparent 38%),
                rgba(255,255,255,0.025);
    border-radius: 30px;
    padding: 28px;
    min-height: 285px;
}

.agent-visual-title {
    color: #E9DEC8;
    font-size: 14px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 24px;
}

.flow-node {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}

.flow-node:last-child {
    border-bottom: none;
}

.node-icon {
    width: 38px;
    height: 38px;
    border-radius: 14px;
    background: #E8DDC8;
    color: #050505;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
}

.node-text {
    font-size: 15px;
    color: #E7E7E7;
    font-weight: 600;
}

.node-sub {
    font-size: 12px;
    color: #8F8F8F;
    margin-top: 3px;
}

.metric-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-top: 18px;
    margin-bottom: 34px;
}

.metric-card {
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.025);
    border-radius: 22px;
    padding: 22px;
    min-height: 118px;
}

.metric-card.accent {
    background: #E8DDC8;
    color: #050505;
}

.metric-label {
    font-size: 13px;
    color: #8D8D8D;
    font-weight: 600;
}

.metric-card.accent .metric-label {
    color: #373737;
}

.metric-value {
    margin-top: 24px;
    font-size: 39px;
    font-weight: 800;
    letter-spacing: -0.06em;
}

.panel-title {
    font-size: 24px;
    font-weight: 750;
    letter-spacing: -0.04em;
    margin-bottom: 14px;
}

.panel {
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.025);
    border-radius: 26px;
    padding: 22px;
}

.agent-row {
    border-bottom: 1px solid rgba(255,255,255,0.07);
    padding: 13px 0;
    color: #D8D8D8;
    font-size: 15px;
}

.agent-row:last-child {
    border-bottom: none;
}

.dot {
    color: #E8DDC8;
}

.ask-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -0.07em;
    margin-top: 22px;
    margin-bottom: 14px;
}

[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.04);
    border-radius: 999px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.035);
    border-radius: 999px;
    padding: 10px 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

div[data-testid="stAlert"] {
    border-radius: 18px;
}
</style>
""")

with st.sidebar:
    st.html("""
    <div class="side-brand">MetricMind <span style="color:#E8DDC8;">●</span></div>
    <div class="side-sub">Agentic analytics workspace for root-cause intelligence.</div>

    <div class="side-section">Sample Questions</div>
    <div class="side-pill">Which category had the highest revenue decline?</div>
    <div class="side-pill">Which region performed worst?</div>
    <div class="side-pill">Show refund rates above 0.08</div>
    <div class="side-pill">Largest revenue drop?</div>

    <div class="side-section">Agent Flow</div>
    <div class="side-pill">Question → SQL Agent</div>
    <div class="side-pill">DuckDB → Analytics</div>
    <div class="side-pill">Insight → Verification</div>
    <div class="side-pill">Report → Download</div>
    """)

root_cause = pd.read_csv("data/metricmind_root_cause_results.csv")
revenue = pd.read_csv("data/metricmind_monthly_revenue.csv")

con = duckdb.connect()
con.register("sales", root_cause)

api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

st.html("""
<div class="top-nav">
    <div class="logo">metricmind ●</div>
    <div class="nav-links">
        <span>SQL Agent</span>
        <span>Evidence</span>
        <span>Reports</span>
        <span>Workspace</span>
    </div>
    <div class="sign-btn">Live Demo</div>
</div>
""")

st.html("""
<div class="hero">
    <div>
        <div class="eyebrow">
            <div class="eyebrow-line"></div>
            Agentic Analytics
        </div>

        <div class="hero-title">
            Business Metrics, <span>Explained.</span>
        </div>

        <div class="hero-desc">
            MetricMind converts business questions into executable SQL,
            validates evidence, and generates decision-ready root-cause insights
            for analytics teams.
        </div>

        <div class="hero-actions">
            <div class="action-primary">Ask MetricMind →</div>
            <div class="action-secondary">View Workflow</div>
        </div>
    </div>

    <div class="agent-card-visual">
        <div class="agent-visual-title">MetricMind Pipeline</div>

        <div class="flow-node">
            <div class="node-icon">Q</div>
            <div>
                <div class="node-text">Natural Language Question</div>
                <div class="node-sub">User asks business metric query</div>
            </div>
        </div>

        <div class="flow-node">
            <div class="node-icon">SQL</div>
            <div>
                <div class="node-text">SQL Generation Agent</div>
                <div class="node-sub">Gemini creates safe DuckDB SQL</div>
            </div>
        </div>

        <div class="flow-node">
            <div class="node-icon">DB</div>
            <div>
                <div class="node-text">Analytics Execution</div>
                <div class="node-sub">DuckDB runs query over root-cause data</div>
            </div>
        </div>

        <div class="flow-node">
            <div class="node-icon">✓</div>
            <div>
                <div class="node-text">Evidence Verification</div>
                <div class="node-sub">Checks insight against result table</div>
            </div>
        </div>
    </div>
</div>
""")

st.html(f"""
<div class="metric-strip">
    <div class="metric-card accent">
        <div class="metric-label">Segments Analyzed ↗</div>
        <div class="metric-value">{len(root_cause)}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Regions ↗</div>
        <div class="metric-value">{root_cause["region"].nunique()}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Categories ↗</div>
        <div class="metric-value">{root_cause["category"].nunique()}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Evidence Score ↗</div>
        <div class="metric-value">9.4</div>
    </div>
</div>
""")

left, right = st.columns([1.45, 1], gap="large")

with left:
    st.html('<div class="panel-title">Revenue Impact Overview</div>')

    if {"category", "revenue_change", "region"}.issubset(root_cause.columns):
        fig_preview = px.bar(
            root_cause,
            x="category",
            y="revenue_change",
            color="region",
            title=None
        )
        fig_preview.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#050505",
            font_color="#F4F4F1",
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", y=1.08, x=1, xanchor="right")
        )
        st.plotly_chart(fig_preview, use_container_width=True)

with right:
    st.html('<div class="panel-title">Agent Status</div>')
    st.html("""
    <div class="panel">
        <div class="agent-row"><span class="dot">●</span> SQL Generation Agent Ready</div>
        <div class="agent-row"><span class="dot">●</span> DuckDB Execution Ready</div>
        <div class="agent-row"><span class="dot">●</span> Failure Detection Active</div>
        <div class="agent-row"><span class="dot">●</span> Evidence Verification Active</div>
        <div class="agent-row"><span class="dot">●</span> Report Export Enabled</div>
    </div>
    """)

st.html('<div class="ask-title">Ask MetricMind</div>')

question = st.chat_input("Ask a business question...")

if question:
    st.markdown("## Analysis Workspace")
    st.markdown(f"**Question:** {question}")

    if model is None:
        st.error("Gemini API key is missing. Add GEMINI_API_KEY in Streamlit secrets.")
        st.stop()

    # 1. SQL Agent
    sql_query = generate_sql(
        question,
        list(root_cause.columns)
    )

    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    # 2. Failure Detection Agent
    if not check_sql(sql_query):
        st.error("Unsafe SQL detected. Query blocked.")
        st.stop()

    # 3. DuckDB Execution
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

    insight = generate_insight(
    question,
    sql_query,
    result.to_string()
)

    verification = verify_evidence(
    insight,
    result.to_string()
)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Generated SQL",
        "Query Result",
        "AI Insight",
        "Evidence Check"
    ])

    with tab1:
        st.code(sql_query, language="sql")

    with tab2:
        st.dataframe(result, use_container_width=True)

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

    with tab3:
        st.markdown(insight)

    with tab4:
        st.write(verification)

    st.download_button(
        label="Download Insight Report",
        data=insight,
        file_name="metricmind_v2_report.txt",
        mime="text/plain"
    )

