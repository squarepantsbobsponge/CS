#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <fcntl.h>
#include"shmdata.h"
#include <string.h>
int main(int argc,char *argv[]){
    struct stat fileattr;
    key_t key;
    int shmid;
    void *shmptr;
    struct shared_struct *shared;
    pid_t childpid1,childpid2;
    char pathname[80],key_str[10],cmd_str[80];
    int shmsize,ret;
    shmsize=TEXT_NUM*sizeof(struct shared_struct);
    printf("max record number = %d, shm size = %d\n", TEXT_NUM, shmsize);

    if(argc<2){
       printf("Usage: ./a.out pathname\n");
        return EXIT_FAILURE;
    }
    strcpy(pathname,argv[1]);
    if(stat(pathname,&fileattr)==-1){//stat检查pathname的文件信息，将结构反馈到fileattr的一个结构体里面
        //pathname不存在就创建一个
        ret=creat(pathname,O_WRONLY);
        if(ret==-1){
            ERR_EXIT("creat()");
        }
        printf("shared file object created\n");
    }

    //得到key
    key=ftok(pathname,0x27);
      if(key==-1){
        ERR_EXIT("shmcon:ftok()");
      }
      printf("key generated: IPC key = 0x%x\n", key);
    //得到共享内存的标识符
      shmid=shmget((key_t)key,shmsize,0666|PERM);
      if(shmid==-1){
        ERR_EXIT("shmcon: shmget()");
      }
    printf("shmcon: shmid = %d\n", shmid);

    //挂载
    shmptr=shmat(shmid,0,0);
    if(shmptr==(void*)-1){
        ERR_EXIT("shmcon: shmat()");
    }
    printf("shmcon: shared Memory attached at %p\n", shmptr);

    //获得共享内存的索引//且格式化共享内存段
    shared=(struct shared_struct *)shmptr;
    shared->written=0;

    //格式化输入字符串cmd_str,获得共享内存段中含shmid的行//并且系统调用
    sprintf(cmd_str,"ipcs -m | grep '%d'\n", shmid);
    printf("\n------ Shared Memory Segments ------\n");
    system(cmd_str);

    //删除挂载
    if(shmdt(shmptr)==-1){
      ERR_EXIT("shmcon: shmdt()");
    }
    //打印相关信息
    printf("\n------ Shared Memory Segments ------\n");
    system(cmd_str);
    //定义char* argv1
    sprintf(key_str, "%x", key);
char *argv1[] = {" ", key_str, 0};
  //生成vfrok并且跳转到其他函数执行
  childpid1=vfork();//为什么用fork，而不是fork
  if(childpid1<0){//共享内存读
      ERR_EXIT("shmcon: 1st vfork()");
  }
  else if(childpid1==0){
    execv("./shmread.o",argv1);//子进程的代码段被覆盖成新的，但是父进程的代码段仍然存在
  }
  else{
    childpid2=vfork();//执行共享内存写
    if(childpid2<0){
      ERR_EXIT("shmcon: 2nd vfork()");
    }
    else if(childpid2==0){
      execv("./shmwrite.o",argv1);
    }
    else{
      wait(&childpid1);
      wait(&childpid2);

      //删除共享内存
      if(shmctl(shmid,IPC_RMID,0)==-1){
       ERR_EXIT("shmcon: shmctl(IPC_RMID)");
      }
      else{
        printf("shmcon: shmid = %d removed \n", shmid);
        printf("\n------ Shared Memory Segments ------\n");
        system(cmd_str);
        printf("nothing found ...\n");
        return EXIT_SUCCESS;
      }
    }
  }
}








