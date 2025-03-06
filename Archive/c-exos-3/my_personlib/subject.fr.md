À la racine du repository, dans le répertoire **my_personlib**.

Fichiers à rendre :

```
.
└── my_personlib.c

1 directory, 1 file
```

---
Écrire un fichier my_personlib.c contenant les fonctions:
```cpp
    #ifndef __STAFFLIB_H
    #define __STAFFLIB_H
    #define _XOPEN_SOURCE
    #include <time.h>

    // un élément de la liste.
    // chaque élément est connecté avec 2 autre membre (avant et après).
    struct member
    {
        char            name[20+1];
        char            lastname[40+1];
        struct tm       birth;
        struct member   *next;
        struct member   *prev;
    };

    // la liste dans son ensemble est définit par cette structure
    struct staff
    {
        struct member   *first;
        struct member   *last;
    };

    // construit la base de la liste chaîné
    struct staff *new_staff();

    // libère tous les élément de la liste
    void destroy_staff(struct staff *);

    // ajoute un élément a la fin de la liste de staff, et retourne
    void staff_append_member(struct staff *staff, struct member *person);

    // ajoute un élément au debut de la liste de staff
    void staff_prepend_member(struct staff *staff, struct member *person);

    // insert un élément apres le membre nommer name
    void staff_insert_after_member_name(struct staff *staff, char *name, struct member *person);

    // construit un nouveau membre
    struct member *new_member(const char *name, const char *lastname, const char *birthdate);

    #endif
```
Vous pouvez utiliser ces fonctions ainsi :
```cpp
    struct staff *s = new_staff();
    staff_append_member(s, new_member("lionel", "auroux", "1977-10-05"));
    staff_append_member(s, new_member("samuel", "lemarchand", "1980-05-25"));
    staff_append_member(s, new_member("sophie", "labadie", "1979-08-13"));
    staff_append_member(s, new_member("marie", "chazan", "1981-02-19"));
```
Vous devez utiliser les structures données.

Les listes chaînées sont très utile pour avoir une collection de variable qui peut grandir a l'infini.
Mais attention les listes chaînées ne peuvent pas être accédé directement comme des tableau

> **Les seules fonctions autorisées sont malloc, free, strptime**
