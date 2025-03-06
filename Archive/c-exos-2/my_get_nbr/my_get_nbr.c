#include "my_get_nbr.h"

int my_get_nbr(char const *str)
{
	long result = 0;  
    	int sign = 1;
    	int i = 0;

    	if (str[0] == '-') {
        	sign = -1;
        	i++;
    	}

    	while (str[i] != '\0') {
        	if (str[i] < '0' || str[i] > '9') {
            	break;
        	}

        	result = result * 10 + (str[i] - '0');

        	if ((sign == 1 && result > 2147483647) || 
            		(sign == -1 && result > 2147483648L)) {
			return 0;
        	}

        	++i;
    	}

    	return (int)(result * sign);
}
