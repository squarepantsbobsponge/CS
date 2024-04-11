#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
int main(){
     int real_fd = mkfifo("./A_pipe.txt", 0666);
    int fd=open("./A_pipe.txt",O_WRONLY);
    if(fd==-1){
        perror("open");
        return -1;
    }
    write(fd,"Hello,world!",13);
    return 0;
}