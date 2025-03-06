#include <stdlib.h>
#include <string.h>
#include "my_put_nbr_base.h"

int my_strlen(const char *str) {
    int lenght = 0;
    while (str[lenght] != '\0') {
        lenght+=1;
    }
    return lenght;
}

char *my_put_nbr_base(int n, const char *base, char sign) {
    int base_len = my_strlen(base);
    if (base_len < 2) {
        return NULL;
    }

    int is_negative = (n < 0) ? 1 : 0;
    if (is_negative) {
        n = -n;
    }

    int num_digits = 1;
    int temp = n;
    while (temp >= base_len) {
        temp /= base_len;
        num_digits+=1;
    }

    char *result = (char *)malloc((num_digits + is_negative + 1) * sizeof(char));
    if (!result) {
        return NULL;
    }

    result[num_digits + is_negative] = '\0';
    for (int i = num_digits - 1; i >= 0; i--) {
        result[i + is_negative] = base[n % base_len];
        n /= base_len;
    }

    if (is_negative) {
        result[0] = sign;
    }

    return result;
}
