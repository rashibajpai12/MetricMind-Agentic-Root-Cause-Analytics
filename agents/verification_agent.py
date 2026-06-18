import google.generativeai as genai

def verify_evidence(insight, result):
    prompt = f"""
Verify whether the insight is supported by the SQL result.

Insight:
{insight}

SQL Result:
{result}

Return:
1. Evidence Score out of 10
2. Supported claims
3. Unsupported claims
4. Final verification status
"""

    response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
    return response.text
