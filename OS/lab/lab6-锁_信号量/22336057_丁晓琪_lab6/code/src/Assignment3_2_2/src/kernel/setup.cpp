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
Semaphore hungry[5];
void philosopher(void* arg){
    int i=*((int*)arg);
    while(true){
        //think()延迟
        
        //拿起筷子
        if(i%2==1){
        chop[i].P();
        printf(" %d is hungry and he took left chop...\n",i);
        int delay = (0xfffffff);//延迟
        while (delay)
            --delay;
        chop[(i+1)%5].P();
        printf(" %d  took right chop...\n",i); 
        }
        else{
        chop[(i+1)%5].P();
        printf(" %d is hungry and he took right chop...\n",i);
        int delay = (0xfffffff);//延迟
        while (delay)
            --delay;
        chop[i].P();   
        printf(" %d  took left chop...\n",i);          
        }
        //吃东西也是延迟
        printf(" %d is eating\n",i);
        //  int delay = 0xffffffff;//延迟
        // while (delay)
        //     --delay;
        //放下筷子
        if(i%2==0){
        chop[i].V();
        chop[(i+1)%5].V();
          programManager.schedule();//强制调度
        }
        else{
        chop[(i+1)%5].V();    
        chop[i].V();        
        programManager.schedule();//强制调度
     }
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
    hungry[i].initialize(1);//当锁用
    }
    int tm1=0;
     programManager.executeThread(philosopher, &tm1, "second thread", 1);
    int tm2=4;
     programManager.executeThread(philosopher, &tm2, "third thread", 1);
    int tm3=3;
     programManager.executeThread(philosopher, &tm3, "fourth thread", 1);
    int tm4=1;
     programManager.executeThread(philosopher, &tm4, "fifth thread", 1);
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
