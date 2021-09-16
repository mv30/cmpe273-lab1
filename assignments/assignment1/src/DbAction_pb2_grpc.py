# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import DbAction_pb2 as DbAction__pb2


class ReplicationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.propogate = channel.stream_unary(
                '/Replication/propogate',
                request_serializer=DbAction__pb2.DbAction.SerializeToString,
                response_deserializer=DbAction__pb2.ExecutionResponse.FromString,
                )


class ReplicationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def propogate(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReplicationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'propogate': grpc.stream_unary_rpc_method_handler(
                    servicer.propogate,
                    request_deserializer=DbAction__pb2.DbAction.FromString,
                    response_serializer=DbAction__pb2.ExecutionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Replication', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Replication(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def propogate(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/Replication/propogate',
            DbAction__pb2.DbAction.SerializeToString,
            DbAction__pb2.ExecutionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)