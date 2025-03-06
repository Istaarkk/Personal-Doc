#include <stddef.h>
#include <stdint.h>
#include "my_bitclean.h"

uint32_t my_bitclean(uint32_t __bitmap, int __pos) {
	
    int position;

    if (__pos == 0) {
		return __bitmap & ~1U; //rend valeur de retour 

	}
	
   	if (__pos > 0) {
        	return __bitmap & ~(1U << __pos);//si supérieur a 0 décale ver la gauche on part du poids faible

    }
    else {

        position = 31 + __pos;
        return __bitmap & ~(1U <<position);//si inferieur on part du poids fort 
    }
	
	return __bitmap;
}




