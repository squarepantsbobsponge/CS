import argparse
import gym
from argument import dqn_arguments, pg_arguments


def parse():
    parser = argparse.ArgumentParser(description="SYSU_RL_HW2")#命令行解析参数
    parser.add_argument('--train_pg', default=False, type=bool, help='whether train policy gradient') #是否训练policy gradient
    parser.add_argument('--train_dqn', default=True, type=bool, help='whether train DQN')#是否训练DQN  #训DQN，打开DQN

    parser = dqn_arguments(parser)
    # parser = pg_arguments(parser)#引用了策略梯度网络的参数
    args = parser.parse_args() #解析参数，现在可以通过arg.learning_rate类型来访问了
    return args


def run(args):
    if args.train_pg:
        env_name = args.env_name
        env = gym.make(env_name) #已经搭建选择了环境
        from agent_dir.agent_pg import AgentPG
        agent = AgentPG(env, args)
        agent.run()

    if args.train_dqn:
        env_name = args.env_name
        env = gym.make(env_name)
        from agent_dir.agent_dqn import AgentDQN
        agent = AgentDQN(env, args)
        agent.run()


if __name__ == '__main__':
    args = parse()
    run(args)
