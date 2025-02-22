![image-20240506113933705](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240506113933705.png)

 

 

​												本科生实验报告

​										学生姓名：      丁晓琪

​										学生学号：       22336057

​										专业名称：	计科

[TOC]

## 第一次开发框架

### 一：实验目的

1. 掌握 SaaS 应用的创建和部署
2. 学会搭建 SaaS 应用本地开发环境
3. 掌握 SaaS 应用开发，实现小型朋友圈应用
4. 通过实践编码结合 pre-commit等规范检查工具，提升代码质量与编程能力

### 二：实验环境

1. 硬件环境需求： PC或笔记本， 支持外网访问

2. 软件环境需求：

   * 系统： Windows
   * 安装 Python 3.6.12 
   * 安装 MySQL 8.3 
   * 安装 Git
   * 安装 VSCode，PyCharm 或其它 IDE

### 三：实验内容

使用蓝鲸 PaaS 平台（https://ce.bktencent.com/）创建并部署 SaaS 应用。搭建蓝鲸应用框架本地开发环境。开发一个小型朋友圈 SaaS 应用，该应用具备三个功能：第一是展示登录用户信息，第二是能够显示已发送朋友圈内容，第三是具有发送朋友圈功能

### 四：实验评分标准

考点一： 通过平台开发者中心创建 SaaS 应用，新建源码仓库并部署示例程序到 PaaS 平台。搭建好本地开发环境。部署后框架界面如图：

<img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241208230357399.png" alt="image-20241208230357399" style="zoom:67%;" />

考点二：添加 moments 应用，并实现 WeChatUser 和 Status 两个model。生成数据库迁移脚本并使用 migrate 变更数据库。其中 WeChatUser 是蓝鲸开发用户（from blueapps.account.models import User）的拓展（OneToOneField），具备motto、pic（头像，可直接使用static/image 中的图像）、region等字段。Status 具备 user、text、pics、pub_time 等字段。

考点三：编写 view 函数实现主页和用户信息展示（前端界面已提供）

考点四：实现发送朋友圈和展示朋友圈功能，效果如下图。使用其他账号登录并发送朋友圈，可以在 /admin 界面给登录用户创建对应的 WeChatUser 数据。

1. Python代码符合[PEP8规范](https://www.python.org/dev/peps/pep-0008/)，配置 pre-commit等格式化工具，可酌情加分

2.     系统边界考虑完善，系统性能优良，可酌情加分

### 五：实验过程和结果

#### (1). 搭建蓝鲸应用框架本地开发环境

1. 在gitee上创建仓库
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241208231440459.png" alt="image-20241208231440459" style="zoom:50%;" />
2. 在开发者中心中新建应用，将新建的仓库地址填入
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241208231913410.png" alt="image-20241208231913410" style="zoom:50%;" />
3. 在本地初始化仓库：
   * 根据开发者中心创建应用成功后的提示下载并解压代码到本地仓库所在目录
   * 在本地仓库添加远程仓库地址且完成推送

4. 创建开发用虚拟环境，更换pip源并安装对应依赖包：按照实验手册操作，由于操作简单此处略

5. pycharm内应用的相关配置

   * pycharm内为项目添加解释器：用上一步创建好的虚拟环境
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209000301289.png" alt="image-20241209000301289" style="zoom:67%;" />
   * pycharm安装EnvFile插件
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209000426882.png" alt="image-20241209000426882" style="zoom:50%;" />
   * 创建dev.env配置文件：在其中填写应用相关信息（应用id和应用secret），注意在本地测试时，CORS允许访问的域为http://dev.ce.bktencent.com:5000。部署时需要更改为https://apps.ce.bktencent.com
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209000700676.png" alt="image-20241209000700676" style="zoom:50%;" />

6. 数据库相关配置

   * 在MySQL中创建数据库，且在config/dev.py 中完成数据库配置信息

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209001330907.png" alt="image-20241209001330907" style="zoom:50%;" />

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209001119364.png" alt="image-20241209001119364" style="zoom:50%;" />

   * 配置数据库迁移的相关操作

     * 配置执行manage操作migrate
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209001831971.png" alt="image-20241209001831971" style="zoom:50%;" />

     * 配置执行manage操作makemigrations

       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209001936267.png" alt="image-20241209001936267" style="zoom:50%;" />

     * 意义：makemigrations是根据模型中的变化生成迁移文件，描述如何将数据库从当前状态迁移到新的状态。migrate用于应用迁移文件，将数据库的实际结构更新为迁移文件所描述的状态。

7. 更改本机host&SaaS应用本地运行

   * Django服务器启动配置：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209002700440.png" alt="image-20241209002700440" style="zoom:50%;" />
   * 更改本机host信息：将`appdev.ce.bktencent.com`和`dev.ce.bktencent.com`这两个域名解析到`127.0.0.1`，这些域名的请求将被重定向到本地计算机，用于开发或测试环境，允许开发者在本地机器上模拟和测试应用程序的行为，而无需将应用程序部署到远程服务器。
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209002756742.png" alt="image-20241209002756742" style="zoom:50%;" />
   * 运行Django服务器：注意要在无痕模式下浏览，不然会自动将http转为https访问，从而访问失败
     ![image-20241209003341112](C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209003341112.png)

#### (2).开发一个小型朋友圈 SaaS 应用

1. 设置数据库：上面(1)已经完成

2. 添加moments应用：运用manage.py操作startapp moments并在config/default.py下的INSTALLED_APPS添加moments
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209003904886.png" alt="image-20241209003904886" style="zoom:50%;" />

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209102757608.png" alt="image-20241209102757608" style="zoom:50%;" />

3. 生成模型：WechatUser(包含user，email，motto，pic，region..)，Status(包含user，text，pics，pub_time)

   * 定义模型：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209103121346.png" alt="image-20241209103121346" style="zoom:67%;" />
   * 执行前面配置好的数据库迁移指令生成数据库迁移脚本

4. 网页模板静态文件：直接复制实验材料的static和templates到moments目录

5. 后端路由函数实现：
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209103605755.png" alt="image-20241209103605755" style="zoom:67%;" />

​	<img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209103653915.png" alt="image-20241209103653915" style="zoom:50%;" />

6. 为应用添加管理员：
   * 设定22336057X为超级管理员
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209104027696.png" alt="image-20241209104027696" style="zoom:50%;" />
   * 添加设定管理员的路由函数：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209104154539.png" alt="image-20241209104154539" style="zoom:50%;" />
   * 运行项目调用set-su接口，添加管理
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209104513431.png" alt="image-20241209104513431" style="zoom:50%;" />
   * 进入管理员页面，登录管理员账号，添加用户

7. 将本地仓库的更改push到远程仓库，更改静态资源的路径，部署应用
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209104726489.png" alt="image-20241209104726489" style="zoom:50%;" />

   成功运行：
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209104758163.png" alt="image-20241209104758163" style="zoom:50%;" />

### 六：实验心得和体会

* 问题1：本地测试时直接点击链接跳转到对应网址时，浏览器会自动将http转为https导致链接不安全错误

  <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210180205681.png" alt="image-20241210180205681" style="zoom:50%;" />
  解决：在浏览器无痕模式下访问

* 问题2：在本地测试时点击访问链接跳转到蓝鲸平台的登录页面，填写账号密码后仍然重定向为登录页面
  解决：清除浏览器缓存

## 第二次作业-第一次迭代（基于配置平台进行游戏主机管理）

### 一：实验目的：

（1）巩固SaaS应用的软件开发&设计能力

（2）了解蓝鲸CMDB配置平台的功能、数据结构与使用方法

（3）掌握蓝鲸网关/ESB组件API的调用方法与鉴权模式

（4）能够通过蓝鲸API联通CMDB平台获取业务主机与架构信息

（5）提升SaaS开发技能，能够进行前后端联调并设计接口

（6）提升SaaS开发技能，进一步熟悉开发框架与后台建模

### 二：实验环境

同第一次实验环境

### 三：实验内容

基于蓝鲸SaaS开发框架开发一个独立SaaS应用，借助蓝鲸CMDB配置平台实现游戏业务主机资源拉取与查询，通过蓝鲸网关/ESB组件API联通 CMDB平台实现数据获取，并根据CMDB主机数据结构，设计查询条件与对应接口。

### 四：实验评分标准

整体要求：请同学们采用迭代方式进行需求分析、面向对象设计和编程实现，实训课报告中需包含相应的需求规约、设计规约、接口文档，项目开发说明

考点一： 创建SaaS应用，通过蓝鲸 ESB组件API联通CMDB配置平台，实现业务、集群、模块级联拉取接口，并在前端进行下拉框组件展示与数据渲染

考点二：添加 根据蓝鲸CMDB配置平台的主机数据结构设计查询条件（包括但不限于主机名称、主机维护人、主机备份人等字段），实现主机查询接口（模糊查询可加分）

考点三：设计前端界面（可参考课程前端样例代码与MagicBox组件库），进行前后端联调，实现前端主机列表数据渲染

考点四：实现主机详情展示接口&界面，要求点击主机后能够查看主机详情信息并通过前端界面进行数据展示

考点五：将实现的后端&前端代码上传至Git代码托管平台，并部署到PaaS平台，数据交互展示无误，不存在CORS、CSRF等问题

### 五：实验过程和结果

1. 本地开发环境搭建：在蓝鲸平台创建应用，依据课程提供的材料包导入前端后端模块，并完成相关配置（如实现第一个Saas应用一样搭建蓝鲸开发框架环境）
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209111119880.png" alt="image-20241209111119880" style="zoom:50%;" />

   补充：不同于第一个实验将所有信息在dev.env或者default.py中配置并且上传到远程仓库，这里将敏感信息放在local_setting.py，并且不上传到远程仓库

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209111633110.png" alt="image-20241209111633110" style="zoom:50%;" />

2. 实现业务列表拉取接口

   * 在后端模块中编写路由函数<code>get_bizs_list</code>，访问API实现业务拉取
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209111844152.png" alt="image-20241209111844152" style="zoom:50%;" />
   * 启动后端的django服务，访问地址http://dev.ce.bktencent.com:8000/biz-list  ，看到接口响应数据
     <img src="C:/Users/丁晓琪/Documents/WeChat Files/wxid_gxqcm4jeu3hf22/FileStorage/Temp/6b676436e0a31f2de0a195a32422b3a.png" alt="6b676436e0a31f2de0a195a32422b3a" style="zoom:50%;" />

3. 实现集群和模块列表拉取接口

   * 集群拉取接口：在后端模块中实现路由函数`get_sets_list`，调用相关api接口
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209112217152.png" alt="image-20241209112217152" style="zoom:50%;" />
     断点调试：在url传入参数bk_biz_id=1234,在调试器中能看到从request_Get中获得请求参数

     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209112347713.png" alt="image-20241209112347713" style="zoom:50%;" />
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209112543517.png" alt="image-20241209112543517" style="zoom:50%;" />

   * 实现模块拉取接口，在后端模块中实现路由函数`get_modules_list`
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209112645078.png" alt="image-20241209112645078" style="zoom:50%;" />

     断点调试：在url中传入参数，在调试器能看到获得了请求参数

     ![image-20241209112741513](C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209112741513.png)

   * 在urls.py中完成路由配置

4. 前端实现级联选框，业务-集群-模块联动，直接使用课程提供的前端材料包。但是注意在 store/modules/example.js 中添加 JS 函数，实现与后端 API 的联通时,访问后端的地址在本地和部署上线时不相同
   下面是部署上线时的情况：

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209113156766.png" alt="image-20241209113156766" style="zoom:50%;" />

5. 实现主机查询接口，在后端模块实现路由函数`get_hosts_list`, 调用API获得信息，注意和前面的路由函数传入给api的参数不同，这里存在可选参数
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209113414069.png" alt="image-20241209113414069" style="zoom:50%;" />

6. 设计额外查询条件&表单，实现主机列表数据渲染至前端。直接使用课程提供的前端代码包

7.   实现主机详情接口：在后端模块添加`get_host_detail`路由函数
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209113711868.png" alt="image-20241209113711868" style="zoom:50%;" />

8. 前端实现主机详情渲染到前端侧边栏

9. 部署上线：

   * 将本地仓库变化push到远程仓库

   * 先部署后端模块

   * 根据后端模块的访问地址调整前后端连通时使用的后端url
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209113156766.png" alt="image-20241209113156766" style="zoom:50%;" />

   * 部署前端模块

   * 访问结果：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241209114315569.png" alt="image-20241209114315569" style="zoom:50%;" />

     ![img](https://smartpublic-10032816.cos-website.ap-shanghai.myqcloud.com/custom/20241129172059/41431/20241129172059/--d573cc1719a4b6477c03d31d9cd6a723.png)

### 六：实验体会和心得

* 问题1：一开始访问biz-list时接口没有返回数据
  <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210180035001.png" alt="image-20241210180035001" style="zoom:50%;" />

  解决：账号没有访问权限，找助教老师帮忙处理

* 问题2：在本地运行正常，但是部署时根据实验手册修改前后端连通访问是后端url后，前端模块访问报错

  <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210180106409.png" alt="image-20241210180106409" style="zoom:50%;" />

  解决：前端模块中访问后端url不能直接按照实验手册修改为https://apps, 查看开发者中心模块配置处后端的访问地址可看见为https://apps1。后面助教老师答疑是由于蓝鲸实验环境加了新的集群，访问地址会有变动，新部署的都是apps1.ce.bktencent.com/<app_code>

## 第三次作业-第二次迭代

### 一：实验目的

（1）     了解蓝鲸作业平台的功能与使用方法

（2）     掌握作业平台的基本概念和作业平台的基本使用

（3）     熟悉脚本的概念和语法，学习简单脚本的编写

（4）     掌握作业平台 “方案执行”、“获取作业执行状态”等接口的调用

（5）     熟悉Django模型的设计和ORM操作，完成备份记录的建模和数据库读写功能

（6）     提升SaaS应用的开发技能，巩固Django基础知识

### 二：实验环境

（1）    硬件环境需求： PC或笔记本， 支持外网访问

（2）    软件环境需求

​		系统： Windows, MacOS, Linux

​		安装 Python 3.6.12 

​		安装 MySQL 8.3 

​		安装 Git (最新版本即可) 

​		安装 pre-commit代码检查工具（可选）

​		安装 VSCode，PyCharm 或其它 IDE

### 三：实验内容

 在《基于CMDB配置平台管理游戏的主机》的基础上，借助蓝鲸作业平台编写脚本，通过蓝鲸网关/ESB组件API调用作业平台接口实现文件的查询和备份，并根据文件查询和备份条件，设计对应接口；同时记下备份记录，实现备份记录的查询功能。

### 四：实验评分标准

考点一：在作业平台编写简单脚本，实现文件查询和文件备份执行方案

考点二：在《基于CMDB配置平台管理游戏的主机》的基础上，实现文件查询接口，通过蓝鲸 ESB组件API联通作业平台进行方案执行和结果查询，并在前端进行参数传递和数据渲染

考点三：实现文件备份接口，通过蓝鲸 ESB组件API联通作业平台进行方案执行和结果查询，记下备份记录，并在前端进行参数传递和数据渲染

考点四：实现备份记录查询接口，展示备份主机、备份文件目录、备份文件后缀等信息，并附上备份执行结果链接，点击可跳转作业平台对应的执行方案结果页面

### 五：实验过程和结果

在第二次作业应用的基础上，新建了前端模块fronted_lab3, 后端模块不变

1. 在作业平台上创建执行方案

   * 文件查询：

     * 创建作业：
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210112136917.png" alt="image-20241210112136917" style="zoom:50%;" />

       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210112153721.png" alt="image-20241210112153721" style="zoom:50%;" />

     * 创建执行方案 :
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210112327040.png" alt="image-20241210112327040" style="zoom:50%;" />

       测试执行方案，成功运行
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210112406073.png" alt="image-20241210112406073" style="zoom:50%;" />

   * 文件备份：

     * 创建作业：

       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210112635145.png" alt="image-20241210112635145" style="zoom:50%;" />

       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210112704988.png" alt="image-20241210112704988" style="zoom:50%;" />

     * 创建执行方案：
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210112755610.png" alt="image-20241210112755610" style="zoom:50%;" />

       调用执行方案，执行成功

       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210112927082.png" alt="image-20241210112927082" style="zoom:50%;" />

2. 后端实现文件查询接口：

   * .env文件中添加访问作业平台的前缀
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210113207928.png" alt="image-20241210113207928" style="zoom:50%;" />

   * 在home application下创建constants.py文件，设置好调用执行方案的预设常量
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210113446173.png" alt="image-20241210113446173" style="zoom:50%;" />

   * 在views.py下编写查询文件的路由函数：

     * 调用execute_job_plan接口执行执行方案
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210113810828.png" alt="image-20241210113810828" style="zoom:50%;" />

     * 调用get_job_instance_status接口获取执行状态
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210113955029.png" alt="image-20241210113955029" style="zoom:50%;" />
     * 调用get_job_instance_ip_log接口获取执行结果并返回
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210114150842.png" alt="image-20241210114150842" style="zoom:50%;" />

3. 前端实现文件查询功能：此处直接使用课程提供的前端代码包

4. 后端实现文件备份接口：

   * 在models.py给备份记录建模：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210114537853.png" alt="image-20241210114537853" style="zoom:50%;" />

   * 实现数据库迁移：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210114655772.png" alt="image-20241210114655772" style="zoom:50%;" />

     ![image-20241210114706917](C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210114706917.png)

   * 在views.py下编写备份文件的路由函数：

     * 调用execute_job_plan接口执行执行方案
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210114822603.png" alt="image-20241210114822603" style="zoom:50%;" />
     * 调用get_job_instance_status接口获取执行状态
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210170206119.png" alt="image-20241210170206119" style="zoom:50%;" />
     * 调用get_job_instance_ip_log接口获取执行结果并返回
       <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210170256778.png" alt="image-20241210170256778" style="zoom:50%;" />

5. 前端实现文件备份功能：此处直接使用课程提供的前端代码包
6. 后端备份记录查询接口：在views.py中完成对应路由函数
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210170500017.png" alt="image-20241210170500017" style="zoom:50%;" />

7. 部署上线：先部署后端模块再部署前端模块，实验结果如下：
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210170745034.png" alt="image-20241210170745034" style="zoom:50%;" />
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210170807008.png" alt="image-20241210170807008" style="zoom:50%;" />

### 六：实验心得和体会

* 问题：部署时前端模块中前后端连通时，前端访问后端模块的url为http开头会导致访问页面为空白

  解决：将http开头改为https开头

* 体会到了如何在后端调用API连通作业平台进行方案执行和结果查询

  

## 第四次作业：第三次迭代

### 一：实验目的

（1）     巩固SaaS应用的软件开发&设计能力

（2）     了解蓝鲸BKVision图表平台的产品功能与使用方法

（3）     掌握基本Django中间件的开发技能与数据采集

（4）     掌握蓝鲸图表平台的嵌入方式与SDK使用

（5）     提升SaaS开发技能，巩固基础数据分析能力与数据采集技能

（6）     提升SaaS开发技能，进一步熟悉开发框架与后台建模

### 二：实验环境

（1）    硬件环境需求： PC或笔记本， 支持外网访问

（2）    软件环境需求

​		系统： Windows, MacOS, Linux

​		安装 Python 3.6.12 

​		安装 MySQL 8.3 

​		安装 Git (最新版本即可) 

​		安装 pre-commit代码检查工具（可选）

​		安装 VSCode，PyCharm 或其它 IDE 

### 三：实验内容

在此前两期SaaS开发作业的基础上，借助蓝鲸BKVision图表平台实现用户行为可视化分析与前端嵌入，通过设计并开发Django中间件，实现用户行为数据埋点采集并存储至数据库，通过BKVision实现仪表盘嵌入。

### 四：实验评分标准

考点一： 在此前两期课程SaaS作业的基础上，通过Django中间件实现用户行为采集并存储到SaaS数据库，比如：登录行为、查询业务列表行为、执行作业行为等

考点二：在BKVision图表平台创建空间，接入对应的SaaS数据库，并对采集的数据进行仪表盘配置（仪表盘样式不限，鼓励大家自由发挥），并发布仪表盘。

考点三：设计通过iFrame或BKVision-SDK方式，实现仪表盘发布并嵌入到对应的SaaS前端界面中。

### 五：实验过程和结果

前后端模块都直接在上次迭代的基础上改动

1. 实现用户行为数据存储model

   * 在models.py中实现ApiRequestCount模型：包含属性API类别，API名称，请求次数
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210172248763.png" alt="image-20241210172248763" style="zoom:50%;" />

2. 执行数据库迁移（前面已经设置过了，可以直接执行）
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210172458554.png" alt="image-20241210172458554" style="zoom:50%;" />
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210172511168.png" alt="image-20241210172511168" style="zoom:50%;" />

3. 设置自定义中间件，实现用户行为埋点记录

   * 原理图：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210172815282.png" alt="image-20241210172815282" style="zoom:50%;" />
   * 在core/middleware.py文件下实现自定义中间件
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210173032238.png" alt="image-20241210173032238" style="zoom:50%;" />
   * 添加自定义中间件到config中：注意自定义中间件要添加到默认中间件的后面
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210173158057.png" alt="image-20241210173158057" style="zoom:50%;" />

4. 推送后端代码到远程仓库并且部署上线

5. 在BKVision平台添加并配置数据源

   * 数据源配置：
     <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210173505418.png" alt="image-20241210173505418" style="zoom:50%;" />、

6. 创建并配置仪表盘：

   仪表盘配置如下：其他柱状图，折线图，扇形图也做类似配置

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210173546306.png" alt="image-20241210173546306" style="zoom:50%;" />

   最终实现效果为：
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210173647094.png" alt="image-20241210173647094" style="zoom:50%;" />

7. 将仪表盘嵌入前端应用：此处直接采用课程提供的前端代码包
   但是需要将src/views/DashBoard目录下的index.vue下的的iFram代码改为BKVision平台中自己仪表盘生成的代码（且把http协议改为https协议）

   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210174729043.png" alt="image-20241210174729043" style="zoom:50%;" />

8. 发布仪表盘并且推送代码到远程仓库，部署上线，实验结果如下
   <img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241210174836873.png" alt="image-20241210174836873" style="zoom:50%;" />

### 六：实验心得和体会

通过本次实验，我了解了丰富的图表类型、灵活的数据配置、以及如何与应用的数据库交互。我学习如何快速上手并使用该平台和如何根据应用数据源配置仪表盘中的参数
通过本次实验，我还掌握了Django中间件的基本概念和原理，还学会了如何编写自己的中间件来实现特定的功能





