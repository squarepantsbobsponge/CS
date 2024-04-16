#include <unistd.h>
#include<stdio.h>
#include<pthread.h>
#include <stdlib.h> 
//全局变量
int aver=0;
int min=1000;
int max=-1;

void* average(void* data){
   int num=*((int*)data);
   int* data_int=(int*)data;
   //int sum=0;
   int i=1;
   for(i=1;i<num+1;i++){
    aver+=data_int[i];
   }
   aver/=num;
   pthread_exit(NULL);
}
void* max_my(void* data){
   int num=*((int*)data);
     int* data_int=(int*)data;
   //int sum=0;
   int i=1;
   int tmp;
   for(i=1;i<num+1;i++){
    tmp=data_int[i];
    if(tmp>max) max=tmp;
   }
   pthread_exit(NULL);
}
void* min_my(void* data){
   int num=*((int*)data);
      int* data_int=(int*)data;
   //int sum=0;
   int i=1;
   int tmp;
   for(i=1;i<num+1;i++){
    tmp=data_int[i];
    if(tmp<min) min=tmp;
   }
   pthread_exit(NULL);
}
int main(int argc,char* argv[]){
    //输入
    //int num[100];//传参最大数量100
    int data[100];
    data[0]=argc-1;//开头第一个放个数
    int i=1;
    for(i=1;i<argc;i++){
      data[i]=atoi(argv[i]);//转为数字
    }
    pthread_t tid;
     pthread_create(&tid, NULL, average,(void* )data);
     
         pthread_t tid2;
     pthread_create(&tid2, NULL, max_my,(void* )data);
  
         pthread_t tid3;
     pthread_create(&tid3, NULL, min_my,(void* )data);
         pthread_join(tid,NULL);
            pthread_join(tid2,NULL);
        pthread_join(tid3,NULL);
    printf("average=%d\n",aver);
    printf("min=%d\n",min);
    printf("max=%d\n",max);
}