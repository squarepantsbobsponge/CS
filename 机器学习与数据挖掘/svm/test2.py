import numpy as np


A=np.array([[-1,-1],[1,1]])
B=np.array([[2,2],[2,2]])
A[A<=0]=1
print(A)#点乘

length = 10  # 示例长度，您可以根据需要修改  
my_list = [1] * length  
print(my_list)

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import random

#加载数据
import csv  
def loadCSVfile1(filename):
    list_file = []
    with open(filename,'r') as csv_file:  
        all_lines=csv.reader(csv_file)  
        next(all_lines)  # 跳过第一行  
        for one_line in all_lines:  
            float_line = [float(value) for value in one_line] #转为浮点数
            list_file.append(float_line)  
    arr_file = np.array(list_file)
    label = arr_file[:, 0]
    data = arr_file[:, 1:]
    return data, label  

class svmtrain:
    def __init__(self,filename_train,filename_test):
        '''
        self.X_train_std: 12665(样本数)*785(特征值（加上偏置那种）)
        self.X_test_std: 2115(测试数)*785
        self.Y_test:1*2115
        self.Y_train:1*12665
        '''
        X_train,self.Y_train=loadCSVfile1(filename_train)
        X_test,self.Y_test=loadCSVfile1(filename_test)
        sc=StandardScaler()
        sc.fit(X_train)
        self.X_train_std=sc.transform(X_train)
        self.X_test_std=sc.transform(X_test)

    def linear_train(self):
        svm=SVC(kernel='linear',C=1.0,random_state=1) #RANDOM_state指定随机种子使每次运行能够得到一样的结果，C为惩罚系数
        svm.fit(self.X_train_std,self.Y_train)
        y_pred=svm.predict(self.X_test_std)

        print('linear Misclassified samples: %d' % (self.Y_test != y_pred).sum())   # 输出错误分类的样本数
        print('linear Accuracy: %.2f' % svm.score(self.X_test_std, self.Y_test))         # 输出分类准确率

    def gauss_train(self):
        svm=SVC(kernel='rbf',C=1.0,random_state=2) #RANDOM_state指定随机种子使每次运行能够得到一样的结果，C为惩罚系数
        svm.fit(self.X_train_std,self.Y_train)
        y_pred=svm.predict(self.X_test_std)

        print('gauss Misclassified samples: %d' % (self.Y_test != y_pred).sum())   # 输出错误分类的样本数
        print('gauss Accuracy: %.2f' % svm.score(self.X_test_std, self.Y_test))         # 输出分类准确率


class cross_entropy_train:
    def __init__(self,filename_train,filename_test,alpha,time):
        '''
        self.X_train_std: 12665(样本数)*785(特征值（加上偏置那种）)
        self.X_test_std: 2115(测试数)*785
        self.Y_test:1*2115
        self.Y_train:1*12665
        self.w_arg:785*1
        '''
        X_train,Y_train=loadCSVfile1(filename_train)
        X_test,Y_test=loadCSVfile1(filename_test)
        sc=StandardScaler()
        sc.fit(X_train)
        X_train_std=sc.transform(X_train)
        X_test_std=sc.transform(X_test)

        new_column = np.ones((X_train_std.shape[0], 1))#偏置，行数样本数
        self.X_train_std=np.hstack((new_column, X_train_std))
        
        new_column_2= np.ones((X_test_std.shape[0], 1))
        self.X_test_std=np.hstack((new_column_2, X_test_std))
        
        self.Y_train=Y_train   #(12665,)，纯数组，没有第二个维度
        print(self.Y_train.shape)
        self.Y_test=Y_test
        self.time=time
        self.alpha=alpha
        self.w_num=self.X_train_std.shape[1] #列数，参数数
        self.w_arg=np.ones((self.w_num,1))#785*1
        self.Loss_list=[]

    
    def sigmoid(self,inX): #传入inX的格式为（a,1）,对第一列的每个元素sigmoid
         res=np.zeros(inX.shape)
         for i in range(inX.shape[0]):
             if inX[i]>=0:
                res[i]=1/(1+np.exp(-inX[i]))
             else:
                res[i]=np.exp(inX[i])/(1+np.exp(inX[i]))
         return res
    
    def Gradient_Descent(self):
        #将标签转为二维数组 12655*1
        Y_train_Mat=np.mat(self.Y_train).transpose()
        grad=-np.dot((Y_train_Mat-self.sigmoid(np.dot(self.X_train_std,self.w_arg))).transpose(),self.X_train_std).transpose()
          # 12655*1 - (12655*785  785*1=12655*1)-->1*12655
          # 1*12655 12655*785=1*785---> 785*1
        #grad/=Y_train_Mat.shape[0]#除平均值
        grad+=self.w_arg
        self.w_arg=self.w_arg-self.alpha*grad
    
    #算出所有训练样本的总loss，比较大没有平均
    def Loss(self):
        y=self.Y_train #1*12655
        Hypothesis_predict=self.sigmoid(np.dot(self.X_train_std,self.w_arg))#12655*785  785*1 =12655*1
        epsilon = 1e-5   #数组+标量=数组每个元素+标量
        #1*12665 12665*1--> 1
        loss=-(np.dot(y,np.log(Hypothesis_predict+epsilon))+np.dot((1-y),np.log(1-Hypothesis_predict+epsilon)))#对数组的所有元素求平均
        w_tm = sum(x**2 for x in self.w_arg) / 2
        loss[0]+=w_tm
        return loss[0]

    def Iterate(self):
        for i in range(0,self.time):
            #阶段性计算损失
            loss=self.Loss()
            print("cross_entropy_train loss: ",loss)
            self.Loss_list.append(loss)
            self.Gradient_Descent()
        #计算正确率
        predict=np.dot(self.X_test_std,self.w_arg) #2115*785  785*1 =2115*1
        correct_sum=0
        for i in range(0,len(self.Y_test)):
            if(predict[i][0]>=0 and self.Y_test[i]==1):
                correct_sum+=1
            elif(predict[i][0]<0 and self.Y_test[i]==0):
                correct_sum+=1
        print("total test:",self.X_test_std.shape[0])
        print("after cross_entropy_train,the correct_sum in test: ",correct_sum)
    
    def showgraph(self,ax1):
        y=self.Loss_list
        x=list(range(len(y)))
        ax1.scatter(x,y,marker='.',color='red')
        ax1.set_xlabel("time")
        ax1.set_ylabel("Loss")
        ax1.set_title("cross_entropy_train:Loss")  

class hinge_loss_train:
    def __init__(self,filename_train,filename_test,alpha,time):
        '''
        self.X_train_std: 12665(样本数)*785(特征值（加上偏置那种）)
        self.X_test_std: 2115(测试数)*785
        self.Y_test:1*2115
        self.Y_train:1*12665
        self.w_arg:785*1
        '''
        X_train,Y_train=loadCSVfile1(filename_train)
        X_test,Y_test=loadCSVfile1(filename_test)
        sc=StandardScaler()
        sc.fit(X_train)
        X_train_std=sc.transform(X_train)
        X_test_std=sc.transform(X_test)

        new_column = np.ones((X_train_std.shape[0], 1))#偏置，行数样本数
        self.X_train_std=np.hstack((new_column, X_train_std))
        
        new_column_2= np.ones((X_test_std.shape[0], 1))
        self.X_test_std=np.hstack((new_column_2, X_test_std))
        
        self.Y_train=Y_train
        self.Y_train[self.Y_train==0]=-1 #(12665,)
        #print(Y_train.shape)
        self.Y_test=Y_test
        self.Y_test[self.Y_test==0]=-1 #要把标签范围改了
        self.time=time
        self.alpha=alpha
        self.w_num=self.X_train_std.shape[1] #列数，参数数
        self.w_arg=0.005*np.ones((self.w_num,1))#785*1  #选1一开始的loss大得离谱 选0.001
        self.Loss_list=[]
        #self.predict_test=[0]*self.Y_test.shape[0]
    
    
    def Loss(self):
        #   12665*785 785*1=12665*1--->12665*1
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
        #正则因子求导之后是 self.w_arg
        #12665*1
        Y_train_Mat=np.mat(self.Y_train).transpose()
        tm=1-np.multiply(Y_train_Mat,np.dot(self.X_train_std,self.w_arg))
        tm[tm<=0]=0
        tm[tm>0]=1
        tm=-np.multiply(tm,Y_train_Mat)
        #785*12665  12665*1
        grad=np.dot(self.X_train_std.transpose(),tm)+self.w_arg
        self.w_arg=self.w_arg-self.alpha*grad

    def Iterate(self):
        for i in range(0,self.time):
            #阶段性计算损失
            loss=self.Loss()
            print("hinge_loss_train loss: ",loss)
            self.Loss_list.append(loss)
            self.Gradient_Descent()
        #计算正确率
        predict=np.dot(self.X_test_std,self.w_arg) #2115*785  785*1 =2115*1
        correct_sum=0
        for i in range(0,len(self.Y_test)):
            if(predict[i][0]>=0):
              if self.Y_test[i]==1:
                correct_sum+=1
              #self.predict_test[i]=1
            elif(predict[i][0]<0):
               if self.Y_test[i]==-1:
                correct_sum+=1
               #self.predict_test[i]=0
        print("total test:",self.X_test_std.shape[0])
        print("after hinge_loss_train,the correct_sum in test: ",correct_sum)
    

    def showgraph(self,ax2,ax3):
        y=self.Loss_list
        x=list(range(len(y)))
        ax2.scatter(x,y,marker='.',color='blue')
        ax2.set_xlabel("time")
        ax2.set_ylabel("Loss")
        ax2.set_title("hinge_loss_train:Loss")  

        # random_indices = random.sample(range(self.Y_test.shape[0]), 20)
        # random_Y = [(self.Y_test[i]) for i in random_indices]
        # random_X = [self.X_test_std[i][54] for i in random_indices]
        # random_predict=[self.predict_test[i] for i in random_indices]
        # colors = ['purple' if pred == 1 else 'green' for pred in random_predict] 
        # ax3.scatter(random_X,random_Y,marker='.',color=colors)
        # ax3.set_xlabel("feature over 666")
        # ax3.set_ylabel("Y")
        # ax3.set_title("hinge_loss_train:classify")  






##绘制决策图
#def plot_decision_regions(X,y,classifier,test_idx=None,resolution=0.02):

#高维好像不太能画图
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
     hinge_loss_train=hinge_loss_train(filename_train,filename_test,0.05,50)
     hinge_loss_train.Iterate()

     fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(18, 6)) 
     cross_entropy_classify.showgraph(ax1)
     hinge_loss_train.showgraph(ax2,ax2)
     plt.tight_layout()
     plt.show()