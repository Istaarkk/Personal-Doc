#include <stdio.h>
#include "my_hanoi.h"

static void hanoi_recursive(unsigned n, int A, int B, int C) {
    if (n == 0) {
        return;
    }

    hanoi_recursive(n - 1, A, C, B);

    putchar(A + '0');
    putchar('-');
    putchar('>');
    putchar(B + '0');
    putchar('\n');

    hanoi_recursive(n - 1, C, B, A);
}

void my_hanoi(unsigned n) {
    hanoi_recursive(n, 1, 3, 2);
}
	
