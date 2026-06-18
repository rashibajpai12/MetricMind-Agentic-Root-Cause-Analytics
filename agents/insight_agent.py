import google.generativeai as genai

def generate_insight(result):

    prompt = f"""
Analyze this business result:

{result}

Provide:
1. Main Finding
2. Business Reason
3. Action
"""

    response = genai.GenerativeModel(
        "gemini-2.5-flash"
    ).generate_content(prompt)

    return response.text
