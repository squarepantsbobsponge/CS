

## Q_learning 算法

数据结构：将<code>state</code>和<code>action</code>对应的Q值建表存储，根据Q值在不同<code>state</code>下选择最大 的Q值对应的<code>action</code>

优化过程：TD时间差分法

伪代码：

![image-20240521175638572](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240521175638572.png)

例子：

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240521175735158.png" alt="image-20240521175735158" style="zoom:67%;" />

![image-20240521175843154](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240521175843154.png)

![image-20240521175900767](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240521175900767.png)

随机选择动作就是所有动作的概率相同，贪心的选择动作就是选择最大Q值的动作

## SARSA算法

与Q_learning的区别所在：Q值更新策略不同

![image-20240521180245682](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240521180245682.png)



![image-20240526123834953](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240526123834953.png)

问题：总是在几个状态处来回切换，q_table始终为0000

问题：其他格子都是0奖励，趋利避害肯定来来回回在安全状态切换

改进：加了回溯惩罚，用欧几里得距离修改了奖励值，使它尽力趋近那个真实奖励值为1的黄点
