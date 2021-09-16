
import time
import grpc
import DbAction_pb2_grpc
import DbAction_pb2
import json
from constants.Wal_Constants import CHANGE_KEY, QUERY_TYPE_KEY, TABLE_NAME_KEY, COLUMN_NAMES_KEY, COLUMN_TYPES_KEY, COLUMN_VALUES_KEY

SLEEP_TIME_OUT_IN_SECONDS = 1.5
records_processed_count = 0

def parse_Db_Actions( json_string) -> list[DbAction_pb2.DbAction]:

    db_changes : list[DbAction_pb2.DbAction] = []
    json_dict = json.loads(json_string)
    changes_list = json_dict[CHANGE_KEY]
    
    for curr_change in changes_list:
    
        action = curr_change[QUERY_TYPE_KEY].upper()
        table = curr_change[TABLE_NAME_KEY]
        column_names = curr_change[COLUMN_NAMES_KEY]
        column_values = curr_change[COLUMN_VALUES_KEY]

        curr_db_action: DbAction_pb2.DbAction = DbAction_pb2.DbAction(type=action,table_name=table,col_names=column_names,values_json=json.dumps(column_values))
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
    channel = grpc.insecure_channel('localhost:50085')
    stub = DbAction_pb2_grpc.ReplicationStub(channel)
    db_changes = get_changes()
    print(' ####### changes to propogate ############ ')
    print(db_changes)
    iterator = get_iterator( db_changes)
    res = stub.propogate(iterator)
    records_processed_count = records_processed_count + len(db_changes)

def run():
    while True:
        check_for_changes()
        time.sleep(SLEEP_TIME_OUT_IN_SECONDS)
        # break

if __name__ == '__main__':
    run()