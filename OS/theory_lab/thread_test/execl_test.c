#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
int main(void){
    printf("before execl..\n");
    execl("/bin/ls","/bin/ls/",NULL);
    printf("after execl...\n");
    return 0;
}