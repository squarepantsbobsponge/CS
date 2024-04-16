#include <unistd.h>
#include<stdio.h>
#include<pthread.h>
void *hello(void* arg) {
  printf("%s\n", (char*)arg);
  return NULL;
}
int main(){
    pid_t pid;
    pid=fork();
    if(pid==0){
        // printf("PID:%d\n",getpid());
        // pid_t pid2;
        fork();
        // if(pid2==0)
        //         printf("PID:%d\n",getpid());
         pthread_t tid;
         pthread_create(&tid, NULL, hello,(void*) "hello world");
    }
    //pid_t pid3;
    fork();
    //  if(pid3==0)
    // printf("PID:%d\n",getpid());
}