#include <stdio.h>
#include "my_putchar.h"
#include "my_echo.h"


void my_echo(char const str[]) {
	for (int i = 0; str[i] != '\0'; ++i) { 
	    my_putchar(str[i]);
	  
    
    }
	my_putchar('\n');
}



