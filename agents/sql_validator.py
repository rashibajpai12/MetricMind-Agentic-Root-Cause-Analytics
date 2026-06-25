def validate_sql(sql):
    blocked = ["drop", "delete", "update", "insert", "alter", "truncate", "create"]
    lowered = sql.lower()

    for word in blocked:
        if word in lowered:
            return False, f"Blocked unsafe SQL keyword: {word}"

    if "sales" not in lowered:
        return False, "SQL must query the sales table."

    return True, "SQL is safe."
