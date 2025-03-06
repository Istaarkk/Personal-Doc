#include <stdio.h>
#include <unistd.h>


int my_alphabet(void){
	
		char letter ;
		int count = 0;

		for (letter = 'a';letter <='z';++letter){

			write(1, &letter, 1);
			count +=1;
		}

		return count;
}


