#!/bin/sh
[ -d /submission/user ] && cd /submission/user

# Skip wrapper if first argument starts with /bin/ or is --exec
[ "${1#/bin/}" != "$1" ] && exec "$@"
[ "$1" = "--exec" ] && shift && exec "$@"

if [ "$1" = "--sh" ]; then
    shift
    sh -c "$*" 2>> /feedback/grading-script-errors >&2
    RES=$?
else
    "$@" 2>> /feedback/grading-script-errors >&2
    RES=$?
fi
[ $RES -ne 0 ] && echo "Received exit code $RES from: $*" >> /feedback/grading-script-errors
[ -s /feedback/.posted ] || grade 2>> /feedback/grading-script-errors >&2
# We ignore RES, as it could be meaningful in the future
exit 0
