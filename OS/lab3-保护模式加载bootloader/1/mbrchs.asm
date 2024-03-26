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
mov bx, 0x7e00           ; bootloader的加载地址   mbr从0x7c00开始,占512bit，则bootloader从这个位置开始
load_bootloader:
    call asm_read_hard_disk  ; 读取硬盘
jmp 0x0000:0x7e00        ; 跳转到bootloader

jmp $ ; 死循环

asm_read_hard_disk:          ;一次性读5个扇区                    
      
    mov bx,0x7e00
    mov al,5  ;五个扇区
    mov ch,0    
    mov cl,2   ;扇区号从2开始
    mov dh,0
    mov dl,80h  ;??
    
    mov ah,2
    int 13h
    
    ret



times 510 - ($ - $$) db 0
db 0x55, 0xaa 