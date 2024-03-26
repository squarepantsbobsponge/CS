%include "boot.inc"
org 0x7e00
[bits 16]
mov ax, 0xb800
mov gs, ax
mov ah, 0x03 ;青色
mov ecx, bootloader_tag_end - bootloader_tag
xor ebx, ebx
mov esi, bootloader_tag
output_bootloader_tag:
    mov al, [esi]
    mov word[gs:bx], ax
    inc esi
    add ebx,2
    loop output_bootloader_tag

;空描述符
mov dword [GDT_START_ADDRESS+0x00],0x00
mov dword [GDT_START_ADDRESS+0x04],0x00  

;创建描述符，这是一个数据段，对应0~4GB的线性地址空间
mov dword [GDT_START_ADDRESS+0x08],0x0000ffff    ; 基地址为0，段界限为0xFFFFF
mov dword [GDT_START_ADDRESS+0x0c],0x00cf9200    ; 粒度为4KB，存储器段描述符 

;建立保护模式下的堆栈段描述符      
mov dword [GDT_START_ADDRESS+0x10],0x00000000    ; 基地址为0x00000000，界限0x0 
mov dword [GDT_START_ADDRESS+0x14],0x00409600    ; 粒度为1个字节

;建立保护模式下的显存描述符   
mov dword [GDT_START_ADDRESS+0x18],0x80007fff    ; 基地址为0x000B8000，界限0x07FFF 
mov dword [GDT_START_ADDRESS+0x1c],0x0040920b    ; 粒度为字节

;创建保护模式下平坦模式代码段描述符
mov dword [GDT_START_ADDRESS+0x20],0x0000ffff    ; 基地址为0，段界限为0xFFFFF
mov dword [GDT_START_ADDRESS+0x24],0x00cf9800    ; 粒度为4kb，代码段描述符 

;初始化描述符表寄存器GDTR
mov word [pgdt], 39      ;描述符表的界限   
lgdt [pgdt]
      
in al,0x92                         ;南桥芯片内的端口 
or al,0000_0010B
out 0x92,al                        ;打开A20

cli                                ;中断机制尚未工作
mov eax,cr0
or eax,1
mov cr0,eax                        ;设置PE位
      
;以下进入保护模式
jmp dword CODE_SELECTOR:protect_mode_begin

;16位的描述符选择子：32位偏移
;清流水线并串行化处理器
[bits 32]           
protect_mode_begin:                              

mov eax, DATA_SELECTOR                     ;加载数据段(0..4GB)选择子
mov ds, eax
mov es, eax
mov eax, STACK_SELECTOR
mov ss, eax
mov eax, VIDEO_SELECTOR
mov gs, eax

mov ecx, protect_mode_tag_end - protect_mode_tag
mov ebx, 80 * 2
mov esi, protect_mode_tag
mov ah, 0x3
output_protect_mode_tag:
    mov al, [esi]
    mov word[gs:ebx], ax
    add ebx, 2
    inc esi
    loop output_protect_mode_tag

xor ax,ax; eax=0
xor ebx,ebx;
xor ecx,ecx;
xor edx,edx;
mov ecx,12 ;行
mov edx,0  ;列

Loop1:;右上
call Get_num
push ebx
xor ebx,ebx
call sleep
imul ebx,ecx,80
add  ebx,edx
imul ebx, ebx,2
mov ah,bl;随即生成颜色
mov word[gs:ebx], ax
pop ebx
inc ebx;出栈回归计数器
cmp edx, 79
jge Loop3
;jge Exit
inc edx
cmp ecx, 0
je Loop2
;je Exit
dec ecx
jmp Loop1

Loop2:;右下
call Get_num
push ebx;压栈用于计算容器
;bx既是计算的容器，也是生成随机数的计数器
xor ebx,ebx;
call sleep;
imul ebx,ecx,80
add ebx,edx
imul ebx, 2
mov ah,bl
mov word[gs:ebx], ax
pop ebx
inc ebx;出栈回归计数器
cmp edx, 79
jge Loop4
;jge Exit
inc edx
cmp ecx, 24
je Loop1
inc ecx
jmp Loop2

Loop3:;左上
call Get_num
push ebx;压栈用于计算容器
xor ebx,ebx;
;bx既是计算的容器，也是生成随机数的计数器
dec edx
call sleep;
imul ebx,ecx,80
add ebx,edx
imul ebx, 2
mov ah,bl
;mov al,bh
mov word[gs:ebx], ax
pop ebx
inc ebx;出栈回归计数器
cmp edx, 0
je Exit
cmp ecx, 0
je Loop4
je Exit
dec ecx
jmp Loop3

Loop4:;左下
call Get_num
push ebx;压栈用于计算容器
;bx既是计算的容器，也是生成随机数的计数器
xor ebx,ebx;
dec edx
call sleep;
imul ebx,ecx,80
add ebx,edx
imul ebx, 2
mov ah,bl
;mov al,bh
mov word[gs:ebx], ax
pop ebx
inc ebx;出栈回归计数器
cmp edx, 0
je Exit
cmp ecx, 24
je Loop3
inc ecx
jmp Loop4

sleep:
  pushad
  mov ecx, 0xFFF  ; 设置循环次数，可以根据需要调整
delay_outer:
  mov edx, 0xFFF ;设置内部循环次数，可以根据需要调整
delay_inner:
  dec edx          ; 内部循环计数器递减
  jnz delay_inner ; 如果内部计数器不为零，则继续内部循环
  dec ecx          ; 外部循环计数器递减
  jnz delay_outer ; 如果外部计数器不为零，则继续外部循环
  popad
  ret

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

pgdt dw 0
     dd GDT_START_ADDRESS

bootloader_tag db 'run bootloader'
bootloader_tag_end:

protect_mode_tag db 'enter protect mode'
protect_mode_tag_end: