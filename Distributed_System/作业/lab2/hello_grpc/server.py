from concurrent import futures #创建线程池执行器
import grpc
from pb.hello_pb2_grpc import HelloServicer #导入服务接口 #导入模块要和该文件在同一个目录下
from pb.hello_pb2 import HelloRequest,HelloResponse
from pb import hello_pb2_grpc

class HelloServer(HelloServicer):
    def SayHello(self, request, context):
        name=request.name
        return HelloResponse(response="hello: {}".format(name))
    

def serve():
    port="40000" #监视端口为40000
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=10))#实例化易感染具有10个工作线程的线程池执行器
    hello_pb2_grpc.add_HelloServicer_to_server(HelloServer(),server)#将Helloerver实例添加到gRPC服务器，为了处理定义的RPC调用
    server.add_insecure_port('[::]:' + port)  # 为服务器添加一个不安全的监听端口。[::] 表示服务器将监听所有可用的网络接口
    server.start() #启动服务器，使其开始监听请求
    print("Server started, listening on " + port) 
    server.wait_for_termination() #使服务器保持运行状态，直到它被明确地关闭或终止

if __name__ == '__main__':  
    serve()

