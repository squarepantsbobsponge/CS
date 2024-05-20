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

Semaphore chop[5];

void philosopher(void* arg){
    int i=*((int*)arg);
    while(true){
        //think()延迟
        int delay = (0xffff);//延迟   //这还是不会饿死人的，只不过是在一个时间片吃很多次
        while (delay)
            --delay;
        //拿起筷子
        chop[i].P();
        //死锁模拟
        printf(" %d is hungry and he took left chop...\n",i);
        int delay2 = (0xfffffff);//延迟
        while (delay2)
            --delay2;
        chop[(i+1)%5].P();
        //吃东西也是延迟
        printf(" %d is eating\n",i);
        // if(i==0){ //0和4邻近会触发延迟，4等的时间长一点，4和1不邻近，1的等待时间应该不会很长
        //  int delay = 0xffffffff;//延迟
        // while (delay)
        //     --delay;
        // }
        //放下筷子
        chop[i].V();
        chop[(i+1)%5].V();
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
    for(int i=0;i<5;i++){
    chop[i].initialize(1);//counter初始化为1
    }
    int tm1=0;
     programManager.executeThread(philosopher, &tm1, "second thread", 1);
    int tm2=4;
     programManager.executeThread(philosopher, &tm2, "third thread", 1);
        // int delay = (0xfffffff);//延迟
        // while (delay)
        //     --delay;
    int tm3=1;
     programManager.executeThread(philosopher, &tm3, "fourth thread", 1);
    int tm4=3;
     programManager.executeThread(philosopher, &tm4, "fifth thread", 1);
        // delay = (0xffffff);//延迟
        // while (delay)
        //     --delay;
    int tm5=2;
     programManager.executeThread(philosopher, &tm5, "sixth thread", 1);    
   

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
