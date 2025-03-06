section .text
global my_strcat

my_strcat:
    push rdi        

.end:
    mov al, [rdi]   
    test al, al     
    jz .loop      
    inc rdi         
    jmp .end   

.loop:
    mov al, [rsi]   
    mov [rdi], al   
    inc rsi         
    inc rdi         
    test al, al     
    jnz .loop     

    pop rax         
    ret             
