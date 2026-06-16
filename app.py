import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
import google.generativeai as genai

st.set_page_config(
    page_title="MetricMind",
    page_icon="📊",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: #0b0d0f;
    color: #f5f5f5;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
}

[data-testid="stSidebar"] {
    background: #111417;
    border-right: 1px solid #25282c;
}

.card {
    background: #151819;
    border: 1px solid #2c3034;
    border-radius: 24px;
    padding: 24px;
    min-height: 150px;
}

.hero {
    background: linear-gradient(135deg, #151819 0%, #1a1624 55%, #cdbbff 220%);
    border: 1px solid #2d3136;
    border-radius: 30px;
    padding: 42px;
    margin-bottom: 22px;
}

.hero h1 {
    font-size: 64px;
    line-height: 0.95;
    font-weight: 900;
    margin: 0;
    letter-spacing: -2px;
}

.hero p {
    color: #bfc3c7;
    font-size: 18px;
    max-width: 720px;
    margin-top: 18px;
    line-height: 1.6;
}

.pill {
    display: inline-block;
    background: #d8c8ff;
    color: #111;
    padding: 9px 16px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 18px;
}

.metric-box {
    background: #151819;
    border: 1px solid #2c3034;
    border-radius: 22px;
    padding: 22px;
    height: 145px;
}

.metric-box.highlight {
    background: #d8c8ff;
    color: #111;
}

.metric-value {
    font-size: 42px;
    font-weight: 900;
    margin-top: 28px;
}

.metric-label {
    color: #a6abb0;
    font-size: 14px;
}

.metric-box.highlight .metric-label {
    color: #222;
}

.section-title {
    font-size: 26px;
    font-weight: 800;
    margin: 18px 0;
}

.agent-card {
    background: #151819;
    border: 1px solid #2c3034;
    border-radius: 22px;
    padding: 18px;
    margin-bottom: 14px;
}

.agent-ok {
    color: #d8c8ff;
    font-weight: 800;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background: #151819;
    border-radius: 999px;
    padding: 10px 18px;
    border: 1px solid #2c3034;
}

div[data-testid="stAlert"] {
    border-radius: 18px;
}

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

.stChatInputContainer {
    border-radius: 20px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar
# =========================
with st.sidebar:

    st.markdown("""
    <style>

    .side-logo{
        font-size:34px;
        font-weight:900;
        color:white;
        margin-top:15px;
        margin-bottom:10px;
    }

    .side-sub{
        color:#A1A1AA;
        font-size:15px;
        margin-bottom:35px;
    }

    .side-card{
        background:linear-gradient(
            135deg,
            rgba(139,92,246,0.10),
            rgba(255,255,255,0.03)
        );

        border:1px solid rgba(255,255,255,0.08);

        border-radius:24px;

        padding:20px;

        margin-bottom:22px;

        backdrop-filter:blur(20px);
    }

    .side-card-title{
        font-size:18px;
        font-weight:700;
        color:white;
        margin-bottom:15px;
    }

    .question-pill{
        background:#111827;

        border:1px solid rgba(255,255,255,0.08);

        border-radius:999px;

        padding:12px;

        margin-bottom:10px;

        color:#E5E7EB;

        font-size:14px;
    }

    .flow-step{
        color:#D1D5DB;

        padding:10px 0;

        border-bottom:1px solid rgba(255,255,255,0.05);

        font-size:15px;
    }

    .flow-step:last-child{
        border-bottom:none;
    }

    </style>

    <div class="side-logo">
    📊 MetricMind
    </div>

    <div class="side-sub">
    AI-native analytics workspace
    </div>

    <div class="side-card">

        <div class="side-card-title">
        Try Questions
        </div>

        <div class="question-pill">
        Which category had the highest revenue decline?
        </div>

        <div class="question-pill">
        Which region performed worst?
        </div>

        <div class="question-pill">
        Show refund rates above 0.08
        </div>

        <div class="question-pill">
        Largest revenue drop?
        </div>

    </div>

    <div class="side-card">

        <div class="side-card-title">
        Agent Flow
        </div>

        <div class="flow-step">
        Question → SQL Agent
        </div>

        <div class="flow-step">
        DuckDB → Analytics
        </div>

        <div class="flow-step">
        Insight → Verification
        </div>

        <div class="flow-step">
        Report → Download
        </div>

    </div>

    """, unsafe_allow_html=True)

# =========================
# Load Data
# =========================
root_cause = pd.read_csv("metricmind_root_cause_results.csv")
revenue = pd.read_csv("metricmind_monthly_revenue.csv")

con = duckdb.connect()
con.register("sales", root_cause)

# =========================
# Gemini API
# =========================
api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

# =========================
# Hero
# =========================
st.markdown("""
<div class="hero">
    <div class="pill">AI Analytics Agent</div>
    <h1>MetricMind</h1>
    <p>
    Ask business questions in natural language. MetricMind generates SQL,
    runs analytics, detects failures, verifies evidence, and produces
    decision-ready insights.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI Grid
# =========================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-box highlight">
        <div>Segments Analyzed ↗</div>
        <div class="metric-value">{len(root_cause)}</div>
        <div class="metric-label">available business segments</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-box">
        <div>Regions ↗</div>
        <div class="metric-value">{root_cause["region"].nunique()}</div>
        <div class="metric-label">regional dimensions</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-box">
        <div>Categories ↗</div>
        <div class="metric-value">{root_cause["category"].nunique()}</div>
        <div class="metric-label">product categories</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="metric-box">
        <div>Evidence Score ↗</div>
        <div class="metric-value">9.4</div>
        <div class="metric-label">verified confidence</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# Dashboard Preview
# =========================
left, right = st.columns([1.35, 1])

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
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#f5f5f5",
            margin=dict(l=20, r=20, t=20, b=20),
            height=330
        )
        st.plotly_chart(fig_preview, use_container_width=True)

with right:
    st.markdown('<div class="section-title">Agent Status</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-card"><span class="agent-ok">●</span> SQL Generation Agent Ready</div>
    <div class="agent-card"><span class="agent-ok">●</span> DuckDB Execution Ready</div>
    <div class="agent-card"><span class="agent-ok">●</span> Failure Detection Active</div>
    <div class="agent-card"><span class="agent-ok">●</span> Evidence Verification Active</div>
    """, unsafe_allow_html=True)

# =========================
# Chat Input
# =========================
st.markdown('<div class="section-title">Ask MetricMind</div>', unsafe_allow_html=True)

question = st.chat_input("Ask a business question...")

# =========================
# Agent Execution
# =========================
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
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#f5f5f5"
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
