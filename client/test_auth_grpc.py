import GetServiceClaims_pb2
import GetServiceClaims_pb2_grpc

import grpc

def get_claims():
    response = []
    with grpc.insecure_channel("localhost:81") as channel:
        stub = GetServiceClaims_pb2_grpc.GetClaimsStub(channel)
        response = stub.GetClaimsList(GetServiceClaims_pb2.EmptyRequest())
    print(response.items)


if __name__ == '__main__':
    get_claims()

