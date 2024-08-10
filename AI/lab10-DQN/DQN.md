# DQN算法原理

## 经验回放

将探索环境得到的数据储存起来 ，随机采样小批次样本更新深度神经网络的参数

怎么采样呢

每个时间步采样一次，但是一开始采样池为空的

两种做法：要不就是按步就班采样，要不就是先采样一部分再开始训练

## 目标网络

额外引入目标网络（和Q网络具有相同的网络结构）

不更新梯度，每隔一段时间将Q网络的参数赋值给此目标网络

跟Q_learning的区别：Q_learnning更新Q值表的时候不会影响其他Q值，但是神经网络会，为了保证监督标签的稳定，所以需要保存一个目标网络。这个在时间差分时给出$Q^‘$​的值

## 环境模型

```
reset()//重置环境
step(self,action)//推进时间步长
render:重绘环境的一帧
close()；关闭环境并且清空内存
```

step返回值：

![image-20240529135200794](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240529135200794.png)

reward是坚持时间

action只有0 1

![image-20240529135559325](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240529135559325.png)

原理：

![image-20240529135728917](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240529135728917.png)![image-20240529135743003](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240529135743003.png)

![image-20240529135752340](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240529135752340.png)



注意：要更新state



## 画图

每次轨迹采样

改一下count和print的顺序

要清空采样池每次改种子的时候

后面看画图的时候种子数弄少一点，等太久了

有点过拟合了，要改一下迭代次数

已经改进成DDQN了效果好很多，可以考虑一下改进采样池数量和迭代次数
