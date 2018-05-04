A docker container that includes a stable Debian Linux and convenience
grading scripts to capture command output and to submit generated
feedback after grading.

This container is a base that new submission grading/assessment
environments can use in the Dockerfile FROM instruction.

The following custom commands are provided in path:

* `testcase [-t title] [-p points_on_success] [-s only_if_zero] CMD...`

    Defines a single test case.
    Useful when running multiple commands for grading.
    Creates `/feedback/<number>` directory with increasing number for every call.

    If `title` is provided, it's stored in `/feedback/<number>/title`.

    If `points_on_success` is provided, it will be written to `/feedback/<number>/max_points`.
    If CMD exits with 0, then it will also be written to `/feedback/<number>/points`.

    If `only_if_zero` is provided and not 0, then CMD is not executed and `testcase` exits with non-zero exit code.

    Status of this test is stored in `/feedback/<number>/status` accordingly.

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

* `points <points> [only_if_zero]`

    Add `points` to given and maximum points in `/feedback/points`.
    If the file exists, it will be updated.
    If `only_if_zero` is given and not zero, then only maximum points are changed.

    This can be used in conjunction with `capture` to give points conditionally.
    For example,

    ```
    capture ./my_assessment_code.sh
    points 10 $?
    ```

    where `$?` is the exit code from `capture`.

* `title [-c class] [-e element] [-O] <text>`

    Writes `text` inside HTML element `element` to `/feedback/out`.
    The element is `h1` by default, but can be changed with `-e`.

    Option `-c` can be used to set HTML class for the element.

    Flag `-O` changes the output to stdout.

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

* `stdio-diff [-c] [-s] [-S] [-p pass_text] [-P] [-f fail_text] <in_file> <expected_out> CMD...`

    Simple text comparison wrapper based on `diff`.
    Given `in_file` and `expected_out`, script will execute CMD with `in_file` as stdin and store it's stdout.
    Finally, it will compare `expected_out` to stdout of the CMD.
    The output from diff is revealed to the user, unless `fail_text` is provided.

    Option `-c` makes output case sensitive.
    Option `-s` makes output space sensitive. There needs to be space between words, but amount doesn't matter.
    Option `-S` makes diff totally ignore space (removes all space before comparison).

    By default, `ok` is printed when the output matches the expected.
    The string can be changed to a custom value with `-p` or to nothing with `-P`.

    This command can be used with `capture` and `testcase`.
    E.g. `capture pre stdio-diff in.txt out.txt ./student_code`.

* `create-test-feedback`

    Combines feedback items from `/feedback/<number>` directories to `/feedback/out`.

* `err-to-out`

    Appends the `/feedback/err` to `/feedback/out` without `alert-danger` class.
    Useful for unit test frameworks that produce the feedback into stderr.

* `force-charset CHARSET`

    Converts recursively all files in working directory from any recognizable
    charsets into desired charset, e.g. utf-8. Discards unconvertible characters.
    May be useful to sanitize output from exotic student environments.

* `set-error [msg]`

    Set submission error state by writing `true` to `/feedback/error`.
    If `msg` is provided, then it is written as the reason to `/feedback/errors`.

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
