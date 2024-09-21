![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科

[TOC]

## 一：实验要求

1. 创建数据库表 CUSTOMERS(CID, CNAME,CITY, DISCNT)，数据库表AGENTS(AID, ANAME,CITY, PERCENT)，数据库表 PRODUCTS(PID. PNAME)，其中，CID，AID, PID分别是各表的主键，具有唯一性约束，表AGENTS中的**PERCENT**属性具有小于100的约束。

2. 创建数据库表 ORDERS( ORDNA, MONTH,CID,AID,PID,QTY, DOLLARS)。
    其中， ORDNA是主键，具有唯一性约束。CID，AID，PID是外键，分别参照的是表 CUSTOMERS的CID字段，表 AGENTS的AID字段，表 PRODUCTS的PID字段。
3. 增加数据库表 PRODUCTS的三个属性列：CITY, QUANTITY, PRICE。
4. 为以上4个表建立各自的按主键增序排列的索引。 
5. 取消步骤(4)建立的4个索引。
6. 创建表CUSTOMERS的按CNAME降序排列的唯一性索引。
7. )删除步骤(3)创建的表AGENTS中的CITY属性。
8. 修改表CUSTOMERS中CITY属性为CHAR(40)
9. 删除步骤(1)创建的表ORDERS

## 二：实验过程

1. 

   * 创建<code> CUSTOMERS(CID, CNAME,CITY, DISCNT)</code>，且指明<code>CID</code>为主键

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917192220760.png" alt="image-20240917192220760" style="zoom:80%;" />

     ![image-20240914170149196](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240914170149196.png)

   * 创建表<code>AGENTS(AID, ANAME,CITY, PERCENT)</code>，<code>AID</code>为主键且<code>PERCENT</code>有小于100的约束

     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917193137216.png" alt="image-20240917193137216" style="zoom:80%;" />

     ![image-20240914171019947](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240914171019947.png)
     （注意<code>PERCENT</code>原本就为数据库关键字，定义为属性名会有所冲突，可以加上<code>'' ''</code>或者<code>[]</code>)

   * 创建表数据库表 <code>PRODUCTS(PID. PNAME)</code>，主键为<code>PID</code>且有唯一性约束
     <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917193733494.png" alt="image-20240917193733494" style="zoom:80%;" />

     ![image-20240914171419195](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240914171419195.png)

2. 创建<code>ORDERS( ORDNA, MONTH,CID,AID,PID,QTY, DOLLARS)</code>，主键<code>ORDNA</code>有唯一性约束。<code>CID,AID,PID</code>为外键

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917194939529.png" alt="image-20240917194939529" style="zoom:80%;" />

   （补充：<code>ORDNA</code>为订单号，所以被设成<code>INT</code>；<code>QTY</code>为数量，被设为<code>INT</code>）

   创建完四个表后的图：
   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240914173607638.png" alt="image-20240914173607638" style="zoom:67%;" />

3. 增加<code> PRODUCTS</code>的三个属性列<code>CITY, QUANTITY, PRICE</code>:

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917200315095.png" alt="image-20240917200315095" style="zoom:67%;" />

   添加属性后:
   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917200428072.png" alt="image-20240917200428072" style="zoom:80%;" />

4. 为上述4个表建立各自的按主键增序排列的索引

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917201507746.png" alt="image-20240917201507746" style="zoom:67%;" />

   增加完后：（可见索引处出现了增加的索引名）
                                                               <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240914175751238.png" alt="image-20240914175751238" style="zoom:67%;" />

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240914175808097.png" alt="image-20240914175808097" style="zoom:67%;" />

   

5. 取消4创建的4个索引：

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917202317245.png" alt="image-20240917202317245" style="zoom:67%;" />

6. 创建表<code>CUSTOMERS</code>的按<code>CNAME</code>降序排列的唯一性索引：

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917202813741.png" alt="image-20240917202813741" style="zoom:67%;" />

   创建成功后：出现<code>C_U_INDEX</code>索引：

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240914180754701.png" alt="image-20240914180754701" style="zoom:80%;" />

7. 删除步骤(3)创建的<code>AGENTS</code> 中的<code>CITY</code>属性：

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917203446404.png" alt="image-20240917203446404" style="zoom:67%;" />

   ![image-20240915090630282](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240915090630282.png)

8. 修改表<code>CUSTOMERS</code>中<code>CITY</code>属性为CHAR(40)

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917203902639.png" alt="image-20240917203902639" style="zoom:67%;" />

   修改后：

   ![image-20240915091008958](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240915091008958.png)

9. 删除步骤(1)创建的表<code>ORDERS</code>

   <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917204143066.png" alt="image-20240917204143066" style="zoom:67%;" />

   删除后：表<code>ODERS</code>从数据库表中消失

   ![image-20240915091251328](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240915091251328.png)

## 三：总结

1. 创建关键表

   ```sql
   CREATE TABLE NAME(
     属性名 属性类型 约束，#NOT NULL为空，UNIQUE为唯一
     ...
     PRIMARY KEY(属性) ,#指定属性为主键
     CHECK(对某属性的约束)
   )
   ```

2. 删除表

   ```sql
   DROP TABLE PR(表名)
   ```

    

3. 在表中设置外键

   * 先声明外键属性<code>A</code>及其类型

   * 再在后面表明主表和完整性要求

     ```sql
     FOREIGN KEY(外键属性) REFERENCES 参考主表 ON DELETE 完整性要求
     ```

     ![image-20240917195607569](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240917195607569.png)

3. 修改已存在表：

   ```sql
   #添加属性
   ALTER TABLE PERSON(表名) ADD Rtype(属性名) CHAR(10)(属性类型);
   #取消约束
   ALTER TABLE PERSON(表名) DROP CONSTRAINT CK__PERSON__Page__0425A276（约束名，在对象资源管理器中查看）;
   #修改属性类型
   ALTER TABLE ROOM（表名） ALTER COLUMN Rname(需要修改的属性名) CHAR(40)(修改后的数据类型);
   #删除表属性
   ALTER TABLE ROOM(表名) DROP COLUMN Rarea(需要删除的属性名)
   
   ```

4. 关于表的索引

   ```sql
   #为表R按照属性A创建升序索引B
   CREATE INDEX B ON R(A)
   #按照降序为表R按照属性A创建升序索引B
   CREATE INDEX B ON R(A DESC)
   # 删除表R的索引B
   DROP INDEX R.B
   #为表R按照属性A以升序创建唯一性索引B
   CREATE UNIQUE INDEX B ON R (A ASC)
   ```



