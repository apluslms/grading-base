A docker container that includes a stable Debian Linux and convenience
grading scripts to capture command output and to submit generated
feedback after grading.

This container is a base that new submission grading/assessment
environments can use in the Dockerfile FROM instruction.

The following custom commands are provided in path:

* `capture CMD...`

    Changes the ownership of the working directory to "nobody",
    executes the command as "nobody",
    and captures the stdout and stderr to /feedback.

* `sudo-capture CMD...`

    Executes the command as "root",
    and captures the stdout and stderr to /feedback.

* `pre CMD...`

    Wraps the stdout of the command into &lt;pre&gt; HTML element.

* `grade`

    Submits the feedback back to the grading service.
    This command MUST be executed at the end of the grading.

    Gets granted points in priority order from:
    a) /feedback/points in format "5/10"
    b) /feedback/out including lines "TotalPoints: 5" and "MaxPoints: 10"

    Gets feedback as HTML from /feedback/out,
    and wraps /feedback/err into alert box at the end.

* `err-to-out`

    Appends the captured stderr to stdout feedback without alert box.
    Useful for unit test frameworks that produce feedback into stderr.

* `force-charset CHARSET`

    Converts recursively all files in working directory from any recognizable
    charsets into desired charset, e.g. utf-8. Dicards unconvertible characters.
    May be useful to sanitize output from exotic student environments.
