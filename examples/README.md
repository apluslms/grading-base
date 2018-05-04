Examples
========

Here are few example `run.sh` scripts that use different tools from `grading-base` container.
You should read those scripts and the exercise pages to understand how to do your own grading script.

However, do remember that `grading-base` does not contain any other programming tools than shell and perl,
so you should use container designed for your language or environment.
To start, checkout containers starting with `grade-` on [apluslms page on docker hub](https://hub.docker.com/u/apluslms/).

Running test environment
------------------------

Presuming you have `docker-ce` and `docker-compose` installed,
you can run `./docker-up.sh` to start a local a-plus in https://localhost:8000.
If you don't have those tools, then follow instructions on [A-plus LMS site](https://apluslms.github.io).
