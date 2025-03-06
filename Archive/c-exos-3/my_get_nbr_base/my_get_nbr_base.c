#include "my_get_nbr_base.h"

int get_base_len(const char base[]) {
    int length = 0;
    while (base[length] != '\0') {
        ++length;
    }
    return length;
}

int char_to_digit(char c, const char base[], int base_len) {
    for (int j = 0; j < base_len; ++j) {
        
        if (c == base[j]) {
            return j;
        }
    }
    return -1; 
}

int my_get_nbr_base(const char num[], const char base[], const char sign) {
    
    int base_len = get_base_len(base);
    int i = 0, res = 0, is_negative = 0;

    if (num[0] == sign) {
        is_negative = 1;
        i = 1;
        }


    while (num[i] != '\0') {
        int digit = char_to_digit(num[i], base, base_len);
        
        if (digit == -1) {
            return 0; 
        }
        res = res * base_len + digit;
        ++i;
    }
    
    if (is_negative) {
        return -res;
        } 
        
    else {
    
        return res;
        }

}

