
import json
from mongopy import MongoClient

class MongoService:

    connection_string = None
    mongo_client = None

    def __init__(self):
        self.connection_string = 'mongodb://localhost:27017'
        self.mongo_client = MongoClient(self.connection_string)
        # with open
        pass

