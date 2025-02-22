### 学习内容：

1. 编写PX4应用程序，并且在仿真（<code>SITL</code>）中运行。

   * 步骤1：编写简单自定义应用程序，打印<code>Hello Sky!</code>。参考：https://docs.px4.io/main/zh/modules/hello_sky.html

   * 步骤2：在PX4-Autopilot/boards/px4/sitl/default.px4board中启用应用程序

   * 步骤3：在PX4-Autopilot/build/px4-sitl_defalut/px4_boardconfig.h中启用引用程序

   * 步骤4：在PX4-Autopilot/下编译 <code>make px4_sitl_default </code>

   * 步骤5：启动仿真环境： <code>make px4_sitl_default {gazebo/gazebo-classic}(选择自己启用的仿真软件)</code>

     * 在控制台输入<code>help</code>时，能找到编写的自定义程序<code>px4_simple_app</code>
       <img src=".\picture\image1.png">  

     * 在控制台输入自定义程序名称，运行该程序会打印相关内容
       <img src=".\picture\image2.png">

### 本周任务：

1. 编写应用程序<code>my_example_app</code>，实现如下功能:

   * 在控制台输入<code>my_example_app time</code>时，控制台隔 1s打印程序启动的时间，效果如下：

     <img src=".\picture\image3.png">

   * 在控制台输入<code>my_example_app count a b</code>时，计算并打印a+b的结果，效果如下

     <img src=".\picture\image4.png">

   * 注意：要在一个程序内完成所有功能

   * 提示：程序如何从控制台获得输入：考虑<code>int my_example_app_main(int argc, char *argv[])</code>中的<code>argc</code>和<code>argv</code> 

### 评分标准：

| 评分项                                  | 积分值 |
| --------------------------------------- | ------ |
| 编写应用程序<code>my_example_app</code> | 30     |
|                                         |        |
|                                         |        |

