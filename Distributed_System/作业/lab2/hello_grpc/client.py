import grpc
from pb.hello_pb2_grpc import HelloStub #客户端存根，用于调用gpc服务器上的方法
from pb.hello_pb2 import HelloRequest

def run():
    #创建到服务器的安全通道
    with grpc.insecure_channel("localhost:40000") as channel:
        #初始化HelloStub实例
        stub=HelloStub(channel)
        #构造一个消息
        request=HelloRequest(name="dxq")
        #调用存根的sayHello,会阻塞知道服务器返回响应
        response=stub.SayHello(request)

        print(response.response)

if __name__ == '__main__':  
    # 当这个脚本作为主程序运行时，调用run函数。  
    run()