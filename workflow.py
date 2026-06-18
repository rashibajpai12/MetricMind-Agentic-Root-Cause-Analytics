def run_workflow(question):

    sql = generate_sql(question)

    safe = verify_sql(sql)

    result = run_query(sql)

    insight = generate_insight(result)

    verification = verify_evidence(
        insight,
        result
    )

    return {
        "sql": sql,
        "result": result,
        "insight": insight,
        "verification": verification
    }
