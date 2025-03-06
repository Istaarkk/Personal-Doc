section .text

global my_bsr

my_bsr:
	
	XOR RAX,RAX
	BSR RAX,RDI
	RET
