import os
import random
import copy
import numpy as np
import torch
from pathlib import Path
from tensorboardX import SummaryWriter
from torch import nn, optim
from agent_dir.agent import Agent
from gym.utils import seeding
import matplotlib.pyplot as plt
def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class QNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(QNetwork, self).__init__()  #先设置一个输入为4，输出为60的隐藏层，两层神经网络
        # YOUR CODE HERE #
        self.hide=nn.Linear(input_size,hidden_size) #有四个状态值
        self.relu=nn.ReLU()  #这个是必要的
        self.hide2=nn.Linear(hidden_size,hidden_size)
        self.relu2=nn.ReLU()
        self.out=nn.Linear(hidden_size,output_size)  #有两个动作（0，1）


    def forward(self, inputs):
        # YOUR CODE HERE #
        x=self.relu(self.hide(inputs))
        #x=self.hide(inputs)
        x=self.relu2(x)
        output=self.out(x)
        return output


class ReplayBuffer:
    def __init__(self, buffer_size):
        # YOUR CODE HERE #
        self.buffer_size=buffer_size
        self.displace=0 #经验回放池满了后从哪里置换新的经验
        self.buffer=[]  
        

    def __len__(self):
        return len(self.buffer)

    def push(self, transition):  #经验样本的格式（s_t,a_t,r_t,s_(t+1)）
        # YOUR CODE HERE #
        #trasition是可变参数，可以直接push，但是push内容是元组形式
        if(len(self.buffer)<self.buffer_size):
            self.buffer.append(transition)
            self.displace+=1
        else:
            self.displace=self.displace%(self.buffer_size)
            self.buffer[self.displace]=transition
            self.displace+=1

    def sample(self, batch_size):#随机取样
        # YOUR CODE HERE #
        sample=random.sample(self.buffer,batch_size)
        state,action,reward,next_state,done=zip(*sample)
        return state,action,reward,next_state,done

    def clean(self):
        # YOUR CODE HERE #
        self.buffer.clear()
        self.displace=0
        self.buffer_size=0

class AgentDQN(Agent):
    def __init__(self, env, args):
        """
        Initialize every things you need here.
        For example: building your model
        """
        self.env=env
        self.args=args##这里有学习率和损失因子 还有批次的大小
        seed_everything(self.args.seed)
        self.seed = self.args.seed
        self.np_random, seed = seeding.np_random(self.seed)
        self.env.seed(seed) #环境也要设置随机种子
        super(AgentDQN, self).__init__(env)
         ##设置随机种子

        # YOUR CODE HERE #
        #设置好网络，一个训练，一个target
        self.DQN=QNetwork(4,250,2)  
        self.TargetDQN=QNetwork(4,250,2)
        #self.TargetDQN.load_state_dict(self.DQN.state_dict()) #网络结构和参数一致
        ##网络训练所需
        self.loss_fn=nn.MSELoss(reduce=True, size_average=False) #平方和误差#要是标量
        self.optimizer=optim.Adam(self.DQN.parameters(),lr=0.0005)
        #建立经验回放池
        self.ReplayBuffer=ReplayBuffer(10000)
        #训练回合数和训练回合中最大步数
        self.train_round=120
        self.max_step=200
        #损失因子
        self.gamma=self.args.gamma
        self.e_greedy=0.15
    
    def init_game_setting(self):
        """

        Testing function will call this function at the begining of new game
        Put anything you want to initialize if necessary

        """
        # YOUR CODE HERE #
        self.env.reset() #重启

    def train(self):
        """
        Implement your training algorithm here
        """
        # YOUR CODE HERE #
        count=0
        means=[] #平均reward    
        stds=[] #平均方差
        for m in range(0,5):
            self.seed+=66 #随机种子改变
            seed_everything(self.args.seed)
            self.np_random, seed = seeding.np_random(self.seed)
            self.env.seed(seed) #环境也要设置随机种子
            self.DQN=QNetwork(4,250,2)  
            self.TargetDQN=QNetwork(4,250,2)
            #self.TargetDQN.load_state_dict(self.DQN.state_dict()) #网络结构和参数一致
            ##网络训练所需
            self.loss_fn=nn.MSELoss(reduce=True, size_average=False) #平方和误差#要是标量
            self.optimizer=optim.Adam(self.DQN.parameters(),lr=0.0005)
            self.ReplayBuffer=ReplayBuffer(10000)
            mean=[]
            std=[]
            for i in range(0,self.train_round): #训练回合数
                state=self.env.reset() #初始状态
                t=0
                done=False
                count=0
                roll_reward=[]
                while t<self.max_step and done==False: #每个回合最大步数
                    #print(t)
                    #将状态输入到DQN，得到最大的a
                    t+=1
                    state_=torch.Tensor(state)
                    output=self.DQN(state_)
                    #贪心策略选动作
                    random_e = np.random.random()
                    if(random_e>self.e_greedy):
                        action= torch.argmax(output).item() #Q值最大的索引为动作
                    else:
                        action=np.random.randint(2) 
                    next_state,reward,done,info=self.env.step(action) 

                    count+=reward
                    if(done==True):
                        
                        reward=-10 #修改reward，达到优化
                    sample=[state,action,reward,next_state,done]
                    self.ReplayBuffer.push(sample) #加入采样池
                    state=next_state
                    ##需要采样池到达一定数量才能训练，每次抽三个批次
                    if len(self.ReplayBuffer)>=64:
                        for j in range(0,5):
                            train_state,train_action,train_reward,train_next_state,train_done=self.ReplayBuffer.sample(64)
                            states_tensor = torch.tensor(train_state, dtype=torch.float)
                            actions_tensor = torch.tensor(train_action).view(-1,1)
                            rewards_tensor = torch.tensor(train_reward, dtype=torch.float).view(-1,1)
                            next_states_tensor = torch.tensor(train_next_state, dtype=torch.float)
                            dones_tensor = torch.tensor(train_done, dtype=torch.float).view(-1,1)
                            q_values = self.DQN(states_tensor).gather(1, actions_tensor)  # [b,1] 收集当前动作Q值
                            ##改用DDQN
                            next_q_values=self.DQN(next_states_tensor)
                            #print(next_q_values.size())
                            next_action = torch.argmax(next_q_values,dim=1)#主网络找下一个状态动作
                            next_action = torch.tensor(next_action).view(-1,1)
                            #print(next_action.size())

                            #max_next_q_values = self.TargetDQN(next_states_tensor).max(1)[0].view(-1,1)
                            max_next_q_values = self.TargetDQN(next_states_tensor).gather(1,next_action) #目标网络收下一个状态的Q值
                            q_targets = rewards_tensor + self.gamma * max_next_q_values * (1 - dones_tensor)
 
                            # 目标网络和训练网络之间的均方误差损失
                            dqn_loss = torch.mean(torch.nn.functional.mse_loss(q_values, q_targets)) #b不知道为啥用上面定义好的MSE有bug
                            # if(t%20==0 and j%5==0):
                            #     print(i,dqn_loss)
                            # PyTorch中默认梯度会累积,这里需要显式将梯度置为0
                            self.optimizer.zero_grad()
                            dqn_loss.backward()
                            self.optimizer.step()

                    if(t%4==0):
                     self.TargetDQN.load_state_dict(self.DQN.state_dict())      
                    #print(len(self.ReplayBuffer))
                roll_reward.append(count) #记录下回报    
                mean.append(np.mean(roll_reward))
                std.append(np.std(roll_reward))
                print(i,count)
            print("mean:",mean)
            print("std:",std)
            self.ReplayBuffer.clean()
            means.append(mean)
            stds.append(std)
        ##存储数据
        print("means:",means)
        print("stds:",std)
        d={"mean":means,"std":stds}
        self.print_train(d)
    
    def print_train(self,d):
        means = d["mean"]
        stds = d["std"]

        # 计算迭代次数
        iterations = len(means[0])        
        # 计算平均值和标准差
        mean_values = np.mean(means, axis=0)
        std_values = np.std(means, axis=0)

    # 绘制曲线和阴影区域
        x = range(iterations)
        print("mean_values:",mean_values)
        plt.plot(x, mean_values, label="Mean", color="blue")
        print("std_values:",std_values)
        plt.fill_between(x, mean_values - std_values, mean_values + std_values, alpha=0.3, color="blue")

        plt.xlabel("Iterations")
        plt.ylabel("Mean Return")
        plt.legend()
        plt.title("Training Curve with Shadow")
        plt.show()     

    def test_update(self,initial_params,trained_params):
        # params_updated = False
        # for name, initial_param in initial_params.items():
        #     trained_param = trained_params[name]
        #     if not torch.equal(initial_param, trained_param):
        #         params_updated = True
        #         break
        # if params_updated:
        #     print("参数已更新")
        # else:
        #      print("参数未更新")
        for name, param in self.DQN.named_parameters():
            if param.grad is None:
                print(name, param.grad_fn)
            else:
                print(param.grad)


    def make_action(self, observation, test=True): #在训练完后不再用e_greedy策略
        """
        Return predicted action of your agent
        Input:observation
        Return:action
        """
        # YOUR CODE HERE #
        observation=torch.Tensor(observation)
        output=self.DQN(observation)
        action= torch.argmax(output).item()
        return action

    def run(self):

        """
        Implement the interaction between agent and environment here
        """
        # YOUR CODE HERE #
        #训练
        self.train()
        print("running")
        for i in range(0,20):
            observation=self.env.reset()
            count=0
            done=False
            while(done==False):
                action=self.make_action(observation)
                state,reward,done,info=self.env.step(action)
                observation=state
                count+=reward
            print("game over! reward=",count)
        
