import asyncio
from typing import List
from app.db.setup import get_db
from app.models.sql import AppDetail, AppId
from app.models.crawlers import AppIdResponse as CrawlerAppIdResponse, AppDetailResponse as CrawlerAppDetailResponse, AppDetail as AppDetailModel
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

async def process_app_detail_batch(app_ids_chunk: List[int], crawler: Crawler, progress_bar: tqdm, max_tries=5):

    session: Session = next(get_db())
    details_to_add: List[AppDetail] = []

    for app_id in app_ids_chunk:
        app_detail_response = None
        for attempt in range(max_tries):
            try:
                app_detail_response: CrawlerAppDetailResponse = await crawler.get_app_detail(app_id)
                logger.info(f"Fetching details for App ID {app_id} (Attempt {attempt + 1})")
                break
            except Exception as e:
                logger.error(f"Error fetching details for App ID {app_id} on attempt {attempt + 1}: {e}")
                if attempt >= max_tries - 1:
                    logger.error(f"Max retries reached for App ID {app_id}, skipping.")
                else:
                    await asyncio.sleep(5)

        if not app_detail_response or not app_detail_response.data:
            logger.warning(f"No valid data for App ID {app_id}, skipping.")
            app_detail_obj = AppDetail(
                steam_appid=app_id,
                name="N/A",
            )
            details_to_add.append(app_detail_obj)
            if progress_bar:
                progress_bar.update(1)
            continue

        app_detail_model: AppDetailModel = app_detail_response.data

        app_detail_obj = AppDetail(**app_detail_model.dict())

        details_to_add.append(app_detail_obj)
        logger.info(f"Prepared {app_detail_obj.steam_appid} for batch insert.")

        if progress_bar:
            progress_bar.update(1)

    if details_to_add:
        try:
            session.add_all(details_to_add)
            session.commit()
            logger.info(f"Successfully batch inserted {len(details_to_add)} app details.")
        except Exception as e:
            logger.error(f"Database batch insert failed: {e}")
            session.rollback()
        finally:
            session.close()
    else:
        logger.info("No new details to add in this batch.")
        session.close()

async def update_app_id_details(workers=5, batch_size=200):
    """
    Orquestra a atualização dos detalhes dos aplicativos de forma concorrente.
    """

    query_session = next(get_db())
    crawler = Crawler()
    app_ids_query = text(
        f"""
        SELECT app_id FROM app_id
        WHERE app_id NOT IN (SELECT steam_appid FROM app_details)
        LIMIT {batch_size}
        """
    )
    app_ids: List[int] = query_session.execute(app_ids_query).scalars().all()
    query_session.close()

    total_ids = len(app_ids)
    if total_ids == 0:
        logger.info("No app details to update. Database is up-to-date.")
        return True

    progress = tqdm(total=total_ids, desc="Atualizando detalhes dos aplicativos", ncols=100)

    chunk_size = (total_ids + workers - 1)
    tasks = []

    for i in range(0, total_ids, chunk_size):
        app_ids_chunk = app_ids[i:i + chunk_size]
        task = asyncio.create_task(
            process_app_detail_batch(app_ids_chunk, crawler, progress)
        )
        tasks.append(task)

    await asyncio.gather(*tasks)
    progress.close()
    return False

async def main():
    """
    Função principal que executa o processo de atualização em um loop.
    """

    await update_app_id()

    while True:

        if await update_app_id_details(workers=2, batch_size=100):
            break
        logger.info("Batch processed. Checking for more app details to update...")
        await asyncio.sleep(2)

    logger.info("All app details are up-to-date. Process finished.")

if __name__ == "__main__":
    asyncio.run(main())