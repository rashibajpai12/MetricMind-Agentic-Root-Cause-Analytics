def check_sql(sql):

    blocked = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER"
    ]

    for word in blocked:
        if word in sql.upper():
            return False

    return True
