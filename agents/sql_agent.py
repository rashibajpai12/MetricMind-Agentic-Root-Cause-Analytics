import google.generativeai as genai

def generate_sql(question, columns):

    prompt = f"""
You are a SQL generation agent.

Table name: sales

Columns:
{columns}

User question:
{question}

Generate one safe DuckDB SQL query only.
Do not use DROP, DELETE, UPDATE, INSERT, ALTER.
Return only SQL, no explanation.
"""

    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)

    return response.text.strip()
