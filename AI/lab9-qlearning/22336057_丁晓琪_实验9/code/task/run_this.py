"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the main part which controls the update method of this example.
"""

from maze_env import Maze
from RL_q_learning import QLearning
from RL_sarsa import Sarsa


def update():
    for episode in range(100):
        # initial observation
        observation = env.reset()
        if episode%10==0:
            RL.epsilon-=0.02
        if episode>90:
            RL.epsilon=0.05
        if(100-episode<10):
                print(episode," time:")
        while True:
            # fresh env
            '''Renders policy once on environment. Watch your agent play!'''
            env.render()  #更新上一次的动作
        
            '''
            RL choose action based on observation
            e.g: action = RL.choose_action(str(observation))
            '''
            # YOUR IMPLEMENTATION HERE #
            state=[0,0]
            s = env.canvas.coords(env.rect)
            state[0]=int((s[1]-5)//40)
            state[1]=int((s[0]-5)//40)
            if(100-episode<10):
                print("now:",state[0],state[1])
            action = RL.choose_action(state)

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            '''
            RL learn from this transition
            e.g: RL.learn(str(observation), action, reward, str(observation_), is_lambda=True)
                 RL.learn(str(observation), action, reward, str(observation_), is_lambda_return=True)
            '''
            #学习，更新表格
            ############
            # YOUR IMPLEMENTATION HERE #
            state_=[0,0]
            s = env.canvas.coords(env.rect)
            state_[0]=int((s[1]-5)//40)
            state_[1]=int((s[0]-5)//40 )
            RL.learn(state, action, reward, state_)                 

            observation = observation_
            if(state_[0]==2 and state_[1]==2):
                print("goal!")
            # break while loop when end of this episode
            if done:
                break

    # end of game
    print('game over')
    env.destroy()


if __name__ == "__main__":
    env = Maze()

    '''
    build RL Class
    RL = QLearning(actions=list(range(env.n_actions)))
    RL = Sarsa(actions=list(range(env.n_actions)))
    '''
    # YOUR IMPLEMENTATION HERE #
    RL = QLearning(actions=list(range(env.n_actions)))
    #RL = Sarsa(actions=list(range(env.n_actions)))
    print( RL.q_table)
    env.after(100, update)
    env.mainloop()

