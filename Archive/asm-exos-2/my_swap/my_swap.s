section .text

global my_swap

my_swap:
	
	mov rax, [rdi]    
	mov rcx, [rsi]    
	mov [rdi], rcx    
	mov [rsi], rax
    
	RET


