import kagglehub
from app.db import db_path
import os
import duckdb
DATASET_URL = 'lucasbuenogodoy/steam-searcher-dataset'

def collect_kaggle_dataset():
    path = kagglehub.dataset_download(DATASET_URL)
    app_ids = os.path.join(path, 'app_ids.parquet')
    details = os.path.join(path, 'details.parquet')
    details_embedding = os.path.join(path, 'details_embedding.parquet')
    with duckdb.connect(db_path) as conn:
        conn.execute(f"CREATE TABLE IF NOT EXISTS app_ids AS SELECT * FROM read_parquet('{app_ids}')")
        conn.execute(f"CREATE TABLE IF NOT EXISTS detail AS SELECT * FROM read_parquet('{details}')")
        conn.execute(f"CREATE TABLE IF NOT EXISTS details_embedding AS SELECT * FROM read_parquet('{details_embedding}')")
        conn.commit()

if __name__ == '__main__':
    collect_kaggle_dataset()
