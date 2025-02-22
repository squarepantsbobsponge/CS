![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科

## 一：实验要求

1.对school数据库分别进行完整备份、差异备份和事务日志备份。

2.对school数据库执行插入、删除或更新操作，再利用school数据库的备份进行还原，对比还原前和还原后的数据库状态。

## 二：实验过程

1. 完整备份和恢复：

   * 备份：
     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013180532146.png" alt="image-20241013180532146" style="zoom:67%;" />

   * 删除操作：

     * 删除前：

       <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013180711310.png" alt="image-20241013180711310" style="zoom:67%;" />

     * 删除：
       <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013180732075.png" alt="image-20241013180732075" style="zoom:67%;" />

     * 删除后：
       <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013180755245.png" alt="image-20241013180755245" style="zoom:67%;" />

   * 恢复：
     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013180822155.png" alt="image-20241013180822155" style="zoom:67%;" />

     删除掉的分数低于60的选课记录的数据恢复

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013180858521.png" alt="image-20241013180858521" style="zoom:67%;" />

2. 差异备份与恢复：

   * 差异性备份：
     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181021209.png" alt="image-20241013181021209" style="zoom:67%;" />

   * 对STUDENTS进行插入操作:
     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181055485.png" alt="image-20241013181055485" style="zoom:67%;" />

   * 恢复：注意差异备份（备份的是距离上一次完整备份以来的数据库变化）要和上一次的完整备份一起恢复，这样才能回到差异备份时刻的数据库状态

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181116157.png" alt="image-20241013181116157" style="zoom:67%;" />

     恢复后在备份后插入的记录还原消失：

     ![image-20241013181135134](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181135134.png)

3. 事务日志备份与恢复：

   * 备份前：插入记录
     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181533504.png" alt="image-20241013181533504" style="zoom:67%;" />

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181543633.png" alt="image-20241013181543633" style="zoom:67%;" />

   * 备份:

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181559613.png" alt="image-20241013181559613" style="zoom:67%;" />

   * 删除刚刚插入的记录：

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181620153.png" alt="image-20241013181620153" style="zoom:67%;" />

   * 恢复：如果要恢复到事务日志备份的时刻，那么前面的完整备份和差异备份也要恢复。完整备份和差异备份能恢复到差异备份的时刻，事务日志备份备份从差异备份时刻以来的事务

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181812203.png" alt="image-20241013181812203" style="zoom:67%;" />

     事务备份前插入记录，备份后删除记录，恢复备份则插入记录仍在数据库中：

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241013181857079.png" alt="image-20241013181857079" style="zoom:67%;" />

