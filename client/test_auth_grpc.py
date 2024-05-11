import auth_pb2
import auth_pb2_grpc
import grpc
from pprint import pprint

def get_claims():
    print("*****************************")
    with grpc.insecure_channel('0.0.0.0:81') as channel:
        print("#################################")
        stub = auth_pb2_grpc.AuthStub(channel)
        print("///////////////////////")
        response = stub.GetClaims(auth_pb2.GetClaimsRequest())
        print(response)
            # print("1111111111111111111111111")
            # print(response)


if __name__ == '__main__':
    get_claims()








