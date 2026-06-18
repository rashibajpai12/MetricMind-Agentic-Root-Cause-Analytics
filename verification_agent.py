import google.generativeai as genai

def verify_evidence(insight, result):

    prompt = f"""
    Check whether this insight is supported by the data.

    Insight:
    {insight}

    Data:
    {result}

    Give:
    1. Evidence Score out of 10
    2. Unsupported claims
    """

    response = model.generate_content(prompt)

    return response.text
