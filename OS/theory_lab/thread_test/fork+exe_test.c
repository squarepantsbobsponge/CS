#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>
int system_test(const char*cmd_str){
    if(cmd_str==-1) return -1;
    if(fork()==0){
        execl(cmd_str,cmd_str,NULL);
        fprintf(stderr,"%s:commmand not found\n",cmd_str);
        exit(-1);
    }
    //加个wait等待挂载
    wait(NULL);
    return 0;
}
int main(void){
    printf("before...\n\n");
    system_test("/bin/ls");
    printf("\nafter...\n");
    return 0;
}