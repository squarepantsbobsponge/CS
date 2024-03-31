org 0x7e00
[bits 16]
mov ax, 0xb800
mov gs, ax
mov ah, 0x03 ;青色
mov ecx, bootloader_tag_end - bootloader_tag ;计数长度为字符串长度
xor ebx, ebx
mov esi, bootloader_tag ;加载字符串的地址
output_bootloader_tag:
    mov al, [esi]
    mov word[gs:bx], ax
    inc esi
    add ebx,2
    loop output_bootloader_tag
jmp $ ; 死循环 ；打印字符串

bootloader_tag db 'run bootloader' ;定义字符串
bootloader_tag_end:;标记字符串的结束位置