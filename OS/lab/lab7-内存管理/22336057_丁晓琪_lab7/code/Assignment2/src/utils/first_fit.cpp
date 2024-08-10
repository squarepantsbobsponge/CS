// #include "first_fit.h"
// #include "fit_list.h"
// #include "stdio.h"

// First_fit::First_fit()
// {
  
// }

// // 设置地址池BitMap
// void First_fit::initialize(int *start, const int length, const int startAddress)
// {   //start为链表存放位置
//     &(resources.head)=start;//更换链表开始位置
//     resources.initialize();
//     Fit_ListItem one;
//     one.begin_address=startAddress;
//     one.size=length;
//     one.is_allocate=0;
//     one.previous=&(resources.head);
//     one.next=0;
//     (resources.head).next=&one;
// }

// // 从地址池中分配count个连续页
// int First_fit::allocate(const int size)
// {
//     resource.allocate(size);
// }

// // 释放若干页的空间
// void First_fit::release(const int address)
// {
//     resources.release(address);
// }