import numpy as np
import pandas as pd
from scipy.stats import mode
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
import time

class Kmeans:
    def __init__(self,k,iter_times,train_labels,train_images):
       # 功能：初始化Kmeans类
       # 输入：k簇数，iter_times训练时迭代次数，train_labels,train_images训练数据
       self.k=k #簇数
       self.iter_times=iter_times #迭代次数
       self.train_labels=train_labels #训练数据
       self.train_images=train_images
       self.test_accuracies = []  # 用于记录每次测试的正确率
    
    def init_center_random(self):
        # 功能：随机从训练实例中挑选10个样本初始化聚类中心
        init_num = np.random.choice(self.train_images.shape[0], self.k, replace=False)
        self.centers= self.train_images[init_num]
    
    def init_center_distance(self):
        # 功能：根据距离初始化聚类中心
        # 1. 选择第一个中心点为随机样本
        self.centers = np.zeros((self.k, self.train_images.shape[1]))
        self.centers[0] = self.train_images[np.random.choice(self.train_images.shape[0])]

        # 2. 计算所有点到第一个中心点的距离
        distances = np.linalg.norm(self.train_images - self.centers[0], axis=1)

        # 3. 选择剩余的中心点
        for i in range(1, self.k):
            # 选择与已有中心点距离最远的点作为新的中心点
            farthest_index = np.argmax(distances)
            self.centers[i] = self.train_images[farthest_index]
            # 更新距离，考虑新中心点
            new_distances = np.linalg.norm(self.train_images - self.centers[i], axis=1)
            # 更新到新中心点的距离
            distances = np.minimum(distances, new_distances)


    def train(self,test_labels,test_images):
        # 功能：训练K-means
        # 输入：test_labels,test_images,检验训练效果的测试集的标签和样本
         
        for t in range(0,self.iter_times):
        # 1.对样本判断所属簇
         # 1.1 创建数组来存储每个样本的簇分配 
            cluster_assignments = np.zeros(self.train_images.shape[0], dtype=int)
            for i in range(0,self.train_images.shape[0]):
                # 计算样本到每个聚类中心的距离
                # 找到最近的聚类中心的索引
                closest_index=self.compute_closest_index(self.train_images[i])
                cluster_assignments[i]=closest_index
        
            # 2: 更新聚类中心
            new_centers = np.zeros((self.k, self.train_images.shape[1]))
            for i in range(0,self.k):
                # 找到第i簇的所有样本
                cluster_i_sample=self.train_images[cluster_assignments==i]
                # 簇不为空时，更新聚类中心
                if cluster_i_sample.size>0:
                    new_centers[i]=cluster_i_sample.mean(axis=0)
            self.centers=new_centers
            self.cluster_assignment=cluster_assignments
            # 3.测试
            if t%5==0:
                self.test(test_labels,test_images)
                print(f"Iteration {t}: Test Accuracy = {self.test_accuracies[-1]}")
            

    
    def test(self,test_labels,test_images):
        # 功能：用test_images样本和它对应的标签test_labels测试模型，计算模型正确率
        # 输入：
        #   test_images: 测试样本
        #   test_labels: 测试样本的标签
        correct_sum=0
        for i in range(0,test_images.shape[0]):
                # 1.计算样本到每个聚类中心的距离
                #   找到最近的聚类中心的索引
                closest_index=self.compute_closest_index(test_images[i])
                # 2. 找该聚类的标签（聚类内样本标签的众数）
                cluster_labels = self.train_labels[self.cluster_assignment == closest_index]
                mode_result = mode(cluster_labels)
                predict_label = mode_result.mode[0]  
                # 3.比较聚类标签和样本真实标签
                if predict_label==test_labels[i]:
                    correct_sum+=1
        accuracy = correct_sum / test_images.shape[0]
        self.test_accuracies.append(accuracy)
        return accuracy

    def plot_accuracies(self,title):
        plt.figure()
        n=range(int(self.iter_times/5)+1)
        x_list = [i * 5 for i in n]
        plt.plot(x_list, self.test_accuracies, marker='o')
        plt.xlabel('Iteration')
        plt.ylabel('Test Accuracy')
        plt.title(title)#'K-means Test Accuracy Over Iterations'
        plt.grid(True)

    

    def compute_closest_index(self, sample):
        # 功能：计算并返回样本sample距离（欧几里得距离）最近的聚类中心的索引
        # 输入：
        #   sample：要计算的样本
        distances = np.sum((self.centers - sample) ** 2, axis=1)
        closest_center_index = np.argmin(distances)
        return closest_center_index
                
class PCA():
    def __init__(self):
        # 功能：初始化PCA类
        # mean为训练数据的平均值，components为主成分
        self.mean=None
        self.components=None
    
    def fit(self,X,n_components):
        # 功能：根据X计算n_components个主成分向量
        # 输入：
        #   X：训练样本
        #   n_components：主成分向量的数量
        m,n=X.shape
        # 1 求协方差矩阵
        self.mean=np.mean(X,axis=0)
        X_centered=X-self.mean #会广播的
        covariance_matrix=np.matmul(X_centered.T,X_centered)/m
        # 2.计算特征值和特征向量（列向量）
        eigenvalues,eigenvectors=np.linalg.eig(covariance_matrix)
        # 3.取出最大的前n个特征向量
            #将特征向量最大到小的索引找出来
        index=np.argsort(eigenvalues)[::-1]
            #排序
        eigenvectors=eigenvectors[:,index]
        #   选择前n个特征向量
        self.components=eigenvectors[:,:n_components]

    def transform(self,X):
        # 功能：将向量转到主成分空间
        # 输入：
        #   X:需要转换的样本
        return np.dot(X-self.mean,self.components)

class GMM:
    def __init__(self,train_images,k,max_iter,train_labels,means_init_method,cov_init_method):
        # 功能：初始化参数：单个高斯分布的权重，单个高斯分布的均值和协方差
        # 输入：
        #   train_images：训练样本
        #   k: 高斯分布的个数
        #   max_iter: 最大迭代次数
        #   train_labels: 训练样本的真实标签
        #   means_init_method: 单个高斯分布的均值初始化方法选项(0:随机，1：根据距离选择)
        #   cov_init_method:单个高斯分布的协方差初始化方法选项（0/1）
        self.k=k
        self.max_iter=max_iter
        self.train_labels=train_labels
        self.train_images=train_images
        self.test_accuracies = [] 
        # 1.初始化每个高斯分布的权重
            #  生成一个包含10个介于0到100之间的随机整数的数组
        random_weights = np.random.randint(0, 101, size=10)
        weights_sum = np.sum(random_weights.astype(float))
        self.weights = random_weights.astype(float) / weights_sum
        # 2. 初始化每个高斯分布的均值
        #   随机抽取k个样本初始化均值
        if(means_init_method==0):
            init_num = np.random.choice(self.train_images.shape[0], self.k, replace=False)
            self.means= self.train_images[init_num]
        # 根据距离来选择哪个样本作为高斯分布的初始化均值
        elif(means_init_method==1):
            # 选择第一个平均值为随机样本
            self.means = np.zeros((self.k, self.train_images.shape[1]))
            self.means[0] = self.train_images[np.random.choice(self.train_images.shape[0])]
            # 计算所有点到第一个中心点的距离
            distances = np.linalg.norm(self.train_images - self.means[0], axis=1)
            # 选择剩余的中心点
            for i in range(1, self.k):
                # 选择与已有中心点距离最远的点作为新的中心点
                farthest_index = np.argmax(distances)
                self.means[i] = self.train_images[farthest_index]
                # 更新距离，考虑新中心点
                new_distances = np.linalg.norm(self.train_images - self.means[i], axis=1)
                # 更新到新中心点的距离
                distances = np.minimum(distances, new_distances)

        # 3. 初始化每个高斯分布是协方差矩阵
        # 要初始化为样本的协方差矩阵的对角矩阵(对角元素不同)
        if(cov_init_method==0):
            cov = np.cov(self.train_images, rowvar=False) + 1e-6 * np.eye(self.train_images.shape[1])
            cov = np.diag(np.diag(cov))
            self.covariance_matrices= cov[np.newaxis, :].repeat(self.k, axis=0)
        elif(cov_init_method==1):
            #初始化对角矩阵元素都相等，球形初始化
            avg_var = np.mean(np.var(self.train_images, axis=0))
            cov = avg_var * np.ones((self.train_images.shape[1], self.train_images.shape[1]))
            # 由于cov需要是对角矩阵，这里仍使用对角矩阵形式
            cov = np.diag(np.full(self.train_images.shape[1], avg_var))
            self.covariance_matrices = cov[np.newaxis, :].repeat(self.k, axis=0)


    def Gaussion_probability(self,index,sample):
        #功能：计算样本sample在第index个高斯分布下出现的概率
        # mean=self.means[index]
        # covariance_matrix=self.covariance_matrices[index]
        # #求协方差的行列式和逆矩阵
        # inv_covariance_matrix = np.linalg.inv(covariance_matrix)
        # det_covariance_matrix = np.linalg.det(covariance_matrix)
        # #
        # diff=sample-mean
        # exponent_term=np.dot(np.dot(diff.T, inv_covariance_matrix), diff)
        # #计算概率
        # feature_dim=sample.shape[0]
        # probability = (1.0 / (np.sqrt((2 * np.pi) ** feature_dim * det_covariance_matrix))) * \
        #               np.exp(-0.5 * exponent_term)
        # return probability
        mvn = multivariate_normal(self.means[index], self.covariance_matrices[index])
        return mvn.pdf(sample)
    
    def EM_train(self,test_images,test_labels):
        # 功能：用E-M法训练模型
        # 输入：
        #   test_images:在训练过程中测试模型正确率的测试集
        #   test_labels: 测试集的真实标签
        
        #每个样本可能属于的聚类
        self.predict_indexs=np.zeros(self.train_images.shape[0], dtype=int)
        for t in range(0,self.max_iter):
            # 1.E步，计算gamma
            gamma_matrix=np.zeros((self.train_images.shape[0],self.k))
            for j in range(0,self.k):
                # 一次性计算所有样本的概率密度
                gamma_matrix[:, j] = self.Gaussion_probability(j,self.train_images) * self.weights[j]
            #print(gamma_matrix)
            gamma_matrix/=gamma_matrix.sum(axis=1,keepdims=True) #按行求和保持维度
            self.predict_indexs=gamma_matrix.argmax(axis=1)
        
            # 2： G步，更新高斯分布的相关参数
            N=np.sum(gamma_matrix,axis=0) #按行求和
            for i in range(0,self.k):
                self.means[i]=(1/N[i])*np.dot(gamma_matrix[:,i].reshape(1,-1),self.train_images) #gamma列向量转为行向量了，这里dot看成矩阵乘法
                self.weights[i]=N[i]/self.train_images.shape[0]
                diff = self.train_images - self.means[i]
                covariance_matrix = (1 / (N[i] + 1e-6)) * np.dot((gamma_matrix[:, i].reshape(-1, 1) * diff).T, diff)
                self.covariance_matrices[i]=covariance_matrix
           
            if t%5==0:
                self.test(test_images,test_labels)
                print(f"Iteration {t}: Test Accuracy = {self.test_accuracies[-1]}")

    def test(self,test_images,test_labels):
        # 功能：已知x求属于哪个聚类z
        correct_sum=0
        gamma_vector=np.zeros((test_images.shape[0],self.k))
        for j in range(0,self.k):
                # 计算每个样本在第j个高斯分布下的概率    
            gamma_vector[:, j] = self.Gaussion_probability(j, test_images) * self.weights[j]

        gamma_vector /= np.sum(gamma_vector, axis=1, keepdims=True)
        predict_test_indexs=np.argmax(gamma_vector,axis=1)
        for i in range(0,test_images.shape[0]):
            cluster_labels = self.train_labels[self.predict_indexs == predict_test_indexs[i]]
            mode_result = mode(cluster_labels)
            predict_label = mode_result.mode[0] 
            #print(i)
            if predict_label == test_labels[i]:
                correct_sum += 1
        
        accuracy = correct_sum / test_images.shape[0]
        self.test_accuracies.append(accuracy)
        return accuracy

    def plot_accuracies(self,title,ax):
        n=range(int(self.max_iter/5)+1)
        x_list = [i * 5 for i in n]
        print(x_list)
        ax.plot(x_list, self.test_accuracies, marker='o')
        ax.set_xlabel('Iteration')  # 设置x轴标签
        ax.set_ylabel('Test Accuracy')  # 设置y轴标签
        ax.set_title(title)  # 设置图表标题
        plt.grid(True)

    

if __name__=='__main__':
    
    np.random.seed(6)
    # 提取数据
    train_df = pd.read_csv('.\material\mnist_train.csv', header=None, skiprows=1)
    test_df = pd.read_csv('.\material\mnist_test.csv', header=None, skiprows=1)
    train_labels = train_df.iloc[:, 0].astype(int).values
    train_images = train_df.iloc[:, 1:].astype(int).values
    test_labels = test_df.iloc[:, 0].astype(int).values
    test_images = test_df.iloc[:, 1:].astype(int).values
    print(test_images.shape)

    pca=PCA()
    pca.fit(train_images,60)
    train_images=pca.transform(train_images)
    test_images=pca.transform(test_images)
    print(test_images.shape)

    kmeans_random=Kmeans(10,50,train_labels=train_labels,train_images=train_images)
    start_time = time.time()
    kmeans_random.init_center_distance()
    kmeans_random.train(test_images=test_images,test_labels=test_labels)
    end_time = time.time()
    training_duration = end_time - start_time
    print(f"训练过程耗时 {training_duration:.2f} 秒")
    print(f"final test accruacy: {kmeans_random.test(test_labels=test_labels,test_images=test_images)}")
    kmeans_random.plot_accuracies("init_random_distance_K_means_Accuracies")


    kmeans_center=Kmeans(10,50,train_labels=train_labels,train_images=train_images)
    start_time = time.time()
    kmeans_center.init_center_distance()
    kmeans_center.train(test_images=test_images,test_labels=test_labels)
    end_time = time.time()
    training_duration = end_time - start_time
    print(f"训练过程耗时 {training_duration:.2f} 秒")
    print(f"final test accruacy: {kmeans_center.test(test_labels=test_labels,test_images=test_images)}")
    kmeans_center.plot_accuracies("init_center_distance_K_means_Accuracies")
    
    fig,ax=plt.subplots(2,2)
    start_time = time.time()
    gmm0=GMM(train_images=train_images,k=10,max_iter=100,train_labels=train_labels,means_init_method=0,cov_init_method=0)
    gmm0.EM_train(test_images,test_labels)
    end_time = time.time()
    training_duration = end_time - start_time
    print(f"训练过程耗时 {training_duration:.2f} 秒")
    print(f"final test accruacy: {gmm0.test(test_labels=test_labels,test_images=test_images)}")
    gmm0.plot_accuracies("0",ax[0][0])

    start_time = time.time()
    gmm1=GMM(train_images=train_images,k=10,max_iter=100,train_labels=train_labels,means_init_method=0,cov_init_method=1)
    gmm1.EM_train(test_images,test_labels)
    end_time = time.time()
    training_duration = end_time - start_time
    print(f"训练过程耗时 {training_duration:.2f} 秒")
    print(f"final test accruacy: {gmm1.test(test_labels=test_labels,test_images=test_images)}")
    gmm1.plot_accuracies("1",ax[0][1])

    start_time = time.time()
    gmm2=GMM(train_images=train_images,k=10,max_iter=100,train_labels=train_labels,means_init_method=1,cov_init_method=0)
    gmm2.EM_train(test_images,test_labels)
    end_time = time.time()
    training_duration = end_time - start_time
    print(f"训练过程耗时 {training_duration:.2f} 秒")
    print(f"final test accruacy: {gmm2.test(test_labels=test_labels,test_images=test_images)}")
    gmm2.plot_accuracies("1",ax[1][0])

    start_time = time.time()
    gmm3=GMM(train_images=train_images,k=10,max_iter=100,train_labels=train_labels,means_init_method=1,cov_init_method=1)
    gmm3.EM_train(test_images,test_labels)
    end_time = time.time()
    training_duration = end_time - start_time
    print(f"训练过程耗时 {training_duration:.2f} 秒")
    print(f"final test accruacy: {gmm3.test(test_labels=test_labels,test_images=test_images)}")
    gmm3.plot_accuracies("1",ax[1][1])

    plt.show()




