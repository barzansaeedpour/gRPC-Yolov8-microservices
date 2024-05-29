import AuthGrpcService_pb2
import AuthGrpcService_pb2_grpc
from dotenv import find_dotenv, load_dotenv
import grpc
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
authentication_service_address = os.getenv("authentication_service_address")


def token_claim_validation(token, claim):
    response = []
    with grpc.insecure_channel(authentication_service_address) as channel:
        stub = AuthGrpcService_pb2_grpc.AuthServiceStub(channel)
        try:
            response = stub.IsAuthorizedToken(AuthGrpcService_pb2.IsAuthorizedTokenRequest(Token=token,Claim=claim))
            return response.Authorized
        except:
            return False

