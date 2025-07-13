import os
import duckdb
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from app.db import db_path
from app.db.setup import engine
print(db_path)

engine.dispose()
load_dotenv()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
table_name = 'detail'
embeddings_table_name = 'details_embedding'
model_size = 1536
with duckdb.connect(db_path) as conn:
    #conn.execute(f"DROP TABLE IF EXISTS {embeddings_table_name};")
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {embeddings_table_name} (
            id VARCHAR,
            name VARCHAR,
            text TEXT,
            embedding FLOAT[{model_size}]
        );
    """)
    conn.execute("INSTALL vss;")
    conn.execute("LOAD vss;")
    conn.execute("SET hnsw_enable_experimental_persistence = true;")
    conn.execute(f"""
    CREATE INDEX IF NOT EXISTS description_index ON {embeddings_table_name} USING HNSW (embedding)
    """)

def process_and_embed_in_batches(batch_size: int):
    batch_num = 1
    while True:
        with duckdb.connect(db_path) as conn:
            conn.execute("LOAD vss;")
            conn.execute("SET hnsw_enable_experimental_persistence = true;")
            df = conn.execute(
                f"""
            SELECT
                id,
                name,
                SUBSTR(
                    CONCAT(
                        short_description,
                        '\\n\\n',
                        detailed_description,
                        '\\n\\n',
                        about_the_game
                    ),
                    1,
                    60000
                ) AS text
            FROM {table_name}
            WHERE CAST(id AS VARCHAR) NOT IN (
                SELECT id FROM {embeddings_table_name}
            )
            LIMIT {batch_size}
                """
            ).df()

            if df.empty:
                print("Não há mais registros novos para processar. O processo foi concluído.")
                break

            print(f"Processando lote {batch_num} com {len(df)} registros.")
        #make this way so it have less chance to disrupt the connection
        df['embedding'] = embeddings.embed_documents(df['text'].tolist(), chunk_size=430)
        df = df[['id', 'name', 'text', 'embedding']]
        with duckdb.connect(db_path) as conn:
            conn.execute("LOAD vss;")
            conn.execute("SET hnsw_enable_experimental_persistence = true;")
            conn.execute(f"INSERT INTO {embeddings_table_name} SELECT * FROM df;")
            print(f"Lote {batch_num} inserido com sucesso.")
            batch_num += 1

if __name__ == "__main__":
    print("Iniciando o processamento e a incorporação dos dados em lotes...")
    process_and_embed_in_batches(batch_size=1000)

