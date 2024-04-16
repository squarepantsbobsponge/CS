# 声明要求的 cmake 最低版本
cmake_minimum_required(VERSION 2.8)
set(CMAKE_CXX_STANDARD 11)

project(TEST)
# 查找Python3库  
find_package(Python3 COMPONENTS Interpreter Development)  
  
# 设置Python头文件路径（通常不需要手动设置，find_package会帮你做这件事）  
# 如果find_package没有正确找到，你可以手动设置  
 set(PYTHON_INCLUDE_DIRS "/usr/include/python3.8")  
  
# 添加头文件到工程  
include_directories(${PYTHON_INCLUDE_DIRS})  
  
# 添加一个可执行程序  
add_executable(test main.cpp APF.cpp APF.h)  
  
# 链接Python库到工程  
target_link_libraries(test PRIVATE ${Python3_LIBRARIES})


