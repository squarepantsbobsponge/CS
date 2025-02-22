import numpy as np
from PIL import Image  
import matplotlib.pyplot as plt

def ostu_threshold(image):
    # 计算图像直方图 hist存储出现次数，bin_edges存储范围
    hist,bin_edges=np.histogram(image,bins=256,range=(0,256))
    # 归一化直方图
    hist=hist.astype(float)/hist.sum()
    hist_print(hist,bin_edges)
    # 类间方差计算
    P_1_k=np.cumsum(hist)
    m_k=np.cumsum(hist*np.arange(256))
    m_G=m_k[-1]
    sigma_B_sq=(m_G*P_1_k-m_k)**2/((P_1_k+1e-10)*(1-P_1_k+1e-10))
    # 找到最佳阈值
    k_star=np.argmax(sigma_B_sq)
    print(P_1_k)
    print(k_star)
    # 得到阈值后的图像
    binary_image = (image > k_star).astype(np.uint8) * 255
    return binary_image


def hist_print(hist,bin_edges):
# 绘制直方图
    plt.subplot(1, 3, 2)
    plt.bar(bin_edges[:-1], hist, width=1, edgecolor='black', align='edge')
# 添加标题和标签
    plt.title('Image Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency') 

if __name__=="__main__":
    image=Image.open('./a.jpg')
    gray_matrix=np.array(image) #256*256
    #ostu_threshold(gray_matrix) #不需要平滑处理
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.imshow(gray_matrix, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    after_image=ostu_threshold(gray_matrix)

    plt.subplot(1, 3, 3)
    plt.imshow(after_image, cmap='gray')
    plt.title(' ostu_threshold Image')
    plt.axis('off')

    plt.show()
