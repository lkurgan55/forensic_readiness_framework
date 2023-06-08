from log_module import LogModule
service_name = 'test_service'

destination_ip = 'localhost'
endpoint = 'tools/register_log'

logger = LogModule(service_name, destination_ip, endpoint)

log_example = {
    'EventName': 'LoginInSystem',
    'UserName': 'test_user',
    'SourceIp': '192.168.0.105',
    'Success': False,
}

logger.send_log_to_api('critical', log_example)
logger.send_system_logs('system/logs/log.file')