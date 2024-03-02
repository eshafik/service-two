from typing import List

from django.conf import settings
from opentelemetry import trace
from pymongo import MongoClient


def get_mongo_client():
    client = MongoClient(f'mongodb://{settings.MONGODB_HOST}:27017/')  # Connect to your MongoDB server
    return client


def get_database(db_name="post_seen"):
    client = get_mongo_client()
    db = client[db_name]
    return db


def insert_data(data: List[dict]):
    db = get_database()  # Use the default database or specify one
    collection = db.myCollection  # Specify your collection name

    result = collection.insert_many(data)
    print('mongo insertion result', result)
    return
