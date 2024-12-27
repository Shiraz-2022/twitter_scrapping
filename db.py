from pymongo import MongoClient
import os

def get_mongo_client():
    client = MongoClient(os.environ.get("MONGO_URL"))
    print("client",client)
    return client

def get_mongo_db(client,db_name="twitter_trends"):
    print("db_name",client[db_name])
    return client[db_name]

def get_trends_collection(db):
    print("trends",db["trends"])
    return db["trends"]