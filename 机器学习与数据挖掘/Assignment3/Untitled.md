![image-20241205220448134](C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241205220448134.png)

![image-20241205221054575](C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241205221054575.png)

![image-20241205221358365](C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241205221358365.png)





就像有k个不同的高斯模型混在一起，每个高斯模型的概率为ak

![img](https://i-blog.csdnimg.cn/blog_migrate/6c68fdf3160fe02c5209f2d38a8dcfa3.jpeg)

EM算法：

多维高斯分布公式
<img src="C:/Users/丁晓琪/AppData/Roaming/Typora/typora-user-images/image-20241206180818511.png" alt="image-20241206180818511" style="zoom:50%;" />



np.dot可以是点积（向量)也可以是矩阵乘法(矩阵)



v*A，v是列向量时会把其广播成A的形状和A点积

这个`GMM`（高斯混合模型）类的算法流程实现了高斯混合模型的EM（期望最大化）算法训练过程。以下是该算法的详细流程，包括必要的数学公式（使用Markdown格式）：

### 算法流程

1. **初始化**

   - 输入训练图像`train_images`、高斯混合成分个数`k`、最大迭代次数`max_iter`、训练标签（虽然在此实现中未使用）、均值初始化方法`means_init_method`、协方差矩阵初始化方法`cov_init_method`。
   - 初始化每个高斯分布的权重`weights`、均值`means`和协方差矩阵`covariance_matrices`。
     - 权重通过生成随机整数并归一化得到。
     - 均值根据`means_init_method`选择：
       - 方法0：随机选择`k`个样本作为初始均值。
       - 方法1：使用最远距离策略选择初始均值。
     - 协方差矩阵根据`cov_init_method`选择：
       - 方法0：使用样本协方差矩阵的对角矩阵形式，并加上一个小常数以避免除以零。
       - 方法1：使用所有特征维度的平均方差初始化一个球形（对角且各元素相等）协方差矩阵。

2. **EM算法迭代**

   - 对于每次迭代`t`（从0到`max_iter-1`）：
     1. **E步（期望步）**
        - 计算每个样本在每个高斯分布下的响应度（或称为后验概率），即γ矩阵。
          - 对于每个样本`x_j`和每个高斯分布`k`，计算`γ_jk = P(Z=k|X=x_j)`，其中`Z`是隐变量（表示样本属于哪个高斯分布）。
          - 使用公式：
            \[
            \gamma_{jk} = \frac{\alpha_k N(x_j|\mu_k,\Sigma_k)}{\sum_{l=1}^{K}\alpha_l N(x_j|\mu_l,\Sigma_l)}
            \]
            其中，`N(x_j|\mu_k,\Sigma_k)`是样本`x_j`在第`k`个高斯分布下的概率密度函数。
        - 将γ矩阵按行归一化，确保每行的和为1。
        - 更新每个样本可能属于的聚类（即预测索引）。
     
     2. **M步（最大化步）**
        - 根据E步得到的γ矩阵，更新高斯分布的参数（权重、均值、协方差矩阵）。
          - 更新权重`α_k`：
            \[
            \alpha_k = \frac{1}{N}\sum_{j=1}^{N}\gamma_{jk}
            \]
          - 更新均值`μ_k`：
            \[
            \mu_k = \frac{\sum_{j=1}^{N}\gamma_{jk}x_j}{\sum_{j=1}^{N}\gamma_{jk}}
            \]
          - 更新协方差矩阵`Σ_k`：
            \[
            \Sigma_k = \frac{\sum_{j=1}^{N}\gamma_{jk}(x_j - \mu_k)^T(x_j - \mu_k)}{\sum_{j=1}^{N}\gamma_{jk}}
            \]
            注意：在实现中，为了避免除以零，可以在分母中加上一个很小的常数（如`1e-6`）。

3. **测试（可选）**

   - 在每次迭代后，可以使用测试数据集（`test_images`和`test_labels`）来评估模型的性能。这部分在代码中以`self.test`方法表示，但具体实现未给出。

### 注意

- 在这个实现中，`train_labels`参数被传入但未使用。在实际应用中，如果标签可用，可以使用它们来初始化参数或评估模型性能，但这不是标准的GMM/EM算法的一部分。
- 协方差矩阵的更新中，为了避免数值问题，通常会在分母中加上一个小的正则化项（如`1e-6`）。
- 在实际应用中，可能需要添加额外的收敛检查，例如检查参数的变化是否小于某个阈值，以确定是否提前停止迭代。
