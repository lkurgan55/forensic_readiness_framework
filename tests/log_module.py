from datetime import datetime
import requests
import json
import asyncio
from io import TextIOWrapper


class LogModule:
    def __init__(self, service_name: str, destination_ip: str, endpoint: str) -> None:
        self.log_route = f'http://{destination_ip}/{endpoint}'
        self.service_name = service_name

    def send_log_to_api(self, type: str, info: dict) -> None:
        log = {
            'service_name': self.service_name,
            'type': type,
            'datetime': str(datetime.now()),
            'info': info
        }
        
        requests.post(url = self.log_route, params = {'log': json.dumps(log)})

    async def follow(self, thefile: TextIOWrapper):
        thefile.seek(0,2) # перейти до кінця файлу
        while True:
            line = thefile.readline()
            if not line:
                await asyncio.sleep(60) # перевіряти нявність події кожну хв
                continue
            yield line

    async def send_system_logs(self, file_to_read: str):
        with open(file_to_read, "r") as log_file:
            follow_generator = self.follow(log_file)
            while True:
                log = await anext(follow_generator)
                log = {
                    'service_name': self.service_name,
                    'type': 'info',
                    'datetime': str(datetime.now()),
                    'info': log
                }
        
                requests.post(url = self.log_route, params = {'log': json.dumps(log)})



