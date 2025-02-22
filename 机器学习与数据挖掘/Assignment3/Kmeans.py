import numpy as np
# matrix_a = np.zeros((4,1))
# matrix_a[0][0]=1
# matrix_a[1][0]=2
# matrix_a[2][0]=3
# matrix_b = np.ones((4,3))
# matrix_product = np.dot(matrix_a, matrix_b)
# print("矩阵乘积结果:\n", matrix_product)

# 定义列向量 v 和矩阵 A
v = np.array([[1], [2], [3]])  # 列向量形状为 (3, 1)
A = np.array([[4, 5], [6, 7], [8, 9]])  # 矩阵形状为 (3, 2)
 
# 进行点积运算
result = v*A
 
print("列向量 v:")
print(v)
print("矩阵 A:")
print(A)
print("结果:")
print(result)