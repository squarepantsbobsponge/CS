import torch#载入模块torch
print(torch.__version__)#输出版本
x = torch.rand(5, 3)#测试运算
print(x)
print(torch.cuda.is_available())#测试是否支持cuda,ture是支持，否则仅CPU