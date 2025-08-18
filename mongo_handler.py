"""
@module
"""
import pymongo
from loggers.loggings import logger



class MongoConnection:
    """
    A class to handle connecting to MongoDB.
    """
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["gryf"]
        self.collections = self.db.list_collection_names()
        self.texts_collection = self.db['texts']

    def insert(self, json: dict|str):
        """

        :param json:
        :return:
        """
        self.texts_collection.insert_one(json)
        logger.info('Json object inserted into MongoDB')

if __name__ == '__main__':
    MC = MongoConnection()
