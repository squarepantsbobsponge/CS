#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"
#include "sync.h"
#include "memory.h"
#include "syscall.h"
#include "tss.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;
// 内存管理器
MemoryManager memoryManager;
// 系统调用
SystemService systemService;
// Task State Segment
TSS tss;

int syscall_0(int first, int second, int third, int forth, int fifth)
{
    printf("systerm call 0: %d, %d, %d, %d, %d\n",
           first, second, third, forth, fifth);
    return first + second + third + forth + fifth;
}
int malloc(int bytes_size) {
    return asm_system_call(5, (int)bytes_size);
}

int syscall_malloc(int bytes_size) {
    return programManager.malloc(bytes_size);
}
int free(int begin_address,int bytes_size) {
    return asm_system_call(6, (int)begin_address,(int)bytes_size);
}

int syscall_free(int begin_address,int bytes_size) {
    return programManager.free(begin_address,bytes_size);//两个参数都是int类型
}
void first_process()
{
     int address1=malloc(5);
     //int address2=malloc(4095);
     //int address3=malloc(2);
     printf("address1: %x\n",(char* )address1);
    // printf("address2: %x\n",(char*) address2);
     //printf("address3: %x\n",(char*) address3);
     free((int)address1,1);

}
void second_process()
{
     int address1=malloc(100);
     //int address2=malloc(4095);
     //int address3=malloc(2);
     printf("address1: %x\n",(char* )address1);
     //printf("address2: %x\n",(char*) address2);
     //printf("address3: %x\n",(char*) address3);
    free((int)address1,1);

}
// void first_process()
// {
//     int pid = fork();

//     if (pid == -1)
//     {
//         printf("can not fork\n");
//         asm_halt();
//     }
//     else
//     {
//         if (pid)
//         {
//             printf("I am father\n");
//             exit(0);
//         }
//         else
//         {
//             printf("I am child, exit\n");
//         }
//     }
// }


void first_thread(void *arg)
{

    programManager.executeProcess((const char *)first_process, 1);
    programManager.executeProcess((const char *)second_process, 2);
    asm_halt();
}

extern "C" void setup_kernel()
{

    // 中断管理器
    interruptManager.initialize();
    interruptManager.enableTimeInterrupt();
    interruptManager.setTimeInterrupt((void *)asm_time_interrupt_handler);

    // 输出管理器
    stdio.initialize();

    // 进程/线程管理器
    programManager.initialize();

    // 初始化系统调用
    systemService.initialize();
    // 设置0号系统调用
    systemService.setSystemCall(0, (int)syscall_0);
    // 设置1号系统调用
    systemService.setSystemCall(1, (int)syscall_write);
    // 设置2号系统调用
    systemService.setSystemCall(2, (int)syscall_fork);
    // 设置3号系统调用
    systemService.setSystemCall(3, (int)syscall_exit);
    // 设置4号系统调用
    systemService.setSystemCall(4, (int)syscall_wait);
    // 设置5号系统调用
    systemService.setSystemCall(5, (int)syscall_malloc);
    // 设置6号系统调用
    systemService.setSystemCall(6, (int)syscall_free);
    // 内存管理器
    memoryManager.initialize();

    // 创建第一个线程
    int pid = programManager.executeThread(first_thread, nullptr, "first thread", 1);
    if (pid == -1)
    {
        printf("can not execute thread\n");
        asm_halt();
    }

    ListItem *item = programManager.readyPrograms.front();
    PCB *firstThread = ListItem2PCB(item, tagInGeneralList);
    firstThread->status = ProgramStatus::RUNNING;
    programManager.readyPrograms.pop_front();
    programManager.running = firstThread;
    asm_switch_thread(0, firstThread);

    asm_halt();
}
