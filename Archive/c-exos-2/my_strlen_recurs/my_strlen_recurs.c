#include <stdio.h>
#include "my_strlen_recurs.h"


int my_strlen_recurs(char const str[]){

	if (*str ==0 ){
	
		return 0;
	}

	return my_strlen_recurs(str+1)+1;
}


