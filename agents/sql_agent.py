import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_sql(question, schema):
    prompt = f"""
You are an expert business analytics SQL agent.

Table name: sales

Schema:
{schema}

Task:
Convert the user's business question into one valid DuckDB SQL query.

Rules:
- Return only SQL.
- No markdown.
- No explanation.
- Use only columns from the schema.
- Prefer aggregation when needed.
- Limit results to 20 rows unless the user asks otherwise.

Question:
{question}
"""

    response = model.generate_content(prompt)
    return response.text.strip().replace("```sql", "").replace("```", "")
