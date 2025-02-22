import numpy as np
from PIL import Image  
import matplotlib.pyplot as plt


def Motion_Blur(M,N, T, a, b):
    # 功能：计算运动模糊的退化滤波核
    # 输入：滤波核大小M，N，运动模糊参数T，a，b
    # 输出：频域上的运动模糊的滤波核
    H = np.zeros((M,N), dtype=np.complex128)
    for u in range(M):
        for v in range(N):
            # 要中心化的频率坐标
            tm = np.pi * ((u-M//2) * a + (v-N//2) * b)
            if abs(tm) < 1e-10:  # 避免除 0 错误
                H_u_v = T
            else:
                H_u_v = T * (np.sin(tm) * np.exp(-1j * tm)) / tm
            H[u,v] =  H_u_v

    return H

def Add_Gaussion_noise(image,mean,variance):
    # 功能：对输入图像image加高斯噪声
    # 输入：图像的空域表达image,高斯噪声的参数mean,variance
    # 输出：加入高斯噪声后的图像result——matrix
    M,N=image.shape
    sigma=variance**0.5
    gauss=np.random.normal(mean,sigma,(M,N))
    gauss=gauss.reshape(M,N)
    result_matrix=image+gauss
    return result_matrix

def estimate_power_spectra(DFT_gray_matrix,G_u_v):
    # 功能：噪声功率谱密度和原始图像的功率谱密度。
    # 输入：原图像的频域表达 DFT_gray_matrix，加入噪声后的频域表达 G_u_v
    power_spectra_image = np.square(np.abs(DFT_gray_matrix))
    power_spectra_noise = np.square(np.abs(G_u_v))
    return power_spectra_image, power_spectra_noise

def Wiener_filtering(G_u_v,noise_power,image_power):
    # 功能：对退化和加上噪声的图像的频域G_u_v做维纳斯滤波
    # 输入：noise_power,image_power都是功率谱密度
    # 输出：对G——u_v加上维纳滤波
    M,N=G_u_v.shape
    H=Motion_Blur(M,N,1,0.1,0.1)
    H_conj = np.conj(H)
    H_abs=np.abs(H)
    H_abs_sq=np.square(H_abs)

    S_eta=noise_power
    S_f=image_power
    factor=S_eta/S_f
    wiener_filtering=H_conj / (H_abs_sq + factor)

    F_restore=wiener_filtering*G_u_v
    return F_restore



if __name__=="__main__":
    image=Image.open('./b.jpg')
    gray_matrix=np.array(image) #大小为688，688,不好直接用上次作业的FFT进行傅里叶变换，直接调包
    M,N=gray_matrix.shape
    # 显示原图像
    plt.figure(figsize=(10, 10))
    plt.subplot(221), plt.imshow(gray_matrix, cmap='gray'), plt.title('Original Image')
    # 运动模糊
    DFT_gray_matrix=np.fft.fft2(gray_matrix) #默认中心化了
    Motion_Blur_matrix=Motion_Blur(M,N,1,0.1,0.1)*DFT_gray_matrix
    IFFT_Motion_Blur_matrix=np.real(np.fft.ifft2(Motion_Blur_matrix))
    plt.subplot(222), plt.imshow(IFFT_Motion_Blur_matrix, cmap='gray'), plt.title('Blurred Image')
    # 添加高斯噪声
    final_degenerate_image= Add_Gaussion_noise(IFFT_Motion_Blur_matrix,0,10)
    plt.subplot(223), plt.imshow(final_degenerate_image, cmap='gray'), plt.title('Noisy Image')
    # 维纳滤波器恢复
    G_u_v=np.fft.fft2(final_degenerate_image)
    power_spectra_image, power_spectra_noise = estimate_power_spectra(DFT_gray_matrix, G_u_v)
    G_restore=Wiener_filtering(G_u_v,power_spectra_noise,power_spectra_image)
    restore_image=np.real(np.fft.ifft2(G_restore))
    plt.subplot(224), plt.imshow(restore_image, cmap='gray'), plt.title('Restored Image')
    
    plt.tight_layout()
    plt.show()

