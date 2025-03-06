section .text
    global my_strrev
    extern malloc, strlen

my_strrev:
    push rbp
    mov rbp, rsp

    mov rdi, rdi
    call strlen

    mov rsi, rax
    inc rsi
    mov rdi, rsi
    call malloc

    mov rdx, rax
    dec rsi
    mov rcx, rsi
    mov rbx, rdi            ; pointeur chaine source

.reverse_loop:
    cmp rcx, -1
    jl .copy_done

    mov al, [rbx + rcx]     
    mov [rdx + rsi - rcx - 1], al 

    dec rcx
    jmp .reverse_loop

.copy_done:
    mov byte [rdx + rsi], 0  ; fin de ligne'\0'

    mov rax, rdx

    leave
    ret
