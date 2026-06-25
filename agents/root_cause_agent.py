import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_root_cause(question, result):
    prompt = f"""
Question:
{question}

Data:
{result}

Identify likely root causes.
Consider revenue, profit, refunds, discount, marketing spend, inventory, delivery days, and rating.

Return 3-5 root causes with evidence.
"""
    return model.generate_content(prompt).text
