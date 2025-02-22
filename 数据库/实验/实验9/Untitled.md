![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科

## 一：实验要求

1.在school数据库中建立一张新表class，包括class_id(varchar(4)), name(varchar(10)), department(varchar(20))三个列，并约束class_id为主键。

2.创建事务T3，在事务中插入一个元组（‘0001’，’01CSC’,’’CS’）,并在T3中嵌套创建事务T4，T4也插入和T3一样的元组，编写代码测试，查看结果。

3.在表class中，尝试设置name=’01CSC‘的记录的class_id 为NULL，查看结果

4.在表class中，不创建事务，插入两个元组 （‘0002’，’01CSC‘。 ’CS‘），（’0002‘，’03CSC‘，’CS‘），然后查看表中有几条记录，为什么？

5.在表class中，创建事务，并设置开启回滚，然后插入两个元组（‘0003’，’03CSC‘。 ’CS‘），（’0001‘，’03CSC‘，’CS‘），查看结果，表中有几条记录？

6.在完成上面几步的前提下，尝试设置’name‘为主键，看能否成功，并思考原因。

## 二：实验过程

1. .在school数据库中建立一张新表class，包括class_id(varchar(4)), name(varchar(10)), department(varchar(20))三个列，并约束class_id为主键

   * 成功创建表class，并且为`class_id` 列创建一个名为 `classid` 的主键约束。

     ![image-20241028164514607](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028164514607.png)

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028164547268.png" alt="image-20241028164547268" style="zoom:67%;" />

2. 创建事务T3，在事务中插入一个元组（‘0001’，’01CSC’,’’CS’）,并在T3中嵌套创建事务T4，T4也插入和T3一样的元组，编写代码测试，查看结果
   * （两次事务都开启了回滚）插入失败，因为主键的唯一属性不允许插入两个主键<code>class_id</code>都一样的元组

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028165020901.png" alt="image-20241028165020901" style="zoom:67%;" />

​				两个事务都失败回滚，没有任何元组插入<code>class</code>
​	                                   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028165232841.png" alt="image-20241028165232841" style="zoom:67%;" />

3. 在表class中，尝试设置name=’01CSC‘的记录的class_id 为NULL，查看结果

   * 先插入一个name=‘01CSC’的元组，再尝试将其的class_id改为NULL

   * 结果：由于class_id为主键，主键的NOT NULL约束导致更改失败

   * （执行完后将该元组从class中删除）

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028165635759.png" alt="image-20241028165635759" style="zoom:67%;" />

4. 在表class中，不创建事务，插入两个元组 （‘0002’，’01CSC‘。 ’CS‘），（’0002‘，’03CSC‘，’CS‘），然后查看表中有几条记录，为什么？

   * 向class中插入两个元组，由于两次插入的主键class_id相同，违反了主键的唯一性，只有第一次插入成功，第二次插入失败

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028170204350.png" alt="image-20241028170204350" style="zoom:67%;" />

   * 由于两次插入不是事务，第二次插入失败不用回滚，则第一次插入成功，表中只有插入的第一次的元组

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028170314038.png" alt="image-20241028170314038" style="zoom:67%;" />

5. 在表class中，创建事务，并设置开启回滚，然后插入两个元组（‘0003’，’03CSC‘。 ’CS‘），（’0001‘，’03CSC‘，’CS‘），查看结果，表中有几条记录？

* 注意：第2个实验任务由于事务中插入元组主键相同，所以没有插入class_id=0001的元组，第3个实验任务中也将class_id=0001的元组在实验后删去
* 事务执行成功

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028170640616.png" alt="image-20241028170640616" style="zoom:67%;" />

* class中有三条记录，本任务插入的两个元组在class中
  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028171017296.png" alt="image-20241028171017296" style="zoom:67%;" />

6. 在完成上面几步的前提下，尝试设置’name‘为主键，看能否成功，并思考原因。

* 为了设置name为主键，要删掉原有的classid的主键

* 设置失败：因为一开始创建表的时候没有设置name列的not null约束，导致name列可以设为null，这个违反了主键的不为null的属性，在当前的环境下无法添加name为主键

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028172113649.png" alt="image-20241028172113649" style="zoom:67%;" />

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20241028172100838.png" alt="image-20241028172100838" style="zoom:67%;" />

## 三：实验总结

* <code>NULL</code>不等于空格和0

* 违反主键的唯一性属性和<code>NOT NULL</code>属性，会破坏实体完整性

* 事务建立：

  ```sql
  BEGIN TRANSACTION T1
  ....
  COMMIT TRANSACTION T1
  ```

  事务回退机制：为ON时，事务有语句错误，整个事务终止回滚，为OFF，只回滚产生错误的SQL语句

  ```sql
  SET XACT ABORT ON/OFF
  ```

* 当与现有数据环境不等时，无法建立实体完整性以及参照完整性

