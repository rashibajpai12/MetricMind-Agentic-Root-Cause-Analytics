from sql_agent import generate_sql
from failure_agent import verify_sql
from insight_agent import generate_insight
from verification_agent import verify_evidence


def run_workflow(question):

    sql = generate_sql(question)

    safe = verify_sql(sql)

    if not safe:
        return "Unsafe SQL"

    result = "query result"

    insight = generate_insight(result)

    verification = verify_evidence(
        insight,
        result
    )

    return {
        "sql": sql,
        "insight": insight,
        "verification": verification
    }
