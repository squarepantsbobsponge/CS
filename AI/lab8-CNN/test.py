
import torch 
print(torch.__version__) # pytorch版本
print(torch.version.cuda) # cuda版本
print(torch.cuda.is_available()) # 查看cuda是否可用

n=torch.Tensor(2,3)#二维矩阵
m=torch.Tensor([2,3])  #一维矩阵
#Conv2d是卷积层
#ReLU激活函数，输入为负数输出为0,输入为非负数，输出等于输入
#nn.MaxPool2d 二维最大池化层。 nn.MaxPool2d（2）（默认池化窗口每次移动2个像素，边界不进行填充，卷积核中元素的间距为1，池化窗口为2*2，每个池化窗口提出最大值作为采样）
