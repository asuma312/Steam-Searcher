import pyarrow.dataset as ds
import polars as pl
import pyarrow.parquet as pq
import pyarrow as pa
import os
import duckdb
from bs4 import BeautifulSoup
db_path = os.path.join(
    os.path.dirname(__file__),
    '..',
    'db', 'db_files'
)
duckdb_path = os.path.join(
    db_path,
    'steam-searcher.duckdb'
)
details_path = os.path.join(db_path, 'bronze', 'details')
silver_path = os.path.join(db_path, 'silver', 'details')
os.makedirs(silver_path, exist_ok=True)
print(duckdb_path)

def generate_silver():

    dataset = ds.dataset(details_path, format='parquet')
    schemas = [pq.read_schema(dataset_file) for dataset_file in dataset.files]
    unified_schema = pa.unify_schemas(schemas)
    dataset = ds.dataset(
        details_path,
        format='parquet',
        schema=unified_schema,
    )
    df = pl.scan_pyarrow_dataset(
        dataset,
    )
    df = df.unique(subset=['steam_appid'])
    df.collect().write_parquet(
        os.path.join(silver_path, 'details.parquet'),
        #300mb
        partition_chunk_size_bytes= 300 * 1024 * 1024,
    )


def generate_gold():
    def fix_html_strings(row):
        print(f"Processing row for app: {row['name']}")
        row['detailed_description'] = BeautifulSoup(
            row['detailed_description'], 'html.parser').get_text(strip=True)
        row['about_the_game'] = BeautifulSoup(
            row['about_the_game'], 'html.parser').get_text(strip=True)
        row['supported_languages'] = BeautifulSoup(
            row['supported_languages'], 'html.parser').get_text(strip=True)
        row['windows_req_rec'] = BeautifulSoup(
            row['windows_req_rec'], 'html.parser').get_text(strip=True)
        row['windows_req_min'] = BeautifulSoup(
            row['windows_req_min'], 'html.parser').get_text(strip=True)
        row['mac_req_rec'] = BeautifulSoup(
            row['mac_req_rec'], 'html.parser').get_text(strip=True)
        row['mac_req_min'] = BeautifulSoup(
            row['mac_req_min'], 'html.parser').get_text(strip=True)
        row['lin_req_rec'] = BeautifulSoup(
            row['lin_req_rec'], 'html.parser').get_text(strip=True)
        row['lin_req_min'] = BeautifulSoup(
            row['lin_req_min'], 'html.parser').get_text(strip=True)
        return row


    with duckdb.connect(duckdb_path) as conn:
        silver_parquet = os.path.join(silver_path, 'details.parquet')
        df = conn.execute(
            f"""
SELECT name,
       is_free,
       detailed_description,
       about_the_game,
       short_description,
       supported_languages,
       pc_requirements.recommended AS windows_req_rec,
       pc_requirements.minimum AS windows_req_min,
       mac_requirements.recommended AS mac_req_rec,
       mac_requirements.minimum AS mac_req_min,
       linux_requirements.recommended AS lin_req_rec,
       linux_requirements.minimum AS lin_req_min,
       price_overview.currency AS currency_cents,
       price_overview.final AS price,
       json_extract(categories, '$[*].description') AS categories,
       json_extract(genres, '$[*].description') AS genres,
       recommendations.total AS recommendations,
       json_extract(release_date, '$[*].date') AS release_date,
       json_extract(content_descriptors, '$[*].notes') AS extras
FROM parquet_scan('{silver_parquet}')
WHERE TYPE = 'game'
            """
        ).df()
        df = df.apply(fix_html_strings, axis=1)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS detail AS
            SELECT * FROM df
            """
        )
        conn.commit()
    pass

if __name__ == "__main__":
    generate_gold()
