import numpy as np
from PIL import Image  
import matplotlib.pyplot as plt

#添加椒盐噪声
def Add_SP_noise(noise_matrix):
    M,N=noise_matrix.shape
    for i in range(0,M):
        for j in range(0,N):
            random_num=np.random.rand()
            if(random_num<=0.2):
                noise_matrix[i][j]=255
            elif random_num>0.2 and random_num<=0.4:
                noise_matrix[i][j]=0

#中值滤波
def Median_Filtering(noise_matrix,kernel_size):
    M,N=noise_matrix.shape
    filtered_matrix = np.zeros_like(noise_matrix, dtype=noise_matrix.dtype)
    ##拓展边界,镜像扩展
    pad_size=kernel_size//2
    padded_matrix=np.pad(noise_matrix,((pad_size, pad_size), (pad_size, pad_size)), mode='reflect')
    print(padded_matrix.shape)
    # 2
    for i in range(pad_size,M+pad_size):
        for j in range(pad_size,N+pad_size):
            window = padded_matrix[i-pad_size:i+pad_size, j-pad_size:j+pad_size]
            median_value=np.median(window)
            filtered_matrix[i-pad_size,j-pad_size]=median_value
    return filtered_matrix


if __name__=="__main__":
    image=Image.open('./a.jpg')
    gray_matrix=np.array(image)
    noise_matrix=np.copy(gray_matrix)
    Add_SP_noise(noise_matrix)
    fitered_matrix=Median_Filtering(noise_matrix,5)
    
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.title('before Image')
    plt.imshow(gray_matrix, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title('Noisy Image')
    plt.imshow(noise_matrix, cmap='gray')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.title('Filtered Image')
    plt.imshow(fitered_matrix, cmap='gray')
    plt.axis('off')
 
    plt.show()