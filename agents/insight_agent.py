import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_insight(question, result):
    prompt = f"""
You are a business analyst.

Question:
{question}

SQL Result:
{result}

Generate:
1. Main insight
2. Business meaning
3. Risk level
4. One-line executive summary

Be concise and specific.
"""
    return model.generate_content(prompt).text
