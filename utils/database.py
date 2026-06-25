import duckdb
import pandas as pd

def load_data():
    df = pd.read_csv("data/metricmind_business_data.csv")
    con = duckdb.connect()
    con.register("sales", df)
    return df, con
