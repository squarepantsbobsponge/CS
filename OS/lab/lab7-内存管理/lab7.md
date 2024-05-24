 

![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科

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

  预先在全局中分配100个孔洞分区<code>Fit_Item item[100]</code>，初始化链表头节点和<code>item[100]</code>

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

  

## 4.实验结果：

## 5.总结

