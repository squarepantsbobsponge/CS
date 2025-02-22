import torch as torch
import torch.nn as nn
import torch.optim as optim
import torchvision as tv
import torchvision.transforms as transforms
import os
import numpy as np
import pickle as p
from torch.utils.data import Dataset,DataLoader
import matplotlib.pyplot as plt
#gpu加速
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")   ##GPU加速

def load_CIFAR_batch(filename,option):
    
    # function: 提取一个批次的数据
    # input：filename文件名，option:{0,1}选择需要重塑的数据形状
    # return：images从文件中提取出的图像信息，labels从文件中提取出的图像标签
    
    with open(filename,'rb') as f:
        data_dict = p.load(f,encoding='bytes')
        images = data_dict[b'data']
        labels = data_dict[b'labels']
        if option==1:
            images = images.reshape(10000, 3,32,32)
        else:
            images = images.reshape(10000, 3072)
        
        labels = np.array(labels)
        return images, labels



def load_CIFAR_data(data_dir,option):

    # function: 完整读取数据的函数,通过多次调用批次读取数据的函数实现
    # input:data_dir数据所在的文件夹名称，option{0,1}选择需要重塑的数据矩阵形状
    # return: Xtrain, Ytrian, Xtest, Ytest,提取出的测试集和训练集的图像信息和标签

    images_train =[]
    labels_train = []
    for i in range(5):
        f = os.path.join(data_dir, 'data_batch_%d'%(i+1))
        print('loading', f)
        image_batch, label_batch = load_CIFAR_batch(f,option)
        images_train.append(image_batch)
        labels_train.append(label_batch)
        Xtrain = np.concatenate(images_train)
        Ytrian = np.concatenate(labels_train)
        del image_batch, label_batch
    Xtest, Ytest = load_CIFAR_batch(os.path.join(data_dir, 'test_batch'),option)
    return Xtrain, Ytrian, Xtest, Ytest
 
##自定义数据集
class CustomDataset(Dataset):
    def __init__(self,X,Y):
        self.X = torch.from_numpy(X).float() / 255   #归一化到0-1
        self.Y = torch.from_numpy(Y).long()

    def __len__(self):
        # function：获取数据集中样本总数
        return len(self.X)
    
    def __getitem__(self,idx): 
        # function: 根据下标获取数据集中对应的元素和标签
        # input:索引
        return self.X[idx],self.Y[idx]

# softmax线性分类器
class SoftmaxClassifier(nn.Module):
    def __init__(self,input_dim,num_labels):
        # function: 初始化网络结构,一个全连接层一个softmax激活函数层
        # input:input_dim，样本的总特征数；num_labels:样本的标签数
        super(SoftmaxClassifier, self).__init__()
        self.linear=nn.Linear(input_dim,num_labels)
        self.softmax=nn.Softmax(dim=1)
    
    def forward(self,x):
        # function:前向传播函数
        x=self.linear(x)
        output=self.softmax(x)
        return output

# MLP分类器
class MLPClassifier(nn.Module):
    def __init__(self,input_dim,num_labels):
        # function:初始化网络结构
        super(MLPClassifier,self).__init__()
        self.linear1=nn.Linear(input_dim,2048)
        self.linear2=nn.Linear(2048,1024)
        self.linear3=nn.Linear(1024,10)
        self.relu=nn.ReLU()
    
    def forward(self,x):
        # function:前向传播函数
        x=self.linear1(x)
        x=self.relu(x)
        x=self.linear2(x)
        x=self.relu(x)
        output=self.linear3(x)
        return output

# CNN分类器
class CNNClassifier(nn.Module):
    def __init__(self):
        # function:初始化网络结构
        super(CNNClassifier,self).__init__()#类继承的初始化
        # 卷积层1
        self.conv1=nn.Sequential( #输入 3*32*32
            nn.Conv2d(  #卷积操作在2维上操作，宽和高，每个特征方程已经结合了三个通道了
                in_channels=3 , #彩色通道RGB
                out_channels=16, #16个滤波器，卷积核
                kernel_size=5, #卷积核大小为5*5
                stride=1 ,#卷积窗口移动步长为1
                padding=2 #填充0保证行列数不变
            ),#输出 (32-5+4)/1+1=32,16*32*32
            nn.ReLU(),#激活函数 RReLU
            nn.MaxPool2d(2),#最大池化层 2*2里面挑一个最大的 输出16*16*16
        )
        # 卷积层2
        self.conv2=nn.Sequential(
            nn.Conv2d(16,32,5,1,2), 
            nn.ReLU(),
            nn.MaxPool2d(2),#输出 32*8*8
        )     
        self.linear1=nn.Linear(32*8*8,1024)
        self.linear2=nn.Linear(1024,10)

    def forward(self,x):
        # function: 前向传播函数
        x=self.conv1(x)
        x=self.conv2(x)
        x=x.view(x.size(0),-1)  #保留第一维度，剩下的都压成一维
        x=self.linear1(x)
        output=self.linear2(x)
        return output

def train_test(choice,Train_loader,Test_loader,option,lr=0.0005,momentum=0.9,betas=(0.9,0.999),EPOCHES=100):
    
    # function:训练测试Softmax线性分类器
    # input:
    #  -choice: 0为softmax线性分类器，1为MLP分类器，2为CNN分类器
    #  -Train_loader,Test_Loder: 训练数据和测试数据加载器
    #  -option：选择优化器，0:SGD；1:SGD+momentum超参数; 2:ADam
    #  -lr:学习率
    #  -momentum：SGD+momentum的超参数
    #  -betas: Adam的超参数
    #  -EPOCHES：训练时迭代次数

    #1. 定义模型，损失函数优化器
    if choice==0:
        model=SoftmaxClassifier(3072,10)
    elif choice==1:
        model=MLPClassifier(3072,10)
    elif choice==2:
        model=CNNClassifier()
    loss_func=nn.CrossEntropyLoss()
    
    if option==0:
        optimizer=optim.SGD(model.parameters(),lr=lr)
    elif option==1:
        optimizer=optim.SGD(model.parameters(),lr=lr,momentum=momentum)
    else:
        optimizer=optim.Adam(model.parameters(),lr=lr,betas=betas)
    model = model.to(device)#gpu训练
    result={'loss':[],'accuracy':[]}
    #2.迭代训练
    for epoch in range(EPOCHES):
     for step,(b_x,b_y) in enumerate(Train_loader):#step为批次索引，b_x为每一批次的输入，b_y为每一批次的标签
        # 将数据和标签移动到GPU
        optimizer.zero_grad() #清除梯度
        b_x = b_x.to(device)  #torch.Size([64, 3072]) 
        b_y = b_y.to(device)  #torch.Size([64])
        output=model(b_x)  #输入每一批次到模型，自动调用forward
        loss=loss_func(output,b_y) #计算损失函数
        loss.backward() #损失函数的反向传播
        optimizer.step() #参数优化
     #3. 每次迭代结束后都在测试集上测试
     for step2,(test_x,test_y) in enumerate(Test_loader): #一个批次弄完
                test_x = test_x.to(device)  
                test_y = test_y.to(device)               
                test_output = model(test_x)
                pred_y = torch.max(test_output, 1)[1].data.detach().cpu().numpy()  #GPU数据移到cpu再移到numpy  #返回概率最大的索引
                accuracy = float((pred_y == test_y.data.detach().cpu().numpy()).astype(int).sum()) / float(test_y.size(0))
                print('Epoch: ', epoch, '| train loss: %.4f' % loss.data.detach().cpu().numpy(), '| test accuracy: %.2f' % accuracy)
                result['accuracy'].append(accuracy)
                result['loss'].append(loss.data.detach().cpu().numpy())
    return result





def plot_result(fig,axes,result0,result1,result2,title):
    axes=axes.flatten()
    epoches=range(1,len(result0['loss'])+1)
    axes[0].plot(epoches,result0['loss'],color='blue')
    axes[0].set_xlabel('Epoches')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True)  # 显示网格
    axes[0].set_title(f'Training Loss over SGD for {title}')

    axes[2].plot(epoches,result1['loss'],color='blue')
    axes[2].set_xlabel('Epoches')
    axes[2].set_ylabel('Loss')
    axes[2].legend()
    axes[2].grid(True)  # 显示网格
    axes[2].set_title(f'Training Loss over SGD_momentum for {title}')

    axes[4].plot(epoches,result2['loss'],color='blue')
    axes[4].set_xlabel('Epoches')
    axes[4].set_ylabel('Loss')
    axes[4].grid(True)  # 显示网格
    axes[4].set_title(f'Training Loss over Adam for {title}')

    axes[1].plot(epoches,result0['accuracy'],color='blue')
    axes[1].set_xlabel('Epoches')
    axes[1].set_ylabel('accuracy')
    axes[1].grid(True)  # 显示网格
    axes[1].set_title(f'Test accuracy over SGD for {title}')

    axes[3].plot(epoches,result1['accuracy'],color='blue')
    axes[3].set_xlabel('Epoches')
    axes[3].set_ylabel('accuracy')
    axes[3].grid(True)  # 显示网格
    axes[3].set_title(f'Test accuracy over SGD_momentum for {title}')

    axes[5].plot(epoches,result2['accuracy'],color='blue')
    axes[5].set_xlabel('Epoches')
    axes[5].set_ylabel('accuracy')
    axes[5].grid(True)  # 显示网格
    axes[5].set_title(f'Test accuracy over Adam for {title}')




if __name__=="__main__":
    #1.提取数据和标签
    data_dir = './data/'  # 解压抽取数据集后的路径
    Xtrain, Ytrain, Xtest, Ytest = load_CIFAR_data(data_dir,0) 
    #2.加载成自定义数据集
    Train_data=CustomDataset(Xtrain,Ytrain)
    Test_data=CustomDataset(Xtest,Ytest)
    #3 创建加载器:每个批次并行处理64个样本，每次迭代要将样本打乱
    Train_loader=DataLoader(dataset=Train_data,batch_size=100,shuffle=True)
    Test_loader=DataLoader(dataset=Test_data,batch_size=10000,shuffle=True)
    #4. 初始化和训练softmax线性模型   
    result0=train_test(0,Train_loader,Test_loader,option=0,EPOCHES=80)
    result1=train_test(0,Train_loader,Test_loader,option=1,EPOCHES=80)
    result2=train_test(0,Train_loader,Test_loader,option=2,EPOCHES=80)
    fig1,axes1=plt.subplots(3,2,figsize=(12,6))
    title=f'softmax Classifier'
    plot_result(fig1,axes1,result0,result1,result2,title)
    #5. 初始化和训练MLP模型
    result0=train_test(1,Train_loader,Test_loader,option=0,EPOCHES=80)
    result1=train_test(1,Train_loader,Test_loader,option=1,EPOCHES=80)
    result2=train_test(1,Train_loader,Test_loader,option=2,EPOCHES=80)
    fig2,axes2=plt.subplots(3,2,figsize=(12,6))
    title=f'MLP Classifier'
    plot_result(fig2,axes2,result0,result1,result2,title)
    #6. 初始化和训练CNN模型
    Xtrain, Ytrain, Xtest, Ytest = load_CIFAR_data(data_dir,1) 
    Train_data=CustomDataset(Xtrain,Ytrain)
    Test_data=CustomDataset(Xtest,Ytest)
    Train_loader=DataLoader(dataset=Train_data,batch_size=100,shuffle=True)
    Test_loader=DataLoader(dataset=Test_data,batch_size=10000,shuffle=True)
    result0=train_test(2,Train_loader,Test_loader,option=0,EPOCHES=80)
    result1=train_test(2,Train_loader,Test_loader,option=1,EPOCHES=80)
    result2=train_test(2,Train_loader,Test_loader,option=2,EPOCHES=80)
    fig3,axes3=plt.subplots(3,2,figsize=(12,6))
    title=f'CNN Classifier'
    plot_result(fig3,axes3,result0,result1,result2,title)
    
    plt.tight_layout()
    plt.show()


    