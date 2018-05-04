#!/bin/bash

# Redirect stderr to errors file, which is only visible to the course staff.
# This is no way mandatory, but will help you when debugging this file.
# Note: `capture` redirects stderr of the sub process to /feedback/err,
# which in contrary is visible to the student.
exec 2>> /feedback/errors

# For now, the grading service puts the student submission into the following path.
# Here, we ensure the working directory is correct
cd /submission/user

# `title` can take class via an argument :)
title -c "text-primary" "Test results"

# Capture part
# First, print the title. Second, capture the output from test1.sh.
# Both, `title` and `capture`, write data to /feedback/out.
# In the last part, we update points in /feedback/points file using `points`.
# Second argument `$?` for the `points` is exit code of `capture`. If test exits
# with non zero exit code, then no points are given.
title -e h4 "Hello world test"
capture pre /exercise/test1.sh
points 10 $?

# Note: capture will take care of running the test with non root user and that
# grading url and submission id are not in the environment.
# If you need to do that your self, then read the source for `capture`,
title -e h4 "Argument test"
capture pre /exercise/test2.sh
points 10 $?

# Always remember to call grade. It will take care of posting the feedback
# and points back to the grading service.
grade
