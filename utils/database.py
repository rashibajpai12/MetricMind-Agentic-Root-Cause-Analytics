import os
import duckdb
import pandas as pd
from utils.sample_data import create_sample_data

def load_data():
    file_path = "data/metricmind_business_data.csv"

    if not os.path.exists(file_path):
        create_sample_data()

    df = pd.read_csv(file_path)
    con = duckdb.connect()
    con.register("sales", df)
    return df, con
