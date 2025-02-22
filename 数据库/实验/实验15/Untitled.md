![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科

## 一：实验任务：

1.在students表上演示锁争夺，通过sp_who查看阻塞的进程。通过设置lock_timeout解除锁争夺。

2.在students表上演示死锁。

3.讨论如何避免死锁以及死锁的处理方法。

## 二：实验过程：

1. 在students表上演示锁争夺，通过sp_who查看阻塞的进程。通过设置lock_timeout解除锁争夺。
   (1) 建立第一个连接：隔离级别为可重复读级别，更新STUDENTS表sid='1'的grade，事务不提交
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202173741292.png" alt="image-20241202173741292" style="zoom:67%;" />

   (2) 建立第二个连接：隔离级别为可重复读级别，查询STUDENTS表

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202173850507.png" alt="image-20241202173850507" style="zoom:67%;" />

   (3) 执行结果：第一个连接执行成功但是未提交，第二个连接被第一个连接更新操作的排它锁阻塞

   * 第一个连接执行成功但是未提交
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202174204214.png" alt="image-20241202174204214" style="zoom:67%;" />
   * 第二个连接的select65号进程被第一个连接的52号进程阻塞
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202174325889.png" alt="image-20241202174325889" style="zoom:67%;" />
   * 第二个连接始终正在执行，无法获得结果
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202174357245.png" alt="image-20241202174357245" style="zoom:67%;" />

   (4).第二个连接设置lock_timeout锁定超时时间间隔
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202174809400.png" alt="image-20241202174809400" style="zoom:67%;" />

2. 在students表上演示死锁。

   (1) 同时打开两个连接，执行一样的事务：先查询STUDENTS表sid='1'的表项，延时5s后更新操作，再次查询
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202175238986.png" alt="image-20241202175238986" style="zoom:67%;" />

   (2) 执行结果：一个连接可以成功查询，一个连接因为死锁牺牲
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202175322621.png" alt="image-20241202175322621" style="zoom:67%;" />

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202175340540.png" alt="image-20241202175340540" style="zoom:67%;" />

3. 讨论如何避免死锁以及死锁的处理方法。

   * 死锁避免：

     * 用较低的隔离级别避免使用REPEATABLE READ，将2的隔离级别降为COMMITED 不会发生死锁，但是执行结果可能和需求的不一样
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202180206370.png" alt="image-20241202180206370" style="zoom:67%;" />

       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202180226608.png" alt="image-20241202180226608" style="zoom:67%;" />

     * 避免不必要的select操作，避免两个事务执行过程中同时持有共享锁，且后续还有更新操作，3中的代码都去掉第一个select后不会出现死锁情况

       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202180458905.png" alt="image-20241202180458905" style="zoom:67%;" />

       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202180510714.png" alt="image-20241202180510714" style="zoom:67%;" />

   * 死锁处理：超时等待则回滚事务，释放锁，在数据库中提供了这样的自动检测死锁机制，死锁超时后会有事务回滚牺牲
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202175322621.png" alt="image-20241202175322621" style="zoom:67%;" />

## 三：实验总结：

* repeatable read隔离级别：事务获取用于保护行的排它锁，在事务完成前一直保持
* 死锁场景：
  <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241202173235392.png" alt="image-20241202173235392" style="zoom:67%;" />