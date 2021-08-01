from dataclasses import dataclass
from discord.errors import ClientException
from config.py import db_password

from pymongo.mongo_client import MongoClient


@dataclass
class DB():
    client: MongoClient

    def __init__(self):
        CONNECTION_STRING = f'mongodb+srv://dbAdmin:{db_password}@beepodb.gcurw.mongodb.net/BeepoDB?retryWrites=true&w=majority'
        self.client = MongoClient(CONNECTION_STRING)

    def getDB(self, db_name: str):
        return self.client[db_name]

    def getCollection(self, db_name: str, collection_name: str):
        return self.client[db_name][collection_name]
