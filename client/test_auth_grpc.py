import claims_pb2
import claims_pb2_grpc
import grpc

def get_claims():
    response = []
    with grpc.insecure_channel("localhost:81") as channel:
        stub = claims_pb2_grpc.ClaimsStub(channel)
        response = stub.GetClaims(claims_pb2.GetClaimsRequest())
    print(response.claims)


if __name__ == '__main__':
    get_claims()








