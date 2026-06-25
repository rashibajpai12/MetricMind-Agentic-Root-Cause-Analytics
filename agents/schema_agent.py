def get_schema(df):
    schema = []
    for col in df.columns:
        schema.append(f"{col}: {df[col].dtype}")
    return "\n".join(schema)
