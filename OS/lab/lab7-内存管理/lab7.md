 

![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科

[TOC]

# Assignment1

## 1.实验要求

复现参考代码，实现二级分页机制，并能够在虚拟机地址空间中进行内存管理，包括内存的申请和释放等，截图并给出过程解释。

## 2.实验过程

1.实现位图

2.实现地址池

3.初始化页表，开启二级页表机制

## 3.关键代码

**3.1实现位图**：

* 作用：用一个bit记录一个分区的分配情况，0为未分配，1为已分配，在分页机制中就是记录每一页的分配情况，便于开启分页机制后管理页的分配和释放

* 数据结构：

  <code>char* bitmap</code>: 一块记录分区分配情况的空间，注意由于是1bit记录一个分区，则操作精度要到每个bit上

* 主要函数：

  <code> int allocate(const int count)</code>: 遍历<code>bitmap</code>，查找连续的count个未被分配的分区，并将其分配

  <code> void release(const int index, const int count);</code>: 释放第index个分区开始的count个跟去

* 注意：单纯的位图实现中并没有说明每个资源的含义和大小，只是将资源做离散化管理，具体地对资源管理的一些定义仍需进一步设置定义

```c++
class BitMap
{
public:
    // 被管理的资源个数，bitmap的总位数
    int length;
    // bitmap的起始地址
    char *bitmap;
public:
    // 初始化
    BitMap();
    // 设置BitMap，bitmap=起始地址，length=总位数(即被管理的资源个数)
    void initialize(char *bitmap, const int length);
    // 获取第index个资源的状态，true=allocated，false=free
    bool get(const int index) const;
    // 设置第index个资源的状态，true=allocated，false=free
    void set(const int index, const bool status);
    // 分配count个连续的资源，若没有则返回-1，否则返回分配的第1个资源单元序号
    int allocate(const int count);
    // 释放第index个资源开始的count个资源
    void release(const int index, const int count);
    // 返回Bitmap存储区域
    char *getBitmap();
    // 返回Bitmap的大小
    int size() const;
private:
    // 禁止Bitmap之间的赋值
    BitMap(const BitMap &) {}
    void operator=(const BitMap&) {}
};
```

**3.2地址池实现**

* 作用：在位图的基础上进一步申明管理的资源的含义和大小，管理的资源是内存且管理粒度为一页4kb

* 数据结构：

  <code>Bitmap resources</code>: 标识内存中划分出每一页的分配情况

  <code>int startAddress</code>: 记录地址池管理的页的共同起始地址。（索引地址池第i页的起始地址：address=startAddress+i×PAGESIZE）

* 主要函数：

  <code> int allocate(const int count)</code>:  在地址池中分配count页内存，通过位图<code>resources</code>的分配函数返回连续count个空闲页开头索引<code>start</code>，再根据<code>startAddress</code>和<code>start</code>计算被分配的空闲页的开头地址

  <code> int allocate(const int count);</code> 释放开始地址为address的amount页。先根据pagesize，address，startAddress计算出释放页在位图中的索引<code>index</code>,再通过位图<code>resources</code>的释放函数将这些页的状态都置为未分配。

  ```c++
   class AddressPool
  {
  public:
      BitMap resources;
      int startAddress;
  
  public:
      AddressPool();
      // 初始化地址池
      void initialize(char *bitmap, const int length, const int startAddress);
      // 从地址池中分配count个连续页，成功则返回第一个页的地址，失败则返回-1
      int allocate(const int count);
      // 释放若干页的空间
      void release(const int address, const int amount);
  };
  ```

**3.3 物理内存的实现**：

* 作用：地址池实现对整个物理内存划分为页，需要进一步划分用户空间和内核空间

* 数据结构:

  <code>AddressPool kernelPhysical;</code>内核地址池

  <code> AddressPool userPhysical;</code> 物理地址池

* 主要函数:

  <code>void initialize();</code>: 留出给内核的0x100000,再预留出1MB（256个4kb页）给内核页目录表和页表，剩下的物理内存内核和用户地址池平分，同时指定内核和物理位图的位置起始0x10000。根据计算出的内存和用户地址池的开始地址和大小以及定义好的位图位置初始化<code> kernelPhysical</code>,<code>userPhysical</code>.

  <code>int allocatePhysicalPages(enum AddressPoolType type, const int count)</code>:根据指定类型去指定地址池调用地址池分配函数分配count页，并且返回页的开始物理地址

  <code>void releasePhysicalPages(enum AddressPoolType type, const int paddr, const int count)</code>: 根据指定的类型去指定地址池调用释放函数，释放起始地址为<code>paddr</code>的<code>count</code>页

```c++
class MemoryManager
{
public:
    // 可管理的内存容量
    int totalMemory;
    // 内核物理地址池
    AddressPool kernelPhysical;
    // 用户物理地址池
    AddressPool userPhysical;
public:
    MemoryManager();
    // 初始化地址池
    void initialize();
    // 从type类型的物理地址池中分配count个连续的页
    // 成功，返回起始地址；失败，返回0
    int allocatePhysicalPages(enum AddressPoolType type, const int count);
    // 释放从paddr开始的count个物理页
    void releasePhysicalPages(enum AddressPoolType type, const int paddr, const int count);
    // 获取内存总容量
    int getTotalMemory();
};
```

**3.4开启二级分页机制**：

* 作用：

  ![image-20240524173804859](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240524173804859.png)

* 步骤：
  

   1.初始化内核页表和页目录表：

* 目前物理内存的使用情况：只有内核在使用而且不超过1MB，所以要为1MB内存做好页表和页目录的映射
* 页目录初始化：前1MB的高10位始终为0，则需要初始化第0个页目录项，将其映射到内核第一个页表的起始地址。页目录表实际上也是一个页表，也要能通过页目录表寻找，所以将页目录表的最后一项映射为页目录表的地址
* 内核第一个页表初始化：前1mb的中间10位只有后8位有值，1mb/4kb=256页，所以需要初始化256个页表项，且定义0-1MB是恒等映射

​    2.将页目录表的地址写入cr3，让MMU能找到页目录表，自动将CPU生成的逻辑地址转化为物理地址

​    3.将cr0的PG位置1，开启分页机制

  ```c++
  void MemoryManager::openPageMechanism()
  {
      // 页目录表指针
      int *directory = (int *)PAGE_DIRECTORY;  //放到0x100000的位置（十六进制也就是在1MB位置处）
      //线性地址0~4MB对应的页表
      int *page = (int *)(PAGE_DIRECTORY + PAGE_SIZE);//之前预留出了2^8*4KB=1MB的位置，前面4KB代表页目录指针，其他都是代表页表
      // 初始化页目录表
      memset(directory, 0, PAGE_SIZE);
      // 初始化线性地址0~4MB对应的页表
      memset(page, 0, PAGE_SIZE);//一个页表可以表示4MB的虚拟内存，现在这个页表要映射内存中前4MB包括预留给内核的1MB的物理内存
      int address = 0;
      // 将线性地址0~1MB恒等映射到物理地址0~1MB（预留给内核的1MB的位置是虚拟地址和物理地址相同）1MB/4KB=2^8个页
      //前1MB 二进制：|00100 00000|00000 00000 00   中间10位只有后8位有值，所以需要初始化2^8=256个表项
      //初始化页表
      for (int i = 0; i < 256; ++i)
      {
          // U/S = 1, R/W = 1, P = 1
          page[i] = address | 0x7;//信息位的初始化
          address += PAGE_SIZE;//加载高20位的页基地址，由于是4KB的倍数，所以只关心高20位
      }
      // 初始化页目录项
      //前1MB的高10位始终是000，则页目录项只要初始化第0项
      // 0~1MB
      directory[0] = ((int)page) | 0x07;
      // 3GB的内核空间
      directory[768] = directory[0];
      // 最后一个页目录项指向页目录表
      directory[1023] = ((int)directory) | 0x7;
  
      // 初始化cr3，cr0，开启分页机制
      asm_init_page_reg(directory);
  
      printf("open page mechanism\n");
      
  }
  
  ```

 

```assembly
asm_init_page_reg:
    push ebp  
    mov ebp, esp
    push eax
    mov eax, [ebp + 4 * 2]
    mov cr3, eax ; 放入页目录表地址
    mov eax, cr0
    or eax, 0x80000000 ;31位变成1
    mov cr0, eax           ; 置PG=1，开启分页机制
    pop eax
    pop ebp
    ret
```



## 4.实验结果

成功分配和释放内存

```c++
    int p1=memoryManager.allocatePhysicalPages(AddressPoolType::KERNEL,3);
    printf("allocate 3 pages,address:%x\n",p1);
    int p2=p1+PAGE_SIZE;
    memoryManager.releasePhysicalPages(AddressPoolType::KERNEL,p2, 1);
    printf("release a page,address:%x\n",p2);
    int p3=memoryManager.allocatePhysicalPages(AddressPoolType::KERNEL,1);
    printf("allocate a pages,address:%x\n",p3);
```

![image-20240524182909779](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240524182909779.png)

## 5.总结

开启分页机制后物理内存图解：

![image-20240524182305328](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240524182305328.png)

# Assignment2

## 1.实验要求：

参照理论课上的学习的物理内存分配算法如first-fit, best-fit等实现动态分区算法等，或者自行提出自己的算法。这里实现first-fit动态分区

## 2.实验过程：

**1.** 实现和初始化存储内存中孔（分区）的信息的数据结构（<code>Fit_List</code>链表），构建管理分区的类<code>First_fit</code> 

**2. **实现<code>first_fit</code>算法，分配<code>Fit_List::allocate(int size)</code>和释放<code>Fit_List::release(int start_address,int size)</code>

**3.** 测试算法，尝试在内存分区中分配和释放空洞

## 3.关键代码：

**3.1.1** 实现和初始化<code>Fit_List</code>：

* 链表节点<code>Fit_ListItem</code>: 

  每个链表节点代表内存中的一个分区，里面保存分区的开始地址，大小，是否被分配

  ```C++
  struct Fit_ListItem
  {
      int begin_address; //空闲孔开始地址
      int size; //空闲孔的大小
      int is_allocate;//是否被分配，0为未被分配，1为被分配
      Fit_ListItem *previous;
      Fit_ListItem *next;
  };
  ```

* 分区链表<code>Fit_List</code>的初始化：

  预先在全局中分配100个孔洞分区对象<code>Fit_Item item[100]</code>，初始化链表头节点和<code>item[100]</code>

  ```c++
  Fit_ListItem item[100];//全局变量，避免局部变量被释放
  void Fit_List::initialize()
  {
      head->next = head->previous = 0;//有头节点的
      head->size=0; 
      //初始化孔洞表
      for(int i=0;i<100;i++){
          item[i].begin_address=-1;
          item[i].is_allocate=0;
          item[i].previous=0;
          item[i].next=0;
      }
  }
  ```

**3.1.2** 实现和初始化<code>First_fit</code>：

* <code>First_fit</code>数据结构：

  * 类成员：保存维护分区信息的链表<code>resources</code>, 管理的连续内存分区的开始地址<code>startAddress</code>, <code>resources</code>的头节点<code>start</code>, <code>resources</code>的第一个节点<code>one</code>

  *  类成员函数: 

    <code>initialize</code>: 初始化动态分区管理类，参数为管理的连续内存的开始地址和长度

    <code>allocate</code>: 分配一个size大小的分区

    <code>release</code>: 释放一个指定开始地址的指定大小的分区

  * 为什么会有<code>start</code>成员：

    由于在内存管理中需要通过<code>resources</code>分配，我们需要指定和保存<code>resources</code>的地址信息，这个start节点就是为了记录下<code>resources</code>的地址信息

```c++
class First_fit
{
public:
    Fit_List resources;
    int startAddress;
    Fit_ListItem start;//
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
```

* 初始化<code>First_fit</code>:

  在resources中建立一个分区节点，代表一开始没有分配还是一整块连续分区的整块被管理的连续内存  

  ```C++
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
  ```


**3.2**分区的分配与释放

* 分区的分配：

  在<code>resources</code>链表中查找到第一个能装申请空间且未被分配的空洞 

  ```c++
  Fit_ListItem* Fit_List::find_fit(int size)
  {
      int pos = 0;
      Fit_ListItem *temp = head->next;
      while (temp&&(temp ->size<size ||temp->is_allocate==1 ))
      {
          temp = temp->next;
          ++pos;
      }
      if (temp && temp->size>=size && temp->is_allocate==0)
      {
          return temp;
      }
      else
      {
          return  0;
      }
  }
  ```

  如果分配的孔洞比申请的空间还要大，会产生内部碎片，需要在<code>resources</code>中插入新的分区节点。

  ```c++
  int Fit_List::allocate(int size)
  {
      Fit_ListItem* itemPtr=find_fit(size);
      while(itemPtr==0){
          itemPtr=find_fit(size);
      }//分配到孔和位置
      int hole_size=itemPtr->size;
      if(hole_size==size){
          itemPtr->is_allocate=1;
          return itemPtr->begin_address;
      }
      else{
         //生成一个新的孔
          Fit_ListItem* new_hole=find_hole();//在已经初始化好的分区节点对象中挑选一个改造插入
         new_hole->begin_address=itemPtr->begin_address+size;
         new_hole->size=hole_size-size;
         new_hole->previous=itemPtr;
         new_hole->next=itemPtr->next;
         itemPtr->next=new_hole;
         (new_hole->next)->previous=new_hole;
         new_hole->is_allocate=0;
         itemPtr->is_allocate=1;
         itemPtr->size=size;
         return itemPtr->begin_address;
      }
  }
  int First_fit::allocate(const int size)
  {
      resources.allocate(size);
  }
  ```

* 分区的释放：

  参数：释放的分区的起始地址，释放的空间大小

  实现：在<code>resources</code>中找到要释放分区所在节点，处理好释放时产生的碎片和释放后与前后空闲分区的合并

  ```c++
  void Fit_List::release(int start_address,int size){
      Fit_ListItem* itemPtr=find_release(start_address);
      if (itemPtr==0){
        printf("error\n");
      }
      if(itemPtr->size<size){
          printf("error\n");
      }
      itemPtr->is_allocate=0;
      Fit_ListItem* previous=itemPtr->previous;
      Fit_ListItem* next=itemPtr->next;
      Fit_ListItem* new_hole=find_hole();
      if(itemPtr->size==size){//无碎片
      if(previous==head){
          itemPtr->is_allocate=0;
      }
      else if(previous->is_allocate==0){//与前面分区合并
          itemPtr->begin_address=previous->begin_address;
          itemPtr->size=itemPtr->size+previous->size;
          erase(previous);
      }
        if(next&&next->is_allocate==0){//与后面分区合并
          itemPtr->size=itemPtr->size+next->size;
          erase(next);
      }  
      }
      else{ //有碎片
          //合并
          if(previous!=head&&previous->is_allocate==0){
              previous->size=size+previous->size;
              //更新
              itemPtr->is_allocate=1;
              itemPtr->begin_address=itemPtr->begin_address+size;
              itemPtr->size=itemPtr->size-size;
          }else{
              new_hole->begin_address=itemPtr->begin_address;
              new_hole->size=size;
              new_hole->is_allocate=0;
              itemPtr->is_allocate=1;
              itemPtr->begin_address=itemPtr->begin_address+size;
              itemPtr->size=itemPtr->size-size;   
              new_hole->previous=previous;
              new_hole->next=itemPtr;
              previous->next=new_hole;
              itemPtr->previous=new_hole;         
          }
      }
  }
  void First_fit::release(const int address,int size)
  {
      resources.release(address,size);
  }
  ```

  

## 4.实验结果：

* 测试：

初始化：管理126MB和起始地址为0的连续内存

分配：分配一个大小为3的分区

释放：释放一个起始地址为0，大小为1的内存分区

```c++
    first_fit.initialize(126,0);
	printf("before allocate:\n");
    first_fit.print();
    printf("\nallocate 3\n");
    first_fit.allocate(3);
    first_fit.print();
    printf("\nrelease 3\n");
    first_fit.release(0,1);
    first_fit.print();
```

* 结果：

  ![image-20240524091056473](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240524091056473.png)

## 5.总结

* 注意：<code>resources</code>中新的节点不能在直接在分配函数中定义生成，不然，节点将会是局部变量，离开函数后就会释放掉，节点的数据将会无法预测。所以一开始就初始化好一个<code>item[100]</code>全局变量，生成新节点时从其中获取。

* 补充图解：

  ![image-20240524093215176](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240524093215176.png)



# Assignment3

## 1.实验要求：

参照理论课上虚拟内存管理的页面置换算法如FIFO、LRU等，实现页面置换。

## 2.实验过程：

在内核的虚拟内存中实现空闲池版FIFO：

1. 创建：基于虚拟内存创建空闲池，空闲池的数据结构为用链表实现的队列（  [为什么基于虚拟内存实现](#test2)）

2. 置换：从空闲池的队头处选择页面释放置换，置换后对应的物理页地址不变，该物理页仍然需要在空闲池中，所以将对应的物理页压入队尾。

3. 图解：

   ![image-20240524120031767](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240524120031767.png)

## 3.关键代码：

**3.1创建：**

* 数据结构：(见注释)

  ```C++
  List FIFO;//FIFO空闲帧池，最大为66个帧，初始化的时候只需要给出需要空闲帧池的虚拟起始地址
  struct ListItem//空闲帧池中的页
  {
      ListItem *previous;
      ListItem *next;
      int start_address;//物理页映射的虚拟页起始地址
  };
  class List
  {
  public:
      ListItem head;
  }
  ```

* 初始化：

  选定一块连续的66页虚拟内存对应的物理页创建空闲帧池

  ```C++
  void MemoryManager::init_FIFO(int start_address){//传进来的是虚拟地址
     for (int i=0;i<66;i++){
      item[i].start_address=start_address+PAGE_SIZE*i;
      FIFO.push_back(&item[i]);
     }
     printf("initialize the free page pool successfully!\n the size:66 pages  the start address:%x\n",start_address );
  }
  ```

**3.2置换**

释放队头虚拟页对应的物理页，并且置页表项无效（页表项的有效位在最低位）。置换后的页更新映射虚拟页，并将其从队头移动到队尾

```C++
void MemoryManager::displace_page(int count,int vaddr){//只是针对内核的，用户还没实现
    for(int i=0;i<count;i++){
        ListItem* tmp=FIFO.front();
        releasePages_FIFO(KERNEL,tmp->start_address,1);
        FIFO.pop_front();
        FIFO.push_back(tmp);
        printf("for displacing,a page(virtual start_address:%x  physical_address:%x) releases\n",tmp->start_address,vaddr2paddr(tmp->start_address));
        tmp->start_address=vaddr;
    }
}
void MemoryManager::releasePages_FIFO(enum AddressPoolType type, const int virtualAddress, const int count)
{
    int vaddr = virtualAddress;
    int *pte;
    for (int i = 0; i < count; ++i, vaddr += PAGE_SIZE)
    {
        // 第一步，对每一个虚拟页，释放为其分配的物理页
        releasePhysicalPages(type, vaddr2paddr(vaddr), 1);

        // 设置页表项为无效，防止释放后被再次使用
        pte = (int *)toPTE(vaddr);
        *pte = *pte&0xfffffffe;
    }
}
```

**3.3总置换流程**

1. 申请到虚拟页后，逐页申请物理页（<code> MemoryManager::allocatePages</code>）

```c++
        flag = false;
        // 第二步：从物理地址池中分配一个物理页//由于物理页是不连续的，所以可以一个一个分
        physicalPageAddress = allocatePhysicalPages(type, 1,vaddress);
        if (physicalPageAddress)
        {
            //printf("allocate physical page 0x%x\n", physicalPageAddress);

            // 第三步：为虚拟页建立页目录项和页表项，使虚拟页内的地址经过分页机制变换到物理页内。
            flag = connectPhysicalVirtualPage(vaddress, physicalPageAddress);
        }
```

2. 申请物理页时，遇到无空闲物理页的情况,进行页面置换，释放页再分配(<code>MemoryManager::allocatePhysicalPages</code>)

   ```C++
       if (type == AddressPoolType::KERNEL)
       {
           start = kernelPhysical.allocate(count);
           while(start==-1&&count==1){//专门针对情况
                   displace_page(1,vaddr);//置换
                   start = kernelPhysical.allocate(count);//重新分配
           }
       }
   ```

## 4.实验结果：

1. 测试：

   经过测试，内核的物理空间最多分配15969页

   p1分配了15969页后，内核的物理空间将无空闲页

   p2想要申请五页时，需要从空闲池置换，空闲池的物理页映射的虚拟页开始地址初始化0xc0100000，则p2会置换掉0xc0100000开始的五个虚拟页的物理页

   ```c++
       memoryManager.init_FIFO(0xc0100000);
      	char *p1 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 15969);
       char *p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 5);
       printf("%x %x \n", p1,p2);
   ```

2. 结果：

   置换了0xc0100000开始的五个虚拟页的物理页，和预测符合

   ![image-20240524123541516](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240524123541516.png)

## 5.总结：

1. 由于物理内存中没有空闲帧，所以需要将挑选内存的部分物理页换出置换，将被置换的物理页对应的虚拟页的页表条目记录为无效，并将被置换的物理页分配给其他虚拟页。如果在物理内存没有空闲帧的情况下申请了连续的多个虚拟页空间，由于虚拟页和物理页是分离的，虚拟页连续物理页可以不连续，所以可以在物理内存中置换出不连续的页，但是映射到连续的虚拟空间中。上述操作都是从物理内存的角度去考虑页面置换，为什么在实现的FIFO直接对已经分配好的虚拟页进行操作，而不是物理页？<a id="test2">跳转锚点</a>

   * **合理性：**因为物理页与虚拟页是映射关系，所以可以通过对虚拟页的操作间接操作物理页。基于虚拟页建立空闲池，其实是对虚拟页映射的物理页建立空闲帧池。进行置换时，对空闲帧池中物理页的释放可以变成对空闲池中虚拟页的”释放“。但是需要注意对虚拟页的”释放“，是把和它对应的物理页解绑，先把物理页的内容写入磁盘，然后将页表项置为无效。

   * **优点：**基于虚拟地址建立很快就能找到页表项，修改页表项，不然还需要根据物理地址遍历页表找到页表项修改更新。而且开启分页机制后，程序面对的是虚拟地址，这样操作起来更方便。

   * **注意：**这里是将页表项有效位置为0而不是直接整个页表项清0。有效位置0代表虚拟地址还在，但是访问的时候会出现缺页错误，需要从磁盘调页，如果直接将页表项清0是程序释放了这段内存，虚拟内存也没有了。

       每次置换后池内页的虚拟页地址会变化，物理页地址不变。由于是基于虚拟页地址进行操作的，所以置换后要把池内页的虚拟页地址进行更新，更新为物理页现在映射的虚拟页，保证池内空闲帧的不变

2. 实现中遇到的bug：

   开始实验实现是基于给出的虚拟内存管理<code>src/5</code> ,**在这里面给内核分配的物理内存和虚拟内存一样大。如果出现物理帧不够的情况，也意味着虚拟内存不够。**如果按照理论将物理页置换，保留虚拟页，将页表项置为无效，即使把整个空闲池释放掉，还是会由于虚拟空间不足没有办法分配空间。

   改进：把虚拟页的页数设置的比物理页大

   ![image-20240524103105174](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240524103105174.png)
