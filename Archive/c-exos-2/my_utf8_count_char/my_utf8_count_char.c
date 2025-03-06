#include <stdio.h>
#include <stdint.h>
#include "my_utf8_count_char.h"

int my_utf8_count_char(const char *str) {
    if (!str) {
        return 0; // default case
    }

    int count = 0;
    //incrémente les octet au fur et a mesure
    while (*str) {
        
        if ((*str & 0x80) == 0) {
            str += 1;
        } 
        
        else if ((*str & 0xE0) == 0xC0) {
            str += 2;
        } 
        
        else if ((*str & 0xF0) == 0xE0) {
            str += 3;
        } 
        
        else if ((*str & 0xF8) == 0xF0) {
            str += 4;
        } 
        
        else {
            str += 1;
        }
        count++;
        
    }

    return count;
}
