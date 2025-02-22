import torch as torch
import torch.nn as nn
import torch.optim as optim
import torchvision as tv
import torchvision.transforms as transforms
import os
import numpy as np
import pickle as p
from torch.utils.data import Dataset, DataLoader, Subset
import torch.nn.functional as F
import matplotlib.pyplot as plt
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.datasets import MNIST
from torch.optim.lr_scheduler import StepLR
import matplotlib.pyplot as plt
import time

#gpu加速
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#定义图像增强函数，只能一张张图片用(transforms默认处理3通道)
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5), #0.5概率翻转
    transforms.RandomApply([transforms.RandomResizedCrop(size=28,scale=(0.8, 1.0))],p=0.5), #0.5概率剪裁成0.8-1.0的大小
    transforms.RandomApply([transforms.GaussianBlur(kernel_size=5, sigma=(0.1, 2.0))], p=0.3), #0.3的概率进行高斯模糊
    transforms.RandomRotation(degrees=15),  #随机旋转
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.1307], std=[0.3081]),
])

def apply_transform(images, transform):
    transformed_images = []
    for image in images:
        #转换为numpy数组并调整维度顺序为HWC,适应PIL图像格式（和CCIFAR10不一样）
        image_np=image.permute(1, 2, 0).numpy()
        #转换为 PIL 图像
        image_pil=transforms.ToPILImage()(image_np)
        #transform
        transformed_image = transform(image_pil)
        transformed_images.append(transformed_image)
    return torch.stack(transformed_images)

class SimCLRModel(nn.Module):
    def __init__(self):
        super(SimCLRModel, self).__init__()
        #CNN,Resnet太复杂了
        self.encoder = nn.Sequential(
            nn.Conv2d(1,32,kernel_size=3,stride=1,padding=1),#1*28*28->32*28*28
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2), #32*28*28->32*14*14
            nn.Conv2d(32,64,kernel_size=3,stride=1,padding=1),#32*14*14->64*14*14
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),#64*14*14->64*7*7
            nn.Flatten(), #64*7*7->3136
            nn.Linear(3136, 128), #128
        )
        # 投影头
        self.projection_head = nn.Sequential(
            nn.Linear(128,64),
            nn.ReLU(),
            nn.Linear(64,32),#32
        )

    def forward(self,x):
        # 提取特征
        features=self.encoder(x)
        #features = features.view(features.size(0), -1)  # 展平为 (batch_size, 512*8*8)
        # 投影到低维空间
        projections=self.projection_head(features)
        return features, projections

## nt_xent_loss对比损失函数的实现
def nt_xent_loss(projections,temperature=0.5):
    # 1. 相似矩阵计算
    batch_size = projections.shape[0]  # 2N
    N = batch_size // 2  #
    similarity_matrix=F.cosine_similarity(projections.unsqueeze(1),projections.unsqueeze(0),dim=-1) #2N*2N
    # 2.屏蔽自身相似度
    mask = torch.eye(batch_size, dtype=torch.bool).to(projections.device)
    similarity_matrix.masked_fill_(mask, 0)
    # 3.提取正样本对
    pos_mask=torch.zeros_like(similarity_matrix,dtype=torch.bool)
    pos_mask[:N,N:]=torch.eye(N) #前N行后N咧
    pos_mask[N:,:N]=torch.eye(N) #后N行前N列
      # 提取正样本相似度，重塑为2N，1
    pos_sim=similarity_matrix[pos_mask].view(batch_size,1)
    # 4.将自身相似度的影响放的最小(后面要求指数)
    all_sim = similarity_matrix.masked_fill(mask, -float('inf'))
    
    pos_sim=pos_sim/temperature
    all_sim=all_sim/temperature
    # 计算所有的相似度和,所有列求和，形状为2N，1
    all_exp=torch.exp(all_sim)
    all_sum=torch.sum(all_exp,dim=1,keepdim=True)
    #求损失
    loss=-torch.log(torch.exp(pos_sim)/all_sum)
    # 返回的是批次的平均损失，标量张量
    loss=loss.mean()
    return loss

def SimCLR_train(model, train_loader, epochs):
    model.to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    #记录损失
    simclr_losses = []
    for epoch in range(epochs):
        model.train() #设置模型为训练模式
        sum_loss=0
        for batch in train_loader:
            images, _ = batch #无标签训练，不要标签
            #数据增强
            view1=images
            view2 = apply_transform(images, transform)
            view1=view1.to(device)
            view2=view2.to(device)
            #输入到模型中，不要编码结果，只要投影结果
            _, proj1=model(view1)
            _, proj2=model(view2)
            #拼接结果
            projections=torch.cat([proj1, proj2], dim=0)
            #计算loss
            loss=nt_xent_loss(projections)
            #反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            sum_loss+=loss.item()
    #计算每个批次平均损失
        avg_loss = sum_loss/len(train_loader)
        simclr_losses.append(avg_loss)
        print(f"Epoch {epoch+1}, Loss: {avg_loss}")

    return simclr_losses

# 冻结预训练的SimCLR的参数
def freeze_encoder(model):
    for param in model.encoder.parameters():
        param.requires_grad = False  # 冻结编码器的权重

# 预训练的SimCLR+分类头
class ClassificationModel(nn.Module):
    def __init__(self, simclr_model):
        super(ClassificationModel, self).__init__()
        self.simclr_model = simclr_model #编码器
        self.classification_head= nn.Sequential(
            nn.Linear(128, 64),  #编码器输出是 128 维
            nn.ReLU(),
            nn.Linear(64, 10),  #10个类别
        )
        # 已经预训练好，不需要再次训练，冻结编码器的权重
        freeze_encoder(self.simclr_model)

    def forward(self, x):
        # 使用 SimCLR 的编码器提取特征，不需要投影器
        features, _ = self.simclr_model(x)
        # 使用分类头进行分类
        label = self.classification_head(features)
        return label

def classification_train(model, train_loader, epochs):
    model.to(device)
    optimizer=optim.Adam(model.parameters(),lr=0.001)
    criterion=nn.CrossEntropyLoss()  # 交叉熵损失函数
    #记录损失和正确率
    classification_losses=[]
    classification_accuracies=[]
    for epoch in range(epochs):
        model.train()
        sum_loss=0
        total_correct=0  # 记录当前 epoch 的正确预测数量
        total_samples=0  # 记录当前 epoch 的总样本数量
        for batch in train_loader:
            images,labels=batch
            images,labels=images.to(device), labels.to(device)
            #获得分类结果
            predict_labels=model(images)
            #计算loss
            loss=criterion(predict_labels,labels)
            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            sum_loss += loss.item()
            # 计算当前批次的正确预测数量
            predictions=torch.argmax(predict_labels, dim=1)  # 获取预测的类别
            correct=(predictions == labels).sum().item()  # 计算正确预测的数量
            total_correct+=correct
            total_samples+=labels.size(0)  # 当前批次的样本数量
        # 计算每个 epoch 的准确率
        avg_loss=sum_loss/len(train_loader)
        accuracy=total_correct/total_samples
        classification_losses.append(avg_loss)
        classification_accuracies.append(accuracy)
        print(f"Epoch {epoch + 1}, Loss: {avg_loss}, Accuracy: {accuracy * 100:.2f}%")
    return classification_losses,classification_accuracies

def evaluate(model, test_loader):
    model.eval()  # 设置模型为评估模式
    total_correct=0  # 正确预测
    total_samples=0  # 总样本数量

    with torch.no_grad():  # 不计算梯度
        for images,label in test_loader:
            images,label=images.to(device), label.to(device)

            p=model(images)
            pres=torch.argmax(p, dim=1)  # 获取预测的类别
            # 计算正确预测的数量
            correct=(pres==label).sum().item()
            total_correct+=correct
            total_samples+=label.size(0)
    
    # 计算准确率
    acc=total_correct/total_samples
    print(f"Test Accuracy: {acc * 100:.2f}%")

def paint(simclr_losses,classification_losses,classification_accuracies):
    plt.figure(figsize=(18, 5))
    #对比网络训练损失曲线
    plt.subplot(1,3,1)
    plt.plot(range(1,len(simclr_losses)+1),simclr_losses,label="SimCLR Loss",color="blue")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("SimCLR Training Loss")
    plt.legend()
    plt.grid(True)
    #分类训练损失曲线
    plt.subplot(1,3,2)
    plt.plot(range(1, len(classification_losses) + 1), classification_losses, label="Classification Loss", color="red")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Classification Training Loss")
    plt.legend()
    plt.grid(True)

    # 分类训练正确率曲线
    plt.subplot(1, 3, 3) 
    plt.plot(range(1, len(classification_accuracies) + 1), classification_accuracies, label="Classification Accuracy", color="green")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.title("Classification Training Accuracy")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()            

if __name__ == "__main__":
    #1. 提取数据和标签
    transform1 = transforms.Compose([
        transforms.ToTensor(),  # 将图像转换为张量
        transforms.Normalize((0.1307,), (0.3081,)),  # 归一化
    ])
    train_dataset = MNIST(root='./data', train=True, transform=transform1, download=True)
    # 只取前两个批次的样本
    num_per_batch=6000  #MNIST每个批次的样本数量
    num_batches = 4  #只取前四个批次
    indices = list(range(num_per_batch  * num_batches))
    train_subset = Subset(train_dataset, indices)

    # 定义数据加载器
    train_loader = DataLoader(train_subset, batch_size=256, shuffle=True)
    # 2.模型
    simclr_model = SimCLRModel()
    # 3.SimCLR训练
    print("Start SimCLR Traing...")
    start_time_train_total=time.time()
    start_time_simclr=time.time()
    simclr_losses=SimCLR_train(simclr_model, train_loader, epochs=10)
    end_time_simclr=time.time()  
    simclr_training_time=end_time_simclr-start_time_simclr
    print(f"SimCLR Training Time: {simclr_training_time:.2f} seconds")
    # 4.分类训练
    num_samples_per_batch_class = 6000  # MNIST 每个批次的样本数量
    start_index = 4 * num_per_batch   # 第4个批次的起始索引
    end_index = 5* num_per_batch  # 第5个批次的结束索引
    indices_class = list(range(start_index, end_index))
    train_subset_class = Subset(train_dataset, indices_class)
    train_class_loader = DataLoader(train_subset_class, batch_size=128, shuffle=True)
    # 模型定义
    classification_model=ClassificationModel(simclr_model)
    
    print("Starting Classification Training...")
    start_time_classification = time.time()  
    classification_losses,classification_accuracies=classification_train(classification_model, train_class_loader, 30)
    end_time_classification=time.time()
    classification_training_time=end_time_classification-start_time_classification
    print(f"Classification Training Time: {classification_training_time:.2f} seconds")

    training_time_total=end_time_classification-start_time_train_total
    print(f"Total Training Time: {training_time_total:.2f} seconds")
    # 绘制训练损失和正确率曲线
    paint(simclr_losses, classification_losses, classification_accuracies)

    # 加载测试数据集
    test_dataset = MNIST(root='./data', train=False, transform=transform1, download=True)

    # 定义测试数据加载器
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)
    # 6. 验证模型
    print("Evaluating on test set...")
    evaluate(classification_model,test_loader)