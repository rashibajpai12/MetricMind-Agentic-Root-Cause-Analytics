import google.generativeai as genai

def generate_sql(question, columns):
    prompt = f"""
You are a SQL generation agent for DuckDB.

Table name: sales

Columns:
{columns}

User question:
{question}

Generate ONE safe DuckDB SQL query only.
Do not use DROP, DELETE, UPDATE, INSERT, ALTER.
Return SQL only. No explanation.
"""

    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
    return response.text.replace("```sql", "").replace("```", "").strip()
