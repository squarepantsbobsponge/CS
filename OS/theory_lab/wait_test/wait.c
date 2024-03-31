#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
int main(void){
    int count=1;
    pid_t childpid,terminatedid;

    childpid=fork();//生成子进程
    if(childpid<0){
        perror("fork()");
        return EXIT_FAILURE;
    }
    else{
        if(childpid==0){
            count++;//子进程执行的代码段
            printf("child's pid=%d,count=%d (addr=%p)\n",getpid(),count,&count);
            printf("child sleeping....\n");
            sleep((5));
            printf("child wake up\n");
        }else{
          //  terminatedid=wait(0);//返回的是等待结束的子进程的pid号//不加这个顺序就是乱的
//             printf("parent pro pid = %d, terminated pid = %d, count = %d (addr = %p)\n",
// getpid(), terminatedid, count, &count);
             printf("parent pro pid = %d, count = %d (addr = %p)\n",
getpid(), count, &count);
        }
    }
    printf("\nTesting point by %d\n",getpid());
    return EXIT_SUCCESS;
}