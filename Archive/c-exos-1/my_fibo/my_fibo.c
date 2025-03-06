#include <stdio.h>
#include "my_fibo.h"

extern unsigned long my_fibo(unsigned long int nombre){
    
	if (nombre == 0 || nombre == 1) {
     
	    return nombre;  
    }


    return my_fibo(nombre - 1) + my_fibo(nombre - 2);



}


