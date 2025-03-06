section .text
global my_strdup
extern malloc
extern strlen

my_strdup:
    push rbp
    mov rbp, rsp
    push rdi
    call strlen wrt ..plt   
    inc rax
    mov rdi, rax
    call malloc wrt ..plt   
    test rax, rax           
    jz .error               
    mov rdi, rax            
    pop rsi                

.copy_loop:
    mov cl, [rsi]          
    mov [rdi], cl          
    inc rsi                
    inc rdi                
    test cl, cl            
    jnz .copy_loop         

    mov rax, rax           
    leave
    ret

.error:
    xor rax, rax           
    leave
    ret

