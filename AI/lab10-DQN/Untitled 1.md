### V值

* 定义：评估状态的价值，代表了智能体在这个状态下，一直到最终状态得到的总的奖励的期望值
* V值：计算当前状态S到最终状态，得到的总的奖励的期望值。

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240613200259792.png" alt="image-20240613200259792" style="zoom:67%;" />

### Q值

* 评估动作的价值，选择该动作后，一直到最终状态得到的总的奖励的期望
* 从某个动作出发，走到最终状态时，最终获得奖励总和的平均值（奖励期望），就是Q值。
* 与V值不同，Q值和策略π \piπ并没有直接关系，而是与环境的状态转移概率有关（环境的状态转移概率是未知的，我们无法学习也无法改变）。

### 根据Q值算V值

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240613200753682.png" alt="image-20240613200753682" style="zoom:67%;" />

### 根据V值算Q值

![image-20240613200914209](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240613200914209.png)

### 根据V值算V值





