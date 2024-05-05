#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;


extern "C" void setup_kernel()
{
    // 中断处理部件
    interruptManager.initialize();
    // 屏幕IO处理部件
    stdio.initialize();
    interruptManager.enableTimeInterrupt();
    interruptManager.setTimeInterrupt((void *)asm_time_interrupt_handler);
    //asm_enable_interrupt();
    int a=1;
    //int* b=&a;
    char* list="abcd";
    char* b=&list[1];
    printf("print percentage: %%\n" //实现了转移
           "print char \"N\": %c\n"
           "print string \"Hello World!\": %s\n"
           "print decimal: \"-1234\": %d\n"
           "print hexadecimal \"0x7abcdef0\": %x\n"
           "print list[1]_address: %p\n"
           "print list_address: %p\n",
           'N', "Hello World!", a,0x7abcdef0, b,list);
    //uint a = 1 / 0;
    asm_halt();
}
