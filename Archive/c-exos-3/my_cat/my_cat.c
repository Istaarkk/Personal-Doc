#include "my_cat.h"
#include <stddef.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int my_cat(const char *const filename) {
    char buff[4096];
    int fd = 0;
    //ssize_t n; 
    int n;
    
    if (filename == NULL) {
        fd = 0; // flot de sortie standar
    } 
    
    else {
        fd = open(filename, O_RDONLY);
    }

    if (fd == -1) {
        return 1; 
    }



    while ((n = read(fd, buff, sizeof(buff))) > 0) {
        if (write(1, buff, n) != n) {
            return 1; // in case of eror
        }
    }

    if (fd > 0) { //case ou la sortie est autre que celle de base 
        close(fd);
    }

    return (n < 0); 
}

