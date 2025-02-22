from PIL import Image  
import numpy as np
import matplotlib.pyplot as plt
import cmath

# #一维快速傅里叶变化
# def ODFFT(matrix,M,yy,x_or_y):
#     #x为一维傅里叶变化的对象
#     #y固定,此时matrix为二维的，需要指定y对哪一行傅里叶变化
#     # u是变量F(u)，需要将一次性u=0-M的傅里叶变换算出来，这样才能减少复杂度
#     result=[0]*M
#     K=M/2
#     if(x_or_y==1):
#         for u in range(0,K):
#             F_even=0
#             F_odd=0
#             for x in range(0,K):
#                 W_K=cmath.exp(complex(0,(-2*cmath.pi*u*x)/K))
#                 F_even+=matrix[2*x][yy]*W_K
#                 F_odd+=matrix[2*x+1][yy]*W_K
#             W_2K=cmath.exp(complex(0,(-cmath.pi*u)/K))
#             result[u]=F_even+F_odd*W_2K
#             result[u+K]=F_even-F_odd*W_2K
#     #y为一维傅里叶变化的对象
#     #matrix为一维，已经完成了x上的傅里叶变化
#     # v为变量
#     else:
#         for v in range(0,K):
#             F_even=0
#             F_odd=0
#             for y in range(0,K):
#                 W_K=cmath.exp(complex(0,(-2*cmath.pi*v*y)/K))
#                 F_even+=matrix[2*y]*W_K
#                 F_odd+=matrix[2*y+1]*W_K
#             W_2K=cmath.exp(complex(0,(-cmath.pi*v)/K))
#             result[v]=F_even+F_odd*W_2K
#             result[v+K]=F_even-F_odd*W_2K
#     return result


# #是要递归实现
# #二维快速傅里叶变化 u，v的取值范围是0-M,x，y的取值范围也是0-M,图像尺寸都为M
# def TDFFT(matrix,M):
#     #最后的频谱
#     F_matrix = []
#     #对内层的x做一维傅里叶变换
#     matrix_y=[]#横轴是u，纵轴是y
#     for y in range(0,M):
#         matrix_y.append(ODFFT(matrix,M,y,1))
#     #转置一下，横轴是y，纵轴是u
#     transposed_matrix_y= [[row[i] for row in matrix] for i in range(len(matrix[0]))]
#     #计算最终结果
#     for u in range(0,M):
#         F_matrix.append(ODFFT(transposed_matrix_y[u],M,0,0))
#     ## F_matrix还是反过来,纵轴为u，横轴为v
#     return F_matrix
 
if __name__=="__main__":
    image=Image.open('./c.jpg')
    gray_matrix=np.array(image)
    fft_result = np.fft.fft2(gray_matrix)
    ifft_result = np.fft.ifft2(fft_result)
    ifft_result=np.real(ifft_result)
    plt.figure(figsize=(8, 8))  # 设置图像大小（可选）
    plt.imshow(ifft_result, cmap='gray')  # 使用灰度颜色映射
    plt.title('Grayscale Image')  # 设置图像标题（可选）
    plt.axis('off')  # 关闭坐标轴（可选）
    plt.show()  # 显示图像



def dft(x):
    x = np.asarray(x, dtype=float)                                  # 将输入的x转换为浮点数
    N = x.shape[0]                                                  # 输出x的形状(1024,)中的第一个位置1024
    n = np.arange(N)                                                # 输出数组[0, 1, 2, ..., 1023]
    k = n.reshape((N, 1))                                           # 将1行1024列转换为1024行1列
    M = np.exp(-2j * np.pi * k * n / N)                             # 二维数组（复数形式表示）（相当于坐标轴）
    return np.dot(M, x)                                             # 返回二维数组与x的点成

#一维FFT：递归实现
def OFFT(matrix):
    M=len(matrix)
    if M<=2:
        return dft(matrix)
    F_even=OFFT(matrix[0::2]) #获得偶数索引
    F_odd=OFFT(matrix[1::2])

    result=np.zeros(M,dtype=complex)
    for u in range(M//2):
        W_2k=np.exp(-2j*np.pi*u/M)
        result[u]=F_even[u]+W_2k*F_odd[u]
        result[u+M//2]=F_even[u]-W_2k*F_odd[u]
    return result


def idft(x):
    x = np.asarray(x, dtype=float)                                  # 将输入的x转换为浮点数
    N = x.shape[0]                                                  # 输出x的形状(1024,)中的第一个位置1024
    n = np.arange(N)                                                # 输出数组[0, 1, 2, ..., 1023]
    k = n.reshape((N, 1))                                           # 将1行1024列转换为1024行1列
    M = np.exp(2j * np.pi * k * n / N)                             # 二维数组（复数形式表示）（相当于坐标轴）
    return np.dot(M, x) 


#一维IFFT逆变换：递归实现
def OIFFT(matrix):
    M=len(matrix)
    if M<=2:
        return idft(matrix)
    
    F_even=OIFFT(matrix[0::2]) #获得偶数索引
    F_odd=OIFFT(matrix[1::2])

    result=np.zeros(M,dtype=complex)
    for u in range(M//2):
        W_2k=np.exp(2j*np.pi*u/M)
        result[u]=F_even[u]+W_2k*F_odd[u]
        result[u+M//2]=F_even[u]-W_2k*F_odd[u]
    return result






def OFFT(x):
    N = len(x)
    if N == 1:      # 递归终止条件
        return x
    else:
        # 递归计算偶数下标和奇数下标
        x_even = OFFT(x[::2])
        x_odd = OFFT(x[1::2])
        # 对偶数下标和奇数下标分别进行DFT计算
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        x_dft_even = x_even + factor[:N // 2] * x_odd
        x_dft_odd = x_even + factor[N // 2:] * x_odd
        # 合并DFT计算结果
        return np.concatenate([x_dft_even, x_dft_odd])

 

#二维FFT函数实现
def DFFT(matrix):
    M_rows,M_cols=matrix.shape
    result = np.zeros((M_rows, M_cols), dtype=complex)
    #对x的每一行应用FFT，存在reslut中，result中行是u,列是y
    for i in range(M_rows):
        result[i,:]=OFFT(matrix[i,:])
    
    #对每一列执行FFT
    for j in range(M_cols):
        colum=result[:,j]
        result[:,j]=OFFT(colum)
    
    return result


def OIFFT(x):
    N = len(x)
    if N == 1:      # 递归终止条件
        return x
    else:
        # 递归计算偶数下标和奇数下标
        x_even = OIFFT(x[::2])
        x_odd = OIFFT(x[1::2])
        # 对偶数下标和奇数下标分别进行DFT计算
        factor = np.exp(2j * np.pi * np.arange(N) / N)
        x_dft_even = x_even + factor[:N // 2] * x_odd
        x_dft_odd = x_even + factor[N // 2:] * x_odd
        # 合并DFT计算结果
        return np.concatenate([x_dft_even, x_dft_odd])
 


#二维FFT逆变换函数实现
def DIFFT(matrix):
    M_rows,M_cols=matrix.shape
    result = np.zeros((M_rows, M_cols), dtype=complex)
    #对x的每一行应用IFFT，存在reslut中，result中行是u,列是y
    for i in range(M_rows):
        result[i,:]=OIFFT(matrix[i,:])
    
    #对每一列执行IFFT
    for j in range(M_cols):
        colum=result[:,j]
        result[:,j]=OIFFT(colum)
    
    return result/(M_cols*M_rows)

def GLPF(matrix,D0):
    M_rows,M_cols=matrix.shape
    magnitude = np.abs(matrix)
    ##构造滤波函数
    center_i, center_j = M_rows // 2, M_cols// 2
    H = np.zeros((M_rows, M_cols))
    for i in range(M_rows):
        for j in range(M_cols):
            # 计算当前点到频域中心的距离D
            D = np.sqrt((i - center_i)**2 + (j - center_j)**2)
            # 应用高斯函数计算响应值
            H[i, j] = np.exp(-(D**2) / (2 * D0**2))
    ##    
    filtered_magnitude = magnitude * H
    angle = np.angle(matrix)  # 保留原始相位信息
    filtered_dft_matrix = filtered_magnitude * np.exp(1j * angle)
    return filtered_dft_matrix


    padded_image_array = np.zeros((2*M, 2*N), dtype=gray_matrix.dtype) #零填充
    # 将原始图像复制到新图像的左上角位置
    padded_image_array[:M, :N] = gray_matrix
    #中心化
    padded_image_array=padded_image_array*power_of_minus_one
    ##傅里叶变化
    DFT_matrix=DFFT(padded_image_array)
    ##高斯低通滤波
    GLPF_DFT_matrix=GLPF(DFT_matrix,30)
    # ##傅里叶反变换
    GLPF_matrix=DIFFT(GLPF_DFT_matrix)
    # ##取实部
    GLPF_matrix = np.real(GLPF_matrix)
    # 反中心化
    GLPF_matrix*=power_of_minus_one
    #8 提取出左上角
    final_matrix2=GLPF_matrix[:M,:N]
    # 使用 matplotlib.pyplot 显示灰度图像
    axes[2].imshow(final_matrix2,cmap='gray')
    axes[2].set_title(f'D0=30')
    axes[2].axis('off')

    padded_image_array = np.zeros((2*M, 2*N), dtype=gray_matrix.dtype) #零填充
    # 将原始图像复制到新图像的左上角位置
    padded_image_array[:M, :N] = gray_matrix
    # 中心化
    padded_image_array=padded_image_array*power_of_minus_one
    ##傅里叶变化
    DFT_matrix=DFFT(padded_image_array)
    ##高斯低通滤波
    GLPF_DFT_matrix=GLPF(DFT_matrix,60)
    # ##傅里叶反变换
    GLPF_matrix=DIFFT(GLPF_DFT_matrix)
    # ##取实部
    GLPF_matrix = np.real(GLPF_matrix)
    #去中心化
    GLPF_matrix*=power_of_minus_one
    #8 提取出左上角
    final_matrix3=GLPF_matrix[:M,:N]
    # 使用 matplotlib.pyplot 显示灰度图像
    axes[3].imshow(final_matrix3,cmap='gray')
    axes[3].set_title(f'D0=60')
    axes[3].axis('off')

    padded_image_array = np.zeros((2*M, 2*N), dtype=gray_matrix.dtype) #零填充
    # 将原始图像复制到新图像的左上角位置
    padded_image_array[:M, :N] = gray_matrix
    #中心化
    padded_image_array=padded_image_array*power_of_minus_one
    ##傅里叶变化
    DFT_matrix=DFFT(padded_image_array)
    ##高斯低通滤波
    GLPF_DFT_matrix=GLPF(DFT_matrix,160)
    # ##傅里叶反变换
    GLPF_matrix=DIFFT(GLPF_DFT_matrix)
    # ##取实部
    GLPF_matrix = np.real(GLPF_matrix)
    #去中心化
    GLPF_matrix*=power_of_minus_one
    #8 提取出左上角
    final_matrix4=GLPF_matrix[:M,:N]
    # 使用 matplotlib.pyplot 显示灰度图像
    axes[4].imshow(final_matrix4,cmap='gray')
    axes[4].set_title(f'D0=160')
    axes[4].axis('off')

    padded_image_array = np.zeros((2*M, 2*N), dtype=gray_matrix.dtype) #零填充
    # 将原始图像复制到新图像的左上角位置
    padded_image_array[:M, :N] = gray_matrix
    # 中心化
    padded_image_array=padded_image_array*power_of_minus_one
    ##傅里叶变化
    DFT_matrix=DFFT(padded_image_array)
    ##高斯低通滤波
    GLPF_DFT_matrix=GLPF(DFT_matrix,460)
    # ##傅里叶反变换
    GLPF_matrix=DIFFT(GLPF_DFT_matrix)
    # ##取实部
    GLPF_matrix = np.real(GLPF_matrix)
    # 去中心化
    GLPF_matrix*=power_of_minus_one
    #8 提取出左上角
    final_matrix5=GLPF_matrix[:M,:N]
    # 使用 matplotlib.pyplot 显示灰度图像
    axes[5].imshow(final_matrix5,cmap='gray')
    axes[5].set_title(f'D0=460')
    axes[5].axis('off')