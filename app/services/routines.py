import asyncio
from app.db.setup import get_db
from app.models.sql import AppDetail, AppId
from app.models.crawlers import AppIdResponse as CrawlerAppIdResponse, AppDetailResponse as CrawlerAppDetailResponse, AppDetail as AppDetailModel
from app.crawlers.steam import Crawler
from app.utils.logger import logger
from sqlalchemy import text
from tqdm import tqdm

async def update_app_id():
    session = next(get_db())
    crawler = Crawler()
    app_ids: CrawlerAppIdResponse = await crawler.get_app_ids()
    id_inputs = AppId.from_pydantic(app_ids, session)
    session.commit()
    logger.info(f"Fetched {len(id_inputs)} app IDs from the crawler.")

async def update_app_detail(app_ids, crawler, progress_bar=None, commit_size=25, max_tries=5):
    session = next(get_db())
    current_commit_size = 0

    for app_id in app_ids:
        next_for = False
        for trie in range(max_tries):
            try:
                app_detail_response: CrawlerAppDetailResponse = await crawler.get_app_detail(app_id)
                logger.info(f"Fetching details for App ID {app_id} (Attempt {trie + 1})")
                break
            except Exception as e:
                logger.error(f"Error fetching details for App ID {app_id}: {e}")
                if trie >= max_tries - 1:
                    logger.error(f"Max retries reached for App ID {app_id}, skipping.")
                    next_for = True
                print('erro')
                await asyncio.sleep(5)

        if next_for:
            if progress_bar:
                progress_bar.update(1)
            continue
        if not app_detail_response:
            logger.error(f"App ID {app_id} doesn't exist in the API, skipping update.")
            if progress_bar:
                progress_bar.update(1)
            continue

        app_detail: AppDetailModel = app_detail_response.data

        app_detail_obj = AppDetail.from_pydantic(app_detail, session)
        logger.info(f"Updated {app_detail_obj.steam_appid} app detail.")
        current_commit_size += 1

        if current_commit_size >= commit_size:
            session.commit()
            logger.info(f"Committed {current_commit_size}")
            current_commit_size = 0

        if progress_bar:
            progress_bar.update(1)

async def update_app_id_details(workers=5):
    session = next(get_db())
    crawler = Crawler()
    app_ids_query = text(
        f"""
SELECT app_id FROM app_id
WHERE app_id NOT IN (SELECT steam_appid FROM app_details)
"""
    )
    app_ids: list[int] = session.execute(app_ids_query).scalars().all()
    total_ids = len(app_ids)
    progress = tqdm(total=total_ids, desc="Atualizando detalhes do aplicativo", ncols=75)
    chunk_size = total_ids // workers + 1
    tasks = []

    for worker in range(workers):
        start = worker * chunk_size
        end = min(start + chunk_size, total_ids)
        task = asyncio.create_task(update_app_detail(app_ids[start:end], crawler, progress))
        tasks.append(task)

    await asyncio.gather(*tasks)
    progress.close()

if __name__ == "__main__":
    asyncio.run(update_app_id_details(300))
    print("App IDs updated successfully.")