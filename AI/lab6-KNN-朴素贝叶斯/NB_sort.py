import string 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation  
class NB:
    def __init__(self,filename):
        self.feature_dict_2=[{} for _ in range(9)] #记录每个特征的dict dict的键为特征所取值，item对应取这个值的数据量 
        self.feature_dict_4=[{} for _ in range(9)] 
        self.sum_2=0 #标签值为2的数据量
        self.sum_4=0 #标签值为4的数据量
        with open(filename,'r') as file:
            for line in file:
                string_list=line.split(",")
                int_list=[int(s) for s in string_list]
                #第一个是患者id，后面是患者的9个特征，再后面是y的取值
                if(int_list[10]==2):
                    self.sum_2+=1
                    for i in range(1,10):
                        if int_list[i] in self.feature_dict_2[i-1]:
                            self.feature_dict_2[i-1][int_list[i]]+=1 #对应特征count+=1
                        else:
                            self.feature_dict_2[i-1][int_list[i]]=1 #对应特征取值初始化为1
                else:
                    self.sum_4+=1
                    for i in range(1,10):
                        if int_list[i] in self.feature_dict_4[i-1]:
                            self.feature_dict_4[i-1][int_list[i]]+=1 #对应特征count+=1
                        else:
                            self.feature_dict_4[i-1][int_list[i]]=1 #对应特征取值初始化为1
    def train(self):#条件概率计算和标签概率运算
        self.feature_P_2=[{} for _ in range(9)] 
        self.feature_P_4=[{} for _ in range(9)]
        #遍历字典
        for i in range(0,9):
            for j in range(1,11):#特征值取值1-10，要拉普拉斯平滑
                if(j in self.feature_dict_2[i]):
                    item=self.feature_dict_2[i][j]
                    self.feature_P_2[i][j]=(item+1)/(self.sum_2+10)
                else:
                    self.feature_P_2[i][j]=1/(self.sum_2+10)
        for i in range(0,9):
            for j in range(1,11):#特征值取值1-10，要拉普拉斯平滑
                if(j in self.feature_dict_4[i]):
                    item=self.feature_dict_4[i][j]
                    self.feature_P_4[i][j]=(item+1)/(self.sum_4+10)
                else:
                    self.feature_P_4[i][j]=1/(self.sum_4+10)        
        self.P_2=(self.sum_2)/(self.sum_2+self.sum_4 )
        self.P_4=(self.sum_4)/(self.sum_2+self.sum_4 ) 
        #调试用
        print(self.feature_P_2)
        print(self.feature_P_4)
        print(self.P_2)
        print(self.P_4)      
    
    def test_model(self,filename):#测试训练集
        sum=0#数据总计数
        correct=0#正确估计的总计数
        self.train()
        with open(filename,'r') as file:
            for line in file:
                string_list=line.split(",")
                int_list=[int(s) for s in string_list]
                sum+=1
                P_2=self.P_2#预测是2的概率
                P_4=self.P_4#预测是4的概率
                for i in range(0,9):
                    feature=int_list[i+1]
                    P_2*=self.feature_P_2[i][feature]
                    P_4*=self.feature_P_4[i][feature]
                if(P_2>P_4 and int_list[10]==2):
                    correct+=1
                elif(P_4>P_2 and int_list[10]==4):
                    correct+=1
        print("正确率为：",correct/sum)
                 

                    

nb=NB("./train.data")
nb.test_model("./test.data")