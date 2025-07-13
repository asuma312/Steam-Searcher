import os

base_path = os.path.join(
    os.path.dirname(__file__),
    'db_files'
)
os.makedirs(base_path, exist_ok=True)
db_name = "steam-searcher.duckdb"
db_path = os.path.join(base_path, db_name)
bronze_path = os.path.join(base_path, 'bronze', 'details')
silver_path = os.path.join(base_path, 'silver', 'details')