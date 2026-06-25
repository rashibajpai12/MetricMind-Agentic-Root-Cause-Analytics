from agents.sql_agent import generate_sql
from agents.failure_agent import check_sql
from agents.insight_agent import generate_insight
from agents.verification_agent import verify_evidence


def run_workflow(question, columns, result_table=None):
    sql_query = generate_sql(question, columns)
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    safe = check_sql(sql_query)

    if not safe:
        return {
            "sql": sql_query,
            "safe": False,
            "insight": "",
            "verification": "Unsafe SQL detected."
        }

    insight = ""
    verification = ""

    if result_table is not None:
        result_text = result_table.to_string()
        insight = generate_insight(question, sql_query, result_text)
        verification = verify_evidence(insight, result_text)

    return {
        "sql": sql_query,
        "safe": True,
        "insight": insight,
        "verification": verification
    }
