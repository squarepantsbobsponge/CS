#include <iostream>

extern "C" void function_from_asm();//禁用C++名称修饰

int main() {
    std::cout << "Call function from assembly." << std::endl;
    function_from_asm();
    std::cout << "Done." << std::endl;
}