#ifndef FIRST_FIT_H
#define FIRST_FIT_H

#include "fit_list.h"
#include "memory.h"
class Heap_pool
{
public:
    Fit_List resources[50];//最多分配100页当成堆池
    int pool_size; //堆池中页的数量
public:
    // 初始化地址池
    void initialize();
    // 从地址池中分配count个连续页，成功则返回第一个页的地址，失败则返回-1
    int allocate( int size);
    // 释放若干页的空间
    void release(const int address,int size);
    void clear();
    void print();
};

#endif