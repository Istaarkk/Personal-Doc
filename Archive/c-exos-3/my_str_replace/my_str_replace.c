#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "my_str_replace.h"

int my_strlen(char const str[]) {
    int i = 0;
    while (str[i] != '\0') {
        ++i;
    }
    return i;
}

char *my_strcpy(char *dest, const char *src) {
    int i = 0;
    while (src[i]) {
        dest[i] = src[i];
        i += 1;
    }
    dest[i] = '\0';
    return dest;
}

char *my_strcat(char *dest, const char *src) {
    int len;
    int i;
    len = my_strlen(dest);
    i = 0;
    while (src[i]) {
        dest[len + i] = src[i];
        i += 1;
    }
    dest[len + i] = '\0';
    return dest;
}

char* my_strncat(char *dest, const char *src, size_t n) {
    size_t dest_len = my_strlen(dest);
    size_t i;

    for (i = 0; i < n && src[i] != '\0'; i++) {
        dest[dest_len + i] = src[i];
    }
    dest[dest_len + i] = '\0';

    return dest;
}
//permet de remplacé les chaines sans utilisé les précédezntes 
static char *replace_without_old_pat(const char *str, const char *new_pat) {
    size_t len_str = my_strlen(str);
    size_t len_new_pat;
    char *result;

    if (new_pat) {
        len_new_pat = my_strlen(new_pat);
    } 
    
    
    else {
        len_new_pat = 0;
    }

    size_t new_len = len_str + len_new_pat * (len_str + 1);
    result = malloc(new_len + 1);

    if (!result) {
        return NULL;
    }

    result[0] = '\0';
    for (size_t i = 0; i < len_str; ++i) {
        if (new_pat) {
            my_strcat(result, new_pat);
        }
        
        my_strncat(result, &str[i], 1);
    }
    if (new_pat) {
        my_strcat(result, new_pat);
    }

    return result;
}
//compte les occurence d'un motif de chaine 
static size_t occurrences(const char *str, const char *old_pat) {
    size_t count = 0;

    for (const char *p = str; (p = strstr(p, old_pat)); p += my_strlen(old_pat)) {
        count++;
    }
    return count;
}
//construit la nouvelle chaine de str 
static char *build_result(const char *str, const char *old_pat, const char *new_pat, size_t len_old_pat, size_t len_new_pat) {
    char *result = malloc(my_strlen(str) + 1);

    if (!result) {
        return NULL;
    }

    char *dst = result;
    const char *src = str;

    while (*src) {
        const char *pos = strstr(src, old_pat);

        if (pos) {
            size_t segment_len = pos - src;

            strncpy(dst, src, segment_len);
            dst += segment_len;

            if (new_pat) {
                my_strcpy(dst, new_pat);
                dst += len_new_pat;
            }
            src = pos + len_old_pat;
        }
        
        
         else {
            my_strcpy(dst, src);
            break;
        }
    }

    return result;
}
//enfin remplace les occurences 
char *my_str_replace(const char *old_pat, const char *str, const char *new_pat) {
    if (!str) {
        return NULL;
    }

    if (!old_pat) {
        return replace_without_old_pat(str, new_pat);
    }

    size_t len_old_pat = my_strlen(old_pat);
    size_t len_new_pat;

    if (new_pat) {
        len_new_pat = my_strlen(new_pat);
    } 
    
    
    else {
        len_new_pat = 0;
    }

    size_t count = occurrences(str, old_pat);
    size_t new_len = my_strlen(str) + count * (len_new_pat - len_old_pat);
    char *result = malloc(new_len + 1);

    if (!result) {
        return NULL;
    }

    return build_result(str, old_pat, new_pat, len_old_pat, len_new_pat);
}
