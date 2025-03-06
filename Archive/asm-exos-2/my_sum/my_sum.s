section .text

global my_sum

my_sum:

	add rdi,rsi
	add rdi,rdx
	add rdi,rcx
	add rdi,r8
	add rdi,r9

	add rdi, [rsp+8]

	mov rax,rdi

	ret
