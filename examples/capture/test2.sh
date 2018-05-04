#!/bin/sh


test() {
    word=$1
    out=$(sh solution.sh $word)

    if [ "$out" != "Hello $word!" ]; then
        echo "Expected 'Hello $word!', but you printed '$out'"
        exit 1
    fi
}

for w in Jack John Mike; do
    test $w
done

for i in `seq 1 5`; do
    w=$(head -c 10 /dev/urandom | md5sum | head -c 7)
    test $w
done

echo "ok"
