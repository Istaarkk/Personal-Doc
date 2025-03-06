Dans un sous-dossier nommé **my_report** situé à la racine du projet.

Fichiers à rendre :

```
.
├── aff_code.sh
├── aff_exec.sh
├── count_code.sh
├── count_exec.sh
├── count_line.sh
└── type_script.sh

1 directory, 6 files
```

---
Vous avez à fournir un certain nombre de petit script d'information sur un code source.
Pour les exemples nous vous fournissons celui de Nasm (Netwide Assembler) dans ``provided_files.zip``.

Pour écrire ces scripts vous devez à utiliser ``find``, ``wc``, ``cpp``, ``grep``, ``sort`` et toutes les built-in de bash.
Toutes autres commandes est interdites.
Tout sera rendue dans le même répertoire il est donc évident que vous pourrez avoir des dépendances avec vos autres scripts.
La moulinette de correction aura pour "working directory" le même répertoire où seront vos scripts.
Vous avez à déduire les subtilités des comportements demandés à partir des exemples.

aff_exec.sh && count_exec.sh
----------------------------

Affiche et Compte le nombre de exécutable:
```shell
    user$ ./aff_exec.sh ../provided_files/nasm-master/ 2>/dev/null | head -5
    ../provided_files/nasm-master/asm/pptok.pl
    ../provided_files/nasm-master/asm/tokhash.pl
    ../provided_files/nasm-master/asm/warnings.pl
    ../provided_files/nasm-master/autoconf/helpers/compile
    ../provided_files/nasm-master/autoconf/helpers/config.guess
    user$ ./count_exec.sh provided_files/nasm-master/
    37
```
- un exécutable est un fichier avec les droits d'exécution

type_script.sh
--------------

Affiche le type du script lorsqu'il est exécutable devant le nom du fichier:
```shell
    user$ ./type_script.sh ../provided_files/nasm-master/ 2>/dev/null | head -6
    Shell ../provided_files/nasm-master/autogen.sh
    Perl ../provided_files/nasm-master/x86/insns.pl
    Perl ../provided_files/nasm-master/x86/regs.pl
    Perl ../provided_files/nasm-master/macros/macros.pl
    Python ../provided_files/nasm-master/travis/nasm-t.py
    user$ ./type_script.sh ../provided_files/extra_script1
    Python ../provided_files/extra_script1
    user$ ./type_script.sh ../provided_files/extra_script2
    Perl ../provided_files/extra_script2
    user$ ./type_script.sh ../provided_files/extra_script3
    Python ../provided_files/extra_script3
    user$ ./type_script.sh ../provided_files/extra_script4
    Perl ../provided_files/extra_script4
```
- ne vous fiez pas tout le temps aux extensions (exemple d'extra_script*)
- comme dans l'exemple précédent les types à afficher dépendant du type de fichier sont:
    * "Perl"
    * "Python"
    * "Shell"
- vous devez respecter la casse concernant l'affichage du préfixe
- il n'y a qu'un seul espace entre le type de script et le nom du script
- un type inconnu ne provoque aucun affichage

aff_code.sh && count_code.sh
----------------------------

Affiche et Compte le nombre de fichier source:
```shell
    user$ ./aff_code.sh ../provided_files/nasm-master/ 2>/dev/null | head -5
    ../provided_files/nasm-master/asm/assemble.c
    ../provided_files/nasm-master/asm/assemble.h
    ../provided_files/nasm-master/asm/directiv.c
    ../provided_files/nasm-master/asm/error.c
    ../provided_files/nasm-master/asm/eval.c
    user$ ./count_code.sh provided_files/nasm-master/
    394
```
- les fichiers sources ne sont pas exécutable
- l'extension précise le langage dans lequel ils sont écrits:
    * .c ou .h : C
    * .pl ou .ph : Perl
    * .asm, .mac ou .inc : Assembleur
    * .py : Python
- vous ne devez pas comptez les fichiers tests travis (et seulement ceux-ci) ou ceux relatif à la documentation (doc, rdoff).

count_line.sh
-------------

Compte le nombre de ligne de code utile pour un programme. Une ligne utile est une ligne ni vide, ni de commentaire.

Pour cet exercice, vous aurez à faire quelques expressions rationnelles en shell utilisant potentiellement quelques opérateurs et/ou variables et/ou test.
Perl, Python, et shell ont leurs lignes de commentaire qui commence par le caractère ``#``.
L'assembleur a ses lignes de commentaire qui commence par le caractère ``;``.

Pour le C, comme le but de ces exercices se limite à grep ou sed et non au Regex de type Perl, il n'est pas envisageable de correctement parser les
commentaires C (cas multi-ligne). Vous aurez donc à utiliser judicieusement l'utilitaire ``cpp`` pour qu'il les filtre pour vous.
```shell
    user# ./count_line.sh provided_files/nasm-master/asm/eval.h
    5
    user# ./count_line.sh provided_files/nasm-master/asm/directiv.c
    384
    user# ./count_line.sh provided_files/nasm-master/test/riprel.asm
    5188
    user# ./count_line.sh provided_files/nasm-master/test/gas2nasm.py
    78
```
Dans le cas du C (et uniquement du C), vous pouvez vous comparer à l'utilitaire ``cloc``.
