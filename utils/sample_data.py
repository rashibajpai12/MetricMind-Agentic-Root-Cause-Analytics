import pandas as pd
import numpy as np
import os

np.random.seed(42)

def create_sample_data(rows=5000):
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")

    data = {
        "date": np.random.choice(dates, rows),
        "region": np.random.choice(["North", "South", "East", "West"], rows),
        "category": np.random.choice(["Electronics", "Furniture", "Fashion", "Grocery", "Beauty"], rows),
        "subcategory": np.random.choice(["Premium", "Standard", "Budget"], rows),
        "customer_segment": np.random.choice(["Consumer", "Corporate", "Small Business"], rows),
        "orders": np.random.randint(20, 500, rows),
        "quantity": np.random.randint(50, 1200, rows),
        "revenue": np.random.randint(50000, 900000, rows),
        "cost": np.random.randint(20000, 600000, rows),
        "refund_rate": np.round(np.random.uniform(0.01, 0.18, rows), 3),
        "discount": np.round(np.random.uniform(0.02, 0.35, rows), 2),
        "marketing_spend": np.random.randint(5000, 120000, rows),
        "inventory": np.random.randint(50, 3000, rows),
        "delivery_days": np.random.randint(1, 15, rows),
        "rating": np.round(np.random.uniform(2.5, 5.0, rows), 1),
    }

    df = pd.DataFrame(data)
    df["profit"] = df["revenue"] - df["cost"]
    df["month"] = pd.to_datetime(df["date"]).dt.month_name()
    df["year"] = pd.to_datetime(df["date"]).dt.year
    df["quarter"] = pd.to_datetime(df["date"]).dt.quarter

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/metricmind_business_data.csv", index=False)

if __name__ == "__main__":
    create_sample_data()
    print("Dataset created successfully.")
