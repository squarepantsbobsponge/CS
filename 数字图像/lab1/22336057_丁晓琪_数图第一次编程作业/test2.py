from PIL import Image  
import numpy as np
import matplotlib.pyplot as plt

def Laplacian_Image(padded_matrix):
    kernel = np.array([[-1, -1, -1],  
                   [-1, 8, -1],  
                   [-1, -1, -1]])
    width=padded_matrix.shape[1]

    height=padded_matrix.shape[0]
    Laplacian_matrix=np.zeros((height-1,width-1))
    for x in range(1,height-1):
        for y in range(1,width-1):
            for m in range(-1,1):
                for n in range(-1,1):
                    Laplacian_matrix[x][y]+=padded_matrix[x+m][y+n]*kernel[m+1][n+1]
    return Laplacian_matrix

def Laplacian_Enhancement(Laplacian_matrix,gray_matrix):
    width=gray_matrix.shape[1]
    height=gray_matrix.shape[0]
    Laplacian_enhancement_matrix=np.zeros((height,width))

    for x in range(0,height):
        for y in range(0,width):
            Laplacian_enhancement_matrix[x][y]=gray_matrix[x][y]+Laplacian_matrix[x][y]
    Laplacian_enhancement_matrix = np.clip(Laplacian_enhancement_matrix, 0, 255)
    return Laplacian_enhancement_matrix

if __name__=="__main__":
    #1.提取矩阵
    image=Image.open("./b.jpg")
    gray_matrix=np.array(image)
    #print(gray_matrix[256])
    #2.填充一圈0
    padded_matrix=np.pad(gray_matrix,((1,1),(1,1)),mode='constant')
    #print(padded_matrix)
    #3. 拉普拉斯锐化
    Laplacian_matrix=Laplacian_Image(padded_matrix)
    #print(Laplacian_matrix[256])
    Laplacian__image = Image.fromarray(Laplacian_matrix.astype('uint8'), 'L')
    Laplacian__image.save('Laplacian_image.jpg')
    #4.拉普拉斯增强
    Laplacian_enhancement_matrix=Laplacian_Enhancement(Laplacian_matrix,gray_matrix)
    Laplacian_enhancement_image = Image.fromarray(Laplacian_enhancement_matrix.astype('uint8'), 'L')
    Laplacian_enhancement_image.save('Laplacian_enhancement_image.jpg')
    #5.画图
    fig3,axes3=plt.subplots(1,3,figsize=(12,6))
    fig3.suptitle(f'Laplacian')
    axes=axes3.flatten()
    axes[0].imshow(gray_matrix,cmap='gray')
    axes[0].set_title(f'origin')
    axes[0].axis('off')
    axes[1].imshow(Laplacian_matrix,cmap='gray')
    axes[1].set_title(f'Laplacian_image')
    axes[1].axis('off')
    axes[2].imshow(Laplacian_enhancement_matrix,cmap='gray')
    axes[2].set_title(f'Laplacian_enhancement_image')
    axes[2].axis('off')
    plt.tight_layout()
    plt.show()


