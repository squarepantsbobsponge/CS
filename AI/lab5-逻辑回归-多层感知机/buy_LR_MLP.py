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
            #这里调整一下y的取值
            if int_list[2]==0:
                int_list[2]=-1
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
        for i in range(0,len(self.x1_x2)):
            self.x1_x2[i][1]=(self.x1_x2[i][1]-min_x1)/(max_x1-min_x1)
            self.x1_x2[i][2]=(self.x1_x2[i][2]-min_x2)/(max_x2-min_x2)            
       #设置参数量，先是逻辑线性回归函数，所以是三个参数a+bx1+cx2
        self.arg_num=3
        #设置初始参数 #随机生成
        self.arg=[]
        self.arg.append(1)
        self.arg.append(1)
        self.arg.append(1)
        #设置学习步长
        self.alpha=0.06 #要逐步减小步长，先固定#0.5步长太大了只会震荡  ##0.05的时候0.788
        #记录代价，画图分析用
        self.loss_list=[]
        
    def Hypothesis_Function(self,index:int):#计算多层感知机的的假设值，index是要计算的数据的标号
        #直接运算,第一个参数0次的不要乘特征  多层感知机是sign函数不是sigmod函数
        z=self.arg[0]+self.x1_x2[index][1]*self.arg[1]+self.x1_x2[index][2]*self.arg[2]
        if z>=0: #对sigmoid函数优化，避免出现极大的数据溢出
            return 1
        else:
            return -1

    
    def Cost(self,index):#单个data损失计算
       # theta=np.matrix(self.arg)
       y=self.lable[index]
       ret=-y*(self.arg[0]+self.x1_x2[index][1]*self.arg[1]+self.x1_x2[index][2]*self.arg[2])
       return ret
    
    def Loss(self):#计算当前模型所有数据的预估和真实之间的误差之和
        num=len(self.data)
        sum=0
        count=0
        ##只有分类错误的才能算代价
        for i in range(0,num):
            if self.Cost(i)>=0:
                sum+=self.Cost(i)
                count+=1 #误分类的总数
        return sum/count 

    
    def Gradient_Descent(self): 
        for index in range(0,len(self.lable)):
            if self.Cost(index)>=0:
                #cost>=0是误分类点，更新参数   #随机梯度下降法，只有误分类点才能更新参数
                for i in range(0,self.arg_num):
                    if i==0:
                        self.arg[i]=self.arg[i]+self.alpha*self.lable[index]
                    else:
                        self.arg[i]=self.arg[i]+self.alpha*self.lable[index]*self.x1_x2[index][i] 
        

    def Iterate(self,time):#参数的迭代更新和每代的误差的获得
        for i in range(0,time):
            self.loss_list.append(self.Loss())
            if(i%10==0):
                print(self.Loss())
            self.Gradient_Descent()#更新所有参数
        #计算正确率arg[0]+arg[1]x1+ arg[2]x2>0 1小于0就是0
        sum=0
        for i in range(0,len(self.lable)):
            tm=self.Hypothesis_Function(i)
            if(tm>=0 and self.lable[i]==1):
                sum+=1
            elif(tm<0 and self.lable[i]==-1):
                sum+=1
        print(sum/len(self.lable))
    def showgraph(self):##最终答案
             fig2=plt.figure(2)
             x1_0=[]
             x2_0=[]
             x1_1=[]
             x2_1=[]
             for i in range(0,len(self.data)):
                 if(self.lable[i]==-1):
                    x1_0.append(self.x1_x2[i][1])
                    x2_0.append(self.x1_x2[i][2])
                 else:
                    x1_1.append(self.x1_x2[i][1])
                    x2_1.append(self.x1_x2[i][2])    
             #print(x1_1)
             plt.scatter(x1_0, x2_0, marker='.', color='red')
             plt.scatter(x1_1, x2_1, marker='.', color='blue')       
             plt.xlabel("x1")
             plt.ylabel("x2")  
                #画直线arg[0]+arg[1]x1+ arg[2]x2=0
             x1_values = np.linspace(0, 1,30)  # 替换起始值、结束值和点数为你需要的值
             print(self.arg)
             x2_values = (0- self.arg[0] - self.arg[1]*x1_values) / self.arg[2]  
             plt.plot(x1_values, x2_values, color='pink')  
             #Loss分析
             fig3=plt.figure(3)
             y=self.loss_list
             x=list(range(len(y)))
            #  for i in range(0,len(x)):  
            #    x[i] *= 10 
            #  print(x)
            #  print(y)
             plt.scatter(x, y, marker='.', color='red')
             plt.xlabel("time")
             plt.ylabel("Loss") 
             plt.show()
                
filename="./data.csv"
LR_classify=LR(filename)
LR_classify.Iterate(3000)
LR_classify.showgraph()