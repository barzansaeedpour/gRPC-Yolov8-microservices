import AuthGrpcService_pb2
import AuthGrpcService_pb2_grpc

import grpc

def token_validation(token, claim_list):
    response = []
    with grpc.insecure_channel("http://authentication:81") as channel:
        stub = AuthGrpcService_pb2_grpc.AuthServiceStub(channel)
        response = stub.IsAuthorizedToken(AuthGrpcService_pb2.IsAuthorizedTokenRequest())
    print(response)


if __name__ == '__main__':
    token_validation(
        token = "eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwidHlwIjoiSldUIiwiY3R5IjoiSldUIn0.XjFdnb3tzj7Fv9ICauVnbhhy0L06Ip3cb1F5f1ZPeYAS_C-J_DOQbg._onjGnpvo0OiFdTY1AlX2Q.mp0HfI-1IU7GZXytUcXMJjoRXPPlWMsvzePAkyMyzsUE31XZYdf0VklM9Ijyon3_FNEKHCbWCPLQHSzSBLUqIvPAVMH2cqYZgdTWwS14zrMunnALmGzXb9mqpGOxbC3kyIdrc3CRzPjVWkXJRUz8RvVHJnlo56kk_2UiYipsvFHK62EHVk6iadAk5KKgoHVVnNHR-DVtgdOCQSDRS5FLuvHuWlzYmNbR2FmJdSuUlL9IrgoaBsVEt4q_LQkRA6Io_kxJxWKOA_CyGQupWiJ7P_XN4ytbSdN2xC1hJbp-2UjBNcFfryrvqcUkmiQJxkh2UYSXHvkb1Eueu66uTusfQqYl7MzM8hO012Yn5CJnOLRdFyOyI-qb1ylf6qaZDfNdvmYlAZ8X0nSseWDem9U_SRazxHPHmkFkTmntK2W_D5lbZ5FGgX0q9hN30v4peizLnd-kDy0IWn0OUJLc1RDLz2pHE3FpuXC950bh4aQZXi5yD0ZO_3uqyIpBIZrZUsVASBUnsf3SjO7PZqQJlcKhYj6twqbXNBD7Z9tqtSD0-gYjB1Zu8t4ALc4PWpmL8ygY.gx_Xw6dFRCS7humME5JIAg",
        claim_list = 'camera_webapp/camera/post',
    )

