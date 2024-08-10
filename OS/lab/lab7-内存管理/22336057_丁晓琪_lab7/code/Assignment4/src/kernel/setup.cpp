#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"
#include "sync.h"
#include "memory.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;
// 内存管理器
MemoryManager memoryManager;
void second_thread(void *arg)
{
    // 第1个线程不可以返回
    // stdio.moveCursor(0);
    // for (int i = 0; i < 25 * 80; ++i)
    // {
    //     stdio.print(' ');
    // }
    // stdio.moveCursor(0);

    char *p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 100);
    printf("allocate 100 pages for p2,address:%x\n",p2);
    // char *p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 10);
    // printf("allocate 10 pages for p2,address:%x\n",p2 );
    // char *p3 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 100);
    //     printf("allocate 100 pages for p3,address:%x\n",p3 );

    // memoryManager.releasePages(AddressPoolType::KERNEL, (int)p2, 10);
    // printf("release 10 pages from p2\n");
    // p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 100);
    // printf("allocate 100 pages for p2,address:%x\n",p2 );
    // // printf("%x\n", p2);

    //  p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 10);
    // printf("allocate 10 pages for p2,address:%x\n",p2 );
    // printf("%x\n", p2);

   
}

void first_thread(void *arg)
{
     programManager.executeThread(second_thread, nullptr, "second thread", 2);
    // 第1个线程不可以返回
    // stdio.moveCursor(0);
    // for (int i = 0; i < 25 * 80; ++i)
    // {
    //     stdio.print(' ');
    // }
    // stdio.moveCursor(0);

    char *p1 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 100);
    printf("allocate 100 pages for p1,address:%x\n",p1 );
    // char *p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 10);
    // printf("allocate 10 pages for p2,address:%x\n",p2 );
     //char *p3 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 5000);
       //  printf("allocate 100 pages for p3,address:%x\n",p3 );

    // memoryManager.releasePages(AddressPoolType::KERNEL, (int)p2, 10);
    // printf("release 10 pages from p2\n");
    // p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 100);
    // printf("allocate 100 pages for p2,address:%x\n",p2 );
    // // printf("%x\n", p2);

    //  p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 10);
    // printf("allocate 10 pages for p2,address:%x\n",p2 );
    // printf("%x\n", p2);

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

    // 内存管理器
    memoryManager.openPageMechanism();
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
    firstThread->status = RUNNING;
    programManager.readyPrograms.pop_front();
    programManager.running = firstThread;
    asm_switch_thread(0, firstThread);

    asm_halt();
}
