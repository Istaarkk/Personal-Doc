section .text
global my_max

my_max:
    mov rax, rdi    

    cmp rsi, rax     
    cmovg rax, rsi    

    cmp rdx, rax       
    cmovg rax, rdx      

    ret                  

