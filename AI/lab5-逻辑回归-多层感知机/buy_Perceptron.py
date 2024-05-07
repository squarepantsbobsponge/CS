import string 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation  
import csv
class Perceptron:
    def __init__(self,filename:string) :#读取数据，整理数据，设置参数初始值和参数数量
        #提取信息
        f=open(filename)
        csv_reader=csv.reader(f)
        flag=1#去掉头信息
        self.lable=[]#数据标准化
        self.x1_x2=[]
        max_x1=0
        max_x2=0
        min_x1=10000000
        min_x2=10000000  
        self.alpha=0.1     
        for line in csv_reader:
            if flag==1:
                flag=0
                continue
            int_list=[int(s) for s in line]
            self.lable.append(int_list[2])
            tmp=[]
            tmp.append(int_list[0])
            tmp.append(int_list[1])
            self.x1_x2.append(tmp)
            if(tmp[0]>max_x1):
                max_x1=tmp[0]
            if(tmp[0]<min_x1):
                min_x1=tmp[0]
            if(tmp[1]>max_x2):
                max_x2=tmp[1]
            if(tmp[1]<min_x2):
                min_x2=tmp[1]
        #标准化
        for i in range(0,len(self.x1_x2)):
            self.x1_x2[i][0]=(self.x1_x2[i][0]-min_x1)/(max_x1-min_x1)
            self.x1_x2[i][1]=(self.x1_x2[i][1]-min_x2)/(max_x2-min_x2)
        #记录代价，画图分析用
        self.loss_list=[]
        ##中间一个隐藏层的算法 而且中间层有两个因子（先不加偏置因子），参数矩阵两个，都是2*2
            #随机初始化两个参数矩阵  #输入层两个因子代表特征没有偏置因子 #输出层只有一个因子
        self.w1=np.random.uniform(0.25,0.3,[2,2])#返回类型为ndarray
        self.w2=np.random.uniform(-0.2,0,2) #一行
        # self.w1 = np.random.randn(2, 3) * np.sqrt(1 / 3)
        # self.w2 = np.random.randn(1, 2) * np.sqrt(1 / 2)
        self.w2=self.w2[np.newaxis,:] #调整矩阵形状
    def sigmoid(self,inX): #对一个列向量的全部元素sigmod
        res = np.zeros(inX.shape)
        for i in range(inX.shape[0]):
            if inX[i] >= 0:
                res[i] = 1 / (1 + np.exp(-inX[i]))
            else:
                res[i] = np.exp(inX[i]) / (1 + np.exp(inX[i]))
        return res   ##inX只能实现列向量
    def sigmoid_x(self,inX):#对一个列向量进行sigmod求导
        res=self.sigmoid(inX)
        return res*(1-res)
    def  Hypothesis_Function(self,index): #前推导 #计算的是第index数据的
        ##求所有层的输入
        ##第一层因子压入就是输入
        Hy_first=[]
        Hy_first.append(self.x1_x2[index][0])
        Hy_first.append(self.x1_x2[index][1])
        Hy_first=np.array(Hy_first) ##转为矩阵类型 列向量
        self.Hy_first=Hy_first[:,np.newaxis] ##输入层的a值
        self.Hy_first_z=self.Hy_first#输入层的z值 a=sigmod（z），但是输入层a=z
        #Hy_matrix.append(Hy_first)
        ##算隐藏层
        self.Hy_second_z=np.dot(self.w1,self.Hy_first) #2*2,2*1= 2*1  ##隐藏层的z值
        self.Hy_second=self.sigmoid(self.Hy_second_z) #应该是列向量 #隐藏层的a值
        ##算输出层
        self.Hy_thrid_z=np.dot(self.w2,self.Hy_second)#已经是1x1了  1*2, 2*1 1*1 输出层的z值
        self.Hy_thrid=self.sigmoid(self.Hy_thrid_z)#列向量输出层1  #输出层的a值
        
    def Cost(self,index):#单个data损失计算
       # theta=np.matrix(self.arg)
       self.Hypothesis_Function(index)
       h_arg=self.Hy_thrid[0][0]     
       y=self.lable[index]
       ret=(-1*y*np.log(h_arg+ 1e-5))-((1-y)*np.log(1-h_arg+ 1e-5))#防止浮点数溢出
       return ret
    
    def Loss(self):#计算代价函数 #输出层只有一行，代价函数跟LR一样
        num=len(self.lable)  
        sum=0
        for i in range(0,num):
            sum+=self.Cost(i)
        return sum/num
    
    def arg_Err(self,index,flag):#后推导  flag代表求第几层 index代表求第几个数据的
     #当层Hy_z列向量的sigmod函数的导，点乘下一层的误差，叉乘当层到下一层w的转置 ##顺序倒过来一下
     #第三层
     derivative_z_third=self.sigmoid_x(self.Hy_thrid_z)   ##求输出层的a值对z值的偏导
     h_arg=self.Hy_thrid[0][0]  ##输出层的因子的值  
     y=self.lable[index]#label值
     derivative_error_third=y/h_arg*(-1)+(1-y)/(1-h_arg)  ##cost对输出层a值的导
     #derivative_error_third=(h_arg-y)/(h_arg*(1-h_arg))
     #derivative_error_third=y-h_arg
     third_error=derivative_z_third*derivative_error_third #点乘  cost对输出层z的偏导
     if flag==3:
         return third_error
     #第二层
     derivative_z_second=self.sigmoid_x(self.Hy_second_z)  #隐藏层a对隐藏层z的求导
     w2_T=self.w2.T #2*1
     second_error=np.dot(w2_T,third_error)*derivative_z_second   #cost对隐藏层a的求导=（参数矩阵2的转置（输出层z对隐藏层a的求导））（矩阵乘法）（cost对输出层z的求导）
     #second_error=np.multiply((third_error*w2_T),derivative_z_second)  #（cost对隐藏层z的求导）=（cost对隐藏层a的求导）（点乘）（隐藏层a对隐藏层z的求导）
     return second_error
     ##第一层,不需要第一层
    #  derivative_z_first=self.sigmoid_x(self.Hypothesis_Function(index,1,1))
    #  first_error=np.dot(self.w1,second_error)*derivative_z_first 
    #w[i,j]的单个梯度就是h[j]error[i]

    def Gradient_Descent(self,time):
        # 计算梯度
        Grandient_w1 = np.zeros(self.w1.shape)
        Grandient_w2 = np.zeros(self.w2.shape)
        for index in range(len(self.lable)):##所有数据的梯度加起来
            self.Hypothesis_Function(index)
            second_error = self.arg_Err(index, 2)
            third_error = self.arg_Err(index, 3)
            #w1矩阵的梯度（cost对w1矩阵的求导）=(cost对隐藏层z的求导）（矩阵乘法）（隐藏层z对w1的求导（输入层的a））
            Grandient_w1 += np.dot( second_error ,self.Hy_first.T) #2*1   1*2=2*2 #前推导和后推导合起来
            Grandient_w2 += third_error*self.Hy_second.T #w2矩阵的梯度 由于输出层只有一个因子，直接点乘
        # 平均梯度
        Grandient_w1 /= len(self.lable)
        Grandient_w2 /= len(self.lable)
        # 更新权重
        self.w1 -= Grandient_w1 * self.alpha           
        self.w2 -= Grandient_w2 * self.alpha                 
    def Iterate(self,time):#参数的迭代更新和每代的误差的获得
        for i in range(0,time):
            if(i%10==0):
                loss=self.Loss()
                self.loss_list.append(loss)
                print(loss)
            self.Gradient_Descent(i)#更新所有参数
        #计算正确率
        sum=0
        for i in range(0,len(self.lable)):
            self.Hypothesis_Function(i)
            tm=self.Hy_thrid[0][0]
            if(tm>=0 and self.lable[i]==1):
                sum+=1
            elif(tm<0 and self.lable[i]==0):
                sum+=1
        print(sum/len(self.lable))
        print(self.w1)
        print(self.w2)
        self.showgraph()
    def showgraph(self):
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
Per=Perceptron("./data.csv")
Per.Iterate(3000)

        
        
 





        

