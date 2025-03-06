section .text

global my_average

my_average:

	MOV RAX,RDI
	ADD RAX,RSI
	ADD RAX,RDX
	ADD RAX,RCX

	MOV RDX,0
	MOV RDI,4

	DIV RDI

	RET

	
	
