 

![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科



[TOC]



# Assignment1

## 1.实验要求

编写一个系统调用，然后在进程中调用之，根据结果回答以下问题。

* 展现系统调用执行结果的正确性，结果截图且说明实现思路。
* 请根据gdb来分析执行系统调用后的栈的变化情况。
* 请根据gdb来说明TSS在系统调用执行过程中的作用。

## 2.实验过程

1. 实现系统调用
   * 实现系统调用服务类，初始化系统调用表
   * 实现系统调用入口函数
   * 实现系统调用处理函数
2. 实现用户进程：
   * 进程创建前的准备：在跳转到内核前开启分页机制，将内核的虚拟地址提升到3GB-4GB
   * 初始化TSS和用户段描述符
   * 进程创建：创建PCB，初始化页目录表，初始化虚拟池
   * 进程调度
3. 添加print系统调用
4. gdb调试（在实验结果中）

## 3.关键代码

**3.1实现系统调用**

* 实现系统调用服务类：

  * 设置系统调用表：<code>system_call_table</code>表项为各种系统调用的处理函数
  * 系统调用服务类的初始化：<code>initialize()</code>初始化系统调用表，且为系统调用中断0x80设置中断描述符。中断描述符的DPL描述需要的特权级，设置为3，能让用户进程调用。
  * 系统调用的设置：<code>setSystemCall</code>将系统调用的处理执行函数放入到系统调用表对应索引位置

  ```c++
  int system_call_table[MAX_SYSTEM_CALL];
  
  SystemService::SystemService() {
      initialize();
  }
  
  void SystemService::initialize()
  {
      memset((char *)system_call_table, 0, sizeof(int) * MAX_SYSTEM_CALL);
      // 代码段选择子默认是DPL=0的平坦模式代码段选择子，DPL=3，否则用户态程序无法使用该中断描述符
      interruptManager.setInterruptDescriptor(0x80, (uint32)asm_system_call_handler, 3);
  }
  
  bool SystemService::setSystemCall(int index, int function)
  {
      system_call_table[index] = function;
      return true;
  }
  ```

* 实现系统调用入口函数<code>asm_system_call</code>:

  * 说明：可以由用户进程直接调用，提供一个处理所有系统调用的接口，提供一些系统调用前的准备，如保护当前进程的现场。执行时用户进程仍然会在特权级3，未跳转到内核态

  * 步骤: 保护现场，转移系统调用参数到寄存器，通过0x80中断跳转系统调用服务函数，系统调用结束返回恢复现场

  * 注意：用户进程传入的系统调用参数在这里要进一步处理，一般由C++函数传入汇编函数的参数是在栈上取得，但是这里需要将栈上的参数暂时转移到寄存器再传入系统调用服务函数。经过中断跳入0x80的中断函数也就是系统调用服务函数时，tss自动加载，此时已经从用户态转为内核态了，栈已经从用户栈转为内核栈，参数是无法再从用户栈获得了

    ```assembly
    	asm_system_call:
    	    push ebp
    	    mov ebp, esp
    	    push ebx
    	    push ecx
    	    push edx
    	    push esi
    	    push edi
    	    push ds
    	    push es
    	    push fs ;保存现场
    	    push gs
    	    mov eax, [ebp + 2 * 4] ;保存系统调用号
    	    mov ebx, [ebp + 3 * 4] ;保存五个参数
    	    mov ecx, [ebp + 4 * 4]
    	    mov edx, [ebp + 5 * 4]
    	    mov esi, [ebp + 6 * 4]
    	    mov edi, [ebp + 7 * 4]
    	    int 0x80 ;调用0x80，会根据eax的系统调用号来调用不同的函数
    	    pop gs  ;恢复现场
    	    pop fs
    	    pop es
    	    pop ds
    	    pop edi
    	    pop esi
    	    pop edx
    	    pop ecx
    	    pop ebx
    	    pop ebp
    	    ret
    ```

* 0x80中断对应的系统处理函数

  * <a id="preface">为什么用中断的形式实现系统调用</a>

    * 用户进程系统调用涉及到特权转换，系统调用的处理都在内核态

    * 中断处理提供特权转换

      1.通过中断向量找到中断描述符

      2.处理器会检查中断描述符中的DPL是否满足条件（目标代码段DPL<=CPL&&CPL<=中断描述符DPL）

      3.检查通过后，处理器加载目标代码段的选择子到CS，包含RPL（请求特权级），特权级转换

      4.中断服务处理结束后，iret返回且切换回原来的特权

      （0x80的中断描述符的DPL设置为3，在前面实验中内核的段选择子的RPL都默认被设置为0）

  * 步骤：

    1.保护内核态跳转真正的系统调用处理函数前的现场

    2.修改特权级转换后的ds，es，fs，gs寄存器

    3.将<code>asm_system_call</code>放在寄存器中传入的参数压栈，通过栈传到系统调用处理函数

    4.根据系统调用号在系统调用表中找函数地址跳转执行

    5.恢复现场，且将系统调用处理函数的返回值放在eax中

  ```assembly
  asm_system_call_handler:
      push ds
      push es
      push fs
      push gs
      pushad
      push eax
      ; 栈段会从tss中自动加载
      mov eax, DATA_SELECTOR
      mov ds, eax
      mov es, eax
      mov eax, VIDEO_SELECTOR
      mov gs, eax
      pop eax
      ; 参数压栈
      push edi
      push esi
      push edx
      push ecx
      push ebx
      sti    
      call dword[system_call_table + eax * 4]
      cli
      add esp, 5 * 4
      mov [ASM_TEMP], eax
      popad
      pop gs
      pop fs
      pop es
      pop ds
      mov eax, [ASM_TEMP]
      
      iret
  ```

**3.2实现用户进程**

* 初始化TSS和用户段描述符

  1. 初始化用户段描述符

     段描述符：

  

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607104628539.png" alt="image-20240607104628539" style="zoom:50%;" />

  ​	段选择子：

  ​	<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607104719903.png" alt="image-20240607104719903" style="zoom:50%;" />

  

  ```C++
      int selector;
  
      selector = asm_add_global_descriptor(USER_CODE_LOW, USER_CODE_HIGH);
      USER_CODE_SELECTOR = (selector << 3) | 0x3; 
  
      selector = asm_add_global_descriptor(USER_DATA_LOW, USER_DATA_HIGH);
      USER_DATA_SELECTOR = (selector << 3) | 0x3;
  
      selector = asm_add_global_descriptor(USER_STACK_LOW, USER_STACK_HIGH);
      USER_STACK_SELECTOR = (selector << 3) | 0x3;
  
  ```

  ```assembly
  	;添加段描述符
  	asm_add_global_descriptor:
  	    push ebp
  	    mov ebp, esp
  	    push ebx
  	    push esi
  	    sgdt [ASM_GDTR]  ;将GDTR的内容读到ASM_GDTR中
  	    mov ebx, [ASM_GDTR + 2] ; GDT地址，ASM——GDTR移动高2两个字节，读取32位的GDT地址
  	    xor esi, esi
  	    mov si, word[ASM_GDTR] ; GDT界限，读取16位的界限
  	    add esi, 1
  	    mov eax, [ebp + 2 * 4] ; low  用户段描述符低32位
  	    mov dword [ebx + esi], eax ;把段描述符写入
  	    mov eax, [ebp + 3 * 4] ; high，用户段描述符高32位
  	    mov dword [ebx + esi + 4], eax ;把段描述符写入
  	    mov eax, esi
  	    shr eax, 3  ;计算段描述符在段表中偏移，这个变成返回数据，是基于段描述符一个一个的索引，右移3位表示除8，一个段描述符8个字节
  	    add word[ASM_GDTR], 8
  	    lgdt [ASM_GDTR]
  	    pop esi
  	    pop ebx
  	    pop ebp
      ret
  ```

   2. 初始化TSS

      * TSS作用：保存和恢复关键寄存器栈信息，支持特权级的安全切换
      * 内容：不同特权级的栈基地址寄存器ss，和栈顶地址寄存器，还有其他的重要寄存器保护特权级切换时的现场（代码略）

      * 初始化：

        ```c++
        void ProgramManager::initializeTSS()
        {
        
            int size = sizeof(TSS);
            int address = (int)&tss;//TSS地址
        
            memset((char *)address, 0, size);
            tss.ss0 = STACK_SELECTOR; // 内核态堆栈段选择子
        
            int low, high, limit;
        
            limit = size - 1;
            low = (address << 16) | (limit & 0xff); //段基地址+界限
            // DPL = 0   段基地址高8位              中8位                           段界限3位              段相关设置位
            high = (address & 0xff000000) | ((address & 0x00ff0000) >> 16) | ((limit & 0xff00) << 16) | 0x00008900;
        
            int selector = asm_add_global_descriptor(low, high);//段描述符写入
            // RPL = 0
            asm_ltr(selector << 3);//tss段选择子写入TR寄存器，处理器特权切换时自动加载TR寄存器里面的tss
            tss.ioMap = address + size;//
        }
        ```

* 进程的创建：

  1. 总：创建进程的PCB，用户进程还需要在内核线程的基础上增加用户空间中的页目录表和用户空间虚拟地址池

  ```C++
  int ProgramManager::executeProcess(const char *filename, int priority)
  {
      bool status = interruptManager.getInterruptStatus();
      interruptManager.disableInterrupt();
      // 在线程创建的基础上初步创建进程的PCB
      int pid = executeThread((ThreadFunction)load_process,
                              (void *)filename, filename, priority);//先像创建一个线程一样创建进程，线程函数是load_process
      if (pid == -1)
      {
          interruptManager.setInterruptStatus(status);
          return -1;
      }
      // 找到刚刚创建的PCB
      PCB *process = ListItem2PCB(allPrograms.back(), tagInAllList);
      // 创建进程的页目录表
      process->pageDirectoryAddress = createProcessPageDirectory();
      if (!process->pageDirectoryAddress)
      {
          process->status = ProgramStatus::DEAD;
          interruptManager.setInterruptStatus(status);
          return -1;
      }    
      // 创建进程的虚拟地址池
      bool res = createUserVirtualPool(process);
  
      if (!res)
      {
          process->status = ProgramStatus::DEAD;
          interruptManager.setInterruptStatus(status);
          return -1;
      }
      interruptManager.setInterruptStatus(status);
      return pid;
  }
  
  ```

  2. 创建页目录表：

     * 创建原因：进程有自己的虚拟地址空间和分页机制

     * 注意<a id="preface2">2</a>：定义好用户的虚拟空间地址3-4GB和内核的虚拟空间地址3-4GB时共享的，需要将用户的虚拟地址映射到内核上，使进程在用户进程的用户空间虚拟地址和内核虚拟地址不冲突的情况下能够访问到内核资源。（**用户进程进入内核态后用的还是自己的虚拟地址空间，根据用户进程的页目录表转换物理地址而不是根据内核的页目录表，如果虚拟地址为0-3GB访问的还是用户地址空间，但是为3GB-4GB时访问的是内核地址空间0。为什么用户进程进到内核能无障碍访问，也是因为内核空间定义的时候，也是将虚拟地址映射到了3GB-4GB，并且内核虚拟地址3GB-4GB和用户的映射的物理内容相同。**）

     * 操作：用户进程页目录表的第768项到第1022项和内核页目录表的第768项到第1022项一致

     ```c++
     int ProgramManager::createProcessPageDirectory()
     {
         // 从内核地址池中分配一页存储用户进程的页目录表
         int vaddr = memoryManager.allocatePages(AddressPoolType::KERNEL, 1);
         if (!vaddr)
         {
             //printf("can not create page from kernel\n");
             return 0;
         }
     
         memset((char *)vaddr, 0, PAGE_SIZE);
     
         // 复制内核目录项到虚拟地址的高1GB
         //现在还是在内核态中，用的是内核虚拟地址，0xfffff000是内核页目录的起始地址
         int *src = (int *)(0xfffff000 + 0x300 * 4);//0x300大小为768，目的要将内核目录表的768项到最后（3-4GB）复制给用户页目录表的（3-4GB），打通内核与用户共享
         int *dst = (int *)(vaddr + 0x300 * 4);
         for (int i = 0; i < 256; ++i)
     
         {
             dst[i] = src[i];
         }
     
         // 用户进程页目录表的最后一项指向用户进程页目录表本身
         ((int *)vaddr)[1023] = memoryManager.vaddr2paddr(vaddr) | 0x7;//用户页目录表本身在内核地址池中
     
         return vaddr;
     }
     ```

  3. 创建虚拟地址池

     ```C++
     bool ProgramManager::createUserVirtualPool(PCB *process)
     {
         int sourcesCount = (0xc0000000 - USER_VADDR_START) / PAGE_SIZE; //计算出用户虚拟空间所占页
         int bitmapLength = ceil(sourcesCount, 8);
         // 计算位图所占的页数
         int pagesCount = ceil(bitmapLength, PAGE_SIZE);
             //分配位图所需空间，也是从kernel中分，但是不需要报备用户页目录表的（用户空间的情况）
         int start = memoryManager.allocatePages(AddressPoolType::KERNEL, pagesCount);
         if (!start)
         {
             return false;
         }
         //初始化位图分配得到的空间
         memset((char *)start, 0, PAGE_SIZE * pagesCount);
         //初始化地址池
         (process->userVirtual).initialize((char *)start, bitmapLength, USER_VADDR_START);
     
         return true;
     }
     ```

  4. 进程启动时的加载函数<code>load_process</code>

     * 注意：这里也涉及到特权级的转换，<code>load_process</code>是为了完成这个特权转换的过程。

     * 步骤：将用户进程用户态的相关信息先保存在<code>interruptStack </code>中，跳转到<code>asm_start_process</code>中根据<code>interruptStack</code> 更新寄存器，通过<code>iret</code>返回切换特权级且执行用户进程函数。<code>interruptStack</code>应该是挂靠在进程PCB的特权级0栈

       ```C++
       void load_process(const char *filename)//filename是要跳转执行的某个函数的地址，这里简化了从磁盘加载程序
       {
           interruptManager.disableInterrupt();
       
           PCB *process = programManager.running;
           ProcessStartStack *interruptStack =
               (ProcessStartStack *)((int)process + PAGE_SIZE - sizeof(ProcessStartStack));
       
           interruptStack->edi = 0;
           interruptStack->esi = 0;
           interruptStack->ebp = 0;
           interruptStack->esp_dummy = 0;
           interruptStack->ebx = 0;
           interruptStack->edx = 0;
           interruptStack->ecx = 0;
           interruptStack->eax = 0;
           interruptStack->gs = 0;
       
           interruptStack->fs = programManager.USER_DATA_SELECTOR;
           interruptStack->es = programManager.USER_DATA_SELECTOR;
           interruptStack->ds = programManager.USER_DATA_SELECTOR;   //初始化栈
       
           interruptStack->eip = (int)filename;
           interruptStack->cs = programManager.USER_CODE_SELECTOR;   // 用户模式平坦模式
           interruptStack->eflags = (0 << 12) | (1 << 9) | (1 << 1); // IOPL, IF = 1 开中断, MBS = 1 默认
       
           interruptStack->esp = memoryManager.allocatePages(AddressPoolType::USER, 1);
           if (interruptStack->esp == 0)
           {
               printf("can not build process!\n");
               process->status = ProgramStatus::DEAD;
               asm_halt();
           }
           interruptStack->esp += PAGE_SIZE;
           interruptStack->ss = programManager.USER_STACK_SELECTOR;
       
           asm_start_process((int)interruptStack); //中断返回进程执行函数
       }
       ```
  
     ```assembly
     asm_start_process:
         ;jmp $
         mov eax, dword[esp+4] ;取出开始栈的起始地址
         mov esp, eax  ;将当前栈转为开始栈
         popad
         pop gs;
         pop fs;
         pop es;
         pop ds;
     
         iret  ;根据开始栈的内容更新寄存器，特权级3的选择子被放入到段寄存器中，代码跳转到进程的起始处执行。
     ```
  
     
  
    5. 进程调度
  
       * 说明：进程和线程调度区别根本在于进程执行时在用户态，需要进程特权级别切换，并且进程有自己的页目录表。则进程切换调度时，不能简单地切换PCB，而是要更新TSS中对应的内核态栈和更新CR3中进程页目录表的地址
  
         ```c++
         void ProgramManager::activateProgramPage(PCB *program)
         {
             int paddr = PAGE_DIRECTORY;
         
             if (program->pageDirectoryAddress)  //如果是用户态进程要加载tts
             {
                 tss.esp0 = (int)program + PAGE_SIZE;
                 paddr = memoryManager.vaddr2paddr(program->pageDirectoryAddress);
             }
         
             asm_update_cr3(paddr);//更新页目录表
         }
         ```
  
         

**3.3.添加系统调用**

添加打印字符串系统调用

```c++
systemService.setSystemCall(1,(int)syscall_1);
int syscall_1(int first, int second, int third, int forth, int fifth){
    char* print=(char*) first;
    printf("%s",print);
}
void first_process()
{
    char* print="hello world\n";
    int help_print=(int)print;
    asm_system_call(0, 132, 324, 12, 124);
    asm_system_call(1,help_print,0,0,0,0);
    asm_halt();
}	
```

## 4.实验结果

1.

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607115623603.png" alt="image-20240607115623603" style="zoom:50%;" />

2.根据gdb来分析执行系统调用后的栈的变化情况和TSS的作用

* 系统调用前：

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607121127731.png" alt="image-20240607121127731" style="zoom: 67%;" />

* 系统调用入口函数：

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607121552504.png" alt="image-20240607121552504" style="zoom:67%;" />

* 系统调用服务函数：TSS重要性在int 0x80中断发生内核态转换时，帮助切换栈和其他信息

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607121949443.png" alt="image-20240607121949443" style="zoom:67%;" />

* 调用系统处理函数返回：

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607122516071.png" alt="image-20240607122516071" style="zoom:67%;" />

* iret中断返回，返回到系统调用入口函数：特权级切换回用户态

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607122840268.png" alt="image-20240607122840268" style="zoom:67%;" />

* 系统调用返回：

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607123005699.png" alt="image-20240607123005699" style="zoom:67%;" />

* TSS作用：

  每次特权级切换，处理器从TSS中加载出对应特权级的栈信息

## 5.总结

* 为什么中断会导致特权级的切换：<a href="#preface">前文跳转</a>

* 为什么需要把用户进程的3GB-4GB映射到内核：<a href="#preface2">前文跳转2</a>

* 特权级切换实现：

  * 系统调用：通过中断和中断返回实现，调用0x80时就已经自动加载TSS转换0特权栈和段选择子了

    (这里的特权栈0就是挂载在进程PCB上面的初始栈（具体见下面用户进程调度特权级跳转），但是在用户进程调度时特权级0栈在<code>load_process</code>里初始化满了用户态的信息，但是在<code>asm_start_process</code>里又全部pop出去了，现在这个栈是干净的)

  * 用户进程调度特权级跳转：

    * 进程调度时先进到<code>activateProgramPage</code>，先把特权级0栈指定到进程PCB的开始（<code> tss.esp0 = (int)program + PAGE_SIZE;</code>）

    * 然后到<code> asm_switch_thread</code>切换进程，跳转到被调度进程的函数地址<code>load_process</code>执行（什么时候指定的：在<code>executeProcess</code>中调用<code>executeThread</code>指定的）

    * 在<code>load_process</code>中，先初始化了PCB的初始栈<code>interruptStack</code>（其实就是前面指定挂靠的特权0栈（<code>ProcessStartStack *interruptStack =(ProcessStartStack *)((int)process + PAGE_SIZE - sizeof(ProcessStartStack));）</code>），然后跳转到<code> asm_start_process</code>

    * 在<code>asm_start_process</code>中把实现的初始栈也就是特权0栈的内容全部弹出，iret返回切换用户态

      （iret为什么能切换回用户态：在<code>asm_start_process</code>已经把当前的栈<code>esp</code>转到初始栈的位置了，iret会将当前栈的段地址和偏移地址弹出（会恢复CS，IP，EFLAGS等等），而这些关于段的寄存器已经在初始栈变更为用户态下的了。iret可以到用户态去）

# Assignment2

## 1.实验要求

* 请根据代码逻辑和执行结果来分析fork实现的基本思路。
* 从子进程第一次被调度执行时开始，逐步跟踪子进程的执行流程一直到子进程从`fork`返回，根据gdb来分析子进程的跳转地址、数据寄存器和段寄存器的变化。同时，比较上述过程和父进程执行完`ProgramManager::fork`后的返回过程的异同。
* 请根据代码逻辑和gdb来解释fork是如何保证子进程的`fork`返回值是0，而父进程的`fork`返回值是子进程的pid。

## 2.实验过程

1. fork()实现

   * 添加fork()系统调用（同Assignment1添加，具体看fork函数的实现）

   * 创建子进程

   *  复制父进程的资源到子进程：0特权级栈，PCB，虚拟地址池，页目录表，页表及其指向的物理页

2. GDB调试（实验结果中）

## 3.关键代码

**3.1总：fork()函数**

* 创建子进程：没有为子进程传入进程函数，后续可以将子进程的内核PCB栈中的函数地址改为父进程的进程函数地址

* 子进程初始化：为子进程复制父进程资源

```c++
int ProgramManager::fork()
{
    bool status = interruptManager.getInterruptStatus();
    interruptManager.disableInterrupt();
    // 禁止内核线程调用
    PCB *parent = this->running;
    if (!parent->pageDirectoryAddress)//内核线程没有这个
    {
        interruptManager.setInterruptStatus(status);
        return -1;
    }
    // 创建子进程
    int pid = executeProcess("", 0); //创建子进程时，没有传入子进程的函数，准备直接copy父进程的
    if (pid == -1)
    {
        interruptManager.setInterruptStatus(status);
        return -1;
    }
    // 初始化子进程
    PCB *child = ListItem2PCB(this->allPrograms.back(), tagInAllList);
    bool flag = copyProcess(parent, child);//资源复制
    if (!flag)
    {
        child->status = ProgramStatus::DEAD;
        interruptManager.setInterruptStatus(status);
        return -1;
    }
    interruptManager.setInterruptStatus(status);
    return pid;
}

```

**3.2父进程资源的复制<code>copyProcess(parent,child)</code>：**

**3.2.1父进程0特权栈的复制和子进程内核PCB栈的初始化：**

* 0特权栈的复制：

  * 为什么：这样可以使得父子进程从相同的返回点开始执行，要找到相同的返回点就要找到父进程系统调用中断前的相关信息，下面分析父进程系统调用中断前的相关信息在哪里：

    在初始化tss时已经将tss的段选择子写入了CPU自动读取的寄存器中，tss中包含了0特权级栈的地址。父进程系统调用的<code>asm_system_call_handler</code>中，CPU自动通过寄存器加载出了tss中的0级特权级栈，并且将中断前的相关信息送入栈中(<code>pushad</code>,还包含<code>eip</code>寄存器)。

    那么就是要找到0级特权栈在哪里，就可以获得相关信息，复制到子进程的启动栈中（存储启动的相关信息）。然后子进程启动时<code>asm_start_process</code>将启动栈内容加载入相关寄存器，iret返回后就能和父进程在相同的返回点开始执行。

  * 怎么做：

    * 找到tss的0特权栈：在<code>activateProgramPage</code>中可以看到<code>tss.esp0 = (int)program + PAGE_SIZE;</code>每次调度进程前会将tss的0特权栈放到要激活进程的PCB的顶部，自顶向下拓展。

      那么激活调度父进程前就将0特权栈放在了父进程PCB的顶部，直接可以到父进程PCB的顶部找到0特权栈

    * 0特权栈的结构和启动栈一样，将在父进程PCB中的0特权栈复制到子进程PCB的相同位置中

      ```c++
      // 复制进程0级栈
      ProcessStartStack *childpss =(ProcessStartStack *)((int)child + PAGE_SIZE - sizeof(ProcessStartStack));//
      ProcessStartStack *parentpss =(ProcessStartStack *)((int)parent + PAGE_SIZE - sizeof(ProcessStartStack));//0特权栈的esp目前位置
      memcpy(parentpss, childpss, sizeof(ProcessStartStack));
      // 设置子进程的返回值为0
      childpss->eax = 0；
      ```

* 子进程PCB内核栈的初始化

  * PCB中还有一个栈保存内核函数调用的局部变量、返回地址等信息，用于支持内核函数的执行。为了能让子进程能够成功加载执行要将内核栈的函数地址初始化为<code>asm_start_process</code>，传入参数为刚刚复制的0特权栈<code>childpss</code>。

    ```
        // 准备执行asm_switch_thread的栈的内容
        child->stack = (int *)childpss - 7;
        child->stack[0] = 0;
        child->stack[1] = 0;
        child->stack[2] = 0;
        child->stack[3] = 0;
        child->stack[4] = (int)asm_start_process;//asm_start_process的参数是要用的栈的地址
        child->stack[5] = 0;             // asm_start_process 返回地址
        child->stack[6] = (int)childpss; // asm_start_process 参数
    ```

**3.2.2复制虚拟地址池**

* 设置子进程PCB

  ```c++
      child->status = ProgramStatus::READY;
      child->parentPid = parent->pid;
      child->priority = parent->priority;
      child->ticks = parent->ticks;
      child->ticksPassedBy = parent->ticksPassedBy;
      strcpy(parent->name, child->name);
  ```

* 复制父进程的虚拟地址池的位图

  ```c++
      // 复制用户虚拟地址池
      int bitmapLength = parent->userVirtual.resources.length;
      int bitmapBytes = ceil(bitmapLength, 8);
      memcpy(parent->userVirtual.resources.bitmap, child->userVirtual.resources.bitmap, bitmapBytes)
  ```

* 复制父进程的页目录表

  * 步骤：遍历父进程页目录表的0-768项，查看有效位是否有效，有效则为子进程分配一个物理页，结合父进程页目录表项的索引和子进程对应的映射的物理页构造子进程页目录表项，写入子进程页目录表中，并且初始化这个物理页

  * 为什么只复制0-768页目录项（进程用户空间虚拟地址的0-3GB）？ 

    在用<code>executeProcess</code>创建子进程时，调用了<code>createProcessPageDirectory</code>将768-1023项（3GB-4GB）初始化好了（内核和用户进程的共享内存）

  * 为什么在复制入子进程的页目录表时需要<code>asm_update_cr3</code>切换处理器中虚拟地址对应的页目录表：

    因为将一个页表项复制入子进程后，需要对这个页表项对应的物理页表初始化，而此时只好通过它在子进程中的虚拟地址定位它，然后进行初始化。

    **为什么进入子进程的虚拟地址空间后还能通过进入前的<code>childpPageDir</code>找到子进程页目录表的位置？进程的页目录表都是在内核地址空间上分配的，而内核地址空间和用户进程虚拟地址的3-4GB是共享的，相同地址映射相同物理页**（也体现了用户3GB-4GB映射的好处）<a id="preface3">3</a>

  ```c++
  	// 子进程页目录表物理地址
      int childPageDirPaddr = memoryManager.vaddr2paddr(child->pageDirectoryAddress);
      // 父进程页目录表物理地址
      int parentPageDirPaddr = memoryManager.vaddr2paddr(parent->pageDirectoryAddress);
      // 子进程页目录表指针(虚拟地址)
      int *childPageDir = (int *)child->pageDirectoryAddress;
      // 父进程页目录表指针(虚拟地址)
      int *parentPageDir = (int *)parent->pageDirectoryAddress;
      // 子进程页目录表初始化
      memset((void *)child->pageDirectoryAddress, 0, 768 * 4);
      // 复制页目录表
      for (int i = 0; i < 768; ++i)//只有0-3GB的需要构造，3-4GB的在创建的时候就映射到内核上了
      {
          // 无对应页表
          if (!(parentPageDir[i] & 0x1))
          {
              continue;
          }
          // 从用户物理地址池中分配一页，作为子进程的页目录项指向的页表
          int paddr = memoryManager.allocatePhysicalPages(AddressPoolType::USER, 1);
          if (!paddr)
          {
              child->status = ProgramStatus::DEAD;
              return false;
          }
          // 页目录项
          int pde = parentPageDir[i];//先完全复制页表项
          // 构造页表的起始虚拟地址
          int *pageTableVaddr = (int *)(0xffc00000 + (i << 12));//对于子进程虚拟地址而言的页表起始地址
          asm_update_cr3(childPageDirPaddr); // 进入子进程虚拟地址空间
          childPageDir[i] = (pde & 0x00000fff) | paddr;//更新页表项的真实物理页地址
          memset(pageTableVaddr, 0, PAGE_SIZE);
          asm_update_cr3(parentPageDirPaddr); // 回到父进程虚拟地址空间
      }
  ```

* 复制页表和物理页

  * 步骤：遍历父进程的每个页表，遍历页表中每个页表项像复制页目录项一样复制到子进程上。对于每个每个页表项对于的物理页数据，先拷贝到中转页上，然后切换子进程虚拟空间时将它拷贝到子进程对于的物理页上。
  * 为什么需要中转页：需要复制的数据在父进程和子进程中的虚拟地址都一样，需要在内核中分配一个中转页，**中转页由于在内核中所以切换了虚拟空间，子进程还是能找到数据的位置**。<a id="preface4">4</a>不然如果直接复制时，切换了子进程的虚拟空间就无法根据数据在父进程的虚拟地址找到数据的物理位置，然后拷贝（也体现了用户3GB到4GB映射的好处）

  ```c++
      //设置中转页
  	char *buffer = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 1);
  	// 复制页表和物理页
      for (int i = 0; i < 768; ++i)
      {
          // 无对应页表
          if (!(parentPageDir[i] & 0x1))
          {
              continue;
          }
          // 计算页表的虚拟地址
          int *pageTableVaddr = (int *)(0xffc00000 + (i << 12));
          // 复制物理页
          for (int j = 0; j < 1024; ++j)
          {
              // 无对应物理页
              if (!(pageTableVaddr[j] & 0x1))
              {
                  continue;
              }
              // 从用户物理地址池中分配一页，作为子进程的页表项指向的物理页
              int paddr = memoryManager.allocatePhysicalPages(AddressPoolType::USER, 1);
              if (!paddr)
              {
                  child->status = ProgramStatus::DEAD;
                  return false;
              }
              // 构造物理页的起始虚拟地址
              void *pageVaddr = (void *)((i << 22) + (j << 12));
              // 页表项
              int pte = pageTableVaddr[j];
              // 复制出父进程物理页的内容到中转页
              memcpy(pageVaddr, buffer, PAGE_SIZE);
              asm_update_cr3(childPageDirPaddr); // 进入子进程虚拟地址空间
              pageTableVaddr[j] = (pte & 0x00000fff) | paddr;
              // 从中转页中复制到子进程的物理页
              memcpy(buffer, pageVaddr, PAGE_SIZE);
              asm_update_cr3(parentPageDirPaddr); // 回到父进程虚拟地址空间
          }
      }
  ```

## 4.实验结果

1. 进程设置：

```c++
void first_process()
{
    int pid = fork();
    if (pid == -1)
    {
        printf("can not fork\n");
    }
    else
    {
        if (pid)
        {
            printf("I am father, fork reutrn: %d\n", pid);
        }
        else
        {
            printf("I am child, fork return: %d, my pid: %d\n", pid, programManager.running->pid);
        }
    }
    asm_halt();
}
```

​	执行结果：父进程成功fork子进程pid为2，子进程被成功调度

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607203538153.png" alt="image-20240607203538153" style="zoom:67%;" />

2. 子进程调度执行

* 准备调度子进程：

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607205048264.png" alt="image-20240607205048264" style="zoom:67%;" />

* asm_switch刚切换完进程，跳转到内核栈中的用户进程地址<code>asm_start_process</code>，此时未加载特权级栈

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607211159196.png" alt="image-20240607211159196" style="zoom:67%;" />

* 特权级栈加载完成，返回地址eip变化，eax返回值为0，堆栈寄存器es和附加段寄存器fs变化，还没用执行iret代码段寄存器和氏锯短寄存器暂时没有变化

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607211707425.png" alt="image-20240607211707425" style="zoom: 80%;" />

* 跳转到执行完0x80中断处理函数的位置，中断返回特权级切换，ds数据寄存器和cs代码段寄存器切换，0特权级栈切换为3特权级栈，返回地址eip也变化了

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607210530321.png" alt="image-20240607210530321" style="zoom:67%;" />

* 返回到fork()函数结束位置：

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607210904199.png" alt="image-20240607210904199" style="zoom: 50%;" />

3. 父进程执行完fork返回：

* 父进程准备执行完fork(): 返回值eax为2

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607213505636.png" alt="image-20240607213505636" style="zoom:67%;" />

* 先返回到系统调用服务函数中，中断处理未结束

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607213705691.png" alt="image-20240607213705691" style="zoom:67%;" />

* 返回中断入口函数：

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240607213835435.png" alt="image-20240607213835435" style="zoom:67%;" />

4. 比较：父进程从fork返回时还要先返回到int 0x80的中断处理函数，而子进程直接返回到系统调用入口函数，（子进程的返回地址是来自于保留在父进程PCB中的0特权级栈，而0特权级栈中保留的返回地址是特权级切换前的地址也就是系统调用入口函数中）

   相同点：父子进程fork返回的寄存器值中除了eax函数返回值不一样其他都相同

5. 子进程返回值为0原因：子进程在复制0特权级的时候就把其中的eax设为0（<code>copyProcess</code>），然后调度执行到<code>asm_start_process</code>时会将特权栈中的保存的寄存器值pop出来，而eax就被pop出为0，同时eax还是函数的返回值，这样就会使子进程的fork函数返回值为0
6. 父进程fork函数返回值为子进程的pid:在progamManager的<code>fork</code>函数中直接返回子进程pid号

## 5.总结

1. 虽然每个进程的PCB中都有内核栈和0特权栈，**0特权栈和内核栈是不一样的**

* 位置上：0特权级栈位于内核栈的上方（高地址）

  ```C++
  //内核栈：
  thread->stack = (int *)((int)thread + PCB_SIZE - sizeof(ProcessStartStack));
  //0特权级栈
  tss.esp0 = (int)program + PAGE_SIZE;
  ```

* 含义：

  * 内核栈：内核栈是每个进程都有的，且是私有的，在进程切换时不会保存和恢复，用于保存内核函数调用的局部变量、返回地址等信息。

  * 0特权栈：主要保存CPU从用户态切换到内核态时的任务状态，包括寄存器的值、中断信息、系统调用参数等，是特权级特有，但是暂时存储在PCB中

* 作用：
  * 0特权栈：仅在CPU从用户态切换到内核态的短暂过程中使用，一旦退出内核态就不再需要。
  * 内核栈：在内核态下的整个执行过程中都有效，用于支持内核函数的执行和切换。

* 图解：

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240615200938395.png" alt="image-20240615200938395" style="zoom:67%;" />



2. 用户态虚拟空间3GB-4GB都映射内核的plus：<a href="#preface3">前文跳转3</a>，<a href="#preface4">前文跳转4</a>

3. “注意到`ProgramStartProcess`中保存了父进程的`eip`，`eip`的内容也是`asm_system_call_handler`的返回地址。” 父进程的0特权级栈的eip存的返回地址到底是什么，而且是在哪里存的？

   * 一开始以为是在<code>asm_system_call_handler</code>里面存的，而是是通过pushad存进特权0栈的，但是经过查询资料<code>pushad</code>只能将通用寄存器入栈，而不能将<code>eip</code>入栈，而且子进程开启时的函数也不是在<code>asm_system_call_handler</code>开头
   * 回顾TSS自动调出的时间是在<code>asm_system_call</code>中的<code>int 0x80</code>早在进入80对应的中断处理函数时就已经转换特权栈0了，而且跳转<code>asm_system_call_handler</code>前已经将返回地址当前的eip入栈。这就能解释为什么子进程启动时到的地方和父进程执行完系统调用返回的位置不一样了。子进程启动时到达的地方刚刚好就是在<code>asm_system_call</code>执行完中断返回的位置

   

# Assignment3

## 1.实验要求

* 请结合代码逻辑和具体的实例来分析exit的执行过程。
* 请分析进程退出后能够隐式地调用exit和此时的exit返回值是0的原因。
* 请结合代码逻辑和具体的实例来分析wait的执行过程。
* 如果一个父进程先于子进程退出，那么子进程在退出之前会被称为孤儿进程。子进程在退出后，从状态被标记为`DEAD`开始到被回收，子进程会被称为僵尸进程。请对代码做出修改，实现回收僵尸进程的有效方法。

## 2.实验过程

1. exit的实现（隐式调用分析在实验结果中）

2. wait的实现
3. 回收僵尸进程：在每个进程exit的时候查看是否有没dead的父进程存在，若有则不释放PCB，否则需要自己释放掉PCB

## 3.关键代码

**3.1exit的实现**

* exit的系统调用处理函数：

  * 步骤：
    * 标记PCB的状态为DEAD;
  
    * 释放进程所占用的物理页、页表、页目录表和虚拟地址池bitmap的空间；
  
    * 立即执行线程/进程调度。
  
  * 注意：此处没有释放进程的PCB

```c++
void ProgramManager::exit(int ret)
{
    // 关中断
    interruptManager.disableInterrupt();
    // 第一步，标记PCB状态为`DEAD`并放入返回值。
    PCB *program = this->running;
    program->retValue = ret;
    program->status = ProgramStatus::DEAD;
    int *pageDir, *page;
    int paddr;
    // 第二步，如果PCB标识的是进程，则释放进程所占用的物理页、页表、页目录表和虚拟地址池bitmap的空间。
    if (program->pageDirectoryAddress)
    {
        pageDir = (int *)program->pageDirectoryAddress;
        for (int i = 0; i < 768; ++i)//只用释放掉0GB-3GB，内核的3GB-4GB不要释放掉了
        {
            if (!(pageDir[i] & 0x1))//检查页目录项是否有效
            {
                continue;			//无效则继续
            }

            page = (int *)(0xffc00000 + (i << 12));//页目录表项对应的虚拟页表地址

            for (int j = 0; j < 1024; ++j)//遍历页表
            {
                if(!(page[j] & 0x1)) {
                    continue;//若页表项无效继续遍历
                }

                paddr = memoryManager.vaddr2paddr((i << 22) + (j << 12));//页的基址虚拟地址
                memoryManager.releasePhysicalPages(AddressPoolType::USER, paddr, 1);//释放物理页
            }

       	    paddr = memoryManager.vaddr2paddr((int)page);//释放页表
            memoryManager.releasePhysicalPages(AddressPoolType::USER, paddr, 1);
        }

        memoryManager.releasePages(AddressPoolType::KERNEL, (int)pageDir, 1);//释放页目录表
        
        int bitmapBytes = ceil(program->userVirtual.resources.length, 8);
        int bitmapPages = ceil(bitmapBytes, PAGE_SIZE);

        memoryManager.releasePages(AddressPoolType::KERNEL, (int)program->userVirtual.resources.bitmap, bitmapPages);//释放位图

    }

    // 第三步，立即执行线程/进程调度。
    schedule();
}
```

* 为了实现进程退出时的隐式调用，修改进程用户态栈的退出函数为<code>exit</code>，当进程结束时

```c++
void load_process(const char *filename)
{
    ... 
    // 设置进程返回地址
    int *userStack = (int *)interruptStack->esp;
    userStack -= 3;
    userStack[0] = (int)exit;//退出函数
    userStack[1] = 0;//exit函数的返回地址
    userStack[2] = 0;//exit函数的参数

    interruptStack->esp = (int)userStack;

    interruptStack->ss = programManager.USER_STACK_SELECTOR;

    asm_start_process((int)interruptStack);
}
```

**3.2wait的实现**

* 步骤：
  * 查找当前所有进程中是否有查询进程的子进程。
  * 若有则看是否为dead状态。
  * 如果存在子进程而且状态为dead，若有返回值要求则存下返回值并且释放子进程的PCB，返回其的pid；
  * 如果没有子进程，直接返回-1；
  * 如果存在子进程但是子进程的状态不是dead，阻塞等待


```C++
int ProgramManager::wait(int *retval)
{
    PCB *child;
    ListItem *item;
    bool interrupt, flag;
    while (true)
    {
        interrupt = interruptManager.getInterruptStatus();
        interruptManager.disableInterrupt();
        item = this->allPrograms.head.next;
        // 查找子进程
        flag = true;
        while (item)
        {
            child = ListItem2PCB(item, tagInAllList);
            //存在子进程
            if (child->parentPid == this->running->pid)
            {
                flag = false;
                //检查子进程的状态
                if (child->status == ProgramStatus::DEAD)
                {
                    break;
                }
            }
            item = item->next;
        }
        // 找到一个子进程且状态为dead
        if (item) 
        {
            if (retval)//接收子进程的返回值
            {
                *retval = child->retValue;
            }
            int pid = child->pid;
            releasePCB(child);
            interruptManager.setInterruptStatus(interrupt);
            return pid;
        }
        else 
        {// 没有找到子进程，直接返回-1
            if (flag) 
            {    
                interruptManager.setInterruptStatus(interrupt);
                return -1;
            }
            else // 存在子进程，但子进程的状态不是DEAD，调度其他进程阻塞等待
            {
                interruptManager.setInterruptStatus(interrupt);
                schedule();
            }
        }
    }
}
```

**3.3回收僵尸进程**

* 思路：
  * 在每个进程exit的时候查看当前所有进程中是否存在该进程的父进程。
  * 若不存在父进程或者存在父进程但是父进程的状态为dead，进程在exit释放掉PCB
  * 若存在父进程且父进程状态不为dead，那进程就不在exit释放PCB而是要等待父进程释放掉子进程的PCB

* 查找每个进程的父进程<code>checkparent</code>：

  * 传入参数pid为子进程PCB中记录的父进程pid
  * 遍历所有进程和线程，查找父进程
  * 父进程存在且状态为dead，返回1
  * 父进程不存在，返回-1
  * 父进程存在但不为dead，返回0

  ```C++
  int ProgramManager::checkparent(int pid)
  {
      PCB *parent;
      ListItem *item;
      bool interrupt, flag;
          interrupt = interruptManager.getInterruptStatus();
          interruptManager.disableInterrupt();
          item = this->allPrograms.head.next;
          // 查找父进程
          flag = true;
          while (item)
          {
              parent = ListItem2PCB(item, tagInAllList);
              //父进程存在
              if (parent->pid ==pid)
              {	//父进程存在且状态为dead
                  flag = false;
                  if (parent->status == ProgramStatus::DEAD)
                  {
                      return 1;
                  }
              }
              item = item->next;
          }
              if (flag) 
              {
                  //父进程不存在
                  interruptManager.setInterruptStatus(interrupt);
                  return -1;
              }
              else // 存在父进程，但子进程的状态不是DEAD
              {
                  interruptManager.setInterruptStatus(interrupt);
                  return 0;
              }
      }
  ```

* 在<code>exit</code>函数的末尾检测是否需要释放PCB

  * 检查是否存在父进程
  * 父进程存在且状态为dead和不存在父进程，释放PCB
  * 存在父进程且状态不为dead，直接调度

  ```C++
  void ProgramManager::exit(int ret)
  {
       ......
           
      int id=checkparent(program->parentPid);
      if(id!=0){
          if(id==1){
              printf("my parent has dead,exit\n");
          }
          else{
              printf("I have no parent,exit\n");
          }
          releasePCB(program);
      }
      schedule();
  }
  ```

* 思考：<a id="preface5">5</a>

  针对不存在父进程的情况讨论：

  进程在初始化的时候，PCB中父进程的id都被初始化为0了，即使进程并不存在fork()上的父进程，但是PCB上的父进程id会指向第一个线程（pid=0）。而第一个线程不会退出，可能会存在进程没有父进程而且状态为dead，但是不会释放PCB。

  可以改良如下，使没有父进程的进程（<code>program->parentPid==0</code>）在exit时可以直接释放PCB。

  ```c++
      int id=checkparent(program->parentPid);
      if(id!=0 || program->parentPid==0){
          if(id==1 || program->parentPid!=0){
              printf("my parent has dead,exit\n");
          }
          else{
              printf("I have no parent,exit\n");
          }
          releasePCB(program);
      }
      schedule();
  ```

## 4.实验结果

**4.1:exit实例和执行过程**

* 实例：由执行结果可见成功退出并且打印相关信息

  ```c++
  void first_process()
  {
      int a = 0;
      exit(0);
  }
  void ProgramManager::exit(int ret)
  {
  	......
      if (program->pageDirectoryAddress)
      {
          ......
          printf("exit!,pid=%d",program->pid);
      }
  
      schedule();
  }
  ```

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240608160431687.png" alt="image-20240608160431687" style="zoom:67%;" />

* 执行步骤：调用exit函数，调用对于exit的系统调用函数：设置进程状态为dead，释放资源（页目录表，页表，页，位图），打印相关信息，调度其他进程

**4.2隐式调用exit**

* 为什么：在进程的启动函数<code>load_process</code>中，把<code>exit</code>的地址,默认参数0,<code>exit</code>返回地址0放在了进程的用户栈上，当进程执行结束时从用户栈弹出返回地址为<code>exit</code>和返回，跳转到<code>exit</code>中执行

* 步骤和显示调用exit没有区别，结果相同

  ```c++
  void first_process()
  {
      int a = 0;
  }
  ```

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240608161548236.png" alt="image-20240608161548236" style="zoom:67%;" />

* gdb过程：

  * 进程执行结束：

    <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240608161632811.png" alt="image-20240608161632811" style="zoom:67%;" />

  * 跳转到<code>exit</code>：

    <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240608161712608.png" alt="image-20240608161712608" style="zoom:67%;" />

**4.3wait执行过程和实例**

* 实例：执行结果同预期一样，父进程(pid=1)等待子进程(pid=2)结束后才退出

  ```c++
  void first_process()
  {
      int pid = fork();
  
      if (pid == -1)
      {
          printf("can not fork\n");
          asm_halt();
      }
      else
      {
          if (pid)
          {
              printf("I am father\n");
              wait(0);
          }
          else
          {
              printf("I am child, exit\n");
          }
      }
  }
  ```

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240608162252699.png" alt="image-20240608162252699" style="zoom:67%;" />

* wait执行过程：

  调用wait函数，调用wait系统调用，查询是否有对应子进程，若有且未结束阻塞等待；若有且结束则收集子进程的返回值并且返回子进程的pid；若无子进程，返回-1

**4.4回收僵尸进程**

* 实例：父进程执行完直接退出不等待子进程，但是子进程也可以成功释放PCB

  ```C++
  void first_process()
  {
      int pid = fork();
  
      if (pid == -1)
      {
          printf("can not fork\n");
          asm_halt();
      }
      else
      {
          if (pid)
          {
              printf("I am father\n");
              exit(0);
          }
          else
          {
              printf("I am child, exit\n");
          }
      }
  }
  ```

  ![image-20240608163007396](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240608163007396.png)

## 5.总结

进程有父线程但是没有父进程的思考：<a href="#preface5">前文跳转5</a>

