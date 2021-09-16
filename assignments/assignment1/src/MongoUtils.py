
import json
from pymongo import MongoClient, mongo_client
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
        table_config = ConfigUtils.ConfigService.get_table_config(db_action.table_name)
        col_values = json.loads(db_action.values_json)
        object_to_create = ConfigUtils.ConfigService.get_json_object( table_config, db_action.col_names, col_values)
        res = self.mongo_client[table_config.mongo_db_name][table_config.mongo_collection_name].insert_one(object_to_create)
        print(res)
        return res

    def performUpdateOperation(self, db_action: DbAction_pb2.DbAction):
        table_config = ConfigUtils.ConfigService.get_table_config(db_action.table_name)
        key_col_values = json.loads(db_action.key_values_json)
        object_to_find = ConfigUtils.ConfigService.get_json_object( table_config, db_action.key_col_names, key_col_values)
        col_values = json.loads(db_action.values_json)
        object_to_update = ConfigUtils.ConfigService.get_json_object( table_config, db_action.col_names, col_values)
        res = self.mongo_client[table_config.mongo_db_name][table_config.mongo_collection_name].update_one(object_to_find,{ '$set': object_to_update  })
        print(res)
        return res

    def update( self, db_action: DbAction_pb2.DbAction):
        if db_action.type == 'INSERT':
            self.performInsertOperation(db_action)
            pass
        elif db_action.type == 'UPDATE':
            self.performUpdateOperation( db_action)
            pass
        elif db_action.type == 'DELTE':
            pass
        else:
            raise NotImplementedError(' Db action not implemented!')
        pass

