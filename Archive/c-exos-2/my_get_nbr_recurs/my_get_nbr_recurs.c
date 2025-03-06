#include <stdio.h>
#include "my_get_nbr_recurs.h"

static int my_get_nbr(char const str[], int index, int result, int sign) {
	if (str[index] == '\0') {
        	return result * sign;
    	}

    	if (index == 0 && (str[index] == '+' || str[index] == '-')) {
        	return my_get_nbr(str, index + 1, result, (str[index] == '-') ? -1 : 1);
    	}

    	if (str[index] < '0' || str[index] > '9') {
        	return result * sign;
    	}

    	int digit = str[index] - '0';
    	result = result * 10 + digit;

    	return my_get_nbr(str, index + 1, result, sign);
	}

int my_get_nbr_recurs(char const str[]) {
    	return my_get_nbr(str, 0, 0, 1);
}

