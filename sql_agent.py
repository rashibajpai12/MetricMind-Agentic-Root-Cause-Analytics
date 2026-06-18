import google.generativeai as genai

def generate_sql(question, columns):

    prompt = f"""
    Generate safe DuckDB SQL.

    Columns:
    {columns}

    Question:
    {question}
    """

    return model.generate_content(prompt).text
