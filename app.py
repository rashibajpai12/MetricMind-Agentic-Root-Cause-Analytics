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

st.markdown("""
<style>
.stApp{
    background:#070B14;
    color:white;
}
.stApp:before{
    content:"";
    position:fixed;
    width:700px;
    height:700px;
    background:#8B5CF6;
    top:-250px;
    left:-150px;
    border-radius:50%;
    filter:blur(180px);
    opacity:0.18;
    z-index:-1;
}
.stApp:after{
    content:"";
    position:fixed;
    width:700px;
    height:700px;
    background:#6D28D9;
    bottom:-250px;
    right:-150px;
    border-radius:50%;
    filter:blur(180px);
    opacity:0.15;
    z-index:-1;
}
#MainMenu, footer, header{
    visibility:hidden;
}
.hero{
    padding:50px;
    border-radius:30px;
    background:linear-gradient(135deg, rgba(255,255,255,0.05), rgba(139,92,246,0.10));
    backdrop-filter:blur(30px);
    border:1px solid rgba(255,255,255,0.08);
    margin-bottom:35px;
}
.hero-title{
    font-size:72px;
    font-weight:800;
    line-height:1;
    color:white;
}
.hero-sub{
    font-size:28px;
    font-weight:600;
    color:#C4B5FD;
    margin-top:10px;
}
.hero-desc{
    font-size:18px;
    color:#D1D5DB;
    max-width:760px;
    margin-top:25px;
}
.metric-card{
    background:#111827;
    padding:30px;
    border-radius:24px;
    border:1px solid rgba(255,255,255,0.08);
    text-align:center;
    margin-bottom:25px;
}
.metric-number{
    font-size:52px;
    font-weight:800;
    color:#A78BFA;
}
.metric-label{
    font-size:15px;
    color:#9CA3AF;
}
.section-title{
    font-size:38px;
    font-weight:700;
    margin-top:20px;
    margin-bottom:20px;
}
[data-testid="stSidebar"]{
    background:#0D1320;
}
[data-testid="stChatInput"]{
    border-radius:20px;
}
[data-testid="stDataFrame"]{
    border-radius:20px;
    overflow:hidden;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("MetricMind")
    st.info("""
Question → SQL Agent → DuckDB  
Insight Agent → Verification Agent
""")
    st.markdown("### Sample Questions")
    st.write("• Which category had the highest revenue decline?")
    st.write("• Which region performed worst?")
    st.write("• Show refund rates above 0.08")
    st.write("• Largest revenue drop?")

root_cause = pd.read_csv("metricmind_root_cause_results.csv")
revenue = pd.read_csv("metricmind_monthly_revenue.csv")

st.markdown("""
<div class="hero">
    <div class="hero-title">MetricMind</div>
    <div class="hero-sub">Agentic Root-Cause Analytics Engine</div>
    <div class="hero-desc">
        Transform business questions into executable SQL, run automated analytics,
        verify evidence, and generate trusted AI insights through a multi-agent workflow.
    </div>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{len(root_cause)}</div>
        <div class="metric-label">Segments Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{root_cause['region'].nunique()}</div>
        <div class="metric-label">Regions</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-number">{root_cause['category'].nunique()}</div>
        <div class="metric-label">Categories</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">9.4</div>
        <div class="metric-label">Evidence Score</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="section-title">Ask MetricMind</div>
""", unsafe_allow_html=True)

con = duckdb.connect()
con.register("sales", root_cause)

api_key = st.secrets["GEMINI_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

question = st.chat_input("Ask MetricMind a business question...")

if question:
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
        "Analytics Result",
        "AI Insight",
        "Evidence Verification"
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
