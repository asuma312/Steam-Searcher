import pyarrow.dataset as ds
import polars as pl
import pyarrow.parquet as pq
import pyarrow as pa
import os
import duckdb
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
import swifter
import time
from app.db import db_path, bronze_path, silver_path
from app.db.setup import engine
engine.dispose()
from uuid import uuid4

os.makedirs(silver_path, exist_ok=True)

requirements_keys = set()


def update_and_padronize_keys(key, threshold=90):
    key = key.strip().lower()

    for existing_key in requirements_keys:

        similarity = fuzz.partial_ratio(key.lower(), existing_key.lower())

        if similarity >= threshold:
            return existing_key
    requirements_keys.add(key)
    return key
def generate_silver():

    dataset = ds.dataset(bronze_path, format='parquet')
    schemas = [pq.read_schema(dataset_file) for dataset_file in dataset.files]
    unified_schema = pa.unify_schemas(schemas)
    dataset = ds.dataset(
        bronze_path,
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
        row['detailed_description'] = BeautifulSoup(
            row['detailed_description'], 'html.parser').get_text(strip=True)
        row['about_the_game'] = BeautifulSoup(
            row['about_the_game'], 'html.parser').get_text(strip=True)
        row['supported_languages'] = BeautifulSoup(
            row['supported_languages'], 'html.parser').get_text(strip=True)

        windows_req_rec = BeautifulSoup(
            row['windows_req_rec'], 'html.parser')
        attributes = windows_req_rec.find_all('li')
        w_rec_parsed_atributes = {
            'extra':''
        }
        for attr in attributes:
            if ':' in attr.text:
                key, value = attr.text.split(':', 1)
                w_rec_parsed_atributes[update_and_padronize_keys(key)] = value.strip()
            else:
                w_rec_parsed_atributes['extra'] += attr.text.strip() + ' '
        row['windows_req_rec'] = w_rec_parsed_atributes


        windows_req_min = BeautifulSoup(
            row['windows_req_min'], 'html.parser')
        attributes = windows_req_min.find_all('li')
        w_min_parsed_atributes = {
            'extra':''
        }
        for attr in attributes:
            if ':' in attr.text:
                key, value = attr.text.split(':', 1)
                w_min_parsed_atributes[update_and_padronize_keys(key)] = value.strip()
            else:
                w_min_parsed_atributes['extra'] += attr.text.strip() + ' '
        row['windows_req_min'] = w_min_parsed_atributes


        mac_req_rec = BeautifulSoup(
            row['mac_req_rec'], 'html.parser')
        attributes = mac_req_rec.find_all('li')
        m_rec_parsed_atributes = {
            'extra':''
        }
        for attr in attributes:
            if ':' in attr.text:
                key, value = attr.text.split(':', 1)
                m_rec_parsed_atributes[update_and_padronize_keys(key)] = value.strip()
            else:
                m_rec_parsed_atributes['extra'] += attr.text.strip() + ' '
        row['mac_req_rec'] = m_rec_parsed_atributes


        mac_req_min = BeautifulSoup(
            row['mac_req_min'], 'html.parser')
        attributes = mac_req_min.find_all('li')
        m_min_parsed_atributes = {
            'extra':''
        }
        for attr in attributes:
            if ':' in attr.text:
                key, value = attr.text.split(':', 1)
                m_min_parsed_atributes[update_and_padronize_keys(key)] = value.strip()
            else:
                m_min_parsed_atributes['extra'] += attr.text.strip() + ' '
        row['mac_req_min'] = m_min_parsed_atributes



        lin_req_rec = BeautifulSoup(
            row['lin_req_rec'], 'html.parser')
        attributes = lin_req_rec.find_all('li')
        l_rec_parsed_atributes = {
            'extra':''
        }
        for attr in attributes:
            if ':' in attr.text:
                key, value = attr.text.split(':', 1)
                l_rec_parsed_atributes[update_and_padronize_keys(key)] = value.strip()
            else:
                l_rec_parsed_atributes['extra'] += attr.text.strip() + ' '
        row['lin_req_rec'] = l_rec_parsed_atributes




        lin_req_min = BeautifulSoup(
            row['lin_req_min'], 'html.parser')
        attributes = lin_req_min.find_all('li')
        l_min_parsed_atributes = {
            'extra':''
        }
        for attr in attributes:
            if ':' in attr.text:
                key, value = attr.text.split(':', 1)
                l_min_parsed_atributes[update_and_padronize_keys(key)] = value.strip()
            else:
                l_min_parsed_atributes['extra'] += attr.text.strip() + ' '
        row['lin_req_min'] = l_min_parsed_atributes
        return row


    with duckdb.connect(db_path) as conn:
        silver_parquet = os.path.join(silver_path, 'details.parquet')
        conn.execute(
            "DROP TABLE IF EXISTS detail"
        )
        
        df = conn.execute(
            f"""
SELECT 
        steam_appid as id,
        name,
        is_free,
        detailed_description,
        about_the_game,
        short_description,
        supported_languages,
        header_image AS image,
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
        df = df.swifter.apply(fix_html_strings, axis=1)
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
