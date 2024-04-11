#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/msg.h>
#include<sys/stat.h>
#include<fcntl.h>
#include"msgdata.h"
int main(int argc,char *argv[]){
    struct msg_struct data;
    long int msg_type;
    char buffer[TEXT_SIZE],pathname[80];
    int msqid,ret,count=0;
    key_t key;
    FILE *fp;
    struct stat fileattr;
    if(argc < 2) {
    printf("Usage: ./a.out pathname\n");
    return EXIT_FAILURE;
    }
    strcpy(pathname,argv[1]);
    //key的依赖文件的打开//要新建一个文件获取！！
    if(stat(pathname, &fileattr) == -1) {
    ret = creat(pathname, O_RDWR);
    if (ret == -1) {    
    ERR_EXIT("creat()");
    }
    printf("shared file object created\n");
    }
    key=ftok(pathname,0x27);
        //检验创建成果
    if(key < 0) {
    ERR_EXIT("ftok()");
    }
    printf("\nIPC key = 0x%x\n", key);
    //创建msgid，邮箱id
    msqid=msgget((key_t)key,0666|IPC_CREAT);
        //检验创造成果
    if(msqid == -1) {
    ERR_EXIT("msgget()");
    }
    //这是在干什么，为什么要打开这个文件？？
    fp = fopen("./mymsgsnd.txt", "rb");
    if(!fp) {
    ERR_EXIT("source data file: ./mymsgsnd.txt fopen()");
    }
   //msgctl函数获取队列属性，并且存储在msqattr（msqid-ds类型）的结构体中
   struct msqid_ds msqattr;
   ret=msgctl(msqid,IPC_STAT,&msqattr);
        //打印相关信息
    printf("number of messages remainded = %ld, empty slots = %ld\n",msqattr.msg_qnum, 16384/TEXT_SIZE-msqattr.msg_qnum);
    printf("Blocking Sending ... \n");
  //发送信息
  while(!feof(fp)){//检查文件指针fp是否到达文件末尾
    ret=fscanf(fp,"%ld %s",&msg_type,buffer); //从fp文件中按格式读取内容到变量中
    if(ret==EOF) break;//ld是长整数格式
    printf("%ld %s\n", msg_type, buffer);
    //初始化消息结构体
    data.msg_type=msg_type;
    strcpy(data.mtext, buffer);
    //发送消息
    ret=msgsnd(msqid,(void*)&data,TEXT_SIZE,0);
    if(ret == -1) {
        ERR_EXIT("msgsnd()");
        }
        count++;
  }
  //打印相关信息，扫尾工作
  printf("number of sent messages = %d\n", count);
fclose(fp);
system("ipcs -q");
exit(EXIT_SUCCESS);
}