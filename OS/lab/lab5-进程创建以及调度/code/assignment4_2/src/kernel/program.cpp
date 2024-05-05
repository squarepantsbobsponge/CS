#include "program.h"
#include "stdlib.h"
#include "interrupt.h"
#include "asm_utils.h"
#include "stdio.h"
#include "thread.h"
#include "os_modules.h"

const int PCB_SIZE = 4096;                   // PCB的大小，4KB。
char PCB_SET[PCB_SIZE * MAX_PROGRAM_AMOUNT]; // 存放PCB的数组，预留了MAX_PROGRAM_AMOUNT个PCB的大小空间。
bool PCB_SET_STATUS[MAX_PROGRAM_AMOUNT];     // PCB的分配状态，true表示已经分配，false表示未分配。

ProgramManager::ProgramManager()
{
    initialize();
}

void ProgramManager::initialize()
{
    allPrograms.initialize();
    readyPrograms.initialize();
    //priority_1st.initialize();
    Priority_2nd.initialize();
    running = nullptr;

    for (int i = 0; i < MAX_PROGRAM_AMOUNT; ++i)
    {
        PCB_SET_STATUS[i] = false;
    }
}

int ProgramManager::executeThread(ThreadFunction function, void *parameter, const char *name, int priority)
{
    // 关中断，防止创建线程的过程被打断
    bool status = interruptManager.getInterruptStatus();
    interruptManager.disableInterrupt();

    // 分配一页作为PCB
    PCB *thread = allocatePCB();

    if (!thread)
        return -1;

    // 初始化分配的页
    memset(thread, 0, PCB_SIZE);

    for (int i = 0; i < MAX_PROGRAM_NAME && name[i]; ++i)
    {
        thread->name[i] = name[i];
    }

    thread->status = ProgramStatus::READY;
    thread->priority = priority;
    thread->ticks = 5;
    thread->ticksPassedBy = 0;
    thread->pid = ((int)thread - (int)PCB_SET) / PCB_SIZE;

    // 线程栈
    thread->stack = (int *)((int)thread + PCB_SIZE);
    thread->stack -= 7;
    thread->stack[0] = 0;
    thread->stack[1] = 0;
    thread->stack[2] = 0;
    thread->stack[3] = 0;
    thread->stack[4] = (int)function;
    thread->stack[5] = (int)program_exit;
    thread->stack[6] = (int)parameter;
    //
    //要根据优先级push进去
        //初始化线程队列中的优先级
        thread->tagInGeneralList.priority=priority;
        thread->tagInAllList.priority=priority;
        //插入到优先级对应位置，规定优先级1最大

    allPrograms.insert_priority(&(thread->tagInAllList));
    if(priority==1){
       // priority_1st.push_back(&(thread->tagInGeneralList));
        readyPrograms.push_front(&(thread->tagInGeneralList)); //
    }
    if(priority==2) readyPrograms.push_back(&(thread->tagInGeneralList));
   

    // 恢复中断
    interruptManager.setInterruptStatus(status);

    return thread->pid;
}

void ProgramManager::schedule()  //
{
    bool status = interruptManager.getInterruptStatus();
    interruptManager.disableInterrupt();

    if (readyPrograms.size()==0)//第二个优先级先到先执行，不抢占//这里只能执行完队列里面的一个线程，没有切换就直接返回推出了//进到这里来的2优先级线程已经进exit了，是执行完了
    {
        interruptManager.setInterruptStatus(status);
        return;//可以忽略了
    }

    if (running->status == ProgramStatus::RUNNING)//第一个优先级时间到了要切换，而且下第二个优先级
    {
        // if(readyPrograms.size() ==0){//第一个优先级都轮过一遍，执行第二个优先级队列，可以直接把ready队列头换成第二个优先级队列头
        //     readyPrograms=Priority_2nd;
        // }
        running->status = ProgramStatus::READY;//换下来
        running->ticks = running->priority * 10;//无所谓，屏蔽不屏蔽都没关系
        readyPrograms.push_back(&(running->tagInGeneralList));//放到第二个优先级队列中
        running->priority=2;//更改优先级
        running->tagInAllList.priority=2;
        running->tagInGeneralList.priority=2;
    }
    else if (running->status == ProgramStatus::DEAD)
    {
        // if(readyPrograms.size() ==0){//第一个优先级都轮过一遍，执行第二个优先级队列，可以直接把ready队列头换成第二个优先级队列头
        //     readyPrograms=Priority_2nd;
        // }   
        releasePCB(running);
    }

    ListItem *item = readyPrograms.front();
    PCB *next = ListItem2PCB(item, tagInGeneralList);
    PCB *cur = running;
    next->status = ProgramStatus::RUNNING;
    running = next;
    readyPrograms.pop_front();

    asm_switch_thread(cur, next);

    interruptManager.setInterruptStatus(status);
}

void program_exit()
{
    PCB *thread = programManager.running;
    thread->status = ProgramStatus::DEAD;

    // if (thread->pid)
    // {
    //     programManager.schedule();
    // }
    if(programManager.readyPrograms.size()||thread->priority==1){
        programManager.schedule();
    }
    else 
    {
        interruptManager.disableInterrupt();
        printf("halt\n");
        asm_halt();
    }
}

PCB *ProgramManager::allocatePCB()
{
    for (int i = 0; i < MAX_PROGRAM_AMOUNT; ++i)
    {
        if (!PCB_SET_STATUS[i])
        {
            PCB_SET_STATUS[i] = true;
            return (PCB *)((int)PCB_SET + PCB_SIZE * i);
        }
    }

    return nullptr;
}

void ProgramManager::releasePCB(PCB *program)
{
    int index = ((int)program - (int)PCB_SET) / PCB_SIZE;
    PCB_SET_STATUS[index] = false;
}