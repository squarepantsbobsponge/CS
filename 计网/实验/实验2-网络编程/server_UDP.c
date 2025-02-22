#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <winsock2.h>
int main(){
    char *client="172.26.105.168";
    SOCKET sockfd;
    struct sockaddr_in client_addr;
    char message[] = "Hello, UDP client!"; 
    int num_sent;
    WSADATA wsadata;

    //
        if (WSAStartup(MAKEWORD(2, 2), &wsadata) != 0) {  
       // errexit("WSAStartup failed\n");  
    }  
    //创建套接字
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd == INVALID_SOCKET) {
        fprintf(stderr, "Error creating socket\n");
        WSACleanup();
        exit(1);
    } 
    //客户信息
        memset(&client_addr, 0, sizeof(client_addr));  
    client_addr.sin_family = AF_INET;  
    client_addr.sin_port = htons(9999);
    client_addr.sin_addr.s_addr = inet_addr(client);//发送给本机就是特殊的addr  
    
    int i=100;
    while (i>0) {  
        // 更新消息内容  
        i--;  
  
        // 发送消息到客户端  
        num_sent = sendto(sockfd, message, strlen(message), 0, (const struct sockaddr *)&client_addr, sizeof(client_addr));  
        if (num_sent < 0) {  
            perror("sendto failed");   
        } else {  
            printf("Message sent: %s\n", message);  
        }  
  
        // 等待一段时间再发送下一条消息  
        sleep(0.1);  
    }
      
      close(sockfd); 
      return 0;  
}