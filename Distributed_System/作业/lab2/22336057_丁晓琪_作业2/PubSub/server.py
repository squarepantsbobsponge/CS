import grpc
import time
import threading
from concurrent import futures
from rpc.pubsub_pb2_grpc import SubService
from rpc import pubsub_pb2,pubsub_pb2_grpc

class SubService_Server(SubService):
    def __init__(self) -> None:
        self.subscribes_topic={} 
        self.message_queue={}
        self.ttl=120#消息存储时间，初始化为一分钟
        self.lock=threading.Lock() 

        self.message_queue["time"]=[] #(ts,mes)
        self.message_queue["count"]=[] #计数器
        self.generator_lock=threading.Lock() 
        # 创建一个线程来定期生成消息  
        self.message_generator_thread_time = threading.Thread(target=self.generate_messages_time)  
        self.message_generator_thread_time.daemon = True  # 确保线程在程序退出时自动终止  
        self.message_generator_thread_time.start()  

        self.message_generator_thread_count = threading.Thread(target=self.generate_messages_count)  
        self.message_generator_thread_count.daemon = True  # 确保线程在程序退出时自动终止  
        self.message_generator_thread_count.start()  
        
  
    def generate_messages_time(self):  
        # 每5秒向"time"主题生成一条消息 
        i=8
        while (i>0):  
            with self.generator_lock: 
                i-=1
                time.sleep(5)  
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())  
                message = f"Current time is {current_time}"  
                timestamp = int(time.time())   
                self.message_queue["time"].append(( timestamp,message))  
                print("add topic time:",message,timestamp)

    def generate_messages_count(self):  
        #每5秒向"count"主题生成一条消息  
        i=10
        while (i>0):  
            with self.generator_lock: 
                time.sleep(5)  
                current_count = 20-i  
                message = f"Current count is {current_count}"  
                timestamp = int(time.time())   
                self.message_queue["count"].append(( timestamp,message))  
                print("add topic count",message,timestamp)
                i-=1

        
    
    def Subscribe(self,request,context):
        topic_name=request.topic_name
        flag=1
        if topic_name not in self.message_queue: #要订阅的话题没有注册
            flag=0 #返回订阅失败

        custom_id=request.id    
        self.subscribes_topic[custom_id]=topic_name
        #返回
        return pubsub_pb2.SubscribeResponse(flag=flag)
    
    def Message_Stream(self,request,context): 
        #提取客户端信息,查找订阅的信息（假设一次只订一个话题）
        custom_id=request.id    
        topic_name=self.subscribes_topic[custom_id]
        read=-1# 记录客户端读取的服务器的索引

        while(1):
            #发送消息:
            len_message=len(self.message_queue[topic_name])
            with self.lock:
                if self.message_queue[topic_name] and read<(len_message-1):
                    read=len_message-1
                    timestamp,message=self.message_queue[topic_name][len_message-1]
                    #响应消息
                    response=pubsub_pb2.topic_Message(topic=topic_name,content=message,timestamp=timestamp)
                    yield response
            time.sleep(5)
            
            #去除过期消息
            with self.lock:  
                current_time = int(time.time())   
               # 创建一个新列表来存储过滤后的消息  
                filtered_messages = []  
               # 遍历 self.message_queue[topic_name] 中的每个元素  
                for ts, msg in self.message_queue[topic_name]:  
                # 检查消息是否未过期  
                    if current_time - ts <= self.ttl:  
             # 如果未过期，则添加到 filtered_messages 列表中  
                        filtered_messages.append((ts, msg))  
                    else:
                        print("time out!",topic_name,"message pop!",msg)
                        read-=1 #删掉的肯定是read前面的消息，放在队列越前面，存放时间越久，越有可能被删掉，read索引向前
  
            # 用过滤后的消息列表替换原来的列表  
                self.message_queue[topic_name] = filtered_messages     
            

            

def serve():
    port="40000" #监视端口为40000
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=10))#实例化易感染具有10个工作线程的线程池执行器
    pubsub_pb2_grpc.add_SubServiceServicer_to_server(SubService_Server(),server)#将Helloerver实例添加到gRPC服务器，为了处理定义的RPC调用
    server.add_insecure_port('[::]:' + port)  # 为服务器添加一个不安全的监听端口，[::] 表示服务器将监听所有可用的网络接口
    server.start() #启动服务器，开始监听请求
    print("Server started, listening on " + port) 
    server.wait_for_termination() #使服务器保持运行状态，直到它被关闭或终止

if __name__ == '__main__':  
    serve()
