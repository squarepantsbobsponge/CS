from PIL import Image  
import numpy as np
import matplotlib.pyplot as plt
import cv2
#归一化处理，计算直方图
def calculate_histogram(gray_matrix):  
    histogram=[0]*256
    width=gray_matrix.shape[1]
    height=gray_matrix.shape[0]
    sum=width*height
    for x in range(0,height):
        for y in range(0,width):
            gray_value=gray_matrix[x][y]
            histogram[int(gray_value)]+=1
    for i in range(0,len(histogram)):
        histogram[i]/=sum
    return histogram


#直方图均衡
def histogram_equalization(histogram,gray_matrix):
    cdf=[0]*256 #累计均衡分布
    cdf[0]=histogram[0] #初始化
    width=gray_matrix.shape[1]
    height=gray_matrix.shape[0]
    for i in range(1,len(cdf)):
        cdf[i]=cdf[i-1]+histogram[i]

    after_matrix=np.zeros((height,width))
    for x in range(0,height):
        for y in range(0,width):
                gray_values=gray_matrix[x][y]
                sk=(255)*cdf[gray_values]
                after_matrix[x][y]=int(sk)
    
    return after_matrix



#打印直方图
def print_histogram_image(histogram1, histogram2,image1,image2):  
    gray_levels = list(range(256))  
    fig, axes= plt.subplots(2, 2, figsize=(12, 6))  
    axes=axes.flatten()    
    # 均衡前的条形图
    axes[0].bar(gray_levels, histogram1, color='blue', alpha=0.7, edgecolor='white')  
    axes[0].set_title('before equalization')  
    axes[0].set_xlabel('Gray Levels')  
    axes[0].set_ylabel('Sum')  
    # 均衡后的条形图  
    axes[1].bar(gray_levels, histogram2, color='green', alpha=0.7, edgecolor='white')  
    axes[1].set_title('after equalization')  
    axes[1].set_xlabel('Gray Levels')  
    axes[1].set_ylabel('Sum')  
    #均衡前的图片
    axes[2].imshow(image1,cmap='gray')
    axes[2].set_title(f'before equalization')
    axes[2].axis('off')
    #均衡后的图片
    axes[3].imshow(image2,cmap='gray')
    axes[3].set_title(f'after equalization')
    axes[3].axis('off')

    plt.tight_layout()  
    plt.show() 

if __name__=="__main__":
    #1. 提取矩阵
    image=Image.open('./a.jpg')
    gray_matrix = np.array(image)
    #print(gray_matrix[256])
    #2. 获得直方图
    histogram_before=calculate_histogram(gray_matrix)
    #4.获得均衡后的灰度矩阵
    after_matrix=histogram_equalization(histogram_before,gray_matrix)
    #5.获得均衡后的直方图
    histogram_after=calculate_histogram(after_matrix)
    #print("before",histogram_before)
    #print("after",histogram_after)
    #6.转为图像输出
# # 假设equalized_matrix是直方图均衡化后的矩阵  
#     equalized_image = Image.fromarray(after_matrix.astype('uint8'), 'L')
#     equalized_image.save('equalized_image.jpg')
    #7.打印
    print_histogram_image(histogram_before,histogram_after,gray_matrix,after_matrix)



