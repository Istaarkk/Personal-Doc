#include <stdio.h>
#include "my_strlen.h"

int my_strlen(char const str[]) {
    	int i = 0;
    	while (str[i] != '\0')  
    	{
        	++i;
    	}
    	return i;
}

