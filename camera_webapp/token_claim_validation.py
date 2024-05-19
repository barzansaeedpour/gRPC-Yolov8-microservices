import AuthGrpcService_pb2
import AuthGrpcService_pb2_grpc

import grpc

def token_claim_validation(token, claim):
    response = []
    with grpc.insecure_channel("localhost:6985") as channel:
        stub = AuthGrpcService_pb2_grpc.AuthServiceStub(channel)
        try:
            response = stub.IsAuthorizedToken(AuthGrpcService_pb2.IsAuthorizedTokenRequest(Token=token,Claim=claim))
            return response.Authorized
        except:
            return False

