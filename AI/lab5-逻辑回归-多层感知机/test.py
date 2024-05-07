import string 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation  
import csv
class test:
    def __init__(self):
        self.w1=np.random.uniform(0,6,[2,3])#返回类型为ndarray
        self.w2=np.random.uniform(0,6,2) #一行
        self.w2=self.w2[np.newaxis:,]
        self.lable=[1]#数据标准化
        self.x1_x2=[[1,2,3]]
        self.alpha=0.5        
    def sigmoid(self,inX):
        res = np.zeros(inX.shape)
        for i in range(inX.shape[0]):
            if inX[i] >= 0:
                res[i] = 1 / (1 + np.exp(-inX[i]))
            else:
                res[i] = np.exp(inX[i]) / (1 + np.exp(inX[i]))
        return res   ##inX只能实现列向量
    def sigmoid_x(self,inX):#求导
        res=self.sigmoid(inX)
        return res*(1-res)
    def  Hypothesis_Function(self,index):
        ##求所有层的输入##单个数据输入时
        ##第一层因子压入就是输入
        Hy_first=[]
        Hy_first.append(self.x1_x2[index][0])
        Hy_first.append(self.x1_x2[index][1])
        Hy_first.append(self.x1_x2[index][2])
        Hy_first=np.array(Hy_first) ##转为矩阵类型 列向量
        self.Hy_first=Hy_first[:,np.newaxis] ##加个线性输入
        self.Hy_first_z=self.Hy_first
        #Hy_matrix.append(Hy_first)
        ##算隐藏层
        self.Hy_second_z=np.dot(self.w1,self.Hy_first)
        self.Hy_second=self.sigmoid(self.Hy_second_z) #应该是列向量 #矩阵乘法前面列要等于后面行
        ##算输出层
        self.Hy_thrid_z=np.dot(self.w2,self.Hy_second)
        self.Hy_thrid=self.sigmoid(self.Hy_thrid_z)#列向量输出层1
        self.Hy_thrid=self.Hy_thrid[:,np.newaxis] ##加个线性输入
        self.Hy_thrid_z=self.Hy_thrid_z[:,np.newaxis] ##加个线性输入
        
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
    
    def arg_Err(self,index):
     #当层Hy_z列向量的sigmod函数的导，点乘下一层的误差，叉乘当层到下一层w的转置 ##顺序倒过来一下
     #第三层
     derivative_z_third=self.sigmoid_x(self.Hy_thrid_z)
     h_arg=self.Hy_thrid[0][0]
     y=self.lable[index]#第三层没有下一层直接求
     derivative_error_third=y*h_arg*(-1)+(1-y)*(1-h_arg)
     third_error=derivative_z_third*derivative_error_third #点乘
     #第二层
     derivative_z_second=self.sigmoid_x(self.Hy_second_z)
     w2_T=self.w2.T[:,np.newaxis]
     second_error=np.dot(w2_T,third_error)*derivative_z_second
     return second_error,third_error
     ##第一层,不需要第一层
    #  derivative_z_first=self.sigmoid_x(self.Hypothesis_Function(index,1,1))
    #  first_error=np.dot(self.w1,second_error)*derivative_z_first 
    #w[i,j]的单个梯度就是h[j]error[i]

    def Gradient_Descent(self):  
          ##第一层参数跟新
          row,col=self.w1.shape
          Grandient_w1=np.zeros(self.w1.shape)
          for i in range(0,row):
              for j in range(0,col):
                  for index in range(0,len(self.lable)):
                      self.Hypothesis_Function(index)
                      second_error=self.arg_Err(index)[0]
                      Grandient_w1[i][j]+=second_error[i][0]*self.Hy_first[j][0]
          self.w2=self.w2[np.newaxis,:]
          row,col=self.w2.shape
          Grandient_w1=Grandient_w1/len(self.lable)
          Grandient_w2=np.zeros(self.w2.shape)
          for i in range(0,row):
              for j in range(0,col):
                  for index in range(0,len(self.lable)):
                      self.Hypothesis_Function(index)
                      third_error=self.arg_Err(index)[1]
                      Grandient_w2[i][j]+=third_error[i][0]*self.Hy_second[j][0]
          Grandient_w2=Grandient_w2/len(self.lable)
          self.w1=self.w1-Grandient_w1*self.alpha
          self.w2=self.w2-Grandient_w2*self.alpha    
test1=test()
test1.Gradient_Descent()