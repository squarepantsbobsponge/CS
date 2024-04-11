#define TEXT_SIZE 512
struct msg_struct
{
    long int msg_type;
    char mtext[TEXT_SIZE];
};
#define PERM S_IRUSR|S_IWUSR|IPC_CREAT //设置文件权限，有读取，写入权限，文件不存在时，则创造它
#define ERR_EXIT(m) \
do { \
perror(m); \
exit(EXIT_FAILURE); \
} while(0)
