import requests
from dotenv import load_dotenv
import os
from app.models.crawlers import AppIdResponse, AppDetailResponse
from app.utils.logger import logger
load_dotenv()


class Crawler:

    url = 'https://ipv4.icanhazip.com'

    proxies = {
        'http': f'http://{os.getenv("PROXY_AUTH")}@{os.getenv("PROXY")}',
        'https': f'http://{os.getenv("PROXY_AUTH")}@{os.getenv("PROXY")}'
    }

    urls = {
        "app_list":"https://api.steampowered.com/ISteamApps/GetAppList/v0002/",
        "app_detail":"https://store.steampowered.com/api/appdetails"
    }

    def __init__(self):
        self.session: requests.Session() = requests.Session()
        self.session.proxies = self.proxies


    def get_app_detail(self, app_id):
        params = {
            "appids": app_id,
        }
        response = self.session.get(self.urls["app_detail"], params=params)
        response.raise_for_status()
        print(response.json())
        data = response.json()[str(app_id)]
        if not data['success']:
            logger.error(f"Failed to retrieve app details for app ID {app_id}.")
            return None
        response = AppDetailResponse.from_dict(data)
        return response



    def get_app_ids(self)-> AppIdResponse:
        params = {
            "format": "json"
        }
        response = self.session.get(self.urls["app_list"], params=params)
        response.raise_for_status()
        data = response.json()
        response = AppIdResponse.from_dict(data)
        logger.info(f"Total apps found: {len(response.applist.apps)}")
        return response

if __name__ == "__main__":
    crawler = Crawler()
    app_id = 2990
    r = crawler.get_app_detail(app_id)
    print(r)
