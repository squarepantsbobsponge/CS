#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>
#include <sys/shm.h>
#include "shmdata.h"
int main(int argc,char* argv[]){
    void *shmptr=NULL;
    struct shared_struct *shared;
    int shmid;
    key_t key;

    sscanf(argv[1],"%x",&key);//将参数输入到key变量中
    printf("%*sshmread: IPC key = 0x%x\n", 30, " ", key);
   //得到共享内存句柄
   shmid=shmget((key_t)key,TEXT_NUM*sizeof(struct shared_struct),0666|PERM);
   if(shmid==-1){
    ERR_EXIT("shread: shmget()");
   }

   //挂载//且获得映射在内存中的句柄
   shmptr=shmat(shmid,0,0);
   if(shmptr==(void*)-1){
    ERR_EXIT("shread: shmat()");
   }
   //打印相关信息
   printf("%*sshmread: shmid = %d\n", 30, " ", shmid);
    printf("%*sshmread: shared memory attached at %p\n", 30, " ", shmptr);
    printf("%*sshmread process ready ...\n", 30, " ");

    //格式化挂载内存段
    shared=(struct shared_struct*)shmptr;
    //读取信息
    while(1){//每次都从头读吗？
        while(shared->written==0){
            sleep(1);//还没有信息写入
        }
        printf("%*sYou wrote: %s\n", 30, " ", shared->mtext);
        shared->written=0;//所有数据读取完，将开关关上
        if(strncmp(shared->mtext,"end",3)==0){//比较前三个字符是否是end
            break;
        }

    }
    //删除挂载
    if(shmdt(shmptr)==-1){
        ERR_EXIT("shmread: shmdt()");
    }
    sleep(1);
    exit(EXIT_SUCCESS);
}