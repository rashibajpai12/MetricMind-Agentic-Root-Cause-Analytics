from agents.sql_agent import generate_sql
from agents.failure_agent import check_sql
from agents.insight_agent import generate_insight
from agents.verification_agent import verify_evidence


def run_workflow(question, result):

    sql_query = generate_sql(question)

    safe = check_sql(sql_query)

    insight = generate_insight(result)

    verification = verify_evidence(insight)

    return {
        "sql": sql_query,
        "safe": safe,
        "insight": insight,
        "verification": verification
    }
