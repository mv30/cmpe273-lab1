
import json
from pymongo import MongoClient
import DbAction_pb2
import ConfigUtils
import datetime

class MongoService:

    connection_string = None
    mongo_client = None

    def __init__(self):
        self.connection_string = ConfigUtils.ConfigService.get_mongo_connection_string()
        self.mongo_client = MongoClient(self.connection_string)
        pass

    def parse_values( self, type_arr, values_arr):
        res = []
        for i in range(len(type_arr)):
            if (type_arr[i] == 'integer') or ("character" in type_arr[i]):
                res.append(values_arr[i])
            elif ("timestamp" in type_arr[i]):
                date_string = values_arr[i]
                mill_start = date_string.find(".")
                time_stamp = None
                if "-" in date_string[mill_start:]:
                    mill_end = date_string.rfind("-")
                    date_string = date_string[:mill_end]
                time_stamp = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
                time_stamp = time_stamp
                res.append(time_stamp)
            else:
                raise NotImplementedError(' parising for datatype not implemented!')
        return res

    def performInsertOperation(self, db_action: DbAction_pb2.DbAction):
        table_config = ConfigUtils.ConfigService.get_table_config(db_action.table_name)
        col_values = self.parse_values(db_action.col_types, json.loads(db_action.values_json)) 
        object_to_create = ConfigUtils.ConfigService.get_json_object( table_config, db_action.col_names, col_values)
        res = self.mongo_client[table_config.mongo_db_name][table_config.mongo_collection_name].insert_one(object_to_create)
        print(res)
        return res

    def performUpdateOperation(self, db_action: DbAction_pb2.DbAction):
        table_config = ConfigUtils.ConfigService.get_table_config(db_action.table_name)
        key_col_values = self.parse_values(db_action.key_col_types, json.loads(db_action.key_values_json))
        object_to_find = ConfigUtils.ConfigService.get_json_object( table_config, db_action.key_col_names, key_col_values)
        col_values = self.parse_values(db_action.col_types, json.loads(db_action.values_json)) 
        object_to_update = ConfigUtils.ConfigService.get_json_object( table_config, db_action.col_names, col_values)
        res = self.mongo_client[table_config.mongo_db_name][table_config.mongo_collection_name].update_one(object_to_find,{ '$set': object_to_update  })
        print(res)
        return res

    def performDeleteOperation(self, db_action: DbAction_pb2.DbAction):
        table_config = ConfigUtils.ConfigService.get_table_config(db_action.table_name)
        key_col_values = self.parse_values(db_action.key_col_types, json.loads(db_action.key_values_json))
        object_to_find = ConfigUtils.ConfigService.get_json_object( table_config, db_action.key_col_names, key_col_values)
        res = self.mongo_client[table_config.mongo_db_name][table_config.mongo_collection_name].delete_one(object_to_find)
        print(res)
        return res

    def update( self, db_action: DbAction_pb2.DbAction):
        if db_action.type == 'INSERT':
            self.performInsertOperation(db_action)
            pass
        elif db_action.type == 'UPDATE':
            self.performUpdateOperation(db_action)
            pass
        elif db_action.type == 'DELETE':
            self.performDeleteOperation(db_action)
        else:
            raise NotImplementedError(' Db action not implemented!')
        pass

