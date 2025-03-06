#ifndef _MY_LOAD_H
#define _MY_LOAD_H

#define _XOPEN_SOURCE
#include <time.h>

enum item_type
{
    STAFF,
    STUFF
};

struct item_staff
{
    char        name[20];
    char        lastname[20];
    struct tm   birth;
    struct tm   begin_job;
};

struct item_stuff
{
    int         id;
    char        title[20];
    char        desc[50];
    double      height;
    double      width;
    double      depth;
    double      weight;
};

union item_union {
    struct item_staff   staff;
    struct item_stuff   stuff;
};

struct item
{
    enum item_type      type;
    union item_union    udata;
};

struct item_list
{
    struct item_list    *next;
    struct item         *data;
};

// créer un nouvel Item
struct item         *new_item(enum item_type, union item_union *data);
// ajoute un Item à la liste
struct item_list    *append_item_list(struct item_list *, struct item *);
// Affiche un Item
void                print_item(struct item *);

// Ecrire ou Lire à partir d'un fichier ouvert dont on possède le File Descriptor
void                save_item_list(int fd, struct item_list*);
struct item_list    *load_item_list(int fd);

#endif /* _MY_LOAD_H */
