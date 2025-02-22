import numpy as np
from PIL import Image  
import matplotlib.pyplot as plt

#膨胀,二值膨胀，只看像素值为0/255的位置的像素,像素不为255的默认为0,按照定义
def binary_dilation(image,kernel):
    # 输入：图像矩阵，膨胀核
    # 输出：膨胀后的图像
    result_image=np.zeros_like(image)
    kernel_height,kernel_width=kernel.shape
    image_height,image_width=image.shape
    pad_height=kernel_height//2
    pad_width=kernel_width//2
    #保持原图像不变，周围填充0
    padded_image=np.pad(image,((pad_height, pad_height), (pad_width, pad_width)), mode='constant', constant_values=0)
    for i in range(image_height):
        for j in range(image_width):
        # 结构元的中点在i,j时
            for ki in range(-pad_height,pad_height+1):
                for kj in range(-pad_width,pad_width+1):
                    # 只有结构元有个元素核图像位置重合
                    if kernel[-ki+pad_height,-kj+pad_width] and padded_image[i+ki,j+kj]==255:
                        result_image[i,j]=255
    
    return result_image

#腐蚀，像素不为0的默认为255，按照定义
def binary_erosion(image,kernel):
    # 输入：图像矩阵，结构元
    result_image=np.zeros_like(image)
    kernel_height,kernel_width=kernel.shape
    image_height,image_width=image.shape
    pad_height=kernel_height//2
    pad_width=kernel_width//2
    # 保持图形腐蚀后大小不变
    padded_image=np.pad(image,((pad_height, pad_height), (pad_width, pad_width)), mode='constant', constant_values=0)

    for i in range(image_height):
        for j in range(image_width):
            inside=True
            # 结构元中心在i,j
            for ki in range(-pad_height,pad_height+1):
                for kj in range(-pad_width,pad_width+1):
                    # 只要结构元和图像背景有交集，则该位置为0
                    if kernel[ki+pad_height,kj+pad_width] and padded_image[i+ki,j+kj]==0:
                        inside=False
                        break
            if inside:
                result_image[i,j]=255
    
    return result_image    

if __name__=="__main__":
    image=Image.open('./a.jpg')
    gray_matrix=np.array(image) #256*256
    print(gray_matrix.shape)
    print(gray_matrix[128])
    kernel = [
        [255, 255, 255],
        [0, 255, 0],
        [0, 255, 0]
    ]
    kernel = np.array(kernel, dtype=int) 
    dilated_image=binary_dilation(gray_matrix,kernel)
    eroded_image=binary_erosion(gray_matrix,kernel)
    # 图像边界，按照定义
    boundary_image=gray_matrix-eroded_image
    # 创建一个包含两个子图的图形窗口
    plt.figure(figsize=(20, 10))

    # 第一个子图显示原始图像
    plt.subplot(2, 2, 1)  
    plt.imshow(gray_matrix, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    # 第二个子图显示膨胀后的图像
    plt.subplot(2, 2, 2) 
    plt.imshow(dilated_image, cmap='gray')
    plt.title('Dilated Image')
    plt.axis('off')

    # 第三个子图显示腐蚀后的图像
    plt.subplot(2, 2, 3) 
    plt.imshow(eroded_image, cmap='gray')
    plt.title('Eroded Image')
    plt.axis('off')

    # 第三个子图显示腐蚀后的图像
    plt.subplot(2, 2, 4)  
    plt.imshow(boundary_image, cmap='gray')
    plt.title('Boundary Image')
    plt.axis('off')

    plt.show()