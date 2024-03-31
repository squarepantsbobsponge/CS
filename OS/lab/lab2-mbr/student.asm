; If you meet compile error, try 'sudo apt install gcc-multilib g++-multilib' first

%include "head.include"
; you code here

your_if:
    push ebx
    mov eax, [a1]          ; 将 a1加载到 eax 中直接寻址

    cmp eax, 12            ; a1 小于 12
    jl less_than_12        

    cmp eax, 24            ; a1 小于 24
    jl less_than_24         

    shl eax, 4             ; a1 大于等于 24
    jmp end_if              

less_than_12:
    shr eax, 1             ; 将 eax 右移 1 位
    add eax, 1             ; 然后加 1
    jmp end_if             

less_than_24:
    mov ebx, 24            ; 将 24 存储到 ebx 中
    sub ebx, eax           ; 计算 (24 - a1)
    imul eax, ebx          ; 将 eax 乘以 ebx 的值
    jmp end_if             

end_if:
    mov [if_flag], eax     ; 将 eax 的值存储到 if_flag 中S
    pop ebx
  ;  ret                    

; put your implementation here

your_while:
   
    cmp  dword[a2], 12     ; a2 大于等于 12
    jl student_function_end        ; 小于 12
    mov ecx, [a2]          ; a2存储到 ebx 中
    sub ecx, 12            ; while_flag 的偏移量
    mov ebx, [while_flag]
    add ebx,ecx
   call my_random         ; 调用 my_random 函数生成随机数，返回值存储在 eax 中
   mov [ebx], al  ; 将随机数存储到 while_flag 数组中对应的位置
   dec dword [a2]         ; a2 减一
   jmp your_while         ; 继续循环

;end_while:
 ; ret 
;put your implementation here

%include "end.include"

your_function:
    pushad
    xor ecx, ecx           ; 使用 ecx 寄存器作为循环计数器，初始化为0
   mov esi, [your_string]       ; 将字符串地址存储到 esi 寄存器中,your_string是指针地址的地址，要间接寻址

for_loop:
    mov al, byte[esi + ecx]  ; 读取字符串中的一个字符到 eax 寄存器
    test al, al             ; 检查字符是否为 '\0'
    jz end_for              ; 如果是 '\0'

    pushad                  ; 保存通用寄存器的值
    push ax                ; 将字符压入栈中
    call print_a_char       ; 调用打印字符的函数
    add esp, 2              ; 栈指针恢复，弹出字符

    popad                   ; 恢复通用寄存器的值
    inc ecx                 ; 循环计数器加一
    jmp for_loop            ; 继续循环

end_for:
popad
ret
; put your implementation here
