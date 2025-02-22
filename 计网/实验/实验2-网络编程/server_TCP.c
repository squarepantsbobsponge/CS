#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <winsock2.h>

#define QLEN 5 
int passiveTCP(int qlen) {
    int server_socket;
    struct sockaddr_in server_addr;
    // 创建 TCP 套接字
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    // 初始化服务器地址结构
    server_addr.sin_family = AF_INET; //指定IPV4地址簇
    server_addr.sin_addr.s_addr = INADDR_ANY; //监听来自任何网络接口的连接请求
    server_addr.sin_port = htons(9999);//绑定的服务器端口
    // 绑定套接字到服务器地址
    bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr));
    // 启动监听
    listen(server_socket, qlen); // 设置监听队列的最大长度
    return server_socket;
}

int main(int argc, char *argv[]) {
    
    struct sockaddr_in fsin; //客户端地址
    SOCKET msock,ssock;//一个监听套接字，一个连接套接字
    int alen;//地址长度
    WSADATA wsadata;//SCOKET 的版本信息
  
    // 初始化Winsock  
    if (WSAStartup(MAKEWORD(2, 2), &wsadata) != 0) { // 注意：使用2.2版本而不是单独的MAKEWORD  
       // errexit("WSAStartup failed\n");  
        exit(1); // 退出程序   //MAKEWORD是要求启动版本号，wsdata是接收返回信息
    }  
    //创建被动套接字,监听来自客户端的请求
    msock = passiveTCP(QLEN);  
    if (msock == INVALID_SOCKET) {  
        exit(1); // 退出程序  
    }  

    
    
    char buffer[1024]; // 用于存储接收的数据
    while(1){ //外层循环监听链接
        alen=sizeof(struct sockaddr); //accept 函数会接受这个连接，创建一个新的套接字 ssock 用于与客户端通信，并将客户端的地址信息存储在 fsin 中。alen 变量用于指示 fsin 结构体的大小。
        ssock=accept(msock,(struct sockaddr*)&fsin,&alen);    
        if (ssock == INVALID_SOCKET) {  
           // errexit("accept failed\n");  
            continue; // 或者选择退出循环  
        }
      
    while(1){ //内层循环接连接的数据
    int bytes_received = recv(ssock, buffer, sizeof(buffer), 0); // 接收数据包
    if (bytes_received == SOCKET_ERROR) {
        break;
    }
    if (bytes_received == 0) {
        break;
    }
    buffer[bytes_received]='\0';
    // 打印接收到的数据
    printf("Received data from client: %s\n", buffer);

    // 清空接收缓冲区
    memset(buffer, 0, sizeof(buffer));
    }    
    

          // 关闭套接字
        close(ssock);


    }



}
