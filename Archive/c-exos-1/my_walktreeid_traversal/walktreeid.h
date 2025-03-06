#ifndef __WALKTREEID_H
#define __WALKTREEID_H

typedef long int treeid;

treeid wkt_create(char);
void wkt_destroy(treeid);

void wkt_add_left(treeid root, treeid child);
void wkt_add_right(treeid root, treeid child);
treeid wkt_get_left(treeid root);
treeid wkt_get_right(treeid root);
char wkt_get_char(treeid root);

#include "walktreeid_traversal.h"

#endif
