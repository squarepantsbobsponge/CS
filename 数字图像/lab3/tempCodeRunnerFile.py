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