#ifndef _MY_PUTCHAR_H
#define _MY_PUTCHAR_H 1
#include <unistd.h>

static inline void my_putchar(char c)
{
    write(STDOUT_FILENO, &c, 1);
}

#endif /* _MY_PUTCHAR_H */
