#ifndef TSS_H
#define TSS_H

struct TSS
{
public:
    int backlink;
    //不同的特权级的栈指针esp和ss
    int esp0;
    int ss0;
    int esp1;
    int ss1;
    int esp2;
    int ss2;
    //下面是特权级切换时保存的现场
    int cr3;
    int eip;
    int eflags;
    int eax;
    int ecx;
    int edx;
    int ebx;
    int esp;
    int ebp;
    int esi;
    int edi;
    int es;
    int cs;
    int ss;
    int ds;
    int fs;
    int gs;
    int ldt;
    int trace;
    int ioMap;
};
#endif