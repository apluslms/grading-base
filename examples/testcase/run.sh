#!/bin/bash

# Testcase is a single graded test case. In short, it runs given command and
# if that command fails, then no points are given. If the command succeeds, then
# points are given.
# Testcase writes all information to files under /feedback/<number>/, where
# <number> is the first free number starting from 0.
testcase -t "Validate script" -p 2 \
    /exercise/check.sh solution.sh
# We keep the exit code, so we can skip next testcases if this one fails
ok=$?

# This is similar as above, except we added `-s $ok`. Testcase won't run the
# command and it won't give points, but it will add max_points. This allows
# us to keep track of total points and still skip some tests.
testcase -t "Addition test" -p 5 -s $ok \
    stdio-diff -S /exercise/given1.in /exercise/expected1.out \
    sh solution.sh
# The command stdio-diff takes the input and the expected output file.
# Then, it runs student code `sh solution.sh` and compares it's output to
# the expected one. If they differ, it will print the difference and exit
# with 1 (thus failing the test).
# Because flag `-S`, diff will ignore space when comparing lines.

# In this final test case, we use `-f` to set fail message for stdio-diff and
# that hides the diff output.
testcase -t "Limit test" -p 5 -s $ok \
    stdio-diff -S -f "failed" /exercise/given2.in /exercise/expected2.out \
    sh solution.sh

# You should return 0, if ecerything goes well. If you don't, you will get a line in the grading-script-errors log.
# You can use commands  `exit 0`, `true` or `:` for example.
:
