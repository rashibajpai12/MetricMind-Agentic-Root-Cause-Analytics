import plotly.express as px

def create_chart(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    if df.empty:
        return None

    if len(text_cols) >= 1 and len(numeric_cols) >= 1:
        return px.bar(df, x=text_cols[0], y=numeric_cols[0], title=f"{numeric_cols[0]} by {text_cols[0]}")

    if len(numeric_cols) >= 2:
        return px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[0]} vs {numeric_cols[1]}")

    return None
