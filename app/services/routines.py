import asyncio
import threading
from typing import List, Coroutine
from app.db.setup import get_db
from app.models.sql import AppDetail, AppId
from app.models.crawlers import AppIdResponse as CrawlerAppIdResponse, AppDetailResponse as CrawlerAppDetailResponse, \
    AppDetail as AppDetailModel
from app.crawlers.steam import Crawler
from app.utils.logger import logger
from sqlalchemy import text
from sqlalchemy.orm import Session
from tqdm import tqdm


async def update_app_id():
    logger.info("Starting app ID update...")
    session: Session = next(get_db())
    crawler = Crawler()
    try:
        app_ids_response: CrawlerAppIdResponse = await crawler.get_app_ids()
        id_objects = [
            AppId(app_id=item.appid, app_name=item.name)
            for item in app_ids_response.applist.apps
        ]
        if not id_objects:
            logger.info("No new app IDs found from the crawler.")
            return
        session.add_all(id_objects)
        session.commit()
        logger.info(f"Batch inserted/updated {len(id_objects)} app IDs.")
    except Exception as e:
        logger.error(f"Failed to update app IDs: {e}")
        session.rollback()
    finally:
        session.close()


def do_batch_insert(details_to_add: List[AppDetail]):
    if not details_to_add:
        logger.info("No app details generated in this thread's batch.")
        return

    session: Session = next(get_db())
    try:
        session.add_all(details_to_add)
        session.commit()
        logger.info(f"Thread {threading.get_ident()} successfully batch inserted {len(details_to_add)} app details.")
    except Exception as e:
        logger.error(f"Thread {threading.get_ident()} database batch insert failed: {e}")
        session.rollback()
    finally:
        session.close()


async def fetch_and_prepare_detail(app_id: int, crawler: Crawler, semaphore: asyncio.Semaphore,
                                   max_tries=5) -> AppDetail:
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
            return AppDetail(steam_appid=app_id, name="N/A")

        app_detail_model: AppDetailModel = app_detail_response.data
        return AppDetail(**app_detail_model.dict())


async def generate_details_for_chunk(app_ids_chunk: List[int], progress_bar: tqdm, async_concurrency: int):
    crawler = Crawler()
    semaphore = asyncio.Semaphore(async_concurrency)

    tasks: List[Coroutine] = [fetch_and_prepare_detail(app_id, crawler, semaphore) for app_id in app_ids_chunk]

    results: List[AppDetail] = []
    for future in asyncio.as_completed(tasks):
        result = await future
        results.append(result)
        if progress_bar:
            progress_bar.update(1)

    await crawler.close_session()
    return results


def thread_worker(app_ids_chunk: List[int], progress_bar: tqdm, async_concurrency: int):
    if not app_ids_chunk:
        return

    details_list = asyncio.run(generate_details_for_chunk(app_ids_chunk, progress_bar, async_concurrency))
    do_batch_insert(details_list)


async def update_app_id_details(num_threads=5, batch_size=200, async_concurrency_per_thread=10):
    query_session = next(get_db())
    try:
        app_ids_query = text(
            f"""
            SELECT app_id FROM app_id
            WHERE app_id NOT IN (SELECT steam_appid FROM app_details)
            LIMIT {batch_size}
            """
        )
        app_ids: List[int] = query_session.execute(app_ids_query).scalars().all()
    finally:
        query_session.close()

    total_ids = len(app_ids)
    if total_ids == 0:
        logger.info("No app details to update. Database is up-to-date.")
        return True

    progress = tqdm(total=total_ids, desc="Atualizando detalhes dos aplicativos", ncols=100)

    chunks = [app_ids[i::num_threads] for i in range(num_threads)]

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


async def main():
    await update_app_id()
    while True:
        is_done = await update_app_id_details(num_threads=5, batch_size=500, async_concurrency_per_thread=10)
        if is_done:
            break
        logger.info("Batch processed. Checking for more app details to update...")
        await asyncio.sleep(2)
    logger.info("All app details are up-to-date. Process finished.")


if __name__ == "__main__":
    asyncio.run(main())