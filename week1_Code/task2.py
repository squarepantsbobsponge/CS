import copy
def MatrixAdd(A,B):
    AA=copy.deepcopy(A)
    BB=copy.deepcopy(B)#拷贝副本，不打乱AB中的数据
    n=len(A)
    '''
    c=n*[None]
    C=n*[c]
    这样会导致矩阵的所有行指向一个引用
    '''
    C = [[0] * n for _ in range(n)]  # 使用列表生成式来初始化结果矩阵C
    for i in range(0,n):
        for j in range(0,n):
            C[i][j]=AA[i][j]+BB[i][j]
    return C
def MatrixMul(A,B):
    AA=copy.deepcopy(A)
    BB=copy.deepcopy(B)#拷贝副本，不打乱AB中的数据
    n=len(A)
    C = [[0] * n for _ in range(n)]  # 使用列表生成式来初始化结果矩阵C
    for i in range(0,n):
        for j in range(0,n):
            for w in range(0,n):
                C[i][j]=AA[i][w]*BB[w][j]+int(C[i][j])
    return C
A=[[1,1,1],[1,1,1],[1,1,1]]
B=[[2,2,2],[2,2,2],[2,2,2]]
print(MatrixAdd(A,B))
print(MatrixMul(A,B))

