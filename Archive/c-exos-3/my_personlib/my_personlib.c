#include "my_personlib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int my_strcmp(char *s1, char *s2)
{
  int i =0;

  while ((s1[i] == s2[i]) && (s1[i] != '\0') && (s2[i] != '\0')){

      i++;
    }

  return (s1[i] - s2[i]);
}


void my_strncpy(char *dest, const char *src, size_t n) {
    size_t i;
    for (i = 0; i < n && src[i] != '\0'; i++) {
        dest[i] = src[i];
    }

    for (; i < n; i++) {
        dest[i] = '\0'; 
    }

}


struct staff *new_staff() {
    struct staff *s = (struct staff *)malloc(sizeof(struct staff));
    
    if (!s) {
        fprintf(stderr, "Erreur d'allocation \n");
        return NULL;
    }

    s->first = NULL;
    s->last = NULL;
    return s;
}

void destroy_staff(struct staff *s) {
    if (s == NULL) return;
    
    struct member *current = s->first;
    struct member *next;

    while (current != NULL) {
        next = current->next;
        free(current);
        current = next;
    }

    free(s);
}

void staff_append_member(struct staff *s, struct member *person) {
    if (s == NULL || person == NULL) return;

    if (s->last == NULL) {
        s->first = person;
        s->last = person;
        person->next = NULL;
        person->prev = NULL;
    } 
    
    else {
        s->last->next = person;
        person->prev = s->last;
        person->next = NULL;
        s->last = person;
    }
}

void staff_prepend_member(struct staff *s, struct member *person) {
    if (s == NULL || person == NULL) return;

    if (s->first == NULL) {
        s->first = person;
        s->last = person;
        person->next = NULL;
        person->prev = NULL;
    } 
    
    else {
        s->first->prev = person;
        person->next = s->first;
        person->prev = NULL;
        s->first = person;
    }
}

void staff_insert_after_member_name(struct staff *s, char *name, struct member *person) {
    if (s == NULL || name == NULL || person == NULL) return;

    struct member *current = s->first;

    while (current != NULL) {
        if (my_strcmp(current->name, name) == 0) {
            person->next = current->next;
            person->prev = current;

            if (current->next != NULL) {
                current->next->prev = person;
            } 
            
            else {
                s->last = person;
            }

            current->next = person;
            return;
        }
        current = current->next;
    }

    fprintf(stderr, "le nom %s non trouvé dans la liste\n", name);
}

struct member *new_member(const char *name, const char *lastname, const char *birthdate) {
    struct member *m = (struct member *)malloc(sizeof(struct member));

    if (!m) {
        fprintf(stderr, "erreur d'allocation");
        return NULL;
    }

    my_strncpy(m->name, name, sizeof(m->name) - 1);
    m->name[sizeof(m->name) - 1] = '\0';

    my_strncpy(m->lastname, lastname, sizeof(m->lastname) - 1);
    m->lastname[sizeof(m->lastname) - 1] = '\0';

    if (strptime(birthdate, "%Y-%m-%d", &m->birth) == NULL) {
        fprintf(stderr, "Erreur de convertion %s\n", birthdate);
        free(m);
        return NULL;
    }

    m->next = NULL;
    m->prev = NULL;

    return m;
}
