#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/msg.h>
#include<sys/stat.h>
#include<fcntl.h>
#include"msgdata.h"
int main(int argc,char* argv[]){
    key_t key;
    struct stat fileattr;
    char pathname[80];
    int msqid,ret,count=0;
    struct msg_struct data;
    long int msgtype=0;
    if(argc < 2) {
    printf("Usage: ./msgrcv pathname msg_type\n");
    return EXIT_FAILURE;
    }
    //获得key
    strcpy(pathname, argv[1]);
    if(stat(pathname, &fileattr) == -1) {
    ERR_EXIT("shared file object stat error");
    }
    if((key = ftok(pathname, 0x27)) < 0) {
ERR_EXIT("ftok()");
}
    printf("\nIPC key = 0x%x\n", key);
    //获得msqid
    msqid=msgget((key_t)key,0666);
    if(msqid == -1) {
    ERR_EXIT("msgget()");
    }
    //这在干什么，谁传给它的第三个参数
    if(argc<3){
        msgtype=0;
    }
    else{
        msgtype=atol(argv[2]);
        if(msgtype<0) msgtype=0;
    }
    printf("Selected message type = %ld\n", msgtype);
   //接受消息
   while(1){
    ret=msgrcv(msqid,(void*)&data,TEXT_SIZE,msgtype,IPC_NOWAIT);//按照msgtype从队列中接受消息存在data中，如果接受不到，马上返回不阻塞
    if(ret==-1){//没收到
        printf("number of received messages = %d\n", count);
         break;
    }
    printf("%ld %s\n", data.msg_type, data.mtext);
    count++;
   }
  //获取邮箱当前状态并且清扫
  struct  msqid_ds msqattr;
  ret=msgctl(msqid,IPC_STAT,&msqattr);
  printf("number of messages remainding = %ld\n", msqattr.msg_qnum); 
  //删除消息队列
  if(msqattr.msg_qnum == 0) {
    printf("do you want to delete this msg queue?(y/n)");
    if (getchar() == 'y') {
    if(msgctl(msqid, IPC_RMID, 0) == -1)
    perror("msgctl(IPC_RMID)");
    }
}
 system("ipcs -q");
exit(EXIT_SUCCESS);
}