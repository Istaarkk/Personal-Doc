section .text
global my_mul_arrays

my_mul_arrays:

    xor eax, eax        
    mov ecx, 4          

.loop:
    mov edx, [rdi]      
    imul edx, [rsi]     
    add eax, edx        

    add rdi, 4          
    add rsi, 4          

    dec ecx             
    jnz .loop           

    ret                 
