section .text
global my_countv

my_countv:

    push rbp
    mov rbp, rsp
    xor rcx, rcx        

    xor eax, eax
    mov [rdx], eax
    mov [rdx+4], eax
    mov [rdx+8], eax
    mov [rdx+12], eax
    mov [rdx+16], eax
    mov [rdx+20], eax

.loop:
    cmp rcx, rsi        
    jge .end

    movzx eax, byte [rdi + rcx]  
    
    cmp al, 'a'
    je .count_a
    cmp al, 'e'
    je .count_e
    cmp al, 'i'
    je .count_i
    cmp al, 'o'
    je .count_o
    cmp al, 'u'
    je .count_u
    cmp al, 'y'
    je .count_y
    jmp .next_char

.count_a:
    inc dword [rdx]
    jmp .next_char
.count_e:
    inc dword [rdx+4]
    jmp .next_char
.count_i:
    inc dword [rdx+8]
    jmp .next_char
.count_o:
    inc dword [rdx+12]
    jmp .next_char
.count_u:
    inc dword [rdx+16]
    jmp .next_char
.count_y:
    inc dword [rdx+20]

.next_char:
    inc rcx
    jmp .loop

.end:
    pop rbp
    ret
