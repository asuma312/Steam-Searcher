from app.db import db_path, bronze_path, silver_path
import duckdb
from sqlalchemy import text
from app.services.embedder import  embeddings, table_name, embeddings_table_name, model_size
import pandas as pd
def do_query_search(query: str):
    with duckdb.connect(db_path) as conn:
        df = conn.execute(
            f"""
            SELECT 
            det.id,
            det.name, 
            det.short_description AS description, 
            
            
            CASE 
                WHEN det.price is NULL THEN 0
                ELSE det.price/100
            END AS price,
            image,
            CONCAT(
                'https://store.steampowered.com/app/',
                det.id
            ) AS link,
            det.windows_req_min AS pc_requirements,
            det.mac_req_min AS mac_requirements,
            det.lin_req_min AS linux_requirements,
            det.genres,
            det.categories
            FROM {embeddings_table_name} as emb
            INNER JOIN {table_name} AS det
            ON emb.id = det.id
            ORDER BY array_distance(embedding, array{embeddings.embed_query(query)}::FLOAT[{model_size}])
            LIMIT 20
            """
        ).df()
    return df
