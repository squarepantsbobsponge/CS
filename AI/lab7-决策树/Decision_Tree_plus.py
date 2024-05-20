import string 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation  
import math
import csv
##多叉树的数据结构
class Node:
    def __init__(self,value,data):#value是父节点分支属性下自己的类别是什么
        self.value=value
        self.children=[]#子节点
        self.sort=None #下一个要分支的属性
        #要不要往里面放data呢
        self.data=data
        self.ent=0 #当层信息熵
        self.leave=-1 #0为0类，1为1类，-1为分支
class D_Tree:
    def __init__(self,filename:string) :#读取数据，整理数据，设置参数初始值和参数数量
        #提取信息
        f=open(filename)
        csv_reader=csv.reader(f)
        self.data_all=[]#存储提取出来的数据，格式为【【A，E，P】, ....】
        flag=1#去掉头信息
        attribute_1=[]##属性集 [[]]
        attribute_2=[]##第一位代表在data中的index
        attribute_3=[]
        attribute_4=[]
        for line in csv_reader:
            if flag==1:
                flag=0
                continue
            #提取整理数据 #不将数据数字化了，直接上，避免测试集还要处理
            for i in range(0,len(line)):
                if(i==0 and line[i] not in attribute_1):
                    attribute_1.append(line[i])
                if(i==1 and line[i] not in attribute_2):
                    attribute_2.append(line[i])
                if(i==2):#对标签处理以下
                    line[i]=int(line[i])
                    if(line[i]<=30000):
                        line[i]=0
                    else:
                        line[i]=1 #标签变成0，1
                if(i==3):#字符串转数字
                    line[i]=int(line[i])//10   
                    if(line[i] not in attribute_3): 
                        attribute_3.append(line[i]) ##这里要离散化处理  每10年一个单位
                if(i==4 and line[i] not in attribute_4):
                    attribute_4.append(line[i])   
            self.data_all.append(line)
            self.data=self.data_all[:500]##训练集
            self.data_test=self.data_all[500:]#预剪枝测试集
           # print(self.data)   
        self.attribute=[attribute_1,attribute_2,[],attribute_3,attribute_4]   #空一位后续便于直接按照[]索引对照data[]索引                 
        self.head=self.Tree_Generate(self.data,self.attribute,0,[])
   
    def Ent(self,data):#信息熵的计算
        sum_1=0
        sum_0=0 #统计标签数
        for i in range(0,len(data)):
            if(data[i][2]==0):
                sum_0+=1
            else:
                sum_1+=1
        ##统计概率
        p_1=sum_1/(sum_1+sum_0)
        p_0=sum_0/(sum_0+sum_1)
        ##计算熵
        if p_1==1 or p_0==1:
            ent=0  #熵为0 令算，不要走对数
        else:
            ent=-p_1*math.log2(p_1)-p_0*math.log2(p_0)
        return ent,sum_1,sum_0
    
    def compute_IGR(self,attribute,node:Node,no_attribute):#计算属性的信息增益率
        #先建立个属性取值字典，key是该属性的具体取值，value是[0,0，0]该取值的总数，和该取值下，0和1的个体数
        ##感觉可以一起求，少遍历
        #初始化完成
        data=node.data
        cur_ent=node.ent
        best_IGR=-1000 #最好的信息增益率
        best_attri=-1
        dict=[{},{},{},{},{}]#空一个便于索引
        for i in range(0,len(attribute)):
            if i==2 :continue
            for j in attribute[i]:
                dict[i][j]=[0,0,0]
        ##遍历数据，整理数据
        for data_singel in data:
            for i in range(0,5):
                if i==2:continue
                dict[i][data_singel[i]][0]+=1
                if data_singel[2]==0:#分类标签为0
                    dict[i][data_singel[i]][1]+=1
                else:
                    dict[i][data_singel[i]][2]+=1
        ##算每个属性的信息增益率
        for i in range(0,len(dict)):
            if i==2 or i in no_attribute:continue
            dict_index=dict[i]
            count_ent=0
            IV=0
            #先算信息增益
            sum=len(data) #数据总数
            for key,item in dict_index.items(): #属性下的单类别
                ##要是标签全部一致，熵为0，不要用对数会有对数错误
                p=item[0]/sum  ##这里还有点问题，万一人家没有这个分类，但是下面解决了，这个分类里面要是没有样本，就选父节点最多的标签
                if item[1]==0 or item[2]==0:
                    d_v_ent=0
                else:
                    p_0=item[1]/item[0]
                    p_1=item[2]/item[0] 
                    d_v_ent=-p_0*math.log2(p_0)-p_1*math.log2(p_1)
                count_ent+=(p*d_v_ent)
                d_v_IV=p*math.log2(p)
                IV-=d_v_IV
            Gain=cur_ent-count_ent
            IGR=Gain/IV
            if(IGR>=best_IGR):
                best_IGR=IGR
                best_attri=i
        node.sort=best_attri
        return best_attri
    def Pre_pruning(self,a_sort:dict,train_most,a_best):
        #找到当前训练集中最多的标签，对测试集做一个初始化的正确率
        init_accuracy=0
        ##判断分支后的正确率是否提升
        ##先判断每个分支给的标签（每个分支中最大的标为分支的标签）
        up_accuracy=0
        dict_test={}
        for key,item in a_sort.items():
            sum1=0
            sum0=0
            for data_index in item:
                if data_index[2]==0:
                    sum0+=1
                else:sum1+=1
            flag=1 if sum1>sum0 else 0
            dict_test[key]=flag
        ##判断分支后的正确率  但是要和前面的全部特征一起看--未解决
        #可以正确率提升一次就把测试集也分一次类，后续过来就不用回溯了
        for data_single in self.data_test:
            if data_single[2]==train_most:
                 init_accuracy+=1
            if data_single[2]==dict_test[data_single[a_best]]:
                up_accuracy+=1 
        if up_accuracy>init_accuracy:
            return 0
        else: return 1   
    def Tree_Generate (self,data,attribute,value,no_attribute):
        node=Node(value,data)
        #当层信息熵计算
        node.ent,sum_1,sum_0=self.Ent(data)
        #终止条件1:如果data中的数据全部属于同一类别，那直接标记为C类叶子节点
        #终止条件2:data在所有属性上取值相同
        flag1=data[0][2] #兼职代表
        flag2=data[0]
        flag=1
        for i in range(1,len(data)):
            if data[i][2]!=flag1:
                flag1=data[i][2]
            for j in range(0,5):#判断属性是否从一而终
                if(flag2[j]!=data[i][j] and j!=2):
                    flag=0
            if(flag1!=data[0][2] and flag==0):
                    break
        if(flag1==data[0][2]):##从头到尾的标签都一样，return为叶子节点
            node.leave=flag1
            return node
        if(flag==1):##是否所有属性全部相同
            node.leave=1 if sum_1>sum_0 else 0
            return node
        ##挑选最佳分类属性
        a_best=self.compute_IGR(attribute,node,no_attribute) #返回分类属性的索引
        ##按照最佳属性分支
        #先把data分好
        a_sort={} #键为取值，value为样本
        #初始化
        for atrri in attribute[a_best]:
            a_sort[atrri]=[]
        #分数据
        for data_index in data:
            a_sort[data_index[a_best]].append(data_index)
        ##是否剪枝
        #分支
        for atrri in attribute[a_best]:
            d_v=a_sort[atrri]
            if(len(d_v)==0):
                child_node=Node(0,data)
                child_node.leave=1 if sum_1>sum_0 else 0
                node.children.append(child_node)
            else:
                ##要是attribute的子集，但是前面都直接拿它当索引了
                no_attribute.append(a_best)
                child_node=self.Tree_Generate(d_v,attribute,atrri,no_attribute)
                node.children.append(child_node)
                no_attribute.remove(a_best) #这是递归式的
        return node 
    def find(self,node:Node,data_index):
        if(node.leave!=-1):
            return node.leave
        a_best=node.sort
        for next_node in node.children:
            if(next_node.value==data_index[a_best]):
                return self.find(next_node,data_index)
    def test(self):
        sum=0
        for i in range(400,600):
           data_index=self.data_all[i]
           test_node=self.head
           test_label=self.find(test_node,data_index)
           if data_index[2]==test_label:
               sum+=1
        print("正确率",sum/200)          
d_tree=D_Tree("./DT_data.csv")
d_tree.test()