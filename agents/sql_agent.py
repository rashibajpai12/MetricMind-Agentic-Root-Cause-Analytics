import google.generativeai as genai

def generate_sql(question, columns):

    prompt = f"""
You are a SQL agent.

Table name: sales

Columns:
{columns}

User Question:
{question}

Generate ONE DuckDB SQL query only.

Return SQL only.
"""

    response = genai.GenerativeModel(
        "gemini-2.5-flash"
    ).generate_content(prompt)

    return response.text.strip()
