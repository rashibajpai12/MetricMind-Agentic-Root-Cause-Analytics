def verify_sql(sql):

    blocked_words = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER"
    ]

    for word in blocked_words:
        if word in sql.upper():
            return False

    return True
