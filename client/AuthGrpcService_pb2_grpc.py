# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import AuthGrpcService_pb2 as AuthGrpcService__pb2


class AuthServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUser = channel.unary_unary(
                '/AuthService.AuthService/GetUser',
                request_serializer=AuthGrpcService__pb2.AuthTokenRequest.SerializeToString,
                response_deserializer=AuthGrpcService__pb2.GetUserReply.FromString,
                )
        self.ValidToken = channel.unary_unary(
                '/AuthService.AuthService/ValidToken',
                request_serializer=AuthGrpcService__pb2.AuthTokenRequest.SerializeToString,
                response_deserializer=AuthGrpcService__pb2.ValidTokenReply.FromString,
                )
        self.GetClaims = channel.unary_unary(
                '/AuthService.AuthService/GetClaims',
                request_serializer=AuthGrpcService__pb2.AuthTokenRequest.SerializeToString,
                response_deserializer=AuthGrpcService__pb2.ClaimArrayReply.FromString,
                )
        self.IsAuthorize = channel.unary_unary(
                '/AuthService.AuthService/IsAuthorize',
                request_serializer=AuthGrpcService__pb2.IsAuthorizeRequest.SerializeToString,
                response_deserializer=AuthGrpcService__pb2.IsAuthorizeReply.FromString,
                )
        self.IsAuthorizedToken = channel.unary_unary(
                '/AuthService.AuthService/IsAuthorizedToken',
                request_serializer=AuthGrpcService__pb2.IsAuthorizedTokenRequest.SerializeToString,
                response_deserializer=AuthGrpcService__pb2.IsAuthorizedTokenReply.FromString,
                )


class AuthServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetClaims(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsAuthorize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsAuthorizedToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUser,
                    request_deserializer=AuthGrpcService__pb2.AuthTokenRequest.FromString,
                    response_serializer=AuthGrpcService__pb2.GetUserReply.SerializeToString,
            ),
            'ValidToken': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidToken,
                    request_deserializer=AuthGrpcService__pb2.AuthTokenRequest.FromString,
                    response_serializer=AuthGrpcService__pb2.ValidTokenReply.SerializeToString,
            ),
            'GetClaims': grpc.unary_unary_rpc_method_handler(
                    servicer.GetClaims,
                    request_deserializer=AuthGrpcService__pb2.AuthTokenRequest.FromString,
                    response_serializer=AuthGrpcService__pb2.ClaimArrayReply.SerializeToString,
            ),
            'IsAuthorize': grpc.unary_unary_rpc_method_handler(
                    servicer.IsAuthorize,
                    request_deserializer=AuthGrpcService__pb2.IsAuthorizeRequest.FromString,
                    response_serializer=AuthGrpcService__pb2.IsAuthorizeReply.SerializeToString,
            ),
            'IsAuthorizedToken': grpc.unary_unary_rpc_method_handler(
                    servicer.IsAuthorizedToken,
                    request_deserializer=AuthGrpcService__pb2.IsAuthorizedTokenRequest.FromString,
                    response_serializer=AuthGrpcService__pb2.IsAuthorizedTokenReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AuthService.AuthService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AuthService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AuthService.AuthService/GetUser',
            AuthGrpcService__pb2.AuthTokenRequest.SerializeToString,
            AuthGrpcService__pb2.GetUserReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ValidToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AuthService.AuthService/ValidToken',
            AuthGrpcService__pb2.AuthTokenRequest.SerializeToString,
            AuthGrpcService__pb2.ValidTokenReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetClaims(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AuthService.AuthService/GetClaims',
            AuthGrpcService__pb2.AuthTokenRequest.SerializeToString,
            AuthGrpcService__pb2.ClaimArrayReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IsAuthorize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AuthService.AuthService/IsAuthorize',
            AuthGrpcService__pb2.IsAuthorizeRequest.SerializeToString,
            AuthGrpcService__pb2.IsAuthorizeReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IsAuthorizedToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AuthService.AuthService/IsAuthorizedToken',
            AuthGrpcService__pb2.IsAuthorizedTokenRequest.SerializeToString,
            AuthGrpcService__pb2.IsAuthorizedTokenReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
