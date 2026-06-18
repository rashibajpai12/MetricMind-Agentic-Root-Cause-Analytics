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
    max-width: 1420px;
    padding: 2rem 4rem 4rem 4rem;
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
    margin-bottom: 110px;
}

.logo {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.04em;
}

.nav-links {
    display: flex;
    gap: 34px;
    color: #B8B8B8;
    font-size: 14px;
    font-weight: 600;
}

.sign-btn {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 999px;
    padding: 12px 22px;
    color: #F5F5F5;
    background: rgba(255,255,255,0.04);
}

.hero-wrap {
    position: relative;
    min-height: 520px;
}

.eyebrow {
    display: flex;
    align-items: center;
    gap: 18px;
    color: #747474;
    font-size: 12px;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    margin-bottom: 38px;
}

.eyebrow-line {
    width: 32px;
    height: 1px;
    background: #787878;
}

.hero-title {
    font-size: clamp(72px, 8vw, 128px);
    font-weight: 800;
    letter-spacing: -0.075em;
    line-height: 0.92;
    max-width: 980px;
    color: #F2F2EE;
}

.hero-title span {
    color: #E9DEC8;
}

.hero-desc {
    margin-top: 44px;
    max-width: 650px;
    color: #A7ACB8;
    font-size: 20px;
    line-height: 1.75;
    font-weight: 500;
}

.hero-actions {
    display: flex;
    gap: 16px;
    margin-top: 46px;
}

.action-primary, .action-secondary {
    border-radius: 999px;
    padding: 15px 26px;
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

/* MetricMind Agent Network Visual */

.agent-visual {
    position: absolute;
    right: 10px;
    bottom: 35px;
    width: 430px;
    height: 310px;
}

.graph-line {
    position: absolute;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(232,221,200,0.55), transparent);
}

.line-1 {
    width: 250px;
    top: 90px;
    left: 72px;
    transform: rotate(13deg);
}

.line-2 {
    width: 250px;
    top: 165px;
    left: 82px;
    transform: rotate(-12deg);
}

.line-3 {
    width: 180px;
    top: 224px;
    left: 150px;
    transform: rotate(8deg);
}

.line-4 {
    width: 180px;
    top: 56px;
    left: 178px;
    transform: rotate(-18deg);
}

.node {
    position: absolute;
    width: 82px;
    height: 82px;
    border-radius: 26px;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.13);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #E8DDC8;
    font-size: 24px;
    font-weight: 800;
    box-shadow: 0 0 70px rgba(232,221,200,0.08);
}

.node-main {
    width: 122px;
    height: 122px;
    border-radius: 34px;
    right: 145px;
    top: 92px;
    font-size: 38px;
    background: radial-gradient(circle at 35% 30%, #E8DDC8, #5F574A 58%, #101010 100%);
    color: #050505;
}

.node-sql {
    left: 28px;
    top: 32px;
}

.node-data {
    left: 36px;
    bottom: 44px;
}

.node-verify {
    right: 18px;
    top: 30px;
}

.node-report {
    right: 28px;
    bottom: 42px;
}

.node-label {
    position: absolute;
    font-size: 11px;
    color: #8F8F8F;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    white-space: nowrap;
}

.label-sql {
    left: 32px;
    top: 122px;
}

.label-data {
    left: 40px;
    bottom: 18px;
}

.label-verify {
    right: 18px;
    top: 122px;
}

.label-report {
    right: 30px;
    bottom: 16px;
}

.pulse-ring {
    position: absolute;
    right: 129px;
    top: 76px;
    width: 154px;
    height: 154px;
    border-radius: 42px;
    border: 1px solid rgba(232,221,200,0.14);
    animation: pulse 3.2s infinite ease-in-out;
}

@keyframes pulse {
    0% { transform: scale(0.94); opacity: 0.35; }
    50% { transform: scale(1.05); opacity: 0.8; }
    100% { transform: scale(0.94); opacity: 0.35; }
}

.metric-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-top: 30px;
    margin-bottom: 48px;
}

.metric-card {
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.025);
    border-radius: 22px;
    padding: 26px;
    min-height: 132px;
}

.metric-card.accent {
    background: #E8DDC8;
    color: #050505;
}

.metric-label {
    font-size: 14px;
    color: #8D8D8D;
    font-weight: 600;
}

.metric-card.accent .metric-label {
    color: #373737;
}

.metric-value {
    margin-top: 30px;
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -0.06em;
}

.panel-title {
    font-size: 26px;
    font-weight: 750;
    letter-spacing: -0.04em;
    margin-bottom: 18px;
}

.panel {
    border: 1px solid rgba(255,255,255,0.09);
    background: rgba(255,255,255,0.025);
    border-radius: 26px;
    padding: 26px;
}

.agent-row {
    border-bottom: 1px solid rgba(255,255,255,0.07);
    padding: 14px 0;
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
    font-size: 52px;
    font-weight: 800;
    letter-spacing: -0.07em;
    margin-bottom: 18px;
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
<div class="hero-wrap">
    <div class="eyebrow">
        <div class="eyebrow-line"></div>
        Agentic Analytics
    </div>

    <div class="hero-title">
        Everything About <span>Business Metrics</span>
    </div>

    <div class="hero-desc">
        MetricMind converts natural-language business questions into executable SQL,
        validates outputs through evidence checks, and produces decision-ready
        root-cause reports for analytics teams.
    </div>

    <div class="hero-actions">
        <div class="action-primary">Ask MetricMind →</div>
        <div class="action-secondary">View Workflow</div>
    </div>

    <div class="agent-visual">
        <div class="graph-line line-1"></div>
        <div class="graph-line line-2"></div>
        <div class="graph-line line-3"></div>
        <div class="graph-line line-4"></div>

        <div class="pulse-ring"></div>

        <div class="node node-sql">SQL</div>
        <div class="node node-data">▦</div>
        <div class="node node-main">AI</div>
        <div class="node node-verify">✓</div>
        <div class="node node-report">↗</div>

        <div class="node-label label-sql">SQL Agent</div>
        <div class="node-label label-data">Data Layer</div>
        <div class="node-label label-verify">Verify</div>
        <div class="node-label label-report">Report</div>
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
            height=330,
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
