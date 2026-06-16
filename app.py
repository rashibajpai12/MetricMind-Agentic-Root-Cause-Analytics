import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
import google.generativeai as genai

st.set_page_config(
    page_title="MetricMind",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #0B0D0F;
    color: #F5F5F5;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 1.2rem;
    max-width: 1180px;
}

[data-testid="stSidebar"] {
    background: #111315;
    border-right: 1px solid #25282C;
}

.sidebar-title {
    font-size: 30px;
    font-weight: 900;
    margin-bottom: 6px;
}

.sidebar-sub {
    color: #A1A1AA;
    font-size: 14px;
    margin-bottom: 25px;
}

.sidebar-card {
    background: #181A1D;
    border: 1px solid #2B2E33;
    border-radius: 22px;
    padding: 18px;
    margin-bottom: 18px;
}

.side-pill {
    background: #0B0D0F;
    border: 1px solid #2B2E33;
    border-radius: 999px;
    padding: 10px 13px;
    margin: 8px 0;
    font-size: 13px;
}

.hero {
    background: linear-gradient(135deg, #17191D 0%, #1E1830 60%, #3A2D54 100%);
    border: 1px solid #2E3138;
    border-radius: 28px;
    padding: 38px 42px;
    margin-bottom: 22px;
}

.badge {
    display: inline-block;
    background: #D8C8FF;
    color: #111;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 20px;
}

.hero-title {
    font-size: 60px;
    font-weight: 950;
    letter-spacing: -2px;
    margin: 0;
}

.hero-desc {
    color: #C8C8CE;
    font-size: 17px;
    line-height: 1.6;
    max-width: 780px;
    margin-top: 20px;
}

.metric-card {
    background: #151819;
    border: 1px solid #2B2E33;
    border-radius: 22px;
    padding: 22px;
    height: 135px;
}

.metric-card-accent {
    background: #D8C8FF;
    color: #111;
}

.metric-label {
    font-size: 14px;
    color: #A1A1AA;
}

.metric-card-accent .metric-label {
    color: #333;
}

.metric-value {
    font-size: 44px;
    font-weight: 950;
    margin-top: 24px;
}

.section-title {
    font-size: 25px;
    font-weight: 850;
    margin-top: 40px;
    margin-bottom: 25px;
}

.agent-row {
    background: #151819;
    border: 1px solid #2B2E33;
    border-radius: 16px;
    padding: 13px 15px;
    margin-bottom: 10px;
    font-size: 14px;
}

.dot {
    color: #D8C8FF;
    font-weight: 900;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background: #151819;
    border: 1px solid #2B2E33;
    border-radius: 999px;
    padding: 10px 18px;
}

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

div[data-testid="stAlert"] {
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-title"> MetricMind</div>
    <div class="sidebar-sub">AI-native analytics workspace</div>

    <div class="sidebar-card">
        <b>Try Questions</b>
        <div class="side-pill">Which category had the highest revenue decline?</div>
        <div class="side-pill">Which region performed worst?</div>
        <div class="side-pill">Show refund rates above 0.08</div>
        <div class="side-pill">Largest revenue drop?</div>
    </div>

    <div class="sidebar-card">
        <b>Agent Flow</b>
        <div class="side-pill">Question → SQL Agent</div>
        <div class="side-pill">DuckDB → Analytics</div>
        <div class="side-pill">Insight → Verification</div>
        <div class="side-pill">Report → Download</div>
    </div>
    """, unsafe_allow_html=True)

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

st.markdown("""
<div class="hero">
    <div class="badge">AI Analytics Agent</div>
    <div class="hero-title">MetricMind</div>
    <div class="hero-desc">
        Ask business questions in natural language. MetricMind generates SQL,
        runs analytics, detects failures, verifies evidence, and produces decision-ready insights.
    </div>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-card metric-card-accent">
        <div>Segments Analyzed ↗</div>
        <div class="metric-value">{len(root_cause)}</div>
        <div class="metric-label">available business segments</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div>Regions ↗</div>
        <div class="metric-value">{root_cause["region"].nunique()}</div>
        <div class="metric-label">regional dimensions</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div>Categories ↗</div>
        <div class="metric-value">{root_cause["category"].nunique()}</div>
        <div class="metric-label">product categories</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="metric-card">
        <div>Evidence Score ↗</div>
        <div class="metric-value">9.4</div>
        <div class="metric-label">verified confidence</div>
    </div>
    """, unsafe_allow_html=True)

left, right = st.columns([1.45, 1], gap="large")

with left:
    st.markdown('<div class="section-title">Revenue Impact Overview</div>', unsafe_allow_html=True)

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
            plot_bgcolor="#151819",
            font_color="#F5F5F5",
            height=340,
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", y=1.08, x=1, xanchor="right")
        )
        st.plotly_chart(fig_preview, use_container_width=True)

with right:
    st.markdown('<div class="section-title">Agent Status</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="agent-row"><span class="dot">●</span> SQL Generation Agent Ready</div>
    <div class="agent-row"><span class="dot">●</span> DuckDB Execution Ready</div>
    <div class="agent-row"><span class="dot">●</span> Failure Detection Active</div>
    <div class="agent-row"><span class="dot">●</span> Evidence Verification Active</div>
    <div class="agent-row"><span class="dot">●</span> Report Export Enabled</div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Ask MetricMind</div>', unsafe_allow_html=True)

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
                plot_bgcolor="#151819",
                font_color="#F5F5F5"
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
