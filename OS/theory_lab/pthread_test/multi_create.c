#include<stdio.h>
#include<pthread.h>
#include <unistd.h>
 void * do_your_job(void *input) {
 int id = *((int *) input);
 printf("My ID number = %d\n", id);

 pthread_exit(NULL);
 }
 int main(void) {
 int i;
 pthread_t tid[5];

 for(i = 0; i < 5; i++){
     pthread_create(&tid[i], NULL, do_your_job, &i);
      sleep(3);
 }

 for(i = 0; i < 5; i++)
 pthread_join(tid[i], NULL);
 return 0;
 }