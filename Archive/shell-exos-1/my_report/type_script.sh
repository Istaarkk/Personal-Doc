#!/bin/bash

find "$1" -type f -executable 2>/dev/null | while read -r file; do
    if head -n 1 "$file" | grep -q '^#!.*perl'; then
        echo "Perl $file"
    elif head -n 1 "$file" | grep -q '^#!.*python'; then
        echo "Python $file"
    elif head -n 1 "$file" | grep -q '^#!.*sh'; then
        echo "Shell $file"
    elif head -n 1 "$file" | grep -q '^#!.*bash'; then
        echo "Shell $file"
    elif [[ "$file" =~ \.pl$ ]]; then
        echo "Perl $file"
    elif [[ "$file" =~ \.py$ ]]; then
        echo "Python $file"
    elif [[ "$file" =~ \.sh$ ]]; then
        echo "Shell $file"
    fi
done
