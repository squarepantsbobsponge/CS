#include<sys/types.h>
#include<stdio.h>
#include<string.h>
#include<unistd.h>
#define BUFFER_SIZE 25
#define READ_END 0
#define WRITE_END 1

int main(void){
    char write_msg[BUFFER_SIZE]="Greetings";
    char read_msg[BUFFER_SIZE];
    int fd[2];//代表管道两端，0是读端，1是写端
    pid_t pid;
    //创造pipe
    if(pipe(fd)==-1){//失败打印相关信息
        fprintf(stderr,"Pipe failed");
        return 1;
    }
    //创建子进程
    pid=fork();
    if(pid<0){//创建失败
        fprintf(stderr, "Fork Failed");
        return 1;
    }
   if(pid>0){//父进程
    close(fd[READ_END]);//关闭读端
    write(fd[WRITE_END],write_msg,strlen(write_msg)+1);//写东西到管道里面
    close(fd[WRITE_END]);//关闭写端
   }
   else{//子进程
    close(fd[WRITE_END]);
    read(fd[READ_END],read_msg,BUFFER_SIZE);
    printf("read %s",read_msg);
    close(fd[READ_END]);
   }
   return 0;
}