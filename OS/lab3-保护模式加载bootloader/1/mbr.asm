org 0x7c00
[bits 16]
xor ax, ax ; eax = 0
; 初始化段寄存器, 段地址全部设为0
mov ds, ax
mov ss, ax
mov es, ax
mov fs, ax
mov gs, ax

; 初始化栈指针
mov sp, 0x7c00
mov ax, 1                ; 逻辑扇区号第0~15位
mov cx, 0                ; 逻辑扇区号第16~31位
mov bx, 0x7e00           ; bootloader的加载地址   mbr从0x7c00开始,占512bit，则bootloader从这个位置开始
load_bootloader:
    call asm_read_hard_disk  ; 读取硬盘
    inc ax
    cmp ax, 5            ;读五个扇区
    jle load_bootloader  ;计数器没到就继续读
jmp 0x0000:0x7e00        ; 跳转到bootloader

jmp $ ; 死循环

asm_read_hard_disk:                           
; 从硬盘读取一个逻辑扇区

; 参数列表
; ax=逻辑扇区号0~15位
; cx=逻辑扇区号16~28位
; ds:bx=读取出的数据放入地址

; 返回值
; bx=bx+512

    mov dx, 0x1f3
    out dx, al    ; LBA地址7~0

    inc dx        ; 0x1f4
    mov al, ah
    out dx, al    ; LBA地址15~8

    mov ax, cx

    inc dx        ; 0x1f5
    out dx, al    ; LBA地址23~16

    inc dx        ; 0x1f6
    mov al, ah
    and al, 0x0f   ;g高四位清空
    or al, 0xe0   ; LBA地址27~24，高四位设置为1110
    out dx, al

    mov dx, 0x1f2
    mov al, 1     ;输入读的扇区数
    out dx, al   ; 读取1个扇区

    mov dx, 0x1f7    ; 0x1f7
    mov al, 0x20     ;读命令
    out dx,al  

    ; 等待处理其他操作
  .waits:
    in al, dx        ; dx = 0x1f7
    and al,0x88         
    cmp al,0x08      ;要等到端口信息允许可读
    jnz .waits                         
    

    ; 读取512字节到地址ds:bx
    mov cx, 256   ; 每次读取一个字，2个字节，因此读取256次即可          
    mov dx, 0x1f0
  .readw:
    in ax, dx
    mov [bx], ax
    add bx, 2  
    loop .readw
      
    ret

times 510 - ($ - $$) db 0
db 0x55, 0xaa
