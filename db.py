from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.environ['DB_URL'])



def db_connect():
    global client
    # client.db.auth.drop()
    return client.db.auth


def bookmark_db_connect():
    global client
    return client.db.bookmarks


def recent_searches_connect():
    global client
    return client.db.recentsearch

