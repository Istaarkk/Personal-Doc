section .text
global my_factorial

my_factorial:
    push rbp
    mov rbp, rsp

    mov rax, 1
    
    cmp rdi, 0
    je fin

start:
    imul rax, rdi
    
    dec rdi
   
    cmp rdi, 1
    jne start

fin:
    pop rbp
    ret
