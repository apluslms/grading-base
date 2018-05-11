#!/bin/sh

while read a b; do
    c=$((a + b))
    test 10 -lt $c && c=10
    echo "$a + $b = $c"
done
