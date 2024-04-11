#include <stdio.h>
#include <stdlib.h>
#include<fcntl.h>
int main(){
    int fd=open("./A_pipe.txt",O_RDONLY);//只读方式打开管道
    if(fd==-1){
        perror("open");
        return -1;
    }
    //从管道中读取数据
    char buffer[1024];
    int n=read(fd,buffer,sizeof(buffer));
    if(n==-1){
        perror("read");
        return -1;
    }
    //打印数据
    printf("%s\n",buffer);
    return 0;
}