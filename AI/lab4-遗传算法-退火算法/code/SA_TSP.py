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

    def produce(self,nxt):
         s=0
         t=0
         while(nxt[s]==nxt[t]):
            s=random.randint(1,(len(nxt)-1))
            t=random.randint(1,(len(nxt))-1)
         if(s==0 or s==(len(nxt)-1)):
                tm=nxt[t]
                nxt[t]=nxt[s]
                nxt[(len(nxt)-s-1)]=tm
                nxt[s]=tm
         elif(t==0 or t==(len(nxt)-1)):
                tm=nxt[s]
                nxt[s]=nxt[t]
                nxt[(len(nxt)-t-1)]=tm
                nxt[t]=tm
         else:
            tm=nxt[s]
            nxt[s]=nxt[t]
            nxt[t]=tm             

    def iterate(self,num_iterations:int):
        #外循环是退火降温
        alpha=0.88
        t=0
        bst=self.population[0]
        cur=self.population[0]
        for i in range(50,0,-1):
           t=pow(alpha,i)#退火参刷
           for j in range(0,60):#新的解生与计算
                #随机交换两个城市生成新的解，注意头尾位置
                nxt=copy.deepcopy(cur)
                self.produce(nxt)
                ##看相差量
                cost_nxt=self.conculate(nxt)
                cost_cur=self.conculate(cur)
                cost_del=cost_nxt-cost_cur
                self.aly.append(cost_nxt)
                ##看是否被接受
                if cost_del<0:
                     cur=nxt
                     bst=nxt
                else:#按概率接受
                    #计算接受概率
                    P_s=np.exp(-cost_del/t)
                    random_num=random.random() #生成0-1的随机数
                    if random_num<=P_s:
                         cur=nxt
        return bst

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
             plt.scatter(x, y, marker='.', color='red')
             plt.xlabel("time")
             plt.ylabel("distance") 
             plt.show()


def main():
     gp=GeneticAlgTSP("./qa194.tsp")


     answer=gp.iterate(3000)
     print(gp.conculate(answer))

     print(answer)

     gp.showgraph(answer)
if __name__ == "__main__":  
    main()
