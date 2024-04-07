import copy
from ChessBoard import *


class Evaluate(object):
    # 棋子棋力得分
    single_chess_point = {
        'c': 989,   # 车
        'm': 439,   # 马
        'p': 442,   # 炮
        's': 226,   # 士
        'x': 210,   # 象
        'z': 55,    # 卒
        'j': 65536  # 将
    }
    # 红兵（卒）位置得分
    red_bin_pos_point = [
        [1, 3, 9, 10, 12, 10, 9, 3, 1],
        [18, 36, 56, 95, 118, 95, 56, 36, 18],
        [15, 28, 42, 73, 80, 73, 42, 28, 15],
        [13, 22, 30, 42, 52, 42, 30, 22, 13],
        [8, 17, 18, 21, 26, 21, 18, 17, 8],
        [3, 0, 7, 0, 8, 0, 7, 0, 3],
        [-1, 0, -3, 0, 3, 0, -3, 0, -1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # 红车位置得分
    red_che_pos_point = [
        [185, 195, 190, 210, 220, 210, 190, 195, 185],
        [185, 203, 198, 230, 245, 230, 198, 203, 185],
        [180, 198, 190, 215, 225, 215, 190, 198, 180],
        [180, 200, 195, 220, 230, 220, 195, 200, 180],
        [180, 190, 180, 205, 225, 205, 180, 190, 180],
        [155, 185, 172, 215, 215, 215, 172, 185, 155],
        [110, 148, 135, 185, 190, 185, 135, 148, 110],
        [100, 115, 105, 140, 135, 140, 105, 115, 110],
        [115, 95, 100, 155, 115, 155, 100, 95, 115],
        [20, 120, 105, 140, 115, 150, 105, 120, 20]
    ]
    # 红马位置得分
    red_ma_pos_point = [
        [80, 105, 135, 120, 80, 120, 135, 105, 80],
        [80, 115, 200, 135, 105, 135, 200, 115, 80],
        [120, 125, 135, 150, 145, 150, 135, 125, 120],
        [105, 175, 145, 175, 150, 175, 145, 175, 105],
        [90, 135, 125, 145, 135, 145, 125, 135, 90],
        [80, 120, 135, 125, 120, 125, 135, 120, 80],
        [45, 90, 105, 190, 110, 90, 105, 90, 45],
        [80, 45, 105, 105, 80, 105, 105, 45, 80],
        [20, 45, 80, 80, -10, 80, 80, 45, 20],
        [20, -20, 20, 20, 20, 20, 20, -20, 20]
    ]
    # 红炮位置得分
    red_pao_pos_point = [
        [190, 180, 190, 70, 10, 70, 190, 180, 190],
        [70, 120, 100, 90, 150, 90, 100, 120, 70],
        [70, 90, 80, 90, 200, 90, 80, 90, 70],
        [60, 80, 60, 50, 210, 50, 60, 80, 60],
        [90, 50, 90, 70, 220, 70, 90, 50, 90],
        [120, 70, 100, 60, 230, 60, 100, 70, 120],
        [10, 30, 10, 30, 120, 30, 10, 30, 10],
        [30, -20, 30, 20, 200, 20, 30, -20, 30],
        [30, 10, 30, 30, -10, 30, 30, 10, 30],
        [20, 20, 20, 20, -10, 20, 20, 20, 20]
    ]
    # 红将位置得分
    red_jiang_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9750, 9800, 9750, 0, 0, 0],
        [0, 0, 0, 9900, 9900, 9900, 0, 0, 0],
        [0, 0, 0, 10000, 10000, 10000, 0, 0, 0],
    ]
    # 红相或士位置得分
    red_xiang_shi_pos_point = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 60, 0, 0, 0, 60, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [80, 0, 0, 80, 90, 80, 0, 0, 80],
        [0, 0, 0, 0, 0, 120, 0, 0, 0],
        [0, 0, 70, 100, 0, 100, 70, 0, 0],
    ]

    red_pos_point = {
        'z': red_bin_pos_point,
        'm': red_ma_pos_point,
        'c': red_che_pos_point,
        'j': red_jiang_pos_point,
        'p': red_pao_pos_point,
        'x': red_xiang_shi_pos_point,
        's': red_xiang_shi_pos_point
    }

    def __init__(self, team):
        self.team = team

    def get_single_chess_point(self, chess: Chess):
        if chess.team == self.team:
            return self.single_chess_point[chess.name]
        else:
            return -1 * self.single_chess_point[chess.name]

    def get_chess_pos_point(self, chess: Chess):
        red_pos_point_table = self.red_pos_point[chess.name]
        if chess.team == 'r':
            pos_point = red_pos_point_table[chess.row][chess.col]
        else:
            pos_point = red_pos_point_table[9 - chess.row][chess.col]
        if chess.team != self.team:
            pos_point *= -1
        return pos_point

    def evaluate(self, chessboard: ChessBoard):
        point = 0
        for chess in chessboard.get_chess():
            point += self.get_single_chess_point(chess)
            point += self.get_chess_pos_point(chess)
        return point


class ChessMap(object):
    def __init__(self, chessboard: ChessBoard):
        self.chess_map = copy.deepcopy(chessboard.chessboard_map)


class ChessAI(object):
    def __init__(self, computer_team):
        self.team = computer_team
        self.evaluate_class = Evaluate(self.team)

            #beta剪枝#返回的是当下这一步的下一步能得到的最小价值#而且要更新aplha，beta值，返回v就是在更新了
    def Min_Value(self,chessboard:ChessBoard,alpha,beta,step):
        # for item in chessboard.chessboard_map:
        #     print(item)
        #要判断是否为最终状态和棋或者输赢#要返回什么直接返回当前状态
        if step==3:
            return  self.evaluate_class.evaluate(chessboard)
        #给v赋值，极大
        v=float('inf')
        chess_list=chessboard.get_chess()
        #得到棋盘里面的所有棋子对象，但是只要自己队伍的
        for chess in chess_list:
             if chess!=None and chess.team==self.team:
                #得到可以下的位置列表
                put_down=chessboard.get_put_down_position(chess)
                #要深度copy一个类对象传下去，不能在原对象的基础上改变
                #或者改变后恢复原状
                ##注意注意next位置上可能有对方可以吃掉的棋子，传下去的时候，可以直接把对方棋子吃掉，但是恢复时要把它恢复回来
                cur_row=chess.row
                cur_col=chess.col
                for next_row,next_col in put_down:
                    chess.row=next_row
                    chess.col=next_col
                    chess_tm=chessboard.chessboard_map[next_row][next_col]#保存对方状态
                    #要更新到chess-boardmap中，先是在list中更新了，但是没有通知get_put_down_position里面的board_map
                    #不能用那个map类，无法深度copy渲染的类型
                    chessboard.chessboard_map[cur_row][cur_col]=None
                    chessboard.chessboard_map[next_row][next_col]=chess
                   
                    v=min(v,self.Max_Value(chessboard,alpha,beta,step+1))
                    #恢复
                    chess.row=cur_row
                    chess.col=cur_col
                    chessboard.chessboard_map[cur_row][cur_col]=chess
                    chessboard.chessboard_map[next_row][next_col]=chess_tm
                    #判断是否剪枝
                    if v<=alpha: return v
                    #更新alpha值
                    beta=min(beta,v)
        return v
    
    #alpha剪枝#返回的是当下这一步的下一步能得到的最大价值#而且要更新aplha，beta值，返回v就是在更新了
    def Max_Value(self,chessboard:ChessBoard,alpha,beta,step):
        #要判断是否为最终状态和棋或者输赢#要返回什么直接返回当前状态
        if step==3:
            return  self.evaluate_class.evaluate(chessboard)
        #给v赋值，极小
        v=float('-inf')
        #得到棋盘里面的所有棋子对象，但是只要自己队伍的
        chess_list=chessboard.get_chess()
        for chess in chess_list:
            if chess and chess.team==self.team:
                #得到可以下的位置列表
                put_down=chessboard.get_put_down_position(chess)
                #要深度copy一个类对象传下去，不能在原对象的基础上改变
                #或者改变后恢复原状
                cur_row=chess.row
                cur_col=chess.col
                for next_row,next_col in put_down:
                    chess.row=next_row
                    chess.col=next_col
                    chess_tm=chessboard.chessboard_map[next_row][next_col]#保存对方状态
                    #要更新到chess-boardmap中，先是在list中更新了，但是没有通知get_put_down_position里面的board_map
                    chessboard.chessboard_map[cur_row][cur_col]=None
                    chessboard.chessboard_map[next_row][next_col]=chess
                    v=max(v,self.Min_Value(chessboard,alpha,beta,step+1))
                    #恢复
                    chess.row=cur_row
                    chess.col=cur_col                    
                    chessboard.chessboard_map[cur_row][cur_col]=chess
                    chessboard.chessboard_map[next_row][next_col]=chess_tm  #不用改对方棋子的数据，直接恢复
                    #判断是否剪枝
                    if step==0 and v>alpha:
                        self.cur_col=cur_col
                        self.cur_row=cur_row
                        self.new_row=next_row
                        self.new_col=next_col
                    alpha=max(alpha,v)
                    if v>=beta: return v
                    #更新alpha值
                    
        return v
    
    def get_next_step(self, chessboard: ChessBoard):    #aplha beta剪枝
        #得到返回一个元组# cur_row, cur_col, nxt_row, nxt_col
        #调用alpha_beta剪枝，返回的是value，要遍历找到value对应的操作
        alpha=float('-inf')
        beta=float('inf')
        v=self.Max_Value(chessboard,alpha,beta,0)
        #得到v对应的动作
        # for chess in chessboard.get_chess():
        #      if chess and chess.team==self.team:
        #         #得到可以下的位置列表
        #         put_down=chessboard.get_put_down_position(chess)
        #         #要深度copy一个类对象传下去，不能在原对象的基础上改变
        #         #或者改变后恢复原状
        #         cur_row=chess.row
        #         cur_col=chess.col
        #         #防止下面异常
        #         if len(put_down)==0: continue
        #         for next_row,next_col in put_down:
        #             chess.row=next_row
        #             chess.col=next_col
        #             v_cmp=self.evaluate_class.evaluate(chessboard)
        #             #恢复
        #             chess.row=cur_row
        #             chess.col=cur_col
        #             if v_cmp==v: break                    
        #         if v_cmp==v: break#这里有问题，不要跟上面那个if一个等级不然v_cmp没定义
        return(self.cur_row,self.cur_col,self.new_row,self.new_col)
