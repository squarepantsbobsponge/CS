[bits 32]

global asm_hello_world
global asm_lidt
global asm_DZE_interrupt
global asm_unhandled_interrupt
global asm_halt

ASM_UNHANDLED_INTERRUPT_INFO db 'Unhandled interrupt happened, halt...'
                             db 0
ASM_DZE_INTERRUPT_INFO db 'DZE: division by zero error, halt...'
                             db 0
ASM_IDTR dw 0  ;定义寄存器的开始 ，一个字
         dd 0   ;双字

;除0中断处理函数
asm_DZE_interrupt:
    cli   ;关中断
    mov esi, ASM_DZE_INTERRUPT_INFO  ;将字符串地址放在esi中
    xor ebx, ebx
    mov ah, 0x03   ;int 3中断
.output_information:  ;输出字符
    cmp byte[esi], 0
    je .end
    mov al, byte[esi]
    mov word[gs:bx], ax
    inc esi
    add ebx, 2
    jmp .output_information
.end:
    jmp $     ;死循环，不返回开中断了


; void asm_unhandled_interrupt()
asm_unhandled_interrupt:
    cli   ;关中断
    mov esi, ASM_UNHANDLED_INTERRUPT_INFO  ;将字符串地址放在esi中
    xor ebx, ebx
    mov ah, 0x03   ;int 3中断
.output_information:  ;输出字符
    cmp byte[esi], 0
    je .end
    mov al, byte[esi]
    mov word[gs:bx], ax
    inc esi
    add ebx, 2
    jmp .output_information
.end:
    jmp $     ;死循环，不返回开中断了
; void asm_lidt(uint32 start, uint16 limit)
asm_lidt:
    push ebp
    mov ebp, esp;栈顶指针
    push eax  ;0x8800IDT地址

    mov eax, [ebp + 4 * 3];先取出界限（256*8-1），16位为什么是4*3;字节为单位的移动；一个参数四个字节，传了三个参数，有个也压进去栈帧参数
    mov [ASM_IDTR], ax    ;放在低16位
    mov eax, [ebp + 4 * 2];再取出0x8800IDT地址
    mov [ASM_IDTR + 2], eax;放在16-47;2的单位是字节，8bit 共16bit的偏移,前16bit放界限
    lidt [ASM_IDTR];初始化IDT

    pop eax;恢复寄存器
    pop ebp
    ret

asm_hello_world:
    push eax
    xor eax, eax

    mov ah, 0x03 ;青色
    mov al, 'H'
    mov [gs:2 * 0], ax

    mov al, 'e'
    mov [gs:2 * 1], ax

    mov al, 'l'
    mov [gs:2 * 2], ax

    mov al, 'l'
    mov [gs:2 * 3], ax

    mov al, 'o'
    mov [gs:2 * 4], ax

    mov al, ' '
    mov [gs:2 * 5], ax

    mov al, 'W'
    mov [gs:2 * 6], ax

    mov al, 'o'
    mov [gs:2 * 7], ax

    mov al, 'r'
    mov [gs:2 * 8], ax

    mov al, 'l'
    mov [gs:2 * 9], ax

    mov al, 'd'
    mov [gs:2 * 10], ax

    pop eax
    ret

asm_halt:
    jmp $
