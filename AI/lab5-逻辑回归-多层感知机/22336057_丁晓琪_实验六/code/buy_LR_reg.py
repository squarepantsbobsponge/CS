import string 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation  
import csv
class LR:
    def __init__(self,filename:string) :#读取数据，整理数据，设置参数初始值和参数数量
        #提取信息
        f=open(filename)
        csv_reader=csv.reader(f)
        self.data=[]#存储提取出来的数据，格式为【【A，E，P】, ....】
        flag=1#去掉头信息
        self.lable=[]#数据标准化
        self.x1_x2=[]
        self.reg=0.01#正则化参数
        max_x1=0
        max_x2=0
        min_x1=10000000
        min_x2=10000000       
        for line in csv_reader:
            if flag==1:
                flag=0
                continue
            int_list=[int(s) for s in line]
            self.data.append(int_list)
            self.lable.append(int_list[2])
            tmp=[]
            tmp.append(1)
            tmp.append(int_list[0])
            tmp.append(int_list[1])
            self.x1_x2.append(tmp)
            if(tmp[1]>max_x1):
                max_x1=tmp[1]
            if(tmp[1]<min_x1):
                min_x1=tmp[1]
            if(tmp[2]>max_x2):
                max_x2=tmp[2]
            if(tmp[2]<min_x2):
                min_x2=tmp[2]
        #标准化
                 #再压一个参数进去x1*x2
        for i in range(0,len(self.x1_x2)):
            self.x1_x2[i][1]=(self.x1_x2[i][1]-min_x1)/(max_x1-min_x1)
            self.x1_x2[i][2]=(self.x1_x2[i][2]-min_x2)/(max_x2-min_x2)
            self.x1_x2[i].append(self.x1_x2[i][2]*self.x1_x2[i][2])
        
       #设置参数量，先是逻辑线性回归函数，所以是三个参数a+bx1+cx2
        self.arg_num=4
        #设置初始参数 #随机生成  #多加个参数
        self.arg=[]
        self.arg.append(1)
        self.arg.append(1)
        self.arg.append(1)
        self.arg.append(1)
        #设置学习步长
        self.alpha=0.01 #要逐步减小步长，先固定#0.5步长太大了只会震荡 0.08
        #记录代价，画图分析用
        self.loss_list=[]
    def Hypothesis_Function(self,index:int):#计算逻辑回归的的假设值，index是要计算的数据的标号
        #直接运算,第一个参数0次的不要乘特征
        z=0
        for h_i in range(0,self.arg_num):
            if(h_i>=len(self.x1_x2[index])):
                fag=1
            z+=(self.arg[h_i]*self.x1_x2[index][h_i])
        #z=self.arg[0]+self.x1_x2[index][1]*self.arg[1]+self.x1_x2[index][2]*self.arg[2]
        if z>=0: #对sigmoid函数优化，避免出现极大的数据溢出
            return 1.0 / (1 + np.exp(-z))
        else:
            return np.exp(z)/(1+np.exp(z))

  ##正则化改到这  
    def Cost(self,index):#单个data损失计算
       # theta=np.matrix(self.arg)
       h_arg=self.Hypothesis_Function(index)
       y=self.lable[index]
       ret=(-1*y*np.log(h_arg+ 1e-5))-((1-y)*np.log(1-h_arg+ 1e-5))#防止浮点数溢出
       return ret
    
    def Loss(self):#计算当前模型所有数据的预估和真实之间的误差之和
        num=len(self.data)
        sum=0
        for i in range(0,num):
            sum+=self.Cost(i)
        ##加入正则化
        sum1=0
        for i in range(1,self.arg_num):#不对第一个参数惩罚
            sum1+=(self.arg[i]*self.arg[i])
        sum1*=self.reg
        sum+=sum1
        return sum/num

    def sigmoid(self,inX):
        res = np.zeros(inX.shape)
        for i in range(inX.shape[0]):
            if inX[i] >= 0:
                res[i] = 1 / (1 + np.exp(-inX[i]))
            else:
                res[i] = np.exp(inX[i]) / (1 + np.exp(inX[i]))
        return res
    
    def Gradient_Descent(self):  
        # num = len(self.data)  
        # gradients = np.zeros_like(self.arg)  # 初始化梯度为0  
        # for i in range(num):  
        #     y = self.data[i][2]  
        #     h_arg_i = self.Hypothesis_Function(i)  
        #     for index in range(self.arg_num):  
        #         xj = self.data[i][index-1] if index > 0 else 1  # 第一个参数对应 x0=1  
        #         gradients[index] += (h_arg_i - y) * xj  
        #     # 更新所有参数  
        # self.arg -= self.alpha * gradients / num
        dataMatrix = np.mat(self.x1_x2)
        labelMat = np.mat(self.lable).transpose()  # 转置
        m, n = dataMatrix.shape
        weights = np.ones((n,1))
        for i in range(0,n):
            weights[i][0]=self.arg[i]
        grad = -((labelMat - self.sigmoid(dataMatrix * weights)).transpose() * dataMatrix).transpose()
        weights = weights - self.alpha * grad
        for i in range(0,n):
           if i==0:
              self.arg[i]= (weights[i][0])[0,0]
           else: 
                self.arg[i]= (weights[i][0])[0,0]-self.alpha*self.reg/m*self.arg[i]  
        #减去正则参数的乘法，除了第一个参数
        


    def Iterate(self,time):#参数的迭代更新和每代的误差的获得
        for i in range(0,time):
            if(i%10==0):
                loss=self.Loss()
                self.loss_list.append(self.Loss())
            self.Gradient_Descent()#更新所有参数
        #计算正确率arg[0]+arg[1]x1+ arg[2]x2>0 1小于0就是0
        sum=0
        for i in range(0,len(self.lable)):
            tm=self.arg[0]*self.x1_x2[i][0]+self.arg[1]*self.x1_x2[i][1]+self.arg[2]*self.x1_x2[i][2]+self.arg[3]*self.x1_x2[i][3]
            if(tm>=0 and self.lable[i]==1):
                sum+=1
            elif(tm<0 and self.lable[i]==0):
                sum+=1
        print("正确率：",sum/len(self.lable))
    def showgraph(self):##最终答案
             fig2=plt.figure(2)
             x1_0=[]
             x2_0=[]
             x1_1=[]
             x2_1=[]
             for i in range(0,len(self.data)):
                 if(self.lable[i]==0):
                    x1_0.append(self.x1_x2[i][1])
                    x2_0.append(self.x1_x2[i][2])
                 else:
                    x1_1.append(self.x1_x2[i][1])
                    x2_1.append(self.x1_x2[i][2])    
             #print(x1_1)
             plt.scatter(x2_0, x1_0, marker='.', color='red')
             plt.scatter(x2_1, x1_1, marker='.', color='blue')       
             plt.xlabel("x2")
             plt.ylabel("x1")  
                #画直线arg[0]+arg[1]x1+ arg[2]x2+arg[3]x2*x2=0
             x2_values = np.linspace(0, 1,30)  # 替换起始值、结束值和点数为你需要的值
             print("参数为",self.arg)
             x1_values = (0- self.arg[0] - self.arg[2]*x2_values-self.arg[3]*x2_values*x2_values) / self.arg[1]  
             plt.plot(x2_values, x1_values, color='pink')  
             #Loss分析
             fig3=plt.figure(3)
             y=self.loss_list
             x=list(range(len(y)))
             for i in range(0,len(x)):  
               x[i] *= 10 
            #  print(x)
            #  print(y)
             plt.scatter(x, y, marker='.', color='red')
             plt.xlabel("time")
             plt.ylabel("Loss") 
             plt.show()
                
def main():
    print("迭代次数为1500")                
    filename="./data.csv"
    LR_classify=LR(filename)
    LR_classify.Iterate(1500)
    LR_classify.showgraph()

if __name__=="__main__":
    main()