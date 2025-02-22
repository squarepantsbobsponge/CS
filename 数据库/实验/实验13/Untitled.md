![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科

## 一：实验任务

(1)编写一个嵌套事务。外层修改students表某记录，内层在teachers表插入一条记录。演示内层插入操作失败后，外层修改操作回滚。

(2)编写一个带有保存点的事务。更新teachers表中数据后，设置事务保存点，然后在表courses中插入数据，如果courses插入数据失败，则回滚到事务保存点。演示courses插入失败，但teachers表更新成功的操作。

(3)编写一个包含事务的存储过程，用于更新courses表的课时。如果更新记录的cid不存在，则输出“课程信息不存在”，其他错误输出“修改课时失败”，如果执行成功，则输出“课时修改成功”。调用该存储过程，演示更新成功与更新失败的操作。

## 二：实验过程

1. 编写一个嵌套事务。外层修改students表某记录，内层在teachers表插入一条记录。演示内层插入操作失败后，外层修改操作回滚。

   * 执行事务前的STUDENTS和teacher表

     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125170227035.png" alt="image-20241125170227035" style="zoom:50%;" />
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125170252446.png" alt="image-20241125170252446" style="zoom:50%;" />

   * 嵌套事务：外层事务是更改STUDENTS表中sid='1'的表项的grade=6，内层事务是插入TEACHERS表，新表项的tid=‘200003125’, 由于tid为主键，且tid='200002135'的表项已经存在，则插入会由于主键冲突失败，内层事务会失败

     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125170538866.png" alt="image-20241125170538866" style="zoom:50%;" />

   * 执行结果：

     * 最开始没有事务时，事务数为0。外层事务begin tran后，事务数为1；内层事务begin tran后，事务数为2；内层事务执行提交失败，回滚后事务数为1；内层事务失败回滚后不影响外层事务，外层事务仍然可以提交，提交后事务数为0

       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125170849497.png" alt="image-20241125170849497" style="zoom:50%;" />
       ![image-20241125170953359](C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125170953359.png)

     * 执行完嵌套事务后的STUDENTS表：由于内层事务失败后回滚，不影响外层事务更新操作的提交，则grade被修改成功
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125171024261.png" alt="image-20241125171024261" style="zoom:50%;" />
     * 执行完嵌套事务后的TEACHERS：插入失败
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125171134342.png" alt="image-20241125171134342" style="zoom:50%;" />

2. 编写一个带有保存点的事务。更新teachers表中数据后，设置事务保存点，然后在表courses中插入数据，如果courses插入数据失败，则回滚到事务保存点。演示courses插入失败，但teachers表更新成功的操作。

   * 执行事务前的TEACHERS和COURSES表
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125171431549.png" alt="image-20241125171431549" style="zoom:50%;" />、
   * 事务：在执行完更新操作后设置事务保存点，在执行完插入操作后检查插入操作是否成功，不成功则要回滚到事务保存点，最后提交整个事务
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125172207091.png" alt="image-20241125172207091" style="zoom:67%;" />
   * 执行结果：由于和主键约束冲突，插入课程表失败。返回到事务保存点，提交事务，更新操作正常执行。
     ![image-20241125172430559](C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125172430559.png)
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125172912247.png" alt="image-20241125172912247" style="zoom:50%;" />

3. 编写一个包含事务的存储过程，用于更新courses表的课时。如果更新记录的cid不存在，则输出“课程信息不存在”，其他错误输出“修改课时失败”，如果执行成功，则输出“课时修改成功”。调用该存储过程，演示更新成功与更新失败的操作。
   * 存储过程定义如下：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125174817628.png" alt="image-20241125174817628" style="zoom:50%;" />
   * 更新前：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125174222843.png" alt="image-20241125174222843" style="zoom:50%;" />
   * 更新失败操作：更新不存在的记录,打印出课程信息不存在
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125174632469.png" alt="image-20241125174632469" style="zoom:67%;" />
   * 更新成功操作：
     ![image-20241125174854361](C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241125174854361.png)

## 实验总结：

* 事务定义：

  ```
  begin tran 事务开始
  ...事务主体
  commit tran 事务结束，提交事务 
  ```

* 批处理：多条SQL语句组成，go语句来终止语句组

* 事务处理vs批处理：批处理，每条语句的完成不影响其他语句的执行；事务处理，单条语句执行失败，事务全部回滚

* 嵌套事务：

  * @@TRANCOUNT: 每一次Begin Transaction都会引起@@TranCount加1。而每一次Commit Transaction都会使@@TranCount减1，而RollBack Transaction会回滚所有的嵌套事务包括已经提交的事务和未提交的事务，而使@@TranCount置0。
  * ROLLBACK TRAN: ROLLBACK TRAN用于撤销事务自BEGIN TRAN以来所做的所有修改，将数据库状态恢复到事务开始之前的状态。
  * COMMIT TRAN: COMMIT TRAN用于提交事务，使事务中的所有修改成为数据库中永久的、不可逆转的一部分

* 事务保存点：

  ```
  保存
  SAVE TRAN upd_teachers
  检测错误并且返回
  	IF @@ERROR!=0 OR @@ROWCOUNT>1
  		BEGIN
  		--撤销事务
  		ROLLBACK TRAN upd_teachers
  		PRINT '插入课程表失败'
  		RETURN
  		END
  ```

* 存储过程：

  * ① 存储过程（Stored Procedure）是一组为了完成特定功能的SQL语句集。经编译后存储在数据库中。

    ② 存储过程是数据库中的一个重要对象，用户通过指定存储过程的名字并给出参数（可以有参数，也可以没有）来执行它。

    ③ 存储过程是由 流控制 和 SQL语句书写的过程，这个过程经编译和优化后存储在数据库服务器中。

    ④ 存储过程 可由应用程序通过一个调用来执行，而且允许用户声明变量。

    ⑤ 同时，存储过程可以接收和输出参数、返回执行存储过程的状态值，也可以嵌套调用。

  * 