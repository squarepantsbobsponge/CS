from PIL import Image  
import numpy as np
import matplotlib.pyplot as plt


def Get_bit_plane(gray_matrix):
    bit_planes=[]
    for i in range(0,8):
        bit_plane=((gray_matrix>>i)&1)*255 #先提取出来的是最低位的,255是为了后期绘图得到二值图（bit=0，灰度为0，bit为1，灰度为255）
        bit_planes.append(bit_plane)
    return bit_planes

def print_image(fig,axes,bit_planes,origin_matrix):
    axes=axes.flatten()
    axes[0].imshow(origin_matrix,cmap='gray')
    axes[0].set_title(f'image')
    axes[0].axis('off')
    i=1
    for bit_plane in bit_planes:
        axes[i].imshow(bit_plane,cmap='gray')
        axes[i].set_title(f'Bit Plane {i-1}')
        axes[i].axis('off')
        i+=1


def change_LSB(LSB):
    height=LSB.shape[0]
    width=LSB.shape[1]
    change_height=height//2
    for i in range(-50,50):
        for j in range(0,width):
            LSB[change_height+i][j]=0  #也就是将对应bit改为0

#将位平面加回图像,位平面取值（0，255（1））
def  merge_bit_planes_to_image(bit_planes):
    height=bit_planes[0].shape[0]
    width=bit_planes[0].shape[1]  
    new_matrix=np.zeros((height,width))

    for x in range(0,height):
        for y in range(0,width):
            for  i in range(0,8):
                if bit_planes[i][x][y]!=0:
                    new_matrix[x][y]+=(pow(2,i))  
    
    return new_matrix

if __name__=="__main__":
    image=Image.open('./c.jpg')
    gray_matrix=np.array(image)
    print(gray_matrix.shape)
    #1.得到可视化的位平面图
    bit_planes=Get_bit_plane(gray_matrix)
    #2.绘制图像
    fig1,axes1=plt.subplots(3,3,figsize=(12,6))
    fig1.suptitle(f'before change')
    print_image(fig1,axes1,bit_planes,gray_matrix)
    #3.随意修改LSB,得到修改LSB后的图像
    change_LSB(bit_planes[0])
    after_change_matrix=merge_bit_planes_to_image(bit_planes)
    #3.绘制图像
    fig2,axes2=plt.subplots(3,3,figsize=(12,6))
    fig2.suptitle(f'after change')
    print_image(fig2,axes2,bit_planes,after_change_matrix)
    #4.compare
    fig3,axes3=plt.subplots(1,2,figsize=(12,6))
    fig3.suptitle(f'compare')
    axes=axes3.flatten()
    axes[0].imshow(gray_matrix,cmap='gray')
    axes[0].set_title(f'before')
    axes[0].axis('off')
    axes[1].imshow(after_change_matrix,cmap='gray')
    axes[1].set_title(f'after')
    axes[1].axis('off')
    plt.tight_layout()
    plt.show()

    