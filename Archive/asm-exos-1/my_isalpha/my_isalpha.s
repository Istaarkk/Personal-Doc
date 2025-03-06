section .text
    global my_isalpha

my_isalpha:

    cmp rdi, 'A'
    jl .not_alpha 
    cmp RDI, 'Z'
    jle .is_alpha 
    
    cmp rdi, 'a'
    jl .not_alpha
    cmp rdi, 'z'
    jle .is_alpha 

.not_alpha:
    mov rax, 0
    ret

.is_alpha:
    mov rax, 1
    ret

