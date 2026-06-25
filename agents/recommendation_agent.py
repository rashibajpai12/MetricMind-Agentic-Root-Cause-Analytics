import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_recommendations(question, result, root_cause):
    prompt = f"""
Question:
{question}

Result:
{result}

Root Cause:
{root_cause}

Give practical business recommendations.
Format:
- Action
- Priority
- Expected impact
"""
    return model.generate_content(prompt).text
