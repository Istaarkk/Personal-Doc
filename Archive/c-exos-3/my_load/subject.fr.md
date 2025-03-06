À la racine du repository, dans le répertoire **my_load**.

Fichiers à rendre :

```
.
└── my_load.c

1 directory, 1 file
```

---
représente des données correspondant à des "STAFF" et/ou du "STUFF".

Votre rôle est donc de comprendre la structure du format `.ilist`. Vous devez
être capable de lire les fichiers fournis afin d'afficher les informations qui y
sont encodées et d'y apporter des modifications, ce qui implique que vous devez
aussi être capable de générer les fichiers `.ilist`.

Écrire les fonctions suivantes:
```cpp
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
```
Le format de date est iso-8601 (Année-Mois-Jours).

Le nombre max d'entrée est sur 32 bit.

Le format d'affichage de la fonction `print_item` est le suivant. Soit un programme appelant la fonction...
```shell
    $ ./print_item1 | cat -e
    ITEM TYPE: STAFF$
    name: arthur$
    lastname: testant$
    birth: 1977-10-05$
    begin_job: 2021-03-01$
```

```shell
    $ ./print_item2 | cat -e
    ITEM TYPE: STUFF$
    id: 12$
    title: test$
    desc: ceci est une description longue$
    height: 1.00$
    width: 0.10$
    depth: 0.50$
    weight: 1.50$
```
Indices:

* Le premier champs du fichier est une identification du type de fichier
* Un fichier contient 7 élément
* Un fichier contient 6 élément
* Rappel: On peut sauver le contenu d'une structure dans un fichier:
```cpp
    struct machin a;
    write(fd, &a, sizeof (struct machin));
```
* Rappel: On peut lire le contenu d'une structure d'un fichier:
```cpp
    struct bidule b;
    read(fd, &b, sizeof (struct bidule));
```
* Revoir l'endianess sur les précis de C et ASM
* Revoir l'alignement et le packing sur le précis de C et ASM
* N'oubliez pas de faire des trucs du style:
```cpp
    printf("STAFF SIZE %d\n", sizeof (struct staff));
    printf("STUFF SIZE %d\n", sizeof (struct stuff));
```
Vous connaissez la taille des structs, le nombre d'élément, et la taille du fichier... Que pouvez vous en déduire ?

Man *hd* pour le forensic...

> **Fonctions autorisés: malloc, memcpy, strftime, write, read**

> **Toutes fonctions non spécifiées sont interdites**

> **Pour être corrigeable, toutes les fonctions doivent êtres définies (même à vide)**
