import google.generativeai as genai

def verify_evidence(insight, result):

    prompt = f"""
Check if the insight is supported by the SQL result.

Insight:
{insight}

SQL Result:
{result}

Give:
1. Evidence Score out of 10
2. Unsupported claims if any
"""

    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)

    return response.text
