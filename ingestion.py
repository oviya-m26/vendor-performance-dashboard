import os
import pandas as pd
import logging
import time
from sqlalchemy import create_engine

logging.basicConfig(
    filename="../logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine("sqlite:///../inventory.db")

def ingest_db(df, table_name, engine):
    """Insert dataframe into SQLite table"""
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"{table_name} loaded")

def load_raw_data():
    """Load CSV files and ingest into database"""

    start = time.time()

    for file in os.listdir("../data"):
        if file.endswith(".csv"):
            df = pd.read_csv("../data/" + file)
            logging.info(f"Ingesting {file}")
            ingest_db(df, file[:-4], engine)

    end = time.time()
    total_time = (end - start) / 60

    logging.info("Ingestion Complete")
    logging.info(f"Total time taken: {total_time} minutes")

if __name__ == "__main__":
    load_raw_data()