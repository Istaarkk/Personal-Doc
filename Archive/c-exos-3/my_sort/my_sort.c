#include "my_sort.h"
#include <stddef.h>

void echange(int *a, int *b) {
    	int temp = *a;
    	*a = *b;	
    	*b = temp;
}

void my_sort(int arr[], unsigned int length) {
    	for (unsigned int i = 0; i < length - 1; i++) {
		for (unsigned int j = 0; j < length - i - 1; j++) {
			if (arr[j] > arr[j + 1]) {
				echange(&arr[j], &arr[j + 1]);
            		}
        	}
    	}
}

