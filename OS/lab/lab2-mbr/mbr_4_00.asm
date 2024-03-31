;org 0x7c00将程序起始地址设为物理内存地址0x7c00
[bits 16]
xor ax,ax; eax=0
xor bx,bx;
xor cx,cx;
xor dx,dx;
;初始化段寄存器
mov ds, ax
mov ss, ax
mov es, ax
mov fs, ax
mov gs, ax
;初始化栈指针
mov sp, 0x7c00;MBR从这里开始放
mov ax, 0xb800;显存地址
mov gs, ax
;

mov cx,12 ;行
mov dx,0  ;列



Loop1:;右上
call Get_num
push bx;压栈用于计算容器
xor bx,bx;
;bx既是计算的容器，也是生成随机数的计数器
call delay_loop;用函数实现延迟
imul bx,cx,80
add bx,dx
imul bx, 2
mov ah,bl;随即生成颜色
mov [gs:bx], ax
pop bx
inc bx;出栈回归计数器
cmp dx, 79
jge Loop3
inc dx
cmp cx, 0
je Loop2
dec cx
jmp Loop1

delay_loop:
  push cx
  push dx
  mov cx, 0xFFFF  ; 设置循环次数，可以根据需要调整
delay_outer:
  mov dx, 0xFFF  ;设置内部循环次数，可以根据需要调整
delay_inner:
  dec dx          ; 内部循环计数器递减
  jnz delay_inner ; 如果内部计数器不为零，则继续内部循环
  dec cx          ; 外部循环计数器递减
  jnz delay_outer ; 如果外部计数器不为零，则继续外部循环
  pop dx
  pop cx
  ret    
    

Loop2:;右下
call Get_num
push bx;压栈用于计算容器
;bx既是计算的容器，也是生成随机数的计数器
xor bx,bx;
call delay_loop;
imul bx,cx,80
add bx,dx
imul bx, 2
mov ah,bl
mov [gs:bx], ax
pop bx
inc bx;出栈回归计数器
cmp dx, 79
jge Loop4
inc dx
cmp cx, 24
je Loop1
inc cx
jmp Loop2

Loop3:;左上
call Get_num
push bx;压栈用于计算容器
xor bx,bx;
;bx既是计算的容器，也是生成随机数的计数器
dec dx
call delay_loop;
imul bx,cx,80
add bx,dx
imul bx, 2
mov ah,bl

mov [gs:bx], ax
pop bx
inc bx;出栈回归计数器
cmp dx, 0
je Exit
cmp cx, 0
je Loop4
dec cx
jmp Loop3

Loop4:;左下
call Get_num
push bx;压栈用于计算容器
;bx既是计算的容器，也是生成随机数的计数器
xor bx,bx;
dec dx
call delay_loop;
imul bx,cx,80
add bx,dx
imul bx, 2
mov ah,bl

mov [gs:bx], ax
pop bx
inc bx;出栈回归计数器
cmp dx, 0
je Exit
cmp cx, 24
je Loop3
inc cx
jmp Loop4
;

Get_num:
 cmp bl, 10
 jl Next
 mov bl,0
 Next:
 mov al, '0'
 add al,bl
 ret

Exit:
jmp $ ; 死循环

times 510 - ($ - $$) db 0
db 0x55, 0xaa



;实现效果两条字符弹射而出不知道为什么
