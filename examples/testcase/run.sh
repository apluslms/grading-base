#!/bin/bash

# Redirect stderr to errors file, which is only visible to the course staff.
# This is no way mandatory, but will help you when debugging this file.
# Note: `capture` redirects stderr of the sub process to /feedback/err,
# which in contrary is visible to the student.
exec 2>> /feedback/errors

# For now, grading service puts the student submission into following path.
# Here, we ensure the working directory is correct
cd /submission/user

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

# Always remember to call grade. It will take care of posting the feedback
# and points back to the grading service.
# You do not need to call `create-test-feedback` as `grade` will do that if needed.
grade
