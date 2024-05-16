import asyncio
import aiohttp
import json


class Response:
    
    def __init__(self, status=None, text=None, headers=None, cookies=None, url=None):
        self.status = status
        self.text = text
        self.headers = headers
        self.cookies = cookies
        self.url = url

    def ok(self):
        return self.status < 400
    
    def json(self):
        return json.loads(self.text)
        
        
class Scraper:
        
    async def request(self, url, method='GET', **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                return Response(
                    status=response.status,
                    text=await response.text(),
                    headers=response.headers,
                    cookies=response.cookies,
                    url=url
                )
    
    async def worker(self, worker_id: int):
        pass
    
    async def __launch_workers(self, num_workers: int):
        await asyncio.gather(*[
            asyncio.create_task(self.worker(i))
            for i in range(num_workers)
        ])   
    
    def scrape(self, num_workers: int):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError: 
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        task = loop.create_task(self.__launch_workers(num_workers))
        
        if not loop.is_running():
            loop.run_until_complete(task)
