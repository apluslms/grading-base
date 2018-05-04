#!/bin/sh

out=$(sh solution.sh)

if [ "$out" != "Hello World!" ]; then
    echo "Expected 'Hello World!', but you printed '$out'"
    exit 1
fi

echo "ok"
