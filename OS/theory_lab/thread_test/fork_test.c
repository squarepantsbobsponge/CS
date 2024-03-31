#include <unistd.h>
#include<stdio.h>
int main(void){
    int result;
    printf("before fork...\n");
    result=fork();
    printf("result=%d\n",result);
    if(result==0){
        printf("I,m the child\n");
        printf("My PID is %d\n", getpid());
    }
    else {
printf("I'm the parent.\n");
printf("My PID is %d\n", getpid());
}
printf("program terminated.\n");    
}