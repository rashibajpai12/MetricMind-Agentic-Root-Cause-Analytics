def check_sql(sql_query):

    blocked_words = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER"
    ]

    return not any(
        word in sql_query.upper()
        for word in blocked_words
    )
