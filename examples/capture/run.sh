#!/bin/bash

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

# You should return 0, if ecerything goes well. If you don't, you will get a line in the grading-script-errors log.
# You can use commands  `exit 0`, `true` or `:` for example.
:
