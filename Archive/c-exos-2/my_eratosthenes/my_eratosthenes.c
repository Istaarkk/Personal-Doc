#include <stdio.h>
#include "my_eratosthenes.h"

void my_eratosthenes(int n) {
	if (n == 0 || n == 1) {
        	printf("0");
        	return;
    	}

    	for (int i = 2; i < 1000; i++) {
        	if (n % i == 0 && n != i) {
            	printf("0");
            	return;
        	}
    	}
    	printf("1");
}

