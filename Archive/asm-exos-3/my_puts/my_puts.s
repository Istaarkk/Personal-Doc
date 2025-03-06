section .data
    newline db 0xA

section .text
global my_puts

my_puts:
    test rdi, rdi
    jz end

    xor rdx, rdx

find_end:
    cmp byte [rdi + rdx], 0
    je  write_string
    inc rdx
    jmp find_end

write_string:
    mov rax, 1
    mov rdi, 1
    mov rsi, rdi
    mov rdx, rdx
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall

end:
    xor rax, rax
    ret
