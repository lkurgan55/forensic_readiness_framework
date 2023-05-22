import boto3
import json
import pandas as pd

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
    """
    Зчитує JSON-файл за вказаним шляхом та повертає його в форматі словника.

    :param file_path: Шлях до JSON-файлу.
    :return: Словник, що містить дані з JSON-файлу.
    """
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        print(f"Сталася помилка під час читання JSON-файлу: {e}")
        return None

def extract_keys(dictionary, keys):
    """
    Витягує значення зі словника за вказаними ключами.

    :param dictionary: Словник, з якого потрібно витягти значення.
    :param keys: Список ключів, які потрібно витягнути.
    :return: Словник, що містить витягнуті значення за ключами.
    """
    extracted_dict = {}

    for key in keys:
        if key in dictionary:
            extracted_dict[key] = dictionary[key]

    return extracted_dict

def save_dict_as_json(dictionary, file_path):
    """
    Зберігає словник у форматі JSON у вказаний файл.

    :param dictionary: Словник, який потрібно зберегти.
    :param file_path: Шлях до файлу для збереження JSON.
    """
    try:
        with open(file_path, 'w') as json_file:
            json.dump(dictionary, json_file, indent=4)
        print(f"Словник успішно збережено як JSON у файлі: {file_path}")
    except Exception as e:
        print(f"Сталася помилка під час збереження JSON-файлу: {e}")

