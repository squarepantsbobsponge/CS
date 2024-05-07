import string 
import tsplib95
import numpy as np
import random
import bisect
import copy
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation  
class GeneticAlgTSP:
    def __init__(self,filename:string) -> None:
        problem=tsplib95.load(filename)  #加载tsp文件
        coordinates=problem.node_coords #获取节点坐标#字典
        self.cities=[]
        self.aly=[]#分析散点图
        for key,value in coordinates.items():
             self.cities.append(value)
        #生成包含10个不同个体的种群
        self.population=[] #先避免个体重复s
        count=0
        while count<10:
            numbers=list(range(0,len(self.cities)))
            random.shuffle(numbers) #打乱排序
            if numbers in self.population:
                continue
            count+=1
            numbers.append(numbers[0])#旅行商问题要回到最开始的位置
            self.population.append(numbers)
    def fitness(self,population:list): #传入种群计算适应度,返回对应的适应度数组
         #适应度评估标准:总长度
         judge0=[]#初始的
         max=0#最大距离
         for ind in population:
            sum=0 #计算个体距离
            for i in range(0,len(ind)): #索引个体中的路线
                 a=ind[i]
                 b=ind[0]
                 if(i!=len(ind)-1):#最后一个点回原点
                      a=ind[i]
                      b=ind[i+1]
                 a_x,a_y=self.cities[a]
                 b_x,b_y=self.cities[b]
                 distance=math.sqrt((a_x-b_x)**2+(a_y-b_y)**2)
                 sum+=distance
            #旅行商要回到原点
            if(sum>max): max=sum
            #距离越短，适应度越高，翻转一下距离成为适应度
            #sum=1//sum##这样的话精度不够适应度会变成0的
            #count+=sum
            judge0.append(sum)
          #适应度为最大费和自己花费之差加1
         for i in range(0,len(judge0)):
              judge0[i]=max-judge0[i]+1#适配度只是相对于自己种群
         return judge0,max
    def RWS(self,fit_arr,population):
         P_S=[]#累计概率数组，直接来累计的省事、
         count=0#总适应度
         count2=0#累计概率
         for i in range(0,len(fit_arr)):
              count+=fit_arr[i]
            #   P_S.append(count)
         for i in range(0,len(fit_arr)):
              count2+=(fit_arr[i]/count)
              P_S.append(count2)
         selected=[]#被选择的有资格产生后代的父代个体
         #生成10次随机数轮盘赌
         for i in range(0,10):
              random_num=random.random() #生成0-1的随机数
              num=bisect.bisect_right(P_S,random_num)#在PS中的索引
              selected.append(population[num])
         return selected
#     def Crossover(self,c_a,c_b):##Subtour Exchange
#      #在去除头和尾的位置中选择一个片段
#         s=random.randint(1,(len(c_a)-1))#不要把开头和结尾算进去，很特殊的
#         t=random.randint(1,(len(c_b)-1))#不然乱了
#         while(s==t or abs(s-t)>=10):#限制一下交叉键数
#             t=random.randint(1,(len(c_a)-1))
#         if s>t:
#               tm=s
#               s=t
#               t=s     
#         #找到这个片段在c_a上对应的基因
#         #找到这些基因在c_b上对应的顺序
#         list_b=[]
#         list_a=[]#若c_a里面有b里面的开头结尾，记下索引，并且避开
#         for gene in range(s,t):##这里没有避开b的开头和结尾
#                 flag=c_b.index(c_a[gene])
#                 if(flag!=0 and flag!=(len(c_b)-1)):
#                     list_b.append(flag)
#                 else:
#                      list_a.append(gene)
#         list_b.sort() #基因在c_b上的顺序按升序排列
#         flag=0
#         for gene in range(s,t): #c_a和list_b范围里面的c_b交换
#           if(gene in list_a):
#                continue
#           tm=c_a[gene]
#           c_a[gene]=c_b[list_b[flag]]
#           c_b[list_b[flag]]=tm
#           flag+=1
    def Crossover(self,c_a,c_b):##要映射，因为是旅行商问题
         #随机在长度范围内生成两个坐标，代笔要交换的位置
         s=random.randint(1,(len(c_a)-2))
         t=random.randint(1,(len(c_a))-2)
         while(s==t or abs(s-t)>=10):#限制一下交叉键数
            t=random.randint(1,(len(c_a)-1))
         a_dict=dict()
         b_dict=dict()
         #s和t要找最大的
         if s>t:
              tm=s
              s=t
              t=s
         #找到要交换片段交换和确认映射关系
         for i in range(s,t):
              #交叉子串，并且建立映射关系
              if(c_b[i]==c_a[i]):
                   continue
              a_dict[c_b[i]]=c_a[i]
              b_dict[c_a[i]]=c_b[i]
              tm=c_a[i]
              c_a[i]=c_b[i]
              c_b[i]=tm
         #映射
         for i in range(0,len(c_a)):
              if i in range(s,t):
                   continue
              #count=0
              while c_a[i] in a_dict: #错在多次映射的情况
                   c_a[i]=a_dict[c_a[i]]
               #     count+=1 调试断点
               #     if(count==30):flag=1
              while c_b[i] in b_dict: #错在多次映射的情况
                   c_b[i]=b_dict[c_b[i]]
    def Mutation(self,child):
        ms=random.randint(1,(len(child)-2))#不要把开头和结尾算进去，很特殊的
        mt=random.randint(1,(len(child)-2))#不然乱了
        if ms>mt:
              tm=ms
              ms=mt
              mt=tm             
        #倒置
        tmp=child[ms:mt]
        child[ms:mt]=tmp[::-1]

    def select(self,fit_arr_child,fit_arr,population,Children,fit_arr_max,fit_arr_child_max):#两个种群适配度的尺度要统一哎，不然没办法比
         fit_dict=dict()
         adopt=fit_arr_max-fit_arr_child_max
         flag=0#此时fit_arr的尺度更大，要更改fit_arr_child
         if(adopt<0):
              adopt=adopt*-1
              flag=1#要更改fit_arr
         for i in range(0,len(fit_arr_child)):
              if(flag==0):
                   fit_arr_child[i]=fit_arr_child[i]+adopt
              fit_dict[fit_arr_child[i]]=Children[i]
         for i in range(0,len(fit_arr)):
              if(flag==1):
                   fit_arr[i]=fit_arr[i]+adopt
              fit_dict[fit_arr[i]]=population[i]
         sorted_dict=dict(sorted(fit_dict.items(),key=lambda item:item[0],reverse=True))#按照key从大到小排序
         top_ten_keys = list(sorted_dict.keys())[:10]
         #调试#这个有问题要是子代和父代的value高度重合，会引起dict里面不足10个键不能索引出10个值
         print(len(top_ten_keys))
         #解决：不足10个值的时候，手动给它加够10个值
         top_ten=[]
         for i in range(0,10):
              #top_ten.append(sorted_dict[top_ten_keys[i]])
             if len(top_ten_keys) > 0 and i < len(top_ten_keys):
                     top_ten.append(sorted_dict[top_ten_keys[i]])
         #手动补足10个值#
         sub=10-len(top_ten)
         i=0
         for j in range(0,sub):
               top_ten.append(top_ten[j])
         #print(top_ten_keys[0])
         return top_ten

    def iterate(self,num_iterations:int):
           for i in range(0,num_iterations):
                Children=[]#后代
                ##计算适应度，轮盘赌方法产生再生的10个数##由于这里直接生成了10个不同的数暂时忽略
                #选择再生轮盘赌
                fit_arr,fit_arr_max=self.fitness(self.population)#传一下最大值，为了统一适配度
                #轮盘赌，生成可以选择产生子代的父代个体
                selected=self.RWS(fit_arr,self.population)
                for j in range(0,5):#后代种群数目，自己指定吗，暂时指定个
                     #从selected中随机选两个交叉组合，注意交叉组合时是拷贝副本交叉组合
                     p_a=random.randint(0,9)
                     p_b=random.randint(0,9)
                     c_a=copy.deepcopy(selected[p_a])
                     c_b=copy.deepcopy(selected[p_b])
                     self.Crossover(c_a,c_b)
                    #检查是否正确交叉映射
                    #  set1 = set(c_a[1:30])
                    # # 检查集合的长度是否小于列表的长度
                    #  if len(set1) < len(c_a)-1:
                    #    print("列表中存在重复元素")
                    #  else:
                    #    print("列表中没有重复元素")
                     ##以一定的概率变异，先以0.05的概率变异
                     pp=random.random()
                     if pp<=0.21:  
                         self.Mutation(c_a)

                         self.Mutation(c_b)
                     if(c_a==c_b):
                         self.Mutation(c_a)
                         self.Mutation(c_b)                          
                     Children.append(c_a)
                     Children.append(c_b)
                #计算合并父子代种群，选最合适的一代
                fit_arr_child,fit_arr_child_max=self.fitness(Children)#传一下最大值为了统一适配度
                self.population=self.select(fit_arr_child,fit_arr,self.population,Children,fit_arr_max,fit_arr_child_max)#其中适应度已经从小到大排列了
                #self.population=self.population+Children
                #self.showgraph(self.population[0])
                print(self.conculate(self.population[0]))
                if(i%10==0):#采样制造分析图
                     self.aly.append(self.conculate(self.population[0]))
     #迭代完取最大适应度种群，由于已经从大到小排列，则解为第一个个体
           return self.population[0]

    def conculate(self,answer):
            sum=0 #计算个体距离
            for i in range(0,len(answer)): #索引个体中的路线
                 a=answer[i]
                 b=answer[0]
                 if(i!=len(answer)-1):#最后一个点回原点
                      a=answer[i]
                      b=answer[i+1]
                 a_x,a_y=self.cities[a]
                 b_x,b_y=self.cities[b]
                 distance=math.sqrt((a_x-b_x)**2+(a_y-b_y)**2)
                 sum+=distance  
            return sum

    def showgraph(self,answer):##最终答案
             fig2 = plt.figure(2)#用于显示最终的解
             x=[]
             y=[]
             for i in range(0,len(answer)):
                  j=answer[i]
                  x.append(self.cities[j][0])
                  y.append(self.cities[j][1])
             for i in range(0,len(x)): #给每个点显示标号
                   plt.text(x[i],y[i],str(i+1))
             plt.plot(x,y)#折线图
             plt.scatter(x,y)#点
             plt.title("TSP")
             plt.xlabel("X")
             plt.ylabel("Y") 
             fig3=plt.figure(3)
             y=self.aly
             x=list(range(len(y)))
             for i in range(len(x)):  
               x[i] *= 10 
             plt.scatter(x, y, marker='.', color='red')
             plt.xlabel("time")
             plt.ylabel("distance") 
             plt.show()

def main():
     #例如：gp=GeneticAlgTSP("./dj38.tsp")
     filepath = input("请输入文件路径: ")  
     gp=GeneticAlgTSP(filepath)
     time=int(input("请输入迭代次数: "))  
     answer=gp.iterate(time)
     print(gp.conculate(answer))
     print(answer)
     gp.showgraph(answer)
if __name__ == "__main__":  
    main()