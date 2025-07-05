from app.db.setup import get_db
from app.models.sql import AppDetail, AppId
from app.models.crawlers import AppIdResponse as CrawlerAppIdResponse, AppDetailResponse as CrawlerAppDetailResponse, AppDetail as AppDetailModel
from app.crawlers.steam import Crawler
from app.utils.logger import logger
from time import sleep
import threading

def update_app_id():
    session = next(get_db())
    crawler = Crawler()
    app_ids: CrawlerAppIdResponse = crawler.get_app_ids()
    id_inputs = AppId.from_pydantic(app_ids, session)
    session.commit()
    logger.info(f"Fetched {len(id_inputs)} app IDs from the crawler.")

def update_app_detail(app_ids, crawler, commit_size=50, max_tries=5):
    session = next(get_db())
    current_commit_size = 0
    for app_obj in app_ids:
        next_for = False

        app_objs = session.query(AppDetail).filter(AppDetail.steam_appid == app_obj.app_id).first()
        if app_objs:
            logger.warning(f"App ID {app_obj.app_id} already exists in the database, skipping update.")
            continue

        for trie in range(max_tries):
            try:
                app_detail_response: CrawlerAppDetailResponse = crawler.get_app_detail(app_obj.app_id)
                logger.info(f"Fetching details for App ID {app_obj.app_id} (Attempt {trie + 1})")
                break
            except Exception as e:
                logger.error(f"Error fetching details for App ID {app_obj.app_id}: {e}")
                if trie >= max_tries - 1:
                    logger.error(f"Max retries reached for App ID {app_obj.app_id}, skipping.")
                    next_for = True
                sleep(5)

        if next_for:
            continue
        if not app_detail_response:
            logger.error(f"App ID {app_obj.app_id} doesn't exist in the API, skipping update.")
            continue
        app_detail: AppDetailModel = app_detail_response.data

        app_detail_obj = AppDetail.from_pydantic(app_detail, session)
        #printing the sqlalchemy obj to debug
        logger.info(f"Updated {app_detail_obj.steam_appid} app detail.")
        current_commit_size += 1
        if current_commit_size >= commit_size:
            session.commit()

            current_commit_size = 0
            logger.info(f"Committed {current_commit_size} commits since last update.")
    session.commit()

def update_app_id_details(workers=5):
    session = next(get_db())
    crawler = Crawler()
    app_ids = session.query(AppId).all()
    chunk_size = len(app_ids) // workers + 1
    threads = []
    for worker in range(workers):
        start = worker * chunk_size
        end = min(start + chunk_size, len(app_ids))
        thread = threading.Thread(target=update_app_detail, args=(app_ids[start:end], crawler))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    session = next(get_db())
    #update_app_id()
    update_app_id_details(10)
    print("App IDs updated successfully.")

