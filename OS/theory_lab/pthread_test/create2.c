#include<pthread.h>
#include<stdio.h>
void * do_your_job(void* input){
    printf("child=%d\n",(*(int*)input));
    (*(int*)input)=20;
    printf("child=%d\n",(*(int*)input));
    pthread_exit(NULL);
}
int main(void){
    pthread_t tid;
    int input=10;
    printf("main=%d\n",input);
    pthread_create(&tid,NULL,do_your_job,&input);
    pthread_join(tid,NULL);
    printf("main=%d\n",input);   
}