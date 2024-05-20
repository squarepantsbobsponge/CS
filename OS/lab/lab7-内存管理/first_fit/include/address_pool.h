#ifndef FIRST_FIT_H
#define FIRST_FIT_H

#include "fit_list.h"

class First_fit
{
public:
    Fit_List resources;
    int startAddress;
    Fit_ListItem start;//这个创建不能放在初始化函数里面，离开了函数会被释放掉的
    Fit_ListItem one;
public:
    // 初始化地址池
    void initialize(const int length, const int startAddress);
    // 从地址池中分配count个连续页，成功则返回第一个页的地址，失败则返回-1
    int allocate( int size);
    // 释放若干页的空间
    void release(const int address,int size);
    void print();
};

#endif