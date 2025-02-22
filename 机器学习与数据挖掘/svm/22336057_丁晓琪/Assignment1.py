import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import csv  
import time  

def loadCSVfile1(filename):
    # 从csv文件中加载数据
    # Parameters:
    #  filename - csv文件名字
    # Returns:
	#  data:数据的特征值
    #  label:数据的标签
    # notes:
    # 要将提取的数据从字符串转为浮点数
    list_file = []
    with open(filename,'r') as csv_file:  
        all_lines=csv.reader(csv_file)  
        next(all_lines)  
        for one_line in all_lines:  
            float_line = [float(value) for value in one_line] 
            list_file.append(float_line)  
    arr_file = np.array(list_file)
    label = arr_file[:, 0]
    data = arr_file[:, 1:]
    return data, label  

class svmtrain:
    def __init__(self,filename_train,filename_test):
    # Parameters:  
    #  filename_train (str): 训练数据的csv文件名字。  
    #  filename_test (str): 测试数据的csv文件名字。    
    # 实例变量：  
    # - self.X_train_std: 标准化后的训练数据特征值。  
    # - self.Y_train: 训练数据的标签。  
    # - self.X_test_std: 标准化后的测试数据特征值。  
    # - self.Y_test: 测试数据的标签。  
        X_train,self.Y_train=loadCSVfile1(filename_train)
        X_test,self.Y_test=loadCSVfile1(filename_test)
        sc=StandardScaler()
        sc.fit(X_train)
        self.X_train_std=sc.transform(X_train)
        self.X_test_std=sc.transform(X_test)

    def linear_train(self):
        #线性核svm分类器
        #输出：模型训练时长，在测试样本上的预测正确率和正确预测数
        start_time = time.time()  
        svm=SVC(kernel='linear',C=1.0,random_state=500) 
        svm.fit(self.X_train_std,self.Y_train)
        end_time = time.time()  
        training_duration = end_time - start_time  
        print(f"线性核SVM训练时长: {training_duration:.4f} 秒")

        y_pred=svm.predict(self.X_test_std)

        print('linear Misclassified samples: %d' % (self.Y_test != y_pred).sum())   
        print('linear Accuracy: %.6f' % svm.score(self.X_test_std, self.Y_test))         

    def gauss_train(self):
        #高斯核svm分类器
        #输出：模型训练时长，在测试样本上的预测正确率和正确预测数
        start_time = time.time()         
        svm=SVC(kernel='rbf',C=1.0,random_state=1000) 
        svm.fit(self.X_train_std,self.Y_train)
        end_time = time.time()  
        training_duration = end_time - start_time  
        print(f"高斯核SVM训练时长: {training_duration:.4f} 秒")

        y_pred=svm.predict(self.X_test_std)

        print('gauss Misclassified samples: %d' % (self.Y_test != y_pred).sum())  
        print('gauss Accuracy: %.6f' % svm.score(self.X_test_std, self.Y_test))         


class cross_entropy_train:
    def __init__(self,filename_train,filename_test,alpha,time):

    # Parameters:  
    #  filename_train (str): 训练数据的csv文件名字。  
    #  filename_test (str): 测试数据的csv文件名字。    
    # 实例变量：  
    # - self.X_train_std: 标准化后的训练数据特征值。  
    # - self.Y_train: 训练数据的标签。{0,1}
    # - self.X_test_std: 标准化后的测试数据特征值。  
    # - self.Y_test: 测试数据的标签。 {0,1}
    # - self.alpha: 训练学习率
    # - self.time: 训练迭代数
    # - self.w_arg: 模型参数值
    # - self.Loss_list: 存储每次训练周期的loss
    # Note:
    # - 在X的第一维度为添加的偏置因子

        X_train,Y_train=loadCSVfile1(filename_train)
        X_test,Y_test=loadCSVfile1(filename_test)
        sc=StandardScaler()
        sc.fit(X_train)
        X_train_std=sc.transform(X_train)
        X_test_std=sc.transform(X_test)

        new_column = np.ones((X_train_std.shape[0], 1))
        self.X_train_std=np.hstack((new_column, X_train_std))
        
        new_column_2= np.ones((X_test_std.shape[0], 1))
        self.X_test_std=np.hstack((new_column_2, X_test_std))
        
        self.Y_train=Y_train   
        print(self.Y_train.shape)
        self.Y_test=Y_test
        self.time=time
        self.alpha=alpha
        self.w_num=self.X_train_std.shape[1] 
        self.w_arg=np.ones((self.w_num,1))
        self.Loss_list=[]

    
    def sigmoid(self,inX): 
         
    #批量计算传入参数的sigmoid值
    #参数：
    #- inX：一般形式为（a,1）
    #返回：
    #- res：对inX的每个元素求sigmoid后的结果值

         res=np.zeros(inX.shape)
         for i in range(inX.shape[0]):
             if inX[i]>=0:
                res[i]=1/(1+np.exp(-inX[i]))
             else:
                res[i]=np.exp(inX[i])/(1+np.exp(inX[i]))
         return res
    
    def Gradient_Descent(self):

    # 对参数self.w_arg每个元素梯度下降更新一次
    # Notes：
    # - grad：计算加入了正则因子的梯度，没有平均

        Y_train_Mat=np.mat(self.Y_train).transpose()
        grad=-np.dot((Y_train_Mat-self.sigmoid(np.dot(self.X_train_std,self.w_arg))).transpose(),self.X_train_std).transpose()
        grad+=self.w_arg
        self.w_arg=self.w_arg-self.alpha*grad
    
    def Loss(self):

    # 算出所有训练样本的总loss，没有平均所以比较大
    # return：
    # - loss[0]: self.w_arg对应的当前模型对训练样本的总loss值

        y=self.Y_train 
        Hypothesis_predict=self.sigmoid(np.dot(self.X_train_std,self.w_arg))
        epsilon = 1e-5   
        loss=-(np.dot(y,np.log(Hypothesis_predict+epsilon))+np.dot((1-y),np.log(1-Hypothesis_predict+epsilon)))
        w_tm = sum(x**2 for x in self.w_arg) / 2
        loss[0]+=w_tm
        return loss[0]

    def Iterate(self):

    # 1. 梯度更新self.time次，训练模型并且记录loss
    # 2. 计算训练完的模型对测试数据的正确率，并且打印输出总测试个数和总正确数

        # 1：
        start_time = time.time()  
        for i in range(0,self.time):
            #阶段性计算损失
            loss=self.Loss()
            print("cross_entropy_train loss: ",loss)
            self.Loss_list.append(loss)
            self.Gradient_Descent()
        end_time = time.time()  
        training_duration = end_time - start_time  
        print(f"cross_entropy_loss训练时长: {training_duration:.4f} 秒")
        #2：
        predict=np.dot(self.X_test_std,self.w_arg) 
        correct_sum=0
        for i in range(0,len(self.Y_test)):
            if(predict[i][0]>=0 and self.Y_test[i]==1):
                correct_sum+=1
            elif(predict[i][0]<0 and self.Y_test[i]==0):
                correct_sum+=1
        print("total test:",self.X_test_std.shape[0])
        print("after cross_entropy_train,the correct_sum in test: ",correct_sum)
    
    def showgraph(self,ax1):

    # 画出Loss散点图，轴为ax1，x轴为迭代周期数，y轴为Loss值

        y=self.Loss_list
        x=list(range(len(y)))
        ax1.scatter(x,y,marker='.',color='red')
        ax1.set_xlabel("time")
        ax1.set_ylabel("Loss")
        ax1.set_title("cross_entropy_train:Loss")  


class hinge_loss_train:

    def __init__(self,filename_train,filename_test,alpha,time):

    # Parameters:  
    #  filename_train (str): 训练数据的csv文件名字。  
    #  filename_test (str): 测试数据的csv文件名字。    
    # 实例变量：  
    # - self.X_train_std: 标准化后的训练数据特征值。  
    # - self.Y_train: 训练数据的标签。{-1,1}
    # - self.X_test_std: 标准化后的测试数据特征值。  
    # - self.Y_test: 测试数据的标签。 {-1,1}
    # - self.alpha: 训练学习率
    # - self.time: 训练迭代数
    # - self.w_arg: 模型参数值
    # - self.Loss_list: 存储每次训练周期的loss
    # Note:
    # - 在X的第一维度为添加的偏置因子
    # - Y更改为{-1，1}

        X_train,Y_train=loadCSVfile1(filename_train)
        X_test,Y_test=loadCSVfile1(filename_test)
        sc=StandardScaler()
        sc.fit(X_train)
        X_train_std=sc.transform(X_train)
        X_test_std=sc.transform(X_test)

        new_column = np.ones((X_train_std.shape[0], 1))
        self.X_train_std=np.hstack((new_column, X_train_std))
        
        new_column_2= np.ones((X_test_std.shape[0], 1))
        self.X_test_std=np.hstack((new_column_2, X_test_std))
        
        self.Y_train=Y_train
        self.Y_train[self.Y_train==0]=-1 
        self.Y_test=Y_test
        self.Y_test[self.Y_test==0]=-1 
        self.time=time
        self.alpha=alpha
        self.w_num=self.X_train_std.shape[1]
        self.w_arg=0.005*np.ones((self.w_num,1))
        self.Loss_list=[]
   
    def Loss(self):

    # 算出所有训练样本的总loss，没有平均所以比较大
    # return：
    # - Loss: self.w_arg对应的当前模型对训练样本的总loss值

        Y_train_Mat=np.mat(self.Y_train).transpose()
        tm=1-np.multiply(Y_train_Mat,np.dot(self.X_train_std,self.w_arg))
        w_tm = sum(x**2 for x in self.w_arg) / 2
        Loss=0
        Loss+=w_tm
        print(tm.shape)
        for i in range(0,tm.shape[0]):
            if tm[i][0]>0:
                Loss+=(tm[i][0])[0,0]
        return Loss
    
    def Gradient_Descent(self):

    # 对参数self.w_arg每个元素梯度下降更新一次
    # Notes：
    # - grad：计算加入了正则因子的梯度，没有平均

        Y_train_Mat=np.mat(self.Y_train).transpose()
        tm=1-np.multiply(Y_train_Mat,np.dot(self.X_train_std,self.w_arg))
        tm[tm<=0]=0
        tm[tm>0]=1
        tm=-np.multiply(tm,Y_train_Mat)
        grad=np.dot(self.X_train_std.transpose(),tm)+self.w_arg
        self.w_arg=self.w_arg-self.alpha*grad

    def Iterate(self):

    # 1. 梯度更新self.time次，训练模型并且记录loss
    # 2. 计算训练完的模型对测试数据的正确率，并且打印输出总测试个数和总正确数
        # 1：
        start_time = time.time()  
        for i in range(0,self.time):
            loss=self.Loss()
            print("hinge_loss_train loss: ",loss)
            self.Loss_list.append(loss)
            self.Gradient_Descent()
        end_time = time.time()  
        training_duration = end_time - start_time  
        print(f"hinge loss训练时长: {training_duration:.4f} 秒")
        # 2：
        predict=np.dot(self.X_test_std,self.w_arg) 
        correct_sum=0
        for i in range(0,len(self.Y_test)):
            if(predict[i][0]>=0):
              if self.Y_test[i]==1:
                correct_sum+=1
            elif(predict[i][0]<0):
               if self.Y_test[i]==-1:
                correct_sum+=1
        print("total test:",self.X_test_std.shape[0])
        print("after hinge_loss_train,the correct_sum in test: ",correct_sum)
    
    def showgraph(self,ax2):

    # 画出Loss散点图，轴为ax2，x轴为迭代周期数，y轴为Loss值

        y=self.Loss_list
        x=list(range(len(y)))
        ax2.scatter(x,y,marker='.',color='blue')
        ax2.set_xlabel("time")
        ax2.set_ylabel("Loss")
        ax2.set_title("hinge_loss_train:Loss")  


if __name__ == "__main__":
     filename_train="./data/mnist_01_train.csv"

     filename_test="./data/mnist_01_test.csv"
    #支持向量机分类
     svm_train=svmtrain(filename_train,filename_test)
     svm_train.gauss_train()
     svm_train.linear_train()

    #交叉熵分类
     cross_entropy_classify=cross_entropy_train(filename_train,filename_test,0.05,50)#选0.3开始震荡了
     cross_entropy_classify.Iterate()
   
    #hinge_loss分类
     hinge_loss_train=hinge_loss_train(filename_train,filename_test,0.05,50) #0.05目前最佳
     hinge_loss_train.Iterate()

     fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(18, 6)) 
     cross_entropy_classify.showgraph(ax1)
     hinge_loss_train.showgraph(ax2)
     plt.tight_layout()
     plt.show()



