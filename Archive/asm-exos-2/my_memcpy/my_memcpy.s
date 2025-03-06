section .text

global my_memcpy

my_memcpy:

	mov rcx,rdx
	mov rax,rdi

	rep movsb

	ret 
