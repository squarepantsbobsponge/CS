#define TEXT_SIZE 4*1024 /* = PAGE_SIZE, size of each message */
#define TEXT_NUM 1
/* maximal number of messages */
/* total size can not exceed current shmmax,
or an 'invalid argument' error occurs when shmget */
#define PERM S_IRUSR|S_IWUSR|IPC_CREAT
#define ERR_EXIT(m) \
do { \
perror(m); \
exit(EXIT_FAILURE); \
} while(0)

struct shared_struct
{
    int written;
    char mtext[TEXT_SIZE];
};
