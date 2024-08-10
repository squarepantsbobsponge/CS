
import numpy as np
import pandas as pd


class Sarsa:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.3):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy  #随机选择动作的概率
        #加个回溯惩罚
        self.last_action=-3
        ''' build q table'''
        # YOUR IMPLEMENTATION HERE #
        #表格存储16个状态s在4个a的状态下的Q（s,a），用二维数组存储，行为0-15（i+j），列为0-3对应a
        #全部初始化为0
        self.q_table=np.zeros((16,len(self.actions)))

    def get_s_(self,state,action):
        if action==0: #向上
            state[0]-=1
        elif action==1: #向下
            state[0]+=1
        elif action==2: #右
            state[1]+=1
        elif action==3: #左
            state[1]-=1
        
    def choose_action(self, observation):
        ''' choose action from q table '''
        # 1.解锁状态（当前位置）observation为当前的位置像素 有四个#这个放在主函数解
            #行：左上角x坐标/一个方格像素值 #修改放在主函数解
        i=observation[0] 
            #列： 左上角y坐标/一个方格像素值
        j=observation[1]
            #在q_table中的位置
        s=i*4+j
        state_=[i,j]
        # YOUR IMPLEMENTATION HERE #
        # 2.生成随机数概率与epsilon比较
        action=0
        p=np.random.rand()
        # 3.在0-0.1范围内，随机选择  #这里选择动作要看动作后的状态是否存在
        if(p<=self.epsilon):
            action = np.random.randint(0, len(self.actions)) 
            self.get_s_(state_,action)
            while(self.check_state_exist(state_)==0): #越界重新生成
                state_=[i,j]#复原状态
                action = np.random.randint(0, len(self.actions)) 
                self.get_s_(state_,action)
            self.last_action=action
            return action
        # 4.选择Q值最大的动作
        else:
            #坚持越界行为，越界重新生成
            q_s_a=np.copy(self.q_table[s])  #深拷贝不要破环q_table
            if(self.last_action!=-3):
                if(self.last_action<=1 ):
                    q_s_a[1-self.last_action]-=0.005
                else:
                    q_s_a[5-self.last_action]-=0.005
            
            max_arr=[]
            max=np.amax(q_s_a)
            for index in range(0,len(q_s_a)):
                if(q_s_a[index]==max):
                    max_arr.append(index)
            ran= np.random.randint(0, len(max_arr))
            action=max_arr[ran] 

            self.get_s_(state_,action)
            while(self.check_state_exist(state_)==0): #越界重新生成
                state_=[i,j]
                q_s_a[action]=-10000 #失去竞选资格
                max_arr=[]
                max=np.amax(q_s_a)
                for index in range(0,len(q_s_a)):
                    if(q_s_a[index]==max):
                        max_arr.append(index)
                ran= np.random.randint(0, len(max_arr))
                action=max_arr[ran] 
                self.get_s_(state_,action) 
            self.last_action=action                   
            return action

    def learn(self, s, a, r, s_):
        ''' update q table ''' #s：当前状态的像素坐标，a：动作，r：a动作后的实际奖励 s_:a动作后的像素坐标
        # YOUR IMPLEMENTATION HERE #
        state=s[0]*4+s[1]
        Q_s_a=self.q_table[state][a]
        state_new=s_[0]*4+s_[1]
        #也需要用eplision来选择S_时的q
        p=np.random.rand()
        if p>0.1:       
            Q_s_a_newmax=np.amax(self.q_table[state_new])
        else:
            action = np.random.randint(0, len(self.actions)) 
            Q_s_a_newmax=self.q_table[state_new][action]            
        #更新q_table
        self.q_table[state][a]=Q_s_a+self.lr*(r+self.gamma*Q_s_a_newmax-Q_s_a)
        #print("now:",s,"  q_s_a:",self.q_table[state])

    def check_state_exist(self, state): #假设传进来的是真实坐标，不是像素
        ''' check state '''
        # YOUR IMPLEMENTATION HERE #
        #越界不存在了
        if state[0]<0 or state[0]>=4 or state[1]<0 or state[1]>=4:
            return 0
        else:
            return 1