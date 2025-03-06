#include "my_nbr_digit.h"
#include <stdio.h>

int my_nbr_digit(int number, int base) {

    int count = 0;

	if (base <= 1) {
        	return -1;
    	}

    	if (number == 0) {
        	return 1;
    	}

    

    	int abs_number;

    	if (number < 0){
    		abs_number =-number;
    
    	}

    	else{
    
    		abs_number = number;
    	}


    	while (abs_number > 0) {
        	abs_number /= base;
        	++count;
    	}

    	return count;
}

