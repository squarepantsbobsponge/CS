#include<stdio.h>
#include<pthread.h>
#include<malloc.h>
#include <unistd.h>
void* do_your_job(void * input){
    int *output=(int*)malloc(sizeof(int));
    *output=10;
    pthread_exit(output);
    sleep(10);
}
int main(void){
    pthread_t tid;
    int input=10,*output; //申明了未初始化的指针int变量
    pthread_create(&tid,NULL,do_your_job,&input);
    pthread_join(tid,(void**)&output);
    printf("%d",(*(int*)output));
}