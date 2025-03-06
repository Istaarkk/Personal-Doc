#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <ctype.h>

//reprogramation de Strlen
size_t my_strlen(const char *str) {
    size_t length = 0;
    
    while (str[length] != '\0') {
        length++;
    }
    
    return length;
}
//ajoute les chaines de caractère entre elle
static void append_str(char** dest, const char* src, size_t* size, size_t* cap) {
    size_t src_len = my_strlen(src);
    if (*size + src_len + 1 >= *cap) {
        *cap = (*cap + src_len + 1) * 2;
        *dest = realloc(*dest, *cap);
        if (*dest == NULL) {
            exit(1);
        }
    }
    strcat(*dest, src);
    *size += src_len;
}
//permet de traiter les chaine qui commence par '{'ainsi que l'indice a gérer pour avoir le bon argument 
static void get_index_placeholder(va_list* args, const char** p, char** res, size_t* size, size_t* cap) {
    int index = 0;
    while (isdigit(**p)) {
        index = index * 10 + (**p - '0');
        (*p)++;
    }

    if (**p == '}') {
        (*p)++;
        va_list args_copy;
        va_copy(args_copy, *args);
        
        for (int i = 0; i < index; i++) {
            va_arg(args_copy, char*);
        }
        
        char* arg = va_arg(args_copy, char*);
        va_end(args_copy);

        if (arg) {
            append_str(res, arg, size, cap);
        }
    } 
    
    else {
        append_str(res, "{", size, cap);
    }
}
//fonction principal génére une chaine de caractere formater
char* my_gen_str(char * const format_string, ...) { //nbr varaible d'args 
    size_t size = 0, cap = 128;
    char* res = malloc(cap);
    if (!res) {
        return NULL;
    }
    res[0] = '\0';

    va_list args;
    va_start(args, format_string);

    const char* p = format_string;
    while (*p) {
        if (*p == '{') {
            p++;
            if (*p == '{') {
                append_str(&res, "{", &size, &cap);
                p++;
            } 
            
            else {
                get_index_placeholder(&args, &p, &res, &size, &cap);
            }
        } 
        
        else {
            char buffer[2] = {*p, '\0'};
            append_str(&res, buffer, &size, &cap);
            p++;
        }
    }

    va_end(args);
    return res;
}
