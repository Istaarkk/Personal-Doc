section .text

global my_strlen

my_strlen:
    xor rax, rax       


.loop:
    cmp byte [rdi + rax], 0  
    je .end            
    inc rax           
    jmp .loop         


.end:
    ret     
