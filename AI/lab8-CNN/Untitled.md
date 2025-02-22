## 一. 数据的提取

此处参考https://blog.csdn.net/weixin_41707744/article/details/104845856

### 1. CIFAR10数据集：



## 二. Pytorch使用基础

### 1. 数据处理和加载

* **Dataset**：表示数据集的接口，后面可以用Dataloader加载方便训练时样本的加载，以下是自定义数据集需要完成的操作

  * 需要自定义数据集类，并且继承pytorch的标准化数据集接口Dataset

  * 重写方法<code>\__init __ </code>: 对传入数据集中的数据和对数据的初始化处理，这里传入提取出来的样本图像信息和标签，将类型转为张量,并且对样本的图像信息归一化

    ```python
        def __init__(self,X,Y):
            self.X = torch.from_numpy(X).float() / 255   #归一化到0-1
            self.Y = torch.from_numpy(Y).long()
    ```

  * 重写方法<code>\__len__</code>: 获取数据集长度

    ```python
        def __len__(self):#数据集中样本总数
            return len(self.X)
    ```

  * 重写方法<code>\__getitem__</code>:根据下标获取数据集中对应的元素和标签

    ```python
        def __getitem__(self,idx): 
            return self.X[idx],self.Y[idx]
    ```

* **Dataloader:** 数据加载器，能够训练时自动加载出每一批次的数据和提供更多对批次中的数据的自定义选项

  * 参数：<code>dataset</code>数据集，<code>batch_size</code>每个批次要加载的样本数，<code>shuffle</code>是否在每次训练迭代重新排列数据

  * 本次实验的设置: <code>Test_loader</code>，由于在测试验证模型是在整个测试集上验证样本的正确性，所以测试集的数据加载器可以定义为一个批次里面包含整个整个数据集

    ```
        Train_loader=DataLoader(dataset=Train_data,batch_size=100,shuffle=True)
        Test_loader=DataLoader(dataset=Test_data,batch_size=10000,shuffle=True)
    ```



