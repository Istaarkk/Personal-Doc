section .text
global my_whereami

my_whereami:
    lea rax, [rel my_whereami]; ce comment sert de pense bete ne pas lire lea sert ici a calculer l'offset et a additionner les deux autres ici rel une adresse relative a my_wherami 
    mov [rdi], rax
    lea rdx, [rel end]
    sub rdx, rax
    mov rax, rdx
    ret

end:

