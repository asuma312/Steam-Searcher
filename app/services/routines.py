import asyncio
import threading
from typing import List, Coroutine
import pandas as pd
import duckdb
import uuid
from app.models.crawlers import AppIdResponse as CrawlerAppIdResponse, AppDetailResponse as CrawlerAppDetailResponse, \
    AppDetail as AppDetailModel
from app.crawlers.steam import Crawler
from app.utils.logger import logger
from tqdm import tqdm
from app.db import db_path,base_path, bronze_path, silver_path
from app.db.setup import engine
engine.dispose()
import os
import kagglehub

ids_path = os.path.join(base_path,'bronze', 'ids')


async def update_app_id():
    logger.info("Starting app ID update...")
    crawler = Crawler()
    try:
        app_ids_response: CrawlerAppIdResponse = await crawler.get_app_ids()
        id_list = [
            {'app_id': item.appid, 'app_name': item.name}
            for item in app_ids_response.applist.apps
        ]
        if not id_list:
            logger.info("No new app IDs found from the crawler.")
            return

        df = pd.DataFrame(id_list)
        output_file = os.path.join(ids_path, 'app_ids.parquet')
        df.to_parquet(output_file, index=False)
        logger.info(f"Saved {len(id_list)} app IDs to {output_file}.")
    except Exception as e:
        logger.error(f"Failed to update app IDs: {e}")


def do_batch_insert(details_to_add: List[AppDetailModel]):
    if not details_to_add:
        logger.info("No app details generated in this thread's batch.")
        return

    try:
        data_dicts = [detail.model_dump() for detail in details_to_add]
        df = pd.DataFrame(data_dicts)

        filename = f"{uuid.uuid4()}.parquet"
        output_file = os.path.join(bronze_path, filename)

        df.to_parquet(output_file, index=False)
        logger.info(
            f"Thread {threading.get_ident()} successfully saved {len(details_to_add)} app details to {filename}.")
    except Exception as e:
        logger.error(f"Thread {threading.get_ident()} parquet file write failed: {e}")


async def fetch_and_prepare_detail(app_id: int, crawler: Crawler, semaphore: asyncio.Semaphore,
                                   max_tries=5) -> AppDetailModel:
    async with semaphore:
        app_detail_response = None
        for attempt in range(max_tries):
            try:
                app_detail_response = await crawler.get_app_detail(app_id)
                logger.info(f"Fetching details for App ID {app_id} (Attempt {attempt + 1})")
                break
            except Exception as e:
                logger.error(f"Error fetching details for App ID {app_id} on attempt {attempt + 1}: {e}")
                if attempt >= max_tries - 1:
                    logger.error(f"Max retries reached for App ID {app_id}, skipping.")
                else:
                    await asyncio.sleep(5)

        if not app_detail_response or not app_detail_response.data:
            logger.warning(f"No valid data for App ID {app_id}, creating placeholder.")
            return AppDetailModel(
                type='N/A',
                name='Unknown',
                steam_appid=app_id,
                required_age=0,
                is_free=False,
                dlc=[],
                detailed_description='',
                about_the_game='',
                short_description='',
                supported_languages='',
                header_image='',
                website='',
                pc_requirements={},
                mac_requirements={},
                linux_requirements={},
                developers=[],
                publishers=[],
                price_overview={},
                packages=[],
                platforms={},
                metacritic={},
                categories=[],
                genres=[],
                screenshots=[],
                movies=[],
                recommendations={},
                achievements={},
                release_date={},
                support_info={},
                background='',
                content_descriptors={},
                tags=[]
            )


        return app_detail_response.data

async def generate_details_for_chunk(app_ids_chunk: List[int], progress_bar: tqdm, async_concurrency: int):
    crawler = Crawler()
    semaphore = asyncio.Semaphore(async_concurrency)

    tasks: List[Coroutine] = [fetch_and_prepare_detail(app_id, crawler, semaphore) for app_id in app_ids_chunk]

    results: List[AppDetailModel] = []
    for future in asyncio.as_completed(tasks):
        result = await future
        if result:
            results.append(result)
        if progress_bar:
            progress_bar.update(1)

    return results


def thread_worker(app_ids_chunk: List[int], progress_bar: tqdm, async_concurrency: int):
    if not app_ids_chunk:
        return

    details_list = asyncio.run(generate_details_for_chunk(app_ids_chunk, progress_bar, async_concurrency))
    do_batch_insert(details_list)


async def update_app_id_details(num_threads=5, batch_size=200, async_concurrency_per_thread=10) -> bool:
    master_id_file = os.path.join(ids_path, 'app_ids.parquet')
    if not os.path.exists(master_id_file):
        logger.error("Master app_ids.parquet file not found. Please run update_app_id first.")
        return True

    try:
        all_ids_df = pd.read_parquet(master_id_file, columns=['app_id'])
        all_ids = set(all_ids_df['app_id'].unique())

        processed_ids = set()
        for file in os.listdir(bronze_path):
            file_path = os.path.join(bronze_path, file)
            if os.path.getsize(file_path) == 0:
                logger.error(f"File {file} has no content. Deleting.")
                os.remove(file_path)
        if os.path.exists(bronze_path) and len(os.listdir(bronze_path)) > 0:
            processed_df = pd.read_parquet(bronze_path, columns=['steam_appid'])
            processed_ids = set(processed_df['steam_appid'].unique())

        app_ids_to_fetch = list(all_ids - processed_ids)

        total_ids = len(app_ids_to_fetch)
        if total_ids == 0:
            logger.info("No new app details to update. All details are up-to-date.")
            return True

        logger.info(f"Found {total_ids} app IDs needing details. Processing a batch of {min(total_ids, batch_size)}.")

        app_ids_batch = app_ids_to_fetch[:batch_size]

        progress = tqdm(total=len(app_ids_batch), desc="Atualizando detalhes dos aplicativos", ncols=100)

        chunks = [app_ids_batch[i::num_threads] for i in range(num_threads)]

        threads: List[threading.Thread] = []
        for chunk in chunks:
            if chunk:
                thread = threading.Thread(
                    target=thread_worker,
                    args=(chunk, progress, async_concurrency_per_thread)
                )
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

        progress.close()
        return False

    except Exception as e:
        logger.error(f"An error occurred during app detail update: {e}")
        return True


async def steam_main():
    await update_app_id()
    while True:
        is_done = await update_app_id_details(num_threads=6, batch_size=300, async_concurrency_per_thread=6)
        if is_done:
            break
        logger.info("Batch processed. Checking for more app details to update...")
        await asyncio.sleep(2)
    logger.info("All app details are up-to-date. Process finished.")



if __name__ == "__main__":
    #asyncio.run(steam_main())
    #TODO GPU CPU dataset
    #setup_gpu_dataset()
    pass