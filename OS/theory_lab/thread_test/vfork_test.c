#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void){
    int count=1;
    pid_t childpid;
    childpid=vfork();//是会挂起父进程直到子进程执行结束
    if(childpid<0){
        perror("vfork()");
        return EXIT_FAILURE;
    }
    else{
        if(childpid==0){
            count++;
            printf("Child pro pid=%d, count=%d (addr=%p)\n",getpid(),count,&count);
            printf("Child taking a nap...\n");
            sleep(10);
            printf("Child waking up!\n");
            _exit(0);
        }else{
            printf("parent pro pid=%d, count=%d (addr=%p)\n",getpid(),count,&count);
        }
    }
}