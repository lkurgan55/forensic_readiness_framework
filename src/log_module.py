from datetime import datetime
import requests

class LogModule:
    def __init__(self, service_name: str, destination_ip: str, endpoint: str) -> None:
        self.log_route = f'{destination_ip}/{endpoint}'
        self.service_name = service_name

    def send_log_to_api(self, type: str, info: dict) -> None:
        log = {
            'service': self.service_name,
            'type': type,
            'datetime': str(datetime.now()),
            'info': info
        }
        
        requests.post(url = self.log_route, data = log)

    def send_system_logs(self, files_to_read: list[str]):
        pass