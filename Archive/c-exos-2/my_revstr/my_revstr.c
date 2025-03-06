#include <stdio.h>
#include "my_revstr.h"


void my_revstr(char str[])
{
	int length = 0;
    	int i;
    	char temp;

    	while (str[length] != '\0')
        	++length;


    	for (i = 0; i < length / 2; i++)
    	{
        	temp = str[i];
        	str[i] = str[length - 1 - i];
        	str[length - 1 - i] = temp;
    	}
}

