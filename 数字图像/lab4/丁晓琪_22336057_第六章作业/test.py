import numpy as np
from PIL import Image  
import matplotlib.pyplot as plt

#归一化处理，计算直方图
def calculate_histogram(channel_matrix):  
    histogram=[0]*256
    width=channel_matrix.shape[1]
    height=channel_matrix.shape[0]
    sum=width*height
    for x in range(0,height):
        for y in range(0,width):
            gray_value=channel_matrix[x][y]
            histogram[int(gray_value)]+=1
    for i in range(0,len(histogram)):
        histogram[i]/=sum
    return histogram


#直方图均衡
def histogram_equalization(channel_matrix):
    histogram=calculate_histogram(channel_matrix)
    #histogram=np.histogram(channel_matrix,256)
    cdf=[0]*256 #累计均衡分布
    cdf[0]=histogram[0] #初始化
    width=channel_matrix.shape[1]
    height=channel_matrix.shape[0]
    for i in range(1,len(cdf)):
        cdf[i]=cdf[i-1]+histogram[i]

    after_matrix=np.zeros((height,width))
    for x in range(0,height):
        for y in range(0,width):
                gray_values=channel_matrix[x][y]
                sk=(255)*cdf[gray_values]
                after_matrix[x][y]=int(sk)
    
    return after_matrix


def RGB_histogram_equalization(rgb_matrix):
    red_channel = rgb_matrix[:, :, 0]   # 红色通道
    green_channel = rgb_matrix[:, :, 1] # 绿色通道
    blue_channel = rgb_matrix[:, :, 2]  # 蓝色通道  
    # 对每个通道直方图均衡
    after_red_channel=histogram_equalization(red_channel)
    after_green_channel=histogram_equalization(green_channel)
    after_blue_channel=histogram_equalization(blue_channel)
    # 防止超出0-255范围（要加不然会曝光）
    after_red_channel = np.clip(after_red_channel, 0, 255).astype(np.uint8)
    after_green_channel = np.clip(after_green_channel, 0, 255).astype(np.uint8)
    after_blue_channel = np.clip(after_blue_channel, 0, 255).astype(np.uint8)
    # 组合
    combined_image=np.stack((after_red_channel, after_green_channel, after_blue_channel), axis=-1)
    plt.subplot(1,4,4)
    plt.imshow(combined_image)
    plt.axis('off')  
    plt.title('RGB_histogram_equalization')

def RGB_TO_HSI(rgb_image):
    # 归一化rgb值
    rgb_image = rgb_image.astype(np.float32)/255.0
    R,G,B = rgb_image[:, :, 0], rgb_image[:, :, 1], rgb_image[:, :, 2]
    # I空间
    I=(R+G+B)/3.0
    # S空间
    min_rgb=np.minimum(np.minimum(R, G),B)
    S=1-(3/(R+G+B+1e-10))*min_rgb
    # H空间 0-1
    theta=np.arccos(0.5*((R-G)+(R-B))/np.sqrt((R-G)**2+(R-B)*(G-B)+1e-10))
    mask=(B<=G)  # 掩码，B<=G为1
    H=np.where(mask,theta/(2*np.pi),(2*np.pi-theta)/(2*np.pi))
    # 合并
    hsi_image=np.stack((H,S,I),axis=-1)
    return hsi_image

def HSI_TO_RGB(hsi_image):
    H,S,I = hsi_image[:, :, 0], hsi_image[:, :, 1], hsi_image[:, :, 2]
    
    R=np.zeros_like(H)
    G=np.zeros_like(H)
    B=np.zeros_like(H)
    #0<=H<120（角度） 
    idx1=(0<=H)&(H<120/360)
    B[idx1]=I[idx1]*(1 - S[idx1])
    R[idx1]=I[idx1]*(1+(S[idx1]*np.cos(H[idx1]*2*np.pi)/np.cos((np.pi/3)-(H[idx1]*2*np.pi))))
    G[idx1]=3*I[idx1]-(R[idx1]+B[idx1]) 
     #120<=H<240
    idx2=(120/360<=H)&(H<240/360)
    H_region2=H[idx2]-120/360
    R[idx2]=I[idx2]*(1-S[idx2])
    G[idx2]=I[idx2]*(1+(S[idx2]*np.cos(H_region2*2*np.pi)/np.cos((np.pi/3)-(H_region2*2*np.pi))))
    B[idx2]=3*I[idx2]-(R[idx2]+G[idx2])

    #240<=H<360
    idx3=(240/360<=H)&(H<1)

    H_region3=H[idx3]-240/360
    G[idx3]=I[idx3]*(1-S[idx3])
    B[idx3]=I[idx3]*(1+(S[idx3]*np.cos(H_region3*2*np.pi)/np.cos((np.pi/3)-(H_region3*2*np.pi))))
    R[idx3]=3*I[idx3]-(G[idx3]+B[idx3])

    RGB_image=np.stack((R, G, B), axis=-1)
    RGB_image=(RGB_image*255).astype(np.uint8)
    return RGB_image  



def HSI_histogram_equalization(rgb_image):
      # 转到RGB空间
      hsi_image=RGB_TO_HSI(rgb_image)
      H, S, I = hsi_image[:, :, 0], hsi_image[:, :, 1], hsi_image[:, :, 2]
      print(np.max(S))
      # I空间映射到0-255
      I_8bit=np.clip(np.round(I*255),0,255).astype(np.uint8)
      # I空间直方图均衡化
      I_equalized_8bit=histogram_equalization(I_8bit)
      # 重新归一化
      I_equalized_normalized=I_equalized_8bit.astype(np.float32)/255.0
      print(np.min(I_equalized_normalized))
      # 重新组合为HSI空间
      hsi_equalized=np.stack((H, S, I_equalized_normalized), axis=-1)
      # 转到RGB空间
      RGB_hsi_equalized=HSI_TO_RGB(hsi_equalized)
      plt.subplot(1,4,3)
      plt.imshow(RGB_hsi_equalized)
      plt.axis('off')  
      plt.title('HSI_histogram_equalization(image)')



if __name__=="__main__":
    image=Image.open('./a.jpg')
    matrix=np.array(image)

    plt.subplot(1,4,1)
    plt.imshow(matrix)
    plt.axis('off') 
    plt.title('image')
    plt.subplot(1,4,2)
    # 验证RGB和HSI互转的正确性
    plt.imshow(HSI_TO_RGB(RGB_TO_HSI(matrix)))
    plt.axis('off') 
    plt.title('HSI_TO_RGB(RGB_TO_HSI(matrix))')
    # 对I空间直方图均衡
    HSI_histogram_equalization(matrix)
    # 对RGB分别直方图均衡
    RGB_histogram_equalization(matrix)
    
    plt.tight_layout() 
    plt.show()   


