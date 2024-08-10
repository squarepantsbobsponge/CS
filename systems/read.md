## LLM

#### 1. 微调Fine-Tuning

Fine-Tuning的基本思想是采用已经在大量文本上进行训练的预训练语言模型，然后在小规模的任务特定上继续训练它。

#### 2. 提示微调Prompt-Tuning

* 特点：让下游任务去迁就预训练模型
* 步骤：构建模板，标签词预测，训练

##### 2.1 上下文学习 In-context learning

* 概述：ICL根据input生成提示和一些上下文演示（就是一些具体的例子），然后输入到语言模型中预测，不需要参数的梯度更新而是直接推理。这些提示和示例共同构建了一个上下文环境，引导模型根据这个环境来生成针对新任务的预测或响应。（这是在一个已经训练好的大模型上面进行微调）
  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240727172619487.png" alt="image-20240727172619487" style="zoom:67%;" />
* **training：**在推理前，通过持续学习让语言模型的ICL能力得到进一步提升，这个过程称之为**model warmup**（模型预热），model warmup会优化语言模型的参数或者新增参数
* **Inference: **，同一个问题如果加上不同的示例，可能会得到不同的模型生成结果。

##### 2.2 Pattern-Verbalizer-Pair（PVP）



## LERAGING REINFORCEMENT LEARNING AND LARGE LANGUAGE MODELS FOR CODE OPTIMIZATION

*  问题：利用大模型和强化学习辅助代码优化，但是训练数据集都是通用的，无法满足需求，或者没有利用好强化学习和环境的反馈交互

*  挑战：
  1. 如何将测试的反馈用于LLM的训练
  2. 如何使小模型的性能和大模型的性能相似
  3. 如何使小模型能生成少错误的可靠代码和解决完成代码优化任务

*  框架：

   *  大模型微调：

      *  codeT5（自然语言混合编程语言的输入）
      *  微调目标：最小化交叉熵损失![image-20240723163401014](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723163401014.png)

   *  样本生成：（采什么的样？？）

      *  策略：贪心采样，随机采样

         贪心策略：topB约束

   * 强化学习：评分模型，奖励模型![image-20240723173446617](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723173446617.png)

     * reward：![image-20240723174255589](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723174255589.png)

     * score：

       ![image-20240723174408255](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723174408255.png)

## RLADAPTER: BRIDGING LARGE LANGUAGE MODELS TO REINFORCEMENT LEARNING IN OPEN WORLDS  
* key: 考虑增加可调节模块来帮助llm适应环境。 这种见解促使提出RLAdapter框架， 旨在增强RL算法
  和llm之间的协作。 (不用修改LLM)![image-20240723215431938](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723215431938.png)
*   