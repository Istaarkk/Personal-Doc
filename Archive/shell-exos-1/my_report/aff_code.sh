#!/bin/bash

find "$1" -type f ! -executable \
    \( -name "*.c" -o -name "*.h" -o -name "*.pl" -o -name "*.ph" -o -name "*.asm" -o -name "*.mac" -o -name "*.inc" -o -name "*.py" \) \
    ! -path "*travis*" -prune ! -path "*/doc/*" ! -path "*/rdoff/*" -true |sort

