#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>
#include <sys/shm.h>
#include "shmdata.h"
int main(int argc,char *argv[]){
    void *shmptr=NULL;
    struct shared_struct *shared=NULL;
    int shmid;
    key_t key;
    char buffer[BUFSIZ+1];
    //写入变量和打印相关信息
    sscanf(argv[1], "%x", &key);
    printf("shmwrite: IPC key = 0x%x\n", key);

    //得到共享段的句柄
    shmid=shmget((key_t)(key),TEXT_NUM*sizeof(struct shared_struct),0666|PERM);
    if(shmid==-1){
        ERR_EXIT("shmwite: shmget()");
    }
    //挂载共享段
    shmptr=shmat(shmid,0,0);
    if(shmptr==(void*)-1){
        ERR_EXIT("shmwrite: shmat()");
    }
    printf("shmwrite: shmid = %d\n", shmid);
    printf("shmwrite: shared memory attached at %p\n", shmptr);
    printf("shmwrite precess ready ...\n");
    //格式化共享段
    shared=(struct shared_struct*)shmptr;
    //写入数据
    while(1){
        while(shared->written==1){
            sleep(1);//读那边在读，等人家读完
        }
        printf("Enter some text: ");
        //从标准输入那里读出数据写到buffer
        fgets(buffer, BUFSIZ, stdin);
        strncpy(shared->mtext,buffer,TEXT_SIZE);//写入到共享内存段
        printf("shared buffer: %s\n",shared->mtext);
        //写完了，将信号置1
        shared->written=1;
        if(strncmp(buffer,"end",3)==0){
            break;
        }
    }
    //删除挂载
    if(shmdt(shmptr)==-1){
        ERR_EXIT("shmwrite: shmdt()");
    }
    sleep(1);
exit(EXIT_SUCCESS);
}