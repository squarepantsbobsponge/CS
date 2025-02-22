#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <winsock2.h>
int main(int argc,char *argv[]){
    //char *host="127.0.0.1";
    WSADATA wsadata;
    SOCKET sockfd;
    struct sockaddr_in client;
    struct sockaddr_in server_addr;
    char buffer[4096];
    if (WSAStartup(MAKEWORD(2, 2), &wsadata) != 0) {  
       // errexit("WSAStartup failed\n");  
    }  
    //创造套接字：UDP
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
     if (sockfd == INVALID_SOCKET) {
        fprintf(stderr, "Error creating socket\n");
        WSACleanup();
        exit(1);
    }   
    //绑定端口
    memset(&client, 0, sizeof(client)); 
    client.sin_family=AF_INET;
    client.sin_addr.s_addr=INADDR_ANY;//本地任意地址 ??
    client.sin_port=htons(9999);
    if(bind(sockfd,(struct sockaddr *)& client, sizeof(client))<0){
        perror("bind failed");  
        close(sockfd);  
        exit(EXIT_FAILURE);  
    }
   //设置服务器相关信息//好像不需要指定，这个调用recvform会获取的
    // memset(&server_addr, 0, sizeof(server_addr));  
    // server_addr.sin_family = AF_INET;  
    // server_addr.sin_port = htons(12346);  // 假设服务器在12346端口上发送数据  
    // server_addr.sin_addr.s_addr = inet_addr(host);//发送给本机就是特殊的addr
 
    ssize_t num_bytes; //如果正常接收是非负数，否则是-1

  //发送方地址长度
  int addr_len=sizeof(server_addr);
  //循环接收来自服务器的数据
  int count=0;//计算丢包

  while(1){
    memset(buffer,0,4096);//清空缓冲区
    num_bytes=recvfrom(sockfd,buffer,4096,0, (struct sockaddr *)&server_addr, &addr_len);
    printf("the number of lost packets: %d\n",count);
    if (num_bytes < 0) {  
            count++;

        }
        //打印  
        buffer[num_bytes] = '\0';  // 确保字符串以null结尾（尽管UDP数据包不保证是字符串）  
        printf("Data: %.*s\n", (int)num_bytes, buffer);  // 使用%.*s来限制打印的字节数  

  }
      close(sockfd); 
      return 0;
}