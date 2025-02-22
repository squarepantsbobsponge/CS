import grpc
import grpc._grpcio_metadata
from rpc import pubsub_pb2
from rpc import pubsub_pb2_grpc
import time
def run():
     with grpc.insecure_channel('localhost:40000') as channel:
          #创建存根
          stub=pubsub_pb2_grpc.SubServiceStub(channel)
          request=pubsub_pb2.SubscribeRequest(topic_name="time",id="123")
          response=stub.Subscribe(request)
          if(response.flag==1):
              print("sub succeed")
          else:
              print("fail")
          
          request2=pubsub_pb2.request_id(id="123")
          for message in stub.Message_Stream(request2):
            print(f"Received message for topic '{message.topic}':")
            print(f"  Content: {message.content}")
            print(f"  Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(message.timestamp / 1000))}")  # 将时间戳转换为可读格式  
            
  
if __name__ == '__main__':  
    run()



