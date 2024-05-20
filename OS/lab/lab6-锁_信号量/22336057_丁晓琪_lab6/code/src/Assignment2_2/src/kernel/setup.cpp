#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"
#include "sync.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;

Semaphore mutex;
Semaphore empty;
Semaphore full;
int buffer[100];
int size=0;
void producer(void *arg)
{
    while(1){    
        empty.P();
        mutex.P(); //上锁
        if(size==100){
      	    printf("full_error\n");
        }
        buffer[size]=1;
           int delay = 0xfffff;//延迟为了一个时间片内只写一次
        while (delay)
        --delay;//还没来的及size++就被读了，当然没东西读
        size++;
        mutex.V();//解锁
        full.V();
        }
}

void resumer(void *arg){
    while(1){
        full.P();
        mutex.P();//上锁
        if(size==0){
	    printf("empty_error\n");
        }
        printf("%d\n",buffer[size-1]);
        buffer[size-1]=0;
        // 破坏了size--的原子性，可能插了一个buffer[size++]的指令近来
        int delay2 = 0xfffff;//延迟为了一次在一个时间片内只读一次
        while (delay2)//可能会读到0，因为这里增加了延迟给了切换成写进程buffer[size++]的可乘之机会，读了还没写的地方
        --delay2;
        size--;
        mutex.V();//解锁,没有进程打断这个过程
        empty.V();
        }
}
void first_thread(void *arg)
{
    // 第1个线程不可以返回
    stdio.moveCursor(0);
    for (int i = 0; i < 25 * 80; ++i)
    {
        stdio.print(' ');
    }
    stdio.moveCursor(0);

    //cheese_burger = 0;
    mutex.initialize(1);//counter初始化为1
    empty.initialize(100); //一开始缓冲区都是空的，counter 100
    full.initialize(0);//初始化为0

    programManager.executeThread(producer, nullptr, "second thread", 1);
    programManager.executeThread(resumer, nullptr, "third thread", 1);

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
