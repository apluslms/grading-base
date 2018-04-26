A docker container that includes a stable Debian Linux and convenience
grading scripts to capture command output and to submit generated
feedback after grading.

This container is a base that new submission grading/assessment
environments can use in the Dockerfile FROM instruction.

The following custom commands are provided in path:


* `capture [-d dir] [-o out] [-e err] [-u user] CMD...`

    Changes the ownership of the working directory to `user`,
    executes the command as `user`,
    and captures the stdout and stderr to `dir`.

    By default `user` is `nobody` and `dir` is `/feedback`.
    Alternative to `-d`, arguments `-o` and `-e` can be used to set stdout and stderr files separately.

    In addition to out and err redirection, `capture` will make sure that the environment does not contain `REC` or `SID` (the variables used for posting feedback).

    For example, `capture pre ./my_test` will execute `./my_test` as `nobody` and redirect stdout and stderr to `/feedback/out` and `/feedback/err`.

    If you need to run captured code as root, then use `sudo-capture`.

* `pre [-c class] CMD...`

    Wraps the stdout of the command into &lt;pre&gt; HTML element
    and escapes any HTML inside. Can be chained, e.g.
    `capture pre ./my_assessment_code.sh arg1 arg2`

    Option `-c` can be used to set HTML class for the element.

* `grade [points/max]`

    Submits the feedback back to the grading service.
    This command **must** be executed at the end of the grading for the grade to be stored.

    Gets granted points in priority order from:
    a) argument in format "5/10"
    b) /feedback/points file in format "5/10"
    c) /feedback/out including lines "TotalPoints: 5" and "MaxPoints: 10"

    Gets feedback as HTML from /feedback/out,
    and wraps /feedback/err into pre with `alert-danger` class at the end.
    If /feedback/appendix exists it will be included at the very end.

* `err-to-out`

    Appends the `/feedback/err` to `/feedback/out` without `alert-danger` class.
    Useful for unit test frameworks that produce the feedback into stderr.

* `force-charset CHARSET`

    Converts recursively all files in working directory from any recognizable
    charsets into desired charset, e.g. utf-8. Discards unconvertible characters.
    May be useful to sanitize output from exotic student environments.

* [chpst](http://smarden.org/runit/chpst.8.html), [setuidgid](https://cr.yp.to/daemontools/setuidgid.html), [softlimit](https://cr.yp.to/daemontools/softlimit.html) and [setlock](https://cr.yp.to/daemontools/setlock.html)

    These utilities are used internally, but can also benefit when writing grading scripts.
    First one provides the other three.
    Read linked documentations for more details.

* `gitlab-api-query.py GIT_HOST [api_token] [require_fork]`

    Reads user repository URL from submitted `gitsource` file,
    e.g. written by mooc-grader types.stdasync.acceptGitAddress,
    and then checks information in GitLab API at given host.
    Prints message and exits non zero if repository is public.

    * api_token

        To access GitLab API as privileged user. Can also check
        that named private repository exists and the fork argument.

    * require_fork

        Requires the submitted repository to be a fork from the
        named one, e.g. lehtint6/material-delivery.

* `git-clone-submission PRIVATE_KEY_PATH [file paths...]`

    Clones repository from URL submitted as `gitsource` file
    into /submission/user-repo. The private ssh key allows
    access to repositories where the public key pair is added
    as a deploy key. Prints status and exits non zero if fails.

    * file paths...

        List of expected files to check inside the repository.
        The files are moved into /submission/user and the
        contents are written as appendix to end of feedback.
