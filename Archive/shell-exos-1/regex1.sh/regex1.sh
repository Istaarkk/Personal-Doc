#!/bin/bash

input=$(echo "$1" | cut -d' ' -f2-)

if [[ "$input" =~ ^[0-9]+$ ]]; then
    echo "INT $input"

elif [[ "$input" =~ ^[a-z]+$ ]]; then
    echo "LOWER $input"

elif [[ "$input" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
    echo "IDENT $input"

elif [[ "$input" =~ ^\".*\"$ ]]; then
    cleaned_input=$(echo "$input" | sed 's/^"\(.*\)"$/\1/' | sed 's/\\"/"/g')
    echo "STR $cleaned_input"

else
    echo "Unknown"
fi
