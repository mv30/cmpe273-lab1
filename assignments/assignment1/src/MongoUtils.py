
import json
from pymongo import MongoClient
import DbAction_pb2

class MongoService:

    connection_string = None
    mongo_client = None

    def __init__(self):
        self.connection_string = 'mongodb://localhost:27017'
        self.mongo_client = MongoClient(self.connection_string)
        pass

    def get_json_object( self, table_name, col_name, values_json):
        pass

    def performInsertOperation(self, db_action: DbAction_pb2.DbAction):

        pass

    def update( self, db_action: DbAction_pb2.DbAction):
        if db_action.type == 'INSERT':
            self.performInsertOperation(db_action)
            pass
        elif db_action.type == 'UPDATE':
            pass
        elif db_action.type == 'DELTE':
            pass
        else:
            raise NotImplementedError(' Db action not implemented!')
        pass

