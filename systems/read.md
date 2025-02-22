[TOC]



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

* pattern：带有mask标记的短文本
* Verbalizer：标签词的映射

##### 2.3 Prompt-Tuning

* Hard Prompt VS Soft Prompt：离散模板构建法的模板参数固定（每个任务都一样），连续模板构建法

#### 3. Instruction-Tuning（指示微调）

* Instruction的目的是告诉模型如何处理数据或执行某个操作，而不是简单地提供上下文或任务相关信息。


  因此，Prompt和instruction都是用于指导模型生成输出的文本，但它们的目的和使用方式是不同的。Prompt更多地用于帮助模型理解任务和上下文，而Instruction则更多地用于指导模型执行具体操作或完成任务。
#### 4. 思维链

思维链简单的说就是一系列中间推理步骤。这篇论文最大的贡献就是发现了在LLM生成推理任务的结果之前，先生成思维链，会使模型的推理性能有大幅度的提升，特别是在复杂的推理任务上，但是有个前提就是LLM的规模要大于10B，否则CoT没用甚至起副作用。

##### 4.1 人工思维链

<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240811220902202.png" alt="image-20240811220902202" style="zoom:67%;" />

##### 4.2 Zero-shot-CoT（零示例思维链）

##### 4.3 Auto-CoT(自动思维链)

#### 5. PEFT 参数有效性微调

部分参数微调

##### 5.1

* Prefix-Tuning： 
* P-Tuning v2
* Adapter-Tuning: ，Adapter-Tuning 则是在预训练模型内部的网络层之间添加新的网络层或模块来适配下游任务。
* LoRA：在模型的Linear层的旁边，增加一个“旁支”，这个“旁支”的作用，就是代替原有的参数矩阵W WW进行训练。
*  对于左右两个部分，右侧看起来像是左侧原有矩阵W WW的分解，将参数量从$d × d $变成了$d × r + d × r $

* AdaLoRA：

#### 6 GPT

##### 6.1 gpt1

* 任务：自然语言推理，问答和常识推理，语义相似度，分类
* 模型结构：<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240812132707676.png" alt="image-20240812132707676" style="zoom:67%;" />
* 模型训练：1）在大规模无标注文本数据上学习到一个高容量的语言模型；2）在标注数据上进行微调。其中第二步是针对具体的下游任务来进行训练的。
  * 无监督训练
  * 监督训练: 
  * 下游任务：
    * 分类任务：将起始和终止token加入到原始序列两端，输入transformer中得到特征向量，最后经过一个全连接得到预测的概率分布；
    * 自然语言推理：将前提（premise）和假设（hypothesis）通过分隔符（Delimiter）隔开，两端加上起始和终止token。再依次通过transformer和全连接得到预测结果；
    * 语义相似度：输入的两个句子，正向和反向各拼接一次（由于相似性质是对称的，为了消除顺序的影响），然后分别输入给transformer，得到的特征向量拼接后再送给全连接得到预测结果；
    * 问答和常识推理：将个选项的问题抽象化为个二分类问题，即每个选项分别和内容进行拼接，然后各送入transformer和全连接中，最后选择置信度最高的作为预测结果。

##### 6.2 gpt2

* 模型训练：

* <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240812134459804.png" alt="image-20240812134459804" style="zoom:67%;" />

  模型训练：只有预训练过程

  * 无监督训练：在下游任务中，不采用Fine-Tuning方法，而是采用zero-shot方法
  * 下游任务：为什么可以这么讲呢？因为作者认为：下游任务 (有监督训练) 可以视为预训练过程 (无监督训练) 的一个子集。无监督目标的全局最优解也是有监督训练的全局最优解。当预训练规模足够大时，把无监督的任务训练好了，有监督的下游任务即不再需要额外训练，就是所谓的zero-shot。

##### 6.3 gpt3

* **模型训练**：GPT-3也只有预训练过程，GPT-3采用了In-context learning。

* 下游任务：

  

## LERAGING REINFORCEMENT LEARNING AND LARGE LANGUAGE MODELS FOR CODE OPTIMIZATION

*  问题：

   *  LLM ----->  LLM+RL(增加与环境的反馈，使给定程序的功能正确性得到确认) ----->  PerfRL（快，小，正确）

   *  利用大模型和强化学习辅助代码优化，但是训练数据集都是通用的，无法满足需求，或者没有利用好强化学习和环境的反馈交互

*  挑战：
  1. 如何将测试的反馈用于LLM的训练
  2. 如何使小模型的性能和大模型的性能相似
  3. 如何使小模型能生成少错误的可靠代码和解决完成代码优化任务

*  补充：

   *  multi-turn program synthesis：在多轮程序合成中，系统通过与用户之间的多次对话来逐步细化和完善生成的程序。这种方法通常用于处理复杂的程序合成任务，其中程序的规模较大或者问题的描述不够清晰，需要更多的交互以便系统能够更好地理解用户的意图并生成符合要求的程序
   *  PIE数据集：包含trajectories of programs（程序的轨迹？），程序从较低的版本优化成高级版本的过程  

*  问题定义：

   *  优化程序集X，使得给定相同输入，优化前后的输出相同
   *  最大化cost：生成的候选优化程序<code>ybest</code>
      ![image-20240905102758409](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240905102758409.png)
      *  <code>perf(ybest)</code>：<code>ybest</code>相当于<code>x</code>在单元测试中的性能改进
      *  <code>eq(R,ybest)</code>：给定input，生成序列和单元测试输出的匹配

   *  最大化生成<code>ybest</code>的概率：
      <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240905103343747.png" alt="image-20240905103343747" style="zoom: 67%;" />
      *  $ \theta ^*$​是模型的最优参数合集

   *  看待代码优化问题的角度：RL算法的复杂性、 LM的大小
      以及所使用的数据集与代码优化任务的相关性  
      <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240905104118647.png" alt="image-20240905104118647" style="zoom:67%;" />
   *  问题：减少模型大小，保证生成代码的可靠性

*  框架：

   *  大模型微调：

      * 在专门用于代码优化任务的数据集上对LLM模型微调

      * codeT5（自然语言混合编程语言的输入）

      * few-shot 采样策略旨在让模型在面对少量标记数据时表现良好，通过有效利用有限的样本来提升模型的泛化能力和适应性，训练codeT5（让模型提高输入程序的性能）

      * 微调目标：最小化交叉熵损失 （？？y）

        ![image-20240723163401014](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723163401014.png)
        $\theta$​：LLM的参数；N：tokens的数量；V：tokenizer的词汇集；pi,j：位置i的词汇表中第j个标记的预测概率  

   *  样本生成：（采什么的样？？候选代码样本）

      *  策略：贪心采样，随机采样

         * 带波束（束宽为B）的贪心采样：
           束搜索：根据评分函数保留保留多个备选解，束宽决定每一步中保留的备选解的数量。
           * 每个样本计算top B候选词汇表及其累积概率并进行排名。 选择所有累积概率最大的候选词汇中的top B序列来重复生成下一个token的过程
             <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240905113242227.png" alt="image-20240905113242227" style="zoom:67%;" />

         * 随机采样：  
           * 根据$p_i$​选择 前k个token，并且随机选择一个
             <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240905113831350.png" alt="image-20240905113831350" style="zoom: 50%;" />

      *  **训练阶段**：

         * **随机抽样**：首先通过随机抽样从独立运行的结果中选择两个候选样本。
         * **贪婪抽样**：对这两个候选样本进行贪婪抽样，选择具有最高概率的候选样本。
         * **目标序列**：为了确保至少有一个正确的样本，将数据集中的目标序列也包含在样本列表中。
         * **输入模型**：将这四个样本用于每一步的模型输入。

      *  **验证和测试阶段**：

         * **贪婪抽样与束搜索**：在验证和测试过程中，使用贪婪抽样与束搜索生成四个样本，并返回排名前两的候选结果。
         * **评估标准**：对于给定的输入，生成两个候选结果进行评估。一个样本被认为成功，当其执行时间优于输入代码时。

   *  强化学习：评分模型，奖励模型

     * 框架：

       ![image-20240723173446617](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723173446617.png)

       * (a)：用训练集数据微调LLM模型；将inputcode放进LLM生成优化样本；在score和reward模型中分别计算每个样本的得分和奖励；利用得分和奖励计算Loss给RL，并利用feedback重新训练模型
       * (b)：reward 模型
       * (c): Inference :  reward不达标的样本直接丢掉

     * reward：![image-20240723174255589](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723174255589.png)

     * score：

       ![image-20240723174408255](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723174408255.png)

     * 最小化奖励较小的输出的概率：
       <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240905121523911.png" alt="image-20240905121523911" style="zoom:67%;" />

     * 最大化最佳奖励候选
       <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240905121815626.png" alt="image-20240905121815626" style="zoom:50%;" />

     * Loss：
       <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240905121913039.png" alt="image-20240905121913039" style="zoom:67%;" />

       

## RLADAPTER: BRIDGING LARGE LANGUAGE MODELS TO REINFORCEMENT LEARNING IN OPEN WORLDS  

* RLAdapter：key: 考虑增加可调节模块来帮助llm适应环境。 这种见解促使提出RLAdapter框架， 旨在增强RL算法和llm之间的协作。 (不用修改LLM)![image-20240723215431938](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240723215431938.png)
* 用下游任务的数据对LLM微调，会导致LLM的泛化性能下降，迁移性下降

#### 3 方法

##### 框架：

##### <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240812190518471.png" alt="image-20240812190518471" style="zoom:67%;" />

env和agent将信息提供给Adapter Model；Adapter Model根据Agent最近的动作和环境的反馈对比LLM提出的子目标，看他们的相似度，给出个理解分数，表示agent是否在正确执行和跟随LLM的子目标的指导；Adapter Model将理解分数提供给LLM，LLM进一步指导agent

* 关注于添加可调节模块来帮助llm灵活地适应环境，而不是直接修改llm。

* 适配性模型：

  * 输入：关于环境的基本信息和agent当前对语言指导的理解水平u

    g为LLM给的目标，$ t $为嵌入后的轨迹，u测量二者的相似度

    ![image-20240907095356523](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240907095356523.png)
  * 将输入整合成适配器模型的提示，提取重要细节，生成汇总信息

* 训练流程：

  * LLM接收到适应的提示c ~ Mada(提示(B, u))时，生成g ~ MLLM(提示(B, c))，随后将其提供给策略π(a|o, gemb)进行训练，其中gemb是由femb编码的文本嵌入

  * 在查询语言模型之间设置预定的间隔，在间隔期间保持一致的指导
    ![image-20240812201407706](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240812201407706.png)
  * 初始化阶段：
    * **策略 π**：初始化一个策略，用于在给定当前状态和环境生成文本（`gt`）的条件下选择动作。
    * **缓冲区 B**：用于存储交互历史，包括观察（`ot`）、动作（`at`）、下一个观察（`ot+1`）、奖励（`rt`）和生成的文本（`gt`）。
    * **SFT 缓冲区 D**：用于存储需要用于监督微调（SFT）的样本。
    * **参数**：设置 LLM 生成文本的间隔 `Ngen`、SFT 的间隔 `Nsft` 以及 ROGUE-L 阈值 `θ`，用于评估生成的文本质量。
  * 生成阶段
    * **步骤 5-9**：每隔 `Ngen` 时间步，使用 `Mada`（可能是指某种适配器模型）和 LLM（大型语言模型）来生成文本 `ct` 和 `gt`。如果未到达生成间隔，则复用前一次的生成结果
  * 环境交互阶段
    * **步骤 10-11**：根据当前策略和生成的文本 `gt` 选择动作 `at`，并与环境交互获得下一个观察 `ot+1`。

  * 更新阶段

    * **步骤 12**：更新缓冲区 B，加入新的交互数据。

    * **步骤 13**：使用缓冲区 B 的数据更新策略 π。

  * 理解和微调阶段

    * **步骤 16**：计算当前生成文本 `gt` 与缓冲区 B 中随机选取的样本 `τ` 的嵌入向量之间的余弦相似度 `ut+1`，作为对生成文本理解程度的评估。

    * **步骤 17-19**：如果 `gt` 的质量（通过 ROGUE-L 分数衡量）低于阈值 `θ`，则将其与相应的提示一起加入 SFT 缓冲区 D。

    * **步骤 20-23**：每隔 `Nsft` 时间步，使用 SFT 缓冲区 D 中的数据对适配器模型 `Mada` 进行监督微调，以提高其生成文本的质量和适应性。

#### 4 实验

* 目的：

  • 适配器模型的集成可以增强大型语言模型对下游任务的理解和智能体的理解能力， 从
  而产生更有意义的指导。
  • 在RLAdapter框架下训练的智能体可以表现出更出色的性能， 并表现出更符合常识的行
  为。  

* 评价指标：
  * 每个环境中：打开新成就，reward+1；获得/减少1个生命点，reward+0.1/-0.1；
  * 22个环境的总评分：
    <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240907103445510.png" alt="image-20240907103445510" style="zoom:67%;" />
* 



## ML-based Fault Injection for Autonomous Vehicles: A Case for Bayesian Fault Injection（注入故障）

故障注入（Fault Injection）是一种重要的测试技术，主要用于评估系统（包括软件和硬件）在面临异常情况时的可靠性和稳定性。通过人为地向系统中引入故障，并观察系统在这些故障条件下的行为，可以检测出潜在的设计缺陷、恢复机制失效以及安全漏洞等问题，从而改进系统设计，增强其抵抗真实故障的能力



介绍了故障注入工具DriveFI， 以及经验评估ADS故障传播、 弹性和安全特性的方法， 以及生成和测试角落案例故障条件的方法。 DriveFI结合了贝叶斯和传统的FI框架， 它们协同工作以加速发现安全关键故障。  

DriveFI包含一个FI引擎，可以改变自动驾驶系统的软硬件状态，和一个机器学习错误引擎（贝叶斯错误引擎），可以找到最有可能违反安全条件的清况和状态

基于横向纵向的安全停止距离来建模安全情况，用真实错误故障模型来模拟软件和硬件错误。

贝叶斯网络可以用可解释的模型对自动驾驶系统组件之间的故障传播进行建模。

使用三个故障模型：关于处理器的；关于ADS软件输出随机和均与故障；ADS模块输出损坏为贝叶斯FI的故障

#### 1 方法概述

* 自动驾驶汽车基本架构：（actuators为制动器）

  由机械部件和执行器组成， 由ADS控制， 它代表自动驾驶的计算(硬件和软件)组件。 在时间t的每一个瞬间， ADS系统从传感器It(例如， 摄像头， 激光雷达， GPS)输入， 从机械部件(例如， 速度vt， 加速度at))获取惯性测量Mt， 并推断驱动命令At(例如， 油门ζ， 制动b， 转向角φ

  将ADS细分为两个组件:(a) ML模块(负责感知和规划)（包含处理输入数据的机器学习模型的具体配置的配置参数C和世界模型）， 将It和Mt作为输入并产生原始驱动命令UA,t， 以(b) PID控制器[33]， 负责平滑输出UA,t以产生  

    <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240813110629166.png" alt="image-20240813110629166" style="zoom: 80%;" />

* 安全：
  
  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240928215758746.png" alt="image-20240928215758746" style="zoom:67%;" />
  
  * 停车距离$d_{stop}$被定义为在应用最大舒适减速amax时，车辆在完全停车前行驶的最大距离。
  * AV车辆的安全包络$d_{safe}$， [2]定义为AV车辆在不与任何静态或动态物体发生碰撞的情况下所能行驶的最大距离
  * 安全潜力δ定义为$δ=d_{safe}-d_{stop}$。 当横向和纵向δ均> 0时， AV处于安全状态。
  
* 故障注入：
  
  * ML和FI相互配合，ML找到最容易导致故障的错误，FI模拟错误
  * 注入障碍由位置和注入值表征
  * 输出：直接将错误注入ADS输出（ADS输入输出存在不同的变量上，变量在内存单元和寄存器，将错误注入到内存单元和寄存器（只需要单个bit或者多个bit错误））将错误注入到内存单元中，但变量被损坏以模拟故障
  * 基线为FI引擎的随机注入
  * 最后几乎没有发现故障，因为ADS堆栈的自然弹性和实施推断的ADS系统，瞬态故障没有机会传播到执行器
  * 贝叶斯故障注入：找到注入故障的临界点，没注入之前是安全的，注入后是不安全![image-20240928222004908](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240928222004908.png)
  * 用贝叶斯网络捕捉因果关系（$I_t$为传感器输入,$M_t$为机器硬件输入（如IMU的运动学信息），$U_{A,t}$ADS ML模块传给PID模块，$A_t$PID控制器传给制动器的命令，$W_t$​​世界模型）贝叶斯网络（红色箭头是随时间变化的）
    <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240928223008627.png" alt="image-20240928223008627" style="zoom:67%;" />
  * 最大似然法预测$M_{t+1}$
  
* 案例（用贝叶斯故障注入的重要性而不是随机注入）：
  * 危险错误：要用贝叶斯故障注入精确注入故障
  * Real-World Crash：特斯拉自驾仪引起的现实故障世界

  #### 2. 贝叶斯故障注入

* 基于运动学的安全模型：

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240813175316829.png" alt="image-20240813175316829" style="zoom:80%;" />

  （车辆在时刻t有一个瞬时位置(xt;Yt)，速度vt，航向θt，转向角φt。）

  $dx_t/dt = v_t cos θ_t; dy_t/dt = v_t sin θ_t; dθ_t/dt = (v_t tan φ_t)/L(L是两个轮子间的距离)  $​

  （只考虑二维简单的情况）

  * 紧急停车机动：d_stop 龙格库达法计算

    <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240929094236500.png" alt="image-20240929094236500" style="zoom:67%;" />

    ![image-20240929094251701](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240929094251701.png)

    * 紧急停车模式下的$d_{stop}$(最大加速度停车且转向角无改变)​

      <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240929095115756.png" alt="image-20240929095115756" style="zoom:67%;" />

      ![image-20240929095201300](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240929095201300.png)

    * dsafe：传感器测量得到的车辆离最近障碍物的距离

  * 离散化：离散时间是ADS的自然选择， 因为控制决策是在与传感器采样频率相对应的离散步骤上做出的。 

* ML model (机器学习模型)
  * 目标：目标故障注入器的目标是找到δ> 0， 但在向ADS堆栈注入故障f(表现为EV运动状态的变化)的情况下， δdo(f)≤0。  （找到临界值）

  * 模型：估计时间k + 1处dstop的值 ，需要知道xk+1、 yk+1、 vk+1、 θk+1和φk+1的值作为启动紧急停止机动的初始条件 （使用ADS的贝叶斯网络的后验概率的最大似然法） 
    
    * DriveFI使用动态贝叶斯网络(DBN)[41]， 特别是3-Temporal贝叶斯网络(TBN)， 即展开三次的DBN， 对xk+1、yk+1、 vk+1、 θk+1和φk+1进行建模。 ![image-20240825144233925](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240825144233925.png) 
    
    * 对节点的条件概率模型为正态分布
      ![image-20240929144243190](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240929144243190.png)
      
    * 概率推理：先在无障碍条件下执行模拟，得到其他变量的正确运行值。首先通过使用马尔可夫链蒙特卡洛方法[41]估计vk+1的后验分布， 然后估计vk+1的最有可能值。其他值类似相同的方法
    
      最后得到：<img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240825154114912.png" alt="image-20240825154114912" style="zoom:67%;" />（这个估计是拿来找到不安全状态，然后找到临界故障的）
    
  * 训练：找到最契合训练数据的$\theta $
  
    ![image-20240825151559973](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240825151559973.png)
  
    * **拓展**：对数概率的期望能够帮助检测模型的拟合性（对数概率 log*P*(*X*∣*μ*,*σ*) 代表了在给定模型参数 *μ* 和 *σ* 下观测到数据 *X* 的“惊喜度”的负对数。当概率 *P*(*X*∣*μ*,*σ*) 较高时，对数概率也较高（尽管是负的），表示观测到 *X* 并不那么“意外”。相反，当概率较低时，对数概率也较低，表示观测到 *X* 是比较“意外”的。）
      对数概率的期望实际上是对数似然函数（log-likelihood function）的期望值，它衡量了模型在给定的参数下，生成观测数据的“合理性”或“可能性”。当对数概率的期望较高时，意味着模型能够很好地解释或拟合观测到的数据。这通常表明模型的参数设置得当，能够捕捉到数据中的关键特征。
  
  * 训练数据获取：
  
    * Xk中的变量是通过在模拟器中多个驾驶场景中执行ADS来测量的  
    * 驾驶场景中注入随机障碍
  
  * 障碍注射
  
    * 先准备好一个没有障碍的模拟执行，得到黄金参数
  
    * 用黄金参数搭建好模拟场景
  
    * 在模拟场景中注入故障（离线执行每个模拟时间点的BN MLE推断， 以找到关键故障集  ）
  
      <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240825153328922.png" alt="image-20240825153328922" style="zoom:67%;" />
  
* ADS架构和仿真（autonomous driving system  自动驾驶系统）

  *  AI平台：
    * 传感器抽象层：输入数据的预处理、噪声滤波、增益控制[45]、音调映射[46]、去马赛克[47]，以及根据传感器类型提取感兴趣的区域。
    * 感知层：处理传感器抽象层传入数据，使用计算机视觉技术(包括深度学习[48])来检测静态物体(如车道、交通标志、障碍物)和动态物体
      * 任务：分割，分类，聚类，对象和车道的实时跟踪，计算各种有用的指标（定义世界模型）
    * Localization Layer  定位层：收集各种数据，在世界模型里定位自动驾驶车辆
    * Prediction Layer   预测层：使用来自世界模型的信息(例如，位置，标题，速度，加速度)为检测到的物体生成轨迹，可以概率地识别自动驾驶汽车路径上的障碍物。
    * Planning & Control Layer    计划控制层：生成导航计划，并向自动驾驶汽车发送控制信号(驱动、制动、转向)
      * 路由模块” 根据请求生成高级导航信息。
        路由模块需要知道路由起点和路由终点， 以便计算通道车
        道和道路。 “规划模块” 通过使用定位输出、 预测输出和
        路由输出， 规划出安全无碰撞的轨迹。 “控制模块” 以规
        划的轨迹为输入， 生成控制命令传递给CAN总线， CAN总
        线将信息传递给AV的机械部件。  
  * 仿真平台：


* V. DRIVEFI架构  

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240825162926731.png" alt="image-20240825162926731" style="zoom:80%;" />

  * 场景协调管理器，活动管理器，事件驱动同步模块
  * 注入计算元素:GPU故障模型 （障碍类型1）       
    * 故障注入：指令输出时注入比特翻转
  * 事件管理器：输入XML，选择FI的故障类型、软件或硬件模块所在位置、故障数量、驱动场景。
  * 将故障注入ADS模块输出变量：
    * SLI源极注射：修改ADS模块的输出变量，破坏ADS内部状态，需要源码修改和重新编译（障碍类型2）
    * 1-固定：在给定ADS软件模块用一个恒定值来破坏给定的ADS软件模块输出，第k个场景注入单个故障。   
    * m-固定：从场景k开始， 将m个故障注入给定的一组ADS软件模块输出， 并继续将故障注入ADS软件模块输出， 直到场景k + m。  
    * 1-Random  ：在均匀随机选择的一组ADS模块输出中， 在第k个场景注入单个故障。 注入的故障值也是均匀随机选择的  
    * 从场景k开始， 在一组随机选择的ADS软件模块输出中注入m个故障， 并继续在ADS软件模块输出中注入故障， 直到场景k + m。   
    * 没有被屏蔽的体系结构状态错误表现为ADS模块内部状态的错误，而在模块中没有被屏蔽的错误传播到模块的输出，最后，在任何模块中未被掩盖的错误都显示为发送给AV的驱动命令错误。

* 一个活动管理器捆绑在一起，该活动管理器将XML配置文件作为输入，以选择故障模型、FI的软件或硬件模块站点、故障数量和驾驶场景。根据配置文件中的值，活动管理器运行指定数量的黄金模拟，在运行驾驶场景时配置ADS，并根据生成的故障计划运行指定数量的实验，每次注入一个或多个故障。

* 结果：

  

## Llumnix: Dynamic Scheduling for Large Language Model Serving  

#### 摘要

* 问题：大语言模型的系统有严重的排队延迟、 糟糕
  的尾部延迟和违反SLO等问题

* Llumnix:  重新调度请求以改善负载平衡和隔离， 减
  轻资源碎片， 并区分请求优先级和slo  

#### 介绍

* 工作负载异构性（workload heterogeneity  ）：问题多样性导致LLM推理工作的异构性
* 执行的不可预测性（execution unpredictability）：由于迭代，请求的执行时间和资源需求是不可预测的
* 更类似于现代操作系统， 它托管具有动态工作集和多核上不同优先级的进程。 管理这样的系统有复杂的目标  
* 难以实现性能隔离：
  Performance Isolation通过物理或逻辑手段，将系统资源（如CPU、内存、网络带宽等）分配给不同的任务或进程，确保它们各自拥有足够的资源来执行任务，而不会相互干扰。其主要目的是提高系统的整体性能和稳定性，同时确保关键任务或高优先级任务能够获得足够的资源保障。
* 优先级：处理时通常请求的优先级一致，但是实际请求的延迟要求不一样
* lumnix采用分布式调度架构

#### 背景

* LLM的应用多样性

* LLM自回归生成（Autoregressive generation  ）：

  * 序列的每一个元素（如文本中的单词、时间序列中的时间点等）都是基于序列中之前所有元素的信息来预测的；每一步都依赖于之前已经生成的序列部分

  * 模型迭代地接受输入序列加上之前的所有输出标记以生成下一个输出标记
  * prefill（预填充）延迟决定和了开始接受响应需要的时间；decode(解码)延迟决定接下来接受速度

* 批处理和内存管理

  * 连续批处理：Continuous Batching允许将一个或多个推理请求组合成单个批次，以最大化吞吐量。与传统的静态批处理不同，静态批处理在推理完成之前批大小保持不变，而Continuous Batching则允许批大小在推理过程中动态变化新的/完成的请求可以立即加入/离开正在运行的批处理，而不是等待所有正在运行的请求完成
  * KV缓存：先验未知-->动态内存分配
    它存储了模型中每个token（词元）的键（Key）和值（Value）向量，这些向量在模型进行连续token生成时，能够避免重复计算，从而提高推理效率。

#### 动机（LLM的关键特征）

* 不可预测的内存需求和抢占
* 请求之间的性能干扰
* 记忆的碎片：内存的实例间碎片化

####  设计（跨模型实例重新调度）

* 动态迁移跨模型实例重新调度

  * 动态实时迁移：减少实例间复制KV和已经计算资源带来的延迟，导致的停机时间
  * 跨模型实例：减少碎片，动态为高优先级腾出专用资源（不用为其分配静态资源），能够很快的添加新的实例和腾空删除旧的实例

* LLM请求的实时迁移（Live Migration of LLM Requests  ）

  * KV cache只会迭代追加，前面已经生成tokens不会再修改（lumnix的实时迁移机制利用KV缓存固有的仅追加特性， 将KV缓存复制与解码计算流水线化 ）

  * 可以一边复制前面的tokens，一边计算新的迭代中的新的tokens

  * 源实例一边计算，目标实例一边复制，直到最后一次迭代，源实例挂起，目标实例复制剩余未复制的tokens，迁移结束，剩下的迭代计算在目标实例上进行。（请求的停机时间仅为复制一次迭代生成的KV缓存的时间。  ）

  * 问题：

    * 迁移过程中，实例耗尽了内存

    * 在迁移过程中，请求完成

    * 解决：引入细粒度的握手

      * 源实例发出预分配请求（确保目标有足够空间）；目标实例尝试分配和预留，并且发送成功或者失败信号给源实例（终止或者继续迁移）；

      * 每个阶段之后，源实例还检查正在迁移的请求是否已完成或已被抢占
      * 在最后阶段完成后，源释放其本地块并通知目的地提交迁移并恢复请求的执行

* 分布式调度框架(llumlets & Global Scheduler)
  * 定义：根据实例的内存负载做出实例的调度决策，包含本地调度器（在触发时决定要迁移的请求）和迁移协调器（指示模型执行器执行内存复制）
  * 任务：计算实例的内存负载（重要），排队、批处理和块管理
  * ![image-20240829113138759](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240829113138759.png)

* 动态调度策略（Dynamic Scheduling Policy  ）

  * 目标：
    * 通过减少排队延迟、抢占和干扰来改善预填充和解码延迟。
    * 负载自适应，以处理不同的集群负载并提高成本效率
    * 新要求的请求优先级

  * Virtual Usage（虚拟用法）

    * 关键：负载平衡，实例上创建空闲空间（碎片清理、优先级排序和耗尽实例）

    * 关键统一成虚拟的负载平衡：设置某些请求的虚拟用法，使实例实际上过载，然后触发负载平衡策略，将请求迁移到其他实例

    * Queuing requests:为在实例中排队的请求分配了一个正的虚拟使用量来反映其对内存需求的资源需求（即使物理使用为0）。排队请求增加了实例的总的虚拟请求量，导致触发了迁移以达到负载平衡，自动实现碎片化整理。

      ![image-20240829120012079](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240829120012079.png)

    * Execution priorities：  请求的虚拟使用为物理使用加上虚拟headroom。虚拟headroom按照运行优先级定义，为了保证高优先级的解码速率。当预留给高优先级的headroom耗光时，实例的总虚拟使用超过限额，会迁移低优先级请求。

      ![image-20240829122249228](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240829122249228.png)

    * Auto-scaling(自动扩展)：当销毁一个实例时，可以在实例上添加一个假的请求（虚拟使用为无限大），由于负载平衡册策略，会自动调度这个实例上的其他请求去其他实例；当创建一个新的实例时，负载平衡策略会自动调度其他实例的请求到这个上面。

      ![image-20240829122636580](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240829122636580.png)

    * 算法：

      ![image-20240829122715530](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240829122715530.png)

  * Policies（策略）

    * Dispatching(调度)：

      1. 请求按优先级调度，同优先级先来先服务；

      2. 请求先分配到自由度最高的实例，自由度的度量为（自由度为负时就是超负载）
         $$
         F=(M-\sum V)/B \\
         M为实例的总内存，\sum V为每个请求的虚拟使用之和\\
         B为请求的个数，代表内存消耗的速率（请求tokens生成会消耗内存）
         $$

    * Migration（迁移）：触发是定时的
      1. 先选择源实例和目标实例的候选集（自由度低于或者超过平均水平的实例）
      2. 反复选择具有最低和最高自由值的两个实例来对这两个集合中的实例进行配对，然后将它们设置为相应的状态
      3. 每个源实例的servlet开始连续地将请求迁移到目标，直到它不再设置为源状态（在选择要迁移的请求时，更倾向于优先级较低且序列长度较短的请求）
      4. 在下一轮中，如果迁移过程中的实例不再超出阈值，lumnix将取消迁移状态的设置，并且迁移将停止
    * Auto-scaling（自动扩展）：lumnix根据集群负载在实例间正常优先级的平均空闲度来缩放实例
      1. 策略将平均空闲度保持在[x,y]范围内，当空闲度在一段时间内分别小于x或大于y时，增加或终止实例。
      2. 选择终止运行请求最少的实例

* 实现：

* 评估：

  * 拓展：
    * **P50**：指的是数据集按升序排列后，位于第50百分位的数据。换句话说，如果有一个数据集，我们将其中的所有数据按照从小到大的顺序排列，那么P50就是位于中间位置的数据，也就是中位数。这个指标在评估数据集的中心趋势时非常有用，特别是当数据集存在偏态分布时，中位数可能比平均数更能代表数据集的中心位置。
    * **P99**：指的是数据集按升序排列后，位于第99百分位的数据。即，如果我们有100个数据点（或更多，这里以100为例进行说明），那么P99就是这些数据点中响应时间最长的前1%的数据点的上界。在性能评估和服务质量监控中，P99经常被用来衡量服务的响应延迟。它表示在绝大多数情况下（99%的情况下），服务的响应时间都不会超过这个值。因此，P99是衡量服务稳定性和用户体验的重要指标之一。

    


## ACROBAT: OPTIMIZING AUTO-BATCHING OF DYNAMIC DEEP LEARNING AT COMPILE TIME  

* 介绍：
  * 动态控制流（RNN可以处理变长序列数据，如文本、语音或时间序列数据。在每个时间步，RNN会根据当前输入和之前的状态动态更新隐藏状态，从而实现动态控制流）
  * 批处理：同时处理多个样本，动态控制流使得人工批处理变得困难
  * ACROBAT：混合静态+动态优化和端到端（整个神经网络训练或推断的完整流程）张量内核编译



## Attention Is All You Need  

* 循环网络：顺序执行影响并行性
* 编码器解码器：都可以是RNN，CNN。编码器负责提取特征向量，解码器负责将特征向量转换为目标向量

​    <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240912160503457.png" alt="image-20240912160503457" style="zoom:50%;" />

* attention:  Q,K,V三个向量分别乘输入X，得到QKV矩阵，Q*K并且归一得到权重系数A矩阵，A * V得到最后value

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240912161426717.png" alt="image-20240912161426717" style="zoom:67%;" />

  * Q是query，是输入的信息；key和value成组出现，通常是原始文本等已有的信息；
  * 通过计算Q与K之间的相关性a，得出不同的K对输出的重要程度；
  * 再与对应的v进行相乘求和，就得到了Q的输出；

* 自注意：（输入的每个元素有自己的QKV,探究输入间的关系），attention的Q来自于外部

  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240912161925032.png" alt="image-20240912161925032" style="zoom:80%;" />

* 多头注意：输入对不同的QKV执行多次注意，将结果输入全连接得到最终输出
  <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240912171450679.png" alt="image-20240912171450679" style="zoom:80%;" />

* transformer：

  * 词embedding+位置embedding=transformer表示-->单词向量表示矩阵

    <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240912174300483.png" alt="image-20240912174300483" style="zoom:67%;" />

    * 位置embeding：
      <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240912214051342.png" alt="image-20240912214051342" style="zoom:67%;" />
  
  * 将单词向量表示矩阵传入六个编码模块
    <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240912174842489.png" alt="image-20240912174842489" style="zoom: 33%;" />
  * 将编码矩阵输入到六个解码器解码，每次一个一个单词翻译（依据前面的翻译结果，后面的单词给掩码）

​                <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240912175302995.png" alt="image-20240912175302995" style="zoom:50%;" />

* 编码器模块：
  * Add: **X**+MultiHeadAttention(**X**)
  * Norm： Layer Normalization，通常用于 RNN 结构，Layer Normalization 会将每一层神经元的输入都转成均值方差都一样的，这样可以加快收敛
  * Feed Forward: 两层全连接层，第一层激活函数为ReLu,第二层不使用激活函数，$max(0,XW_1+b_1)W_2+b_2$

* 解码器模块：

  * 第一个<code>Multi-Head Attention</code>：采用masked操作，翻译的过程中是顺序翻译的，即翻译完第 i 个单词，才可以翻译第 i+1 个单词
    * 确定输入矩阵（输入语句为正确单词序列 Teacher Forcing）和Mask矩阵
    * 计算$QK^T$
    * $QK^T$和$Mask$矩阵按位相乘，遮挡单词信息
    * $MaskQK^T$​和V相乘得到Z
  * 第二个<code>Multi-Head Attention</code>：
    * K,V 为编码器传入的编码信息矩阵C
    * Q为上一个解码器模块的输出计算，若为第一个解码器模块的输入，则为X

  * <code>Softmax</code>：利用最终输出预测单词

* <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240912214941431.png" alt="image-20240912214941431" style="zoom:50%;" />

## Improving Language Understanding by Generative Pre-Training

无监督学习未标注样本（预训练+微调）

* 困难：预训练的优化目标，迁移预训练学习的表示到目标任务的有效方法
* 半监督方法：在未标注数据上用语言建模目标来学习神经网络模型的初始参数；用有监督目标对参数进行调整以适应目标任务
* 框架：
  * 无监督预训练：
    * log P(ui|ui−k, . . . , ui−1)给定前k个标记的条件下预测第i个标记ui的概率；在训练过程中，模型会尝试调整其参数Θ，使得L1(U)的值尽可能大
      <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240913001343955.png" alt="image-20240913001343955" style="zoom:50%;" />
  * 有监督微调：
    * <img src="C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240913002823323.png" alt="image-20240913002823323" style="zoom:50%;" />
      $L_2(c)$是有监督学习的目标函数，$L_1(c)$​语言建模的目标函数（无监督），用于最大化模型在给定上下文条件下预测下一个标记的概率
  * 任务特定的输入转换：
    * 文本蕴含：蕴含任务，前提和假设之间用分隔符分隔
    * 相似性：包含两种可能的句子顺序（中间有分隔符）
    * 问答和常识推理：给定一个上下文文档z，一个问题q，以及一组可能的答案{ak}。我们将文档上下文和问题与每个可能的答案连接起来，中间添加分隔符标记（$），得到[z; q; $​; ak]

## Language Models are Unsupervised Multitask Learners

零样本学习：让预先训练好的模型预测先前未知数据的类别标签，即训练数据中不存在的数据样本（没有标注数据的情况下，预训练得到多任务的语言模型）

多任务学习，提高通用性能，利用预训练和有监督微调的结合，但是没有监督数据可用时，语言模型能够在零样本（zero-shot）设置下执行下游任务——无需任何参数或架构修改

* 方法：

  * 语言建模的核心目标是对自然语言中符号序列的概率分布进行建模，这些序列可以是单词、字符或其他类型的符号。
    * 在给定数据集上进行无监督分布估计，输出为候选单词的概率，候选单词来自于输入数据集
  * 多任务概率框架建模：p(output|input, task)
  * 语言模型在没有明确指导哪些符号是输出目标的情况下，理论下可以学习执行特定任务，但是学习速度慢
  * 训练数据集：构建大且多样化的数据集，避免对要执行的任务做出假设
  * 输入表示：字节版BPE，为了避免次优合并，防止字节序列跨字符类别合并，但是空格为例外
  * 模型：
* 实验：

  * 儿童书籍测试，LAMBADA（测试系统在文本建模长距离依赖能力），Winograd Schema挑战（解决文本中的歧义能力），阅读理解，翻译，问答，泛化与记忆；




## Language Models are Few-Shot Learners

扩大语言模型极大地提高了与任务无关的、少样本的性能，有时甚至可以与之前最先进的微调方法相媲美 

* pre-train + fine-tune存在问题：fine-tune需要大量标注数据集，pre-train容易过拟合，泛化能力差
  * 解决：meta-learning和增大变压器语言模型的容量

* 不给微调和梯度更新，只给上下文提示
  ![image-20240913152624666](C:\Users\丁晓琪\AppData\Roaming\Typora\typora-user-images\image-20240913152624666.png)
* 训练数据处理：基于高质量参考语料库对语料过滤；执行模糊重复数据消除；将已知高质量参考预料库添加到训练组合中



