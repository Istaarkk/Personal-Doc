#!/bin/bash

file="$1"
ext="${file##*.}"

if [[ "$ext" == "c" || "$ext" == "h" ]]; then
    # Pour les fichiers C, utiliser cpp pour enlever les commentaires
    cpp -fpreprocessed "$file" | grep -v '^\s*$' | wc -l
else
    # Pour Perl, Python, Shell et Assembleur, on filtre avec grep
    comment_char='#'
    [[ "$ext" == "asm" || "$ext" == "mac" || "$ext" == "inc" ]] && comment_char=';'

    grep -v "^\s*$" "$file" | grep -v "^\s*$comment_char" | wc -l
fi
