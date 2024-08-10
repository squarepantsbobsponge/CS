#include "heap_pool.h"
#include "memory.h"
#include "os_constant.h"
#include "stdlib.h"
#include "asm_utils.h"
#include "stdio.h"
#include "program.h"
#include "os_modules.h"
// 设置地址池BitMap
void Heap_pool::initialize()
{   
    //resources.initialize();//等到分配堆页时用
    pool_size=0;
    for(int i=0;i<50;i++){
        resources[i].initialize();
    }
    // one.begin_address=startAddress;  //这个留到分配堆页的时候做
}

int Heap_pool::allocate(const int size)
{
    //首先先看现存堆池能否满足要求//这里假设申请的字节一次性不超过一页
    int address=0;
    for(int i=0;i<pool_size;i++){
       address=resources[i].allocate(size);
       if(address!=-1) return address+(int)resources[i].start_address;;
    }
    if(size==50){
        printf("full error!\n");
        return -1;//堆池满了，不成功
    }
    else{//堆池为0
       //先申请分配一个用户空间的页
      char *startAddress= (char *)memoryManager.allocatePages(AddressPoolType::USER,1);//给的就是running进程的页的虚拟地址
       resources[pool_size].start_address=startAddress;
       address=(int)startAddress+resources[pool_size].allocate(size);
       pool_size++;//启动一个链表管理
       return address;
    }
}

void Heap_pool::release(const int address,int size)
{
    for(int i=0;i<pool_size;i++){
        int re_address=(int)resources[i].start_address;
        if(address>=re_address&& address<re_address+4096){
            resources[i].release(address-re_address,size);
            break;
        }
    }
    //resources.release(address,size);
}
void Heap_pool::print(){
    for(int i=0;i<pool_size;i++){
        resources[i].print_allocate();
    }
    //resources.print_allocate();
}
void Heap_pool::clear(){
      for(int i=0;i<pool_size;i++){
        resources[i].clear();
    }
}