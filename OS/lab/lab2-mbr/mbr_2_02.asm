;[org 0x7c00]
[bits 16]
;在当前光标处输出学号
mov cx, 8
mov sp, 0x7c00
mov si, sp
print_num:
    mov ah, 9  
    mov bh, 0
    mov bl, 1
    mov al, [si + string]
    int 10h
    inc si
    call move
    loop print_num
string db '22336057'
; 获取当前光标位置
call move
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



jmp $            ; 
;string db '22336057'
times 510-($-$$) db 0
dw 0xaa55        ; 