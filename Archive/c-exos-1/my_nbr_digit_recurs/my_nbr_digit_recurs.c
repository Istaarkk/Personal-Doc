#include "my_nbr_digit_recurs.h"


int my_nbr_digit(int number, int base) {
    
	if (number == 0) {
        	return 0;
    	}

  
    	return 1 + my_nbr_digit(number / base, base);
}

int my_nbr_digit_recurs(int number, int base) {
    	
	if (base <= 1) {
        	return -1; 
    	}

    	if (number == 0) {
        	return 1; 
    	}
    
    	int abs_number;

    	if (number < 0) {
    		abs_number = -number; 
		} 


    	else {
    		abs_number = number;  
		}

   
    	return my_nbr_digit(abs_number, base);
}
