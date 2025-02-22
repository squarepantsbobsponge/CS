import numpy as np
from PIL import Image  
import matplotlib.pyplot as plt




#一维FFT：递归实现
def OFFT(matrix):
    M=len(matrix)
    if M==1:
        return matrix
    F_even=OFFT(matrix[0::2]) #获得偶数索引
    F_odd=OFFT(matrix[1::2])

    result=np.zeros(M,dtype=complex)
    for u in range(M//2):
        W_2k=np.exp(-2j*np.pi*u/M)
        result[u]=F_even[u]+W_2k*F_odd[u]
        result[u+M//2]=F_even[u]-W_2k*F_odd[u]
    return result

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


#一维IFFT逆变换：递归实现
def OIFFT(matrix):
    M=len(matrix)
    if M==1:
        return matrix
    
    F_even=OIFFT(matrix[0::2]) #获得偶数索引
    F_odd=OIFFT(matrix[1::2])

    result=np.zeros(M,dtype=complex)
    for u in range(M//2):
        W_2k=np.exp(2j*np.pi*u/M)
        result[u]=F_even[u]+W_2k*F_odd[u]
        result[u+M//2]=F_even[u]-W_2k*F_odd[u]
    return result
 


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

#输入频域F（u，v）输出滤波后的F（u,v）,截止频率D0
def GLPF(matrix,D0,axes):
    M_rows,M_cols=matrix.shape

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
    log_magnitude_spectrum_H=20*np.log(np.abs(H)+1)
    axes[4].imshow(np.real(log_magnitude_spectrum_H),cmap='gray')
    axes[4].set_title('H')
    axes[4].axis('off')

    filtered_dft_matrix = matrix*H
    return filtered_dft_matrix

if __name__=="__main__":
    image=Image.open('./c.jpg')
    gray_matrix=np.array(image)
    gray_matrix= np.pad(gray_matrix, ((6, 6), (6, 6)), mode='constant', constant_values=0)# 要转为512*512
    M,N=gray_matrix.shape
    print(M,N)

    fig,axes=plt.subplots(3,3,figsize=(12,6))
    fig.suptitle(f'compare')
    axes=axes.flatten()
    axes[0].imshow(gray_matrix,cmap='gray')
    axes[0].set_title(f'before')
    axes[0].axis('off')

    #中心化的数组
    indices_sum = np.indices((2*M, 2*N)).sum(axis=0)
    power_of_minus_one = (-1) ** indices_sum

    #1.
    padded_image_array = np.zeros((2*M, 2*N), dtype=gray_matrix.dtype) #零填充
    # 将原始图像复制到新图像的左上角位置
    padded_image_array[:M, :N] = gray_matrix
    axes[1].imshow(padded_image_array,cmap='gray')
    axes[1].set_title(f"zero-padded image")
    axes[1].axis('off')
    #中心化
    padded_image_array=power_of_minus_one*padded_image_array
    axes[2].imshow(padded_image_array,cmap='gray')
    axes[2].set_title(f'after centering')
    axes[2].axis('off')
    ##傅里叶变化
    DFT_matrix=DFFT(padded_image_array)
    log_magnitude_spectrum_DFT_matrix=20*np.log10(np.abs(DFT_matrix)+1e-10)
    axes[3].imshow(np.real(log_magnitude_spectrum_DFT_matrix),cmap='gray')
    axes[3].set_title(f'the spectrum after Fourier transform')
    axes[3].axis('off')
    ##高斯低通滤波
    GLPF_DFT_matrix=GLPF(DFT_matrix,80,axes)
    log_magnitude_spectrum_GLPF_DFT_matrix=20*np.log(np.abs(GLPF_DFT_matrix)+1)
    axes[5].imshow(np.real(log_magnitude_spectrum_GLPF_DFT_matrix),cmap='gray')
    axes[5].set_title(f'the spectrum after Gaussian low-pass filtering')
    axes[5].axis('off')
    # ##傅里叶反变换
    GLPF_matrix=DIFFT(GLPF_DFT_matrix)
    # ##取实部
    GLPF_matrix = np.real(GLPF_matrix)
    #去中心化
    GLPF_matrix*=power_of_minus_one
    axes[6].imshow(GLPF_matrix,cmap='gray')
    axes[6].set_title(f'the image after decentering')
    axes[6].axis('off')
    #8 提取出左上角
    final_matrix1=GLPF_matrix[:M,:N]
    # 使用 matplotlib.pyplot 显示灰度图像
    axes[7].imshow(final_matrix1,cmap='gray')
    axes[7].set_title(f'final D0=10')
    axes[7].axis('off')

    
    plt.show()  # 显示图像


    
