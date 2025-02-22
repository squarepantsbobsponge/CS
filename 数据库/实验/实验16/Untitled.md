![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科

## 一：实验任务

1.在school数据库上创建用户“王二”，在students表上创建视图grade2000，将年级为2000的学生元组放入视图。

2.授予用户王二在视图grade2000的select权限。

3.授予用户王二在视图grade2000的修改sname列的权限。

4.查看SQL Server错误日志

## 二：实验过程

1. 在school数据库上创建用户“王二”，在students表上创建视图grade2000，将年级为2000的学生元组放入视图。

   * 创建用户“王二”：

     * 使用`sp_addlogin`存储过程来创建一个新的登录名`'王二'`，密码为`'123456'`，并且指定默认数据库为`'school'`和语言为`'English'`
     * 使用`use`语句切换到`'School'`数据库
     * 使用`sp_grantdbaccess`存储过程来授予登录名`'王二'`对`'School'`数据库的访问权限
       下面是重复执行的错误消息，但是已经创建好了

     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209165202527.png" alt="image-20241209165202527" style="zoom:67%;" />

   * 在students表上创建视图grade2000，将年级为2000的学生元组放入视图
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209165538004.png" alt="image-20241209165538004" style="zoom:50%;" />

2. 授予用户王二在视图grade2000的select权限

   * 授予王二在视图grade2000的select权限

     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209165737130.png" alt="image-20241209165737130" style="zoom:50%;" />

   * 以王二身份登录，对grade2000进行select,查询成功
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209165953500.png" alt="image-20241209165953500" style="zoom:50%;" />

3. 授予用户王二在视图grade2000的修改sname列的权限。

   * 授予王二权限：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209170434178.png" alt="image-20241209170434178" style="zoom:50%;" />

   * 以王二身份登录数据库，更改grade2000的sname属性，更改成功

     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209170628534.png" alt="image-20241209170628534" style="zoom:50%;" />

4. 查看SQL Server错误日志

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209171359139.png" alt="image-20241209171359139" style="zoom:50%;" />

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209171323855.png" alt="image-20241209171323855" style="zoom:50%;" />

## 三：实验总结

* 使授权粒度达到元组级，要利用视图机制和授权机制配合使用

  1. 创建用户：

     ```
     exec sp_addlogin '王二','123456','school','English'
     go 
     use School
     go
     exec sp_grantdbaccess='王二'
     ```

  2. 创建视图：

     ```
     create VIEW 视图名 as 子查询
     ```

  2. 授予权限：

     ```
     grant select(权限) on grade2000(视图) to 王二(用户名) 
     ```

     

  2. 授予视图的属性列权限：

     ```
     USE School
     go
     grant update on dbo.[grade2000(视图名)]([sname(属性列名)])
     to 王二
     ```

* DBCC log命令：从内存中读取当前活动的全部日志记录

  ```
  DBCC log ({dbid | dbname}, [, type=(-1| 0 | 1 | 2 | 3 | 4 }])
  ```

  <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209164500080.png" alt="image-20241209164500080" style="zoom:50%;" />