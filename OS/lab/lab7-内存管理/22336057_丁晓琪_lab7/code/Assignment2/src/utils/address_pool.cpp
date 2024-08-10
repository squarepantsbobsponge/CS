#include "address_pool.h"
#include "os_constant.h"



// 设置地址池BitMap
void First_fit::initialize(const int length, const int startAddress)
{   //start为链表存放位置
    resources.head=&start;//更换链表开始位置
    resources.initialize();
    one.begin_address=startAddress;
    one.size=length;
    one.is_allocate=0;
    one.previous=resources.head;
    one.next=0;
    resources.head->next=&one;
}

// 从地址池中分配count个连续页
int First_fit::allocate(const int size)
{
    resources.allocate(size);
}

// 释放若干页的空间
void First_fit::release(const int address,int size)
{
    resources.release(address,size);
}
void First_fit::print(){
    resources.print_allocate();
}