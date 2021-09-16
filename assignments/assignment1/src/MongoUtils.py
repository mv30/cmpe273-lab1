
import json
from pymongo import MongoClient
import DbAction_pb2
import ConfigUtils

class MongoService:

    connection_string = None
    mongo_client = None

    def __init__(self):
        self.connection_string = 'mongodb://localhost:27017'
        self.mongo_client = MongoClient(self.connection_string)
        pass

    def performInsertOperation(self, db_action: DbAction_pb2.DbAction):
        col_values = json.loads(db_action.values_json)
        table_config = ConfigUtils.ConfigService.get_table_config(db_action.table_name)
        object_to_create = ConfigUtils.ConfigService.get_json_object( table_config, db_action.col_names, col_values)
        res = self.mongo_client[table_config.mongo_db_name][table_config.mongo_collection_name].insert_one(object_to_create)
        print(res)
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

