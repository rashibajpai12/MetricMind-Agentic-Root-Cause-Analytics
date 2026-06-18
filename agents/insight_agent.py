import google.generativeai as genai

def generate_insight(question, sql_query, result):
    prompt = f"""
You are MetricMind, an evidence-backed analytics agent.

User question:
{question}

SQL query:
{sql_query}

SQL result:
{result}

Generate:
1. Main finding
2. Evidence
3. Possible reason
4. Recommended action
5. Confidence level

Use only the SQL result. Do not invent numbers.
"""

    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
    return response.text
