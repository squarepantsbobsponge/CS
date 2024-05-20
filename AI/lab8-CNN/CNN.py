import torch
import os
from torch.utils.data import DataLoader ,ConcatDataset 
from torchvision import datasets, transforms  
import torch.nn as nn
import shutil
import matplotlib.pyplot as plt
import numpy as np
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")   ##GPU加速
LR=0.001 #学习步长
EPOCH=100 #数据集被迭代次数
loss_rate=[]
accuracy_rate=[]

#把测试集提取出来
#创造一个文件夹
#源文件夹的位置
# source_dir="./test"
# destination_dir="./test_plus"
# os.makedirs("./test_plus",False)
# os.makedirs("./test_plus/baihe")
# os.makedirs("./test_plus/dangshen")
# os.makedirs("./test_plus/gouqi")
# os.makedirs("./test_plus/huaihua")
# os.makedirs("./test_plus/jinyinhua")
# ##读取test里面的文件并且转移
# for filename in os.listdir(source_dir):
#     #构建完整的source路径
#     file_path=os.path.join(source_dir,filename)
#     if "baihe" in filename:
#         destination_path="./test_plus/baihe"
#     elif "dangshen" in filename:
#          destination_path="./test_plus/dangshen"
#     elif "gouqi" in filename:
#          destination_path="./test_plus/gouqi"
#     elif "huaihua" in filename:
#          destination_path="./test_plus/huaihua"  
#     elif "jinyinhua" in filename:
#          destination_path="./test_plus/jinyinhua"
#     destination_path=os.path.join(destination_path,filename)
#     shutil.move(file_path, destination_path)  

##转换图片为数据##dataloader自动化处理样本
transform=transforms.Compose([
    transforms.Resize((200,200)), #图片大小调整为224*224
    transforms.ToTensor()]  #归一化了 0，255变成0，1
)  #图片预处理操作步骤集合
train_dataset=datasets.ImageFolder(root="./train",transform=transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)  
test_dataset = datasets.ImageFolder(root="./test_plus", transform=transform)  
# 定义数据加载器（这里不使用 batch_size，因为我们可能希望一次处理整个测试集）  
test_loader = DataLoader(dataset=test_dataset, batch_size=10, shuffle=False) 

##CNN结构
class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()#类继承的初始化
        self.conv1=nn.Sequential( #输入 3*200*200
            nn.Conv2d(  #卷积操作在2维上操作，宽和高，每个特征方程已经结合了三个通道了
                in_channels=3 , #彩色通道RGB
                out_channels=16, #16个滤波器，卷积核
                kernel_size=5, #卷积核大小为5*5
                stride=1 ,#卷积窗口移动步长为1
                padding=2 #填充0保证行列数不变
            ),#输出 16*200*200
            nn.ReLU(),#激活函数 RReLU
            nn.MaxPool2d(2),#最大池化层 2*2里面挑一个最大的 输出16*100*100
        )
        self.conv2=nn.Sequential(
            nn.Conv2d(16,32,5,1,2), 
            nn.ReLU(),
            nn.MaxPool2d(2),#输出 32*50*50
        )
        self.conv3=nn.Sequential(
            nn.Conv2d(32,32,5,1,2), 
            nn.ReLU(),
            nn.MaxPool2d(2),#输出 32*25*25
        )
        self.output=nn.Linear(32*25*25,5)

    def forward(self,x):
        x=self.conv1(x)
        x=self.conv2(x)
        x=self.conv3(x)
        x=x.view(x.size(0),-1)  #保留第一维度，剩下的都压成一维
        output=self.output(x)
        return output,x
    
##实现网络优化，调参
device = torch.device("cuda")
cnn=CNN()
cnn.to(device)
optimizer=torch.optim.Adam(cnn.parameters(),lr=LR) #设置更新网络参数的优化器，lr为学习率 
loss_func=nn.CrossEntropyLoss() #交叉熵,定义损失函数  

for epoch in range(EPOCH):
    for step,(b_x,b_y) in enumerate(train_loader):#step为批次索引，b_x为每一批次的输入，b_y为每一批次的标签
        # 将数据和标签移动到GPU  
        b_x = b_x.to(device)  
        b_y = b_y.to(device)
        output=cnn(b_x)[0]  #输入每一批次到cnn，自动调用forward
        loss=loss_func(output,b_y) #计算损失函数
        loss_rate.append(loss.item())
        optimizer.zero_grad() #清除梯度
        loss.backward() #损失函数的反向传播
        optimizer.step() #参数优化
        
        if step % 32 == 0: #每隔一些批次，测试测试集，打印准确率
            for step2,(test_x,test_y) in enumerate(test_loader): #一个批次弄完
                test_x = test_x.to(device)  
                test_y = test_y.to(device)               
                test_output, last_layer = cnn(test_x)
                pred_y = torch.max(test_output, 1)[1].data.detach().cpu().numpy()  #GPU数据移到cpu再移到numpy  #返回概率最大的索引
                accuracy = float((pred_y == test_y.data.detach().cpu().numpy()).astype(int).sum()) / float(test_y.size(0))
                accuracy_rate.append(accuracy)
                print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.detach().cpu().numpy(), '| test accuracy: %.2f' % accuracy)

train_count=0
train_sum=0
for step,(b_x,b_y) in enumerate(train_loader):
    b_x =b_x.to(device)  
    b_y =b_y.to(device)        
    output, last_layer = cnn(b_x)          
    pred_y = torch.max(output, 1)[1].data.detach().cpu().numpy() 
    train_sum+=(b_y.size(0))
    train_count+=(pred_y == b_y.data.detach().cpu().numpy()).astype(int).sum()
print("final_train_accuracy:",float(train_count)/train_sum,"(correct=",train_count,")")
# 创建图形窗口  
plt.figure(figsize=(10, 6))  
  
# 第一个子图：损失  
plt.subplot(2, 1, 1)  # 2行1列，当前是第1个子图  
plt.plot(loss_rate, marker='o', linestyle='-', label='Loss over epochs')  
plt.xlabel('Epochs')  
plt.ylabel('Loss')  
plt.title('Loss over Epochs')  
plt.legend()  
  
# 第二个子图：准确率  
plt.subplot(2, 1, 2)  # 2行1列，当前是第2个子图  
plt.plot(accuracy_rate, marker='o', linestyle='-', label='Accuracy over epochs')  
plt.xlabel('Epochs')  
plt.ylabel('Accuracy')  
plt.title('Accuracy over Epochs')  
plt.legend()  
  
# 显示图形  
plt.tight_layout()  # 调整子图参数，使之填充整个图像区域  
plt.show()