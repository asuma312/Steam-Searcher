import aiohttp
from dotenv import load_dotenv
import os
from app.models.crawlers import AppIdResponse, AppDetailResponse
from app.utils.logger import logger
import asyncio
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


    async def detect_ip(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get('https://api.ipify.org?format=json', proxy=self.proxies.get('https')) as response:
                print(f"Response: {await response.json()}")


    async def get_app_detail(self, app_id):
        params = {
            "appids": app_id,
        }
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), proxy=self.proxies.get('https')) as session:
            async with session.get(self.urls["app_detail"], params=params) as response:
                response.raise_for_status()
                data = await response.json()
                app_data = data.get(str(app_id))
                if not app_data or not app_data.get('success'):
                    logger.error(f"Failed to retrieve app details for app ID {app_id}.")
                    return None
                response = AppDetailResponse.from_dict(app_data)
                return response



    async def get_app_ids(self)-> AppIdResponse:
        params = {
            "format": "json"
        }
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), proxy=self.proxies.get('https')) as session:
            async with session.get(self.urls["app_list"], params=params) as response:
                response.raise_for_status()
                data = await response.json()
                response = AppIdResponse.from_dict(data)
                logger.info(f"Total apps found: {len(response.applist.apps)}")
                return response
if __name__ == '__main__':
    crawler = Crawler()
    x = asyncio.run(crawler.get_app_detail('428020'))
    print(x)