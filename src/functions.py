import boto3
import json
import pandas as pd
import os
import gzip
import json
from datetime import datetime


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        print(f"Сталася помилка під час читання JSON-файлу: {e}")
        return None

def extract_keys(dictionary, keys):
    extracted_dict = {}

    for key in keys:
        if key in dictionary:
            extracted_dict[key] = dictionary[key]

    return extracted_dict

def save_dict_as_json(dictionary, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(dictionary, json_file, indent=4)
        print(f"Дані успішно збережено як JSON у файлі: {file_path}")
    except Exception as e:
        print(f"Сталася помилка під час збереження: {e}")

def configure_cloudtrail(trail_name, bucket_name, include_global_events=True, **session):
    # Ініціалізуємо клієнта boto3 для AWS CloudTrail
    cloudtrail_client = boto3.client('cloudtrail', **session)
    # Створюємо конфігурацію CloudTrail
    cloudtrail_client.create_trail(
        Name=trail_name,
        S3BucketName=bucket_name,
        IncludeGlobalServiceEvents=include_global_events
    )
    # Вмикаємо CloudTrail
    cloudtrail_client.start_logging(Name=trail_name)

def create_s3_bucket(bucket_name, **session):
    # Ініціалізуємо клієнта boto3 для Amazon S3
    s3_client = boto3.client('s3', **session)
    try: # Перевіряємо, чи існує вже бакет з вказаною назвою
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Бакет з назвою '{bucket_name}' вже існує.")
    except: # Якщо бакет не існує, створюємо його
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Бакет з назвою '{bucket_name}' був успішно створений.")

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Папка '{directory_path}' була успішно створена.")
    else:
        print(f"Папка '{directory_path}' вже існує.")

def download_logs(bucket_name: str, destination: str, date: str = '', logs_region_name: str = '', **session):
    s3_client = boto3.client('s3', **session)

    check_string = f"{logs_region_name}/{date}"
    destination = f'{destination}/{date.replace("/","_")}' 
    files = s3_client.list_objects(Bucket=bucket_name)['Contents']
    files_to_download = [file['Key'] for file in files if check_string in file.get('Key', '')]
    create_directory(destination)
    records = []
    for file in files_to_download:
        file_name = f"{destination}/{file.split('/')[-1]}"
        s3_client.download_file(bucket_name, file, file_name) 

        with gzip.open(file_name) as json_file:
            data = json.load(json_file) 
            records += data.get('Records', [])
        
        os.remove(file_name)
    
    with open(f'{destination}/logs.json', 'w') as json_file:
        json.dump(records, json_file)
    
    return len(records)

def register_log(destination: str, log: dict):
    print(log)
    service_name = log.get('service_name', '')
    date = datetime.now().strftime('%Y_%d_%m')
    destination = f'{destination}/{service_name}' if service_name \
    else f'{destination}/no_named'
    
    create_directory(destination)
    file_name = f'{destination}/{date}.json'
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            logs = json.load(file)
    else: logs = []
    logs.append(log)
    with open(file_name, 'w') as file:
        json.dump(logs, file)

def convert_logs(destination: str, date: str = ''):
    destination = f'{destination}/{date.replace("/","_")}' 

