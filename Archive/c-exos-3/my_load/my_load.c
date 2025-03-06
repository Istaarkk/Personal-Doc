#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "my_load.h"

void sauvegarde_item_liste(int fd, struct item_list *liste) {
    struct item_list *current = liste;
    
    while (current) {
        write(fd, &current->data->type, sizeof(enum item_type));
        
        if (current->data->type == STAFF) {
            write(fd, &current->data->udata.staff, sizeof(struct item_staff));
        } 
        
        else {
            write(fd, &current->data->udata.stuff, sizeof(struct item_stuff));
        }

        current = current->next;
    }
}

void affiche_item(struct item *item) {
    
    if (item->type == STAFF) {
        printf("ITEM TYPE: STAFF\n");
        printf("name: %s\n", item->udata.staff.name);
        printf("lastname: %s\n", item->udata.staff.lastname);
        
        char naissance[11], debut_travail[11];
        strftime(naissance, sizeof(naissance), "%Y-%m-%d", &item->udata.staff.birth);
        strftime(debut_travail, sizeof(debut_travail), "%Y-%m-%d", &item->udata.staff.begin_job);
        
        printf("birth: %s\n", naissance);
        printf("begin_job: %s\n", debut_travail);
    } 
    
    else {
        printf("ITEM TYPE: STUFF\n");
        printf("id: %d\n", item->udata.stuff.id);
        printf("title: %s\n", item->udata.stuff.title);
        printf("desc: %s\n", item->udata.stuff.desc);
        printf("height: %.2f\n", item->udata.stuff.height);
        printf("width: %.2f\n", item->udata.stuff.width);
        printf("depth: %.2f\n", item->udata.stuff.depth);
        printf("weight: %.2f\n", item->udata.stuff.weight);
    }
}

struct item_list *charge_item_liste(int fd) {
    struct item_list *liste = NULL;
    struct item *new_item_data;
    enum item_type type;
    int bytes_read;
    
    while (1) {
        bytes_read = read(fd, &type, sizeof(enum item_type));
        if (bytes_read == 0) {
            break;
        }
        if (bytes_read < 0) {
            perror("Erreur de lecture");
            break;
        }

        union item_union data;
        if (type == STAFF) {
            bytes_read = read(fd, &data.staff, sizeof(struct item_staff));
            if (bytes_read < 0) {
                perror("Erreur de lecture");
                break;
            }
        } 
        
        else {
            bytes_read = read(fd, &data.stuff, sizeof(struct item_stuff));
            if (bytes_read < 0) {
                perror("Erreur de lecture");
                break;
            }
        }

        new_item_data = new_item(type, &data);
        if (!new_item_data) {
            perror("Erreur d'allocation mémoire");
            break;
        }

        liste = ajoute_item_liste(liste, new_item_data);
    }
    
    return liste;
}

struct item_list *ajoute_item_liste(struct item_list *liste, struct item *data) {
    struct item_list *nouveau_noeud = malloc(sizeof(struct item_list));
    if (!nouveau_noeud) 
        return NULL;
    

    nouveau_noeud->data = data;
    nouveau_noeud->next = NULL;

    if (!liste) {
        return nouveau_noeud;
    }

    struct item_list *current = liste;

    while (current->next) {
        current = current->next;
    }
    current->next = nouveau_noeud;

    return liste;
}

struct item *new_item(enum item_type type, union item_union *data) {
    struct item *new_item = malloc(sizeof(struct item));
    if (!new_item) {
        return NULL;
    }
    
    new_item->type = type;
    if (type == STAFF) {
        new_item->udata.staff = data->staff;
    } 
    
    else {
        new_item->udata.stuff = data->stuff;
    }
    
    return new_item;
}
