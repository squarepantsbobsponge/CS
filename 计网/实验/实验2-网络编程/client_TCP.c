#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <winsock2.h>
int main(int argc, char *argv[]) {  
    /* usage: TCPdaytime [host [port]] */  
    /* host can be an IP address or domain name, port can be the port number or service name */  
    char *host = "172.26.105.168"; /* host to use if none supplied */  //192.168.20.10
    char *service = ""; /* default service port */   
    WSADATA wsadata; 
    if (WSAStartup(MAKEWORD(2, 2), &wsadata) != 0) {  
       // errexit("WSAStartup failed\n");  
    }  

   //创造一个套接字  
       SOCKET sockfd;
       sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == INVALID_SOCKET) {
        fprintf(stderr, "Error creating socket\n");
        WSACleanup();
        exit(1);
    }

    char *host = "172.26.105.168"; /* host to use if none supplied */  //192.168.20.10 
    struct sockaddr_in server;
   //定义发送到的服务器的信息
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr(host);//发送给本机就是特殊的addr
    server.sin_port = htons(9999); //不是随机的，是监听到的端口
// 向服务器发送连接请求
if (connect(sockfd, (struct sockaddr *)&server, sizeof(server)) != 0) {
    fprintf(stderr, "Error connecting to server\n");
    closesocket(sockfd);
    WSACleanup();
    exit(1);
}

// Send "123"
int i=10;
const char *data1 = "123";
 while(i>0){
 i--;
send(sockfd, data1, strlen(data1), 0);
 sleep(1);
 }

printf("send successfully");
// Close the socket and cleanup
closesocket(sockfd);
WSACleanup();

return 0;

}