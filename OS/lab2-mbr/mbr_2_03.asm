[org 0x7c00]
[bits 16]
Input:
    mov ah, 0      ; 键盘输入
    int 16h          ; 中断
     cmp al, '$'   ;如果是'$'就退出
     je Exit
    mov ah, 9        ;  
    mov bh, 0
    mov bl, 5        ;颜色为红色
    mov cx, 1
    int 10h          ; 显示
    call move 
    jmp Input            ; 死循环
get:
push cx ;这里修改了cx，所以要压栈，后面还要恢复的
mov ah, 3        ; 中断获取光标位置
mov bh, 0        ; 页号为0
int 10h          ; 中断
pop cx
ret

move:
call get
mov ah, 2        ; 中断将光标移动到新位置
mov bh, 0        ; 页号为0
inc dl       ; 列号
int 10h          ; 中断
ret

Exit:
times 510-($-$$) db 0
dw 0xaa55          ; 主引导记录标志
