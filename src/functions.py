import boto3
import json
import pandas as pd
import os
import gzip
import json

def download_data_from_s3(bucket_name, object_key, destination_file_path):
    """
    Завантажує об'єкт з Amazon S3 у вказаний шлях файлу.
    
    :param bucket_name: Ім'я сховища (bucket) в Amazon S3.
    :param object_key: Ключ об'єкта (файлу) в Amazon S3.
    :param destination_file_path: Шлях до файлу, куди буде збережений завантажений об'єкт.
    """
    s3_client = boto3.client('s3')
    
    try:
        s3_client.download_file(bucket_name, object_key, destination_file_path)
        print(f"Файл успішно завантажено з S3. Шлях до файлу: {destination_file_path}")
    except Exception as e:
        print(f"Сталася помилка під час завантаження файлу з S3: {e}")

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

def download_logs(bucket_name: str, destination: str, date: str = '', region_name: str = '', **session):
    s3_client = boto3.client('s3', **session)

    date = '2023/05/27'
    region_name = 'us-east-1'

    check_string = f"{region_name}/{date}"
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

def convert_logs(destination: str, date: str = ''):
    destination = f'{destination}/{date.replace("/","_")}' 

