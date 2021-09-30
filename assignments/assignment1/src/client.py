from concurrent.futures import thread
import time
import os
import grpc
import DbAction_pb2_grpc
import DbAction_pb2
import json
import constants.Wal_Constants
import threading
from grpc_requests import StubClient

CHANGE_KEY = constants.Wal_Constants.CHANGE_KEY
QUERY_TYPE_KEY = constants.Wal_Constants.QUERY_TYPE_KEY
TABLE_NAME_KEY = constants.Wal_Constants.TABLE_NAME_KEY
COLUMN_NAMES_KEY = constants.Wal_Constants.COLUMN_NAMES_KEY
COLUMN_TYPES_KEY = constants.Wal_Constants.COLUMN_TYPES_KEY
COLUMN_VALUES_KEY = constants.Wal_Constants.COLUMN_VALUES_KEY
OLD_SET_KEY = constants.Wal_Constants.OLD_SET_KEY
OLD_SET_NAMES_KEY = constants.Wal_Constants.OLD_SET_NAMES_KEY
OLD_SET_TYPES_KEY = constants.Wal_Constants.OLD_SET_TYPES_KEY
OLD_SET_VALUES_KEY = constants.Wal_Constants.OLD_SET_VALUES_KEY

SLEEP_TIME_OUT_IN_SECONDS = 1.5
records_processed_count = 0

def parse_Db_Actions( json_string) -> list[DbAction_pb2.DbAction]:

    db_changes : list[DbAction_pb2.DbAction] = []
    json_dict = json.loads(json_string)
    changes_list = json_dict[CHANGE_KEY]
    
    for curr_change in changes_list:
    
        action = curr_change[QUERY_TYPE_KEY].upper()
        table = curr_change[TABLE_NAME_KEY]
        
        column_names = None
        column_types = None
        column_values= None
        if action == 'INSERT' or action == 'UPDATE':
            column_names = curr_change[COLUMN_NAMES_KEY]
            column_types = curr_change[COLUMN_TYPES_KEY]
            column_values = curr_change[COLUMN_VALUES_KEY]
        
        key_column_names = None
        key_column_types = None
        key_column_values = None
        if action == 'UPDATE' or action == 'DELETE':
            key_column_names = curr_change[OLD_SET_KEY][OLD_SET_NAMES_KEY]
            key_column_types = curr_change[OLD_SET_KEY][OLD_SET_TYPES_KEY]
            key_column_values = curr_change[OLD_SET_KEY][OLD_SET_VALUES_KEY]

        curr_db_action: DbAction_pb2.DbAction = DbAction_pb2.DbAction(type=action,table_name=table,col_names=column_names,col_types=column_types,values_json=json.dumps(column_values),key_col_names=key_column_names,key_col_types=key_column_types,key_values_json=json.dumps(key_column_values))
        db_changes.append(curr_db_action)
    
    return db_changes

def get_changes()-> list[DbAction_pb2.DbAction]:
    
    db_changes : list[DbAction_pb2.DbAction] = []
    json_file = open('./logs/output.txt', 'r', encoding="ascii")
    string_content = json_file.read()
    json_file.close()
    
    while True:
        
        end_id = string_content.rfind('}')
        
        if end_id == -1:
            break

        start_id = string_content.rfind('"change":')
        start_id = string_content.rfind('{',0,start_id)
        json_string  = string_content[start_id:]
        string_content = string_content[:start_id]

        temp_db_actions : list[DbAction_pb2.DbAction] = parse_Db_Actions(json_string)
        temp_db_actions.reverse()
        for temp_db_action in temp_db_actions:
            db_changes.append(temp_db_action)
    
    db_changes.reverse()
    db_changes_pending = db_changes[records_processed_count:]
    return db_changes_pending

def get_iterator( db_changes):
    for i in range(len(db_changes)):
        yield db_changes[i]

def check_for_changes():
    
    global records_processed_count
    db_changes = get_changes()

    print(' ####### changes to propogate ############ ')
    print(db_changes)
    
    # --- without grpc_requests ---
    
    # channel = grpc.insecure_channel('localhost:50085')
    # stub = DbAction_pb2_grpc.ReplicationStub(channel)
    # iterator = get_iterator( db_changes)
    # res = stub.propogate(iterator)
    
    # --- with grpc_requests ---

    service_descriptor = DbAction_pb2.DESCRIPTOR.services_by_name['Replication']
    client = StubClient.get_by_endpoint('localhost:50085',service_descriptors=[service_descriptor,])
    replicator_service = client.service('Replication')
    replicator_service.propogate(db_changes)

    records_processed_count = records_processed_count + len(db_changes)

def run():
    while True:
        check_for_changes()
        time.sleep(SLEEP_TIME_OUT_IN_SECONDS)

def initialise():
    os.system('pg_recvlogical -d college --slot test_slot --create-slot -P wal2json')
    os.system('pg_recvlogical -d college --slot test_slot --start -o pretty-print=1 -f - >> ./logs/output.txt')
    os.wait()

if __name__ == '__main__':
    thread_1 = threading.Thread(target=run)
    thread_2 = threading.Thread(target=initialise)
    thread_1.start()
    thread_2.start()
