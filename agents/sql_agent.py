def generate_sql(question, schema=None):
    q = question.lower()

    if "highest revenue" in q or "most revenue" in q:
        if "category" in q:
            return """
            SELECT category, SUM(revenue) AS total_revenue
            FROM sales
            GROUP BY category
            ORDER BY total_revenue DESC
            LIMIT 10
            """
        if "region" in q:
            return """
            SELECT region, SUM(revenue) AS total_revenue
            FROM sales
            GROUP BY region
            ORDER BY total_revenue DESC
            LIMIT 10
            """

    if "lowest profit" in q or "worst profit" in q:
        return """
        SELECT region, SUM(profit) AS total_profit
        FROM sales
        GROUP BY region
        ORDER BY total_profit ASC
        LIMIT 10
        """

    if "monthly revenue" in q or "revenue trend" in q:
        return """
        SELECT year, month, SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY year, month
        ORDER BY year, month
        """

    if "refund" in q:
        return """
        SELECT category, AVG(refund_rate) AS avg_refund_rate
        FROM sales
        GROUP BY category
        ORDER BY avg_refund_rate DESC
        LIMIT 10
        """

    if "customer segment" in q or "most profitable" in q:
        return """
        SELECT customer_segment, SUM(profit) AS total_profit
        FROM sales
        GROUP BY customer_segment
        ORDER BY total_profit DESC
        LIMIT 10
        """

    if "compare revenue by region and category" in q:
        return """
        SELECT region, category, SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY region, category
        ORDER BY total_revenue DESC
        LIMIT 20
        """

    return """
    SELECT category, region, SUM(revenue) AS total_revenue, SUM(profit) AS total_profit, AVG(refund_rate) AS avg_refund_rate
    FROM sales
    GROUP BY category, region
    ORDER BY total_revenue DESC
    LIMIT 20
    """
