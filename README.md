A docker container that includes a stable Debian Linux and convenience
grading scripts to capture command output and to submit generated
feedback after grading.

This container is a base that new submission grading/assessment
environments can use in the Dockerfile FROM instruction.

The following custom commands are provided in path:

* `sudo-capture CMD...`

    Executes the command and captures the stdout and stderr to /feedback.
    This executes as root (default user in docker).

* `capture CMD...`

    Changes the ownership of the working directory to "nobody",
    executes the command as "nobody",
    and captures the stdout and stderr to /feedback.

* `pre CMD...`

    Wraps the stdout of the command into &lt;pre&gt; HTML element
    and escapes any HTML inside. Can be chained, e.g.
    `capture pre my_assessment_code.sh arg1 arg2`

* `grade [points/max]`

    Submits the feedback back to the grading service.
    This command MUST be executed at the end of the grading.

    Gets granted points in priority order from:
    a) argument in format "5/10"
    b) /feedback/points file in format "5/10"
    c) /feedback/out including lines "TotalPoints: 5" and "MaxPoints: 10"

    Gets feedback as HTML from /feedback/out,
    and wraps /feedback/err into alert box at the end.
    If /feedback/appendix exists it will be included at the very end.

* `err-to-out`

    Appends the captured stderr to stdout feedback without alert box.
    Useful for unit test frameworks that produce feedback into stderr.

* `force-charset CHARSET`

    Converts recursively all files in working directory from any recognizable
    charsets into desired charset, e.g. utf-8. Discards unconvertible characters.
    May be useful to sanitize output from exotic student environments.

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
