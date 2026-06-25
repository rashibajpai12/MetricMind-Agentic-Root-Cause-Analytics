import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def verify_evidence(insight, result):
    prompt = f"""
Check whether the insight is supported by the data.

Insight:
{insight}

Data:
{result}

Return:
- Verified / Partially Verified / Not Verified
- Evidence
- Confidence score out of 100
"""
    return model.generate_content(prompt).text
