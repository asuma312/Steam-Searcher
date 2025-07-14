from app.db import db_path, bronze_path, silver_path
import duckdb
from sqlalchemy import text
from app.services.embedder import  embeddings, table_name, embeddings_table_name, model_size
import pandas as pd
def do_query_search(query: str, category: list[str], genre: list[str], price_start: int, price_end: int) -> pd.DataFrame:
    with duckdb.connect(db_path) as conn:
        sql_query = f"""
            SELECT
                det.id,
                det.name,
                det.short_description AS description,
                CASE
                    WHEN det.price IS NULL THEN 0
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
            FROM {embeddings_table_name} AS emb
            INNER JOIN {table_name} AS det
                ON emb.id = det.id
            WHERE
                det.price >= ? AND 
                det.price <= ? AND
                list_has_any(det.categories, ?) AND
                list_has_any(det.genres, ?)
            ORDER BY array_distance(embedding, array{embeddings.embed_query(query)}::FLOAT[{model_size}])
            LIMIT 20
        """
        params = [
            price_start,
            price_end,
            category,
            genre
        ]
        df = conn.execute(sql_query, params).df()

    return df

def do_category_search():
    with duckdb.connect(db_path) as conn:
        df = conn.execute(
            """
            SELECT category FROM app_categories
            """
        ).df()
    return [x['unnest'] for x in df['category'].tolist()]

def do_genre_search():
    with duckdb.connect(db_path) as conn:
        df = conn.execute(
            """
            SELECT genre FROM app_genres
            """
        ).df()
    return [x['unnest'] for x in df['genre'].tolist()]