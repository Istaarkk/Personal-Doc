section .text

global my_fillstruct

my_fillstruct:
	mov[rdi],rsi
	
	sub rsp,8
	movsd[rsp],xmm0
	fld qword[rsp]
	fstp qword[rdi+8]

	
	add rsp,8
	ret
