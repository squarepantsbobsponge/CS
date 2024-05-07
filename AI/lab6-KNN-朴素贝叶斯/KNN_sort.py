import string 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation  
class KNN:  ##这里样本特征不用归一化，因为尺度都一样
    def __init__(self,filename):
        self.feature_dict_2=[{} for _ in range(9)] #记录每个特征的dict dict的键为特征所取值，item对应取这个值的数据量 
        self.feature_dict_4=[{} for _ in range(9)] 
        self.sum_2=0 #标签值为2的数据量
        self.sum_4=0 #标签值为4的数据量
        self.train=[] ##要把数据放进来
        with open(filename,'r') as file:
            for line in file:
                string_list=line.split(",")
                int_list=[int(s) for s in string_list]
                self.train.append(int_list) #第一个[0]为病号Id, [10]标签
        self.k=round(np.sqrt(len(self.train))) #转为整数 k为取前k个最相似的标签的众数
        self.count=self.sum_2+self.sum_4##训练数据量
    def EDU_dist(self,test:list,index_train): #标签间欧式距离平方版，不开方
        train=self.train[index_train]
        sum=0
        for i in range(1,10):
            sum+=pow((test[i]-train[i]),2)
        return sum
    def sort_singal(self,test:list):#返回该数据的预测分类 #单个测试数据
        #数据间计算欧式距离
        sort_dict=[] #key为欧式距离 value为对应的train_ID的标签值,不允许重复键改为list实现 0
        for i in range(0,len(self.train)):
            tm=[]
            edu_dist=self.EDU_dist(test,i)
            tm.append(edu_dist)
            tm.append(self.train[i][10])
            sort_dict.append(tm)
        #按升序排列
        sorted_dict=sorted(sort_dict, key=lambda x: x[0])
        ##计算前k个标签众数
        count_4=0
        count_2=0
        for i in(range(0,self.k)):
            if sorted_dict[i][1]==2:
                count_2+=1
            else:
                count_4+=1
        if(count_4>=count_2):
            return 4
        else:
            return 2

    def test_model(self,filename):#测试训练集
        sum=0#数据总计数
        correct=0#正确估计的总计数
        with open(filename,'r') as file:
            for line in file:
                string_list=line.split(",")
                int_list=[int(s) for s in string_list]
                sum+=1

                if(int_list[10]==2 and self.sort_singal(int_list)==2):
                    correct+=1
                elif(int_list[10]==4 and self.sort_singal(int_list)==4):
                    correct+=1
        print("正确率为：",correct/sum) ##正确率超高的1.0  

knn=KNN("./train.data")
knn.test_model("./test.data")

        