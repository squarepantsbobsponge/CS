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

Semaphore semaphore;

// int cheese_burger;

// void a_mother(void *arg)
// {
//     semaphore.P();
//     int delay = 0;

//     printf("mother: start to make cheese burger, there are %d cheese burger now\n", cheese_burger);
//     // make 10 cheese_burger
//     cheese_burger += 10;

//     printf("mother: oh, I have to hang clothes out.\n");
//     // hanging clothes out
//     delay = 0xfffffff;
//     while (delay)
//         --delay;
//     // done

//     printf("mother: Oh, Jesus! There are %d cheese burgers\n", cheese_burger);
//     semaphore.V();
// }

// void a_naughty_boy(void *arg)
// {
//     semaphore.P();
//     printf("boy   : Look what I found!\n");
//     // eat all cheese_burgers out secretly
//     cheese_burger -= 10;
//     // run away as fast as possible
//     semaphore.V();
// }
int buffer[100];
int size=0;
void producer(void *arg)
{
    while(1){
        
        //aLock.lock();//好像一直获得锁不放手死锁了，就是在这个时间片里锁到一半换别人，但所是锁在自己手上，别人无法执行，就这样一直下去
        if(size==100){
      	    printf("full_error\n");
	    continue;
        }
       // semaphore.P(); //上锁
        buffer[size]=1;
           int delay = 0xffffff;//延迟为了一个时间片内只写一次
            while (delay)
        --delay;//还没来的及size++就被读了，当然没东西读
        size++;
      // semaphore.V();//解锁
        }
}

void resumer(void *arg){
    
    while(1){
       //  aLock.lock();
        if(size==0){
	    printf("empty_error\n");
 	    continue;
        }
        //semaphore.P();//上锁
        printf("%d\n",buffer[size-1]);
        buffer[size-1]=0;
        //破坏了size--的原子性，可能插了一个buffer[size++]的指令近来
        int delay2 = 0xffffff;//延迟为了一次在一个时间片内只读一次
        while (delay2)//可能会读到0，因为这里增加了延迟给了切换成写进程buffer[size++]的可乘之机会，读了还没写的地方
        --delay2;
        size--;
    // semaphore.V();//解锁,没有进程打断这个过程
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
    semaphore.initialize(1);//counter初始化为1

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
