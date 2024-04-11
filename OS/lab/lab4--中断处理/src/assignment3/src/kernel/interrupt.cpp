#include "interrupt.h"
#include "os_type.h"
#include "os_constant.h"
#include "asm_utils.h"

InterruptManager::InterruptManager()
{
    initialize();
}

void InterruptManager::initialize()
{
    // 初始化IDT
    IDT = (uint32 *)IDT_START_ADDRESS;//IDT位置设置在08880
    asm_lidt(IDT_START_ADDRESS, 256 * 8 - 1);//初始化IDT
    setInterruptDescriptor(0, (uint32)asm_DZE_interrupt, 0);//除0错误的中断处理函数
    for (uint i = 1; i < 256; ++i)
    {
        setInterruptDescriptor(i, (uint32)asm_unhandled_interrupt, 0);
    }//放置默认中断符 i:第几个中断描述符,中断处理程序的偏移,特权级

}

void InterruptManager::setInterruptDescriptor(uint32 index, uint32 address, byte DPL)
{
    // 中断描述符的低32位
    IDT[index * 2] = (CODE_SELECTOR << 16) | (address & 0xffff); //只要偏移量的0-15位，address&运算高位置0，保留地位//高16位段选择子，或运算出来
    // 中断描述符的高32位
    IDT[index * 2 + 1] = (address & 0xffff0000) | (0x1 << 15) | (DPL << 13) | (0xe << 8);//设置高32位//处理程序是同一个，地址都一样，直接传函数名也算传地址了
    //IDT是中断符号表的基地址，每个中断符号的大小都是两个uint32，这里2的单位是uint32，实际上位移8个字节，64bit
}
