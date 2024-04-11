#include <iostream>


extern "C" void function_from_CPP() {//规定产生的函数名为这个，便于汇编代码定位
    std::cout << "This is a function from C++." << std::endl;
}