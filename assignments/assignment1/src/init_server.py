
from pymongo import MongoClient

import grpc
from concurrent import futures

import DbAction_pb2
import DbAction_pb2_grpc

class CustomReplicationServicer(DbAction_pb2_grpc.ReplicationServicer):

    def propogate(self, request_iterator, context):
        print(' started proceesing ')
        for db_action in request_iterator:
            print(db_action)
        response = DbAction_pb2.ExecutionResponse(status='COMPLETED')
        print(' completed proceesing ')
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    DbAction_pb2_grpc.add_ReplicationServicer_to_server(CustomReplicationServicer(), server)
    server.add_insecure_port('[::]:50085')
    server.start()
    print(' server up and running ')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


# mongo_client = MongoClient('mongodb://localhost:27017')
# db = mongo_client.my_db
# db.first_collection.insert_one({ 'name': 'Mayank', 'age': 23 })


