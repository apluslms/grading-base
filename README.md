A docker container that includes a stable Debian Linux and convenience commands for grading a student submission.
Commands include tools from capturing the test output to submitting a feedback back to the grading service.

This container is just a base and does not include tools for different programming and scripting languages.
Thus, actual grading/assessment containers should derive from this container via the FROM instruction in their Dockerfiles.

You can find many grading containers on [the apluslms page on docker hub](https://hub.docker.com/u/apluslms/).
Containers starting with `grade-` are relevant for this purpose.

Version of grading base has format `<major>.<minor>`.
Major is updated when there is backwards incompatible change.
For example, when deprecated tool is removed.
Minor number is updated every time there is something new, where that bug fixes, added features or update on the debian base image.
Derived containers typically use format `<tool version>-<garding-base version>u<update>`,
where tool version is the version from upstream, grading-base is the version of this container and update is number that indicates update on containerisation.
So, for example, grade-python `3.5-2.2u1` means that there is python 3.5 on top of grading-base 2.2 and it's first update after initial release.
Update part is optional and can be omitted.

# The container entry point, the grade wrapper

Container has grade wrapper `/gw` set as the entry point.
This means that everything executed within this container (or derivative) is executed through this script.

The wrapper will take care of redirecting output (stdout and stderr) to `/feedback/grading-script-errors`.
In addition, the script will make sure that the working directory is set correctly.
After the grading script has been executed, the wrapper will execute `grade`.
Thus, the grading script does not need to call `cd` or `grade` anymore.

The wrapper has three different operations, based on the first argument.

1. If the first argument starts with `/bin/` or is `--exec`,
   then arguments are executed and the wrapper itself stops here.
   No redirections are done and `grade` is not executed.

2. If the first argument is `--sh`, then rest of the arguments are evaluated with `sh -c "$*"`.
   This makes strings with quoted text possible in mooc-grader environment.

3. The typical case. Argument list is executed as is.

The exit code from the grading script is stored in the grading-script-errors, but the grade wrapper always exits with 0.

# Filesystem layout

* `/submission/user`

    Files for the solution submitted by the student are stored here.
    This path can be used as working directory.

* `/exercise`

    Exercise files are mounted here in a read only mode.
    With mooc-grader, that means the path you entered in `mount`.
    Typically, this includes `run.sh` and unit test files.

* `/feedback`

    Grading script should store feedback in this path.
    Most utility commands do so, including `capture`, `testcase` and `grade`.
    In the future, mooc-grader will read files from this path instead of expecting a post request.

    * `/feedback/points`:

        Final points.
        Valid format for the data is `<points>/<max_points>` e.g. `5/10`.
        You can use `points` to update this file.
        Points are read by `grade`.

    * `/feedback/out`:

        Feedback that is going be presented in the LMS.
        Typically, data is in html format.
        You should use `pre` to wrap plain text to html.
        You can capture feedback with `capture pre <command>`, for example.

    * `/feedback/err`:

        Error messages from a student or a testing code.
        If present, `grade` will append this inside a pre tag at the end of the out file.
        This file typically contains stderr from the test code.
        For example, `capture` redirects stderr to this file.
        If stderr is normal output (e.g. with python unit tests), then you should consider using `err-to-out`.

    * `/feedback/grading-script-errors`:

        Errors that should be visible only to the staff.
        This file is added as a part of `grading_data` with key `errors` and send to the grading service.
        Then, data can be shown in the LMS to the course staff.
        Data is expected to be plain text messages from `run.sh` and other tools.
        By default, `/gw` redirects stdout and stderr from the `run.sh` to this file.

    * `/feedback/submission-set-error`:

        If this file contains `true`, then the submission is set in an error state in the LMS.
        You can use `set-error` in your script to set this file.

* `/feedback/<number>`

    A single feedback item.
    A set of these directories is considered the feedback list.
    Typically, one folder matches one test case.
    For now, this feedback list is not fully supported and the tool `create-test-feedback` is provided to render these directories to `/feedback/out`.
    Nevertheless, this allows building tools and scripts that export feedback in this format.
    In future, different templates can be used to render the feedback list in the grading service.
    The `grade` tool will automatically merge these directories to a single html file, if grading service doesn't support feedback as a list.

    For every numbered path (feedback item), there can exists any number of files, but following files are typical.
    Following files are supported by `create-test-feedback` and a basic template on the grading service.
    More advanced or specific templates can of course deviate from those.

    * `.../title`: A title or a display name for this feedback item.
    * `.../status`: The status of this feedback. Valid values: `skipped`, `passed`, `failed`, `error`.
    * `.../points`: Points given from this item.
    * `.../max_points`: Maximum points that could be given from this item.
    * `.../out.txt`: Stdout from the test.
    * `.../err.txt`: Stderr from the test.


# Utility commands

Following utility commands are provided in the path.

* `testcase [-t title] [-p points_on_success] [-s only_if_zero] CMD...`

    Defines a single test case.
    Useful when running multiple commands for grading.
    Creates `/feedback/<number>` directory with increasing number for every call.

    If `title` is provided, it's stored in `/feedback/<number>/title`.

    If `points_on_success` is provided, it will be written to `/feedback/<number>/max_points`.
    If CMD exits with 0, then it will also be written to `/feedback/<number>/points`.

    If `only_if_zero` is provided and not 0, then CMD is not executed and `testcase` exits with non-zero exit code.

    Status of this test is stored in `/feedback/<number>/status` accordingly.

* `capture [-o out] [-e err] [-u user] CMD...`

    Changes the ownership of the working directory to `user`,
    executes the command as `user`,
    and captures the stdout to `out` and the stderr to `err`.
    In addition, `capture` ensures that the environment does not contain `REC` or `SID` (the variables used for posting feedback).

    By default `user` is `nobody`, `out` is `/feedback/out` and `err` is `/feedback/err`.

    For example, `capture pre ./my_test` will execute `./my_test` as `nobody` and redirect stdout and stderr to `/feedback/out` and `/feedback/err`.

    If you need to run captured code as root, then use `capture -u root`.

* `asuser [-u user] CMD...`

    Drops privileges to the `user` and executes `CMD`.
    See command `capture`, which does output redirection before calling `asuser`.

    NB `asuser` must be executed as the user `root`, as we can only drop privileges.

    In addition to privileges, `asuser` makes following changes to the environment variables:

    * set `USER` to the `user`
    * set `HOME` to the home path of the `user`
    * set `UID` to the numerical id of the `user`
    * set `GID` to the numerical id of the main group of the `user`
    * drop locations ending in `*/sbin` from the `PATH`
    * remove `REC` and `SID` (used to post feedback to MOOC-Grader)

    _New in version 2.8._

    _Changed in version 3.1_: Added environment variables `UID` and `GID`

* `pre [-c class] CMD...`

    Wraps the stdout of the command into `<pre>` HTML element and escapes any HTML inside.
    Can be chained, e.g. `capture pre ./my_assessment_code.sh arg1 arg2`

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
    The grade wrapper will execute this command after the grading script.
    This command exits without changes if it is executed for the second time,
    thus grading script can call this too, but is not required to.

    If no argument is provided, there isn't `/feedback/points` and any of `/feedback/<number>` directories exists,
    then `create-test-feedback` is executed before reading the feedback.

    Gets granted points in priority order from:
    a) argument in format "5/10"
    b) /feedback/points file in format "5/10"
    c) /feedback/out including lines "TotalPoints: 5" and "MaxPoints: 10"

    Gets feedback as HTML from /feedback/out,
    and wraps /feedback/err into pre with `alert-danger` class at the end.
    If /feedback/appendix exists it will be included at the very end.

* `replace [-o out_file] REPLACE=in.txt [ANOTHER=another.txt] <template_file>`

    A simple string replace tool for handling untrusted inputs.
    The tool reads `template_file` and replaces all shell variables given as arguments with contents of the given files.
    For example, when given `REPLACE=in.txt` and `template_file`, then all instances of `$REPLACE` and `${REPLACE}` in `template_file` are replaced with contents of the file `in.txt`.
    Note that, if there exists a new line in the end of `in.txt`, it will be removed when the file is read.

    Please notice, the only valid shell variable names can be used, i.e. names consisting of letters, numbers and the underscore.

    This tool is wrapper around `envsubst` and the above command is basically the same as the following:

    ```sh
    REPLACE=$(cat in.txt) ANOTHER=$(cat another.txt) \
        envsubst '$REPLACE $ANOTHER' < in_file > out_file
    ```

    Keep in mind that for some purposes `sed` and `envsubst` are simpler,
    but when handling user input, `replace` might be cleaner.

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
    This is automatically executed by `grade` if preconditions apply.

* `err-to-out`

    Appends the `/feedback/err` to `/feedback/out` without `alert-danger` class.
    Useful for unit test frameworks that produce the feedback into stderr.

* `force-charset CHARSET`

    Converts recursively all files in working directory from any recognizable
    charsets into desired charset, e.g. utf-8. Discards unconvertible characters.
    May be useful to sanitize output from exotic student environments.

* `set-error [msg]`

    Sets submission error state by writing `true` to `/feedback/submission-set-error`.
    If `msg` is provided, then it is written as the reason to `/feedback/grading-script-errors`.

* [chpst](http://smarden.org/runit/chpst.8.html), [setuidgid](https://cr.yp.to/daemontools/setuidgid.html), [softlimit](https://cr.yp.to/daemontools/softlimit.html) and [setlock](https://cr.yp.to/daemontools/setlock.html)

    These utilities are used internally, but can also benefit when writing grading scripts.
    First one provides the other three.
    Read linked documentations for more details.

* [envsubst](http://man7.org/linux/man-pages/man1/envsubst.1.html)

    Substitutes environment variables in shell format strings.

    An example usage:

    ```sh
    $ echo 'My $COLOR dog is huge.' | COLOR=brown envsubst '$COLOR'
    My brown dog is huge.
    ```

* [time](http://man7.org/linux/man-pages/man1/time.1.html)

    Utility to measure statistics about timings (e.g. CPU usage).

* [timeout](http://man7.org/linux/man-pages/man1/timeout.1.html)

    Utility command to set wallclock timeouts for commands.
    You can use this to make sure a test fails after some timeout,
    so you can run second test before container is killed.

* `gitlab-api-query [-u git_url | -U git_url_file] TESTS.. GIT_HOST [api_token] [require_fork]`

    Checks information in GitLab API (v4) at the given host for given `git_url`.
    If no `git_url` is provided, then it is read from `git_url_file`.
    Default for `git_url_file` is `/submission/user/gitsource`, which is created by mooc-grader `types.stdasync.acceptGitAddress` for example,
    The `git_url` should end with `username/repo` or `username/repo.git`.

    GitLab API often requires authentication and a api token should be set in `api_token`.
    If the parameter starts with `.` or `/`, then it is expected to be a file containing the token.

    Supported tests:

    * `-p`: require that the project visibility is set to private.
    * `-f forked_repo`: require that the project is a fork from `forked_repo` (e.g. `username/upstream_repo`).

    Command exists with non zero if no tests are provided.

* `git-clone-submission PRIVATE_KEY_PATH [file paths...]`

    Clones repository from URL submitted as `gitsource` file
    into /submission-repo. The private ssh key allows
    access to repositories where the public key pair is added
    as a deploy key. Prints status and exits non zero if fails.

    * file paths...

        List of expected files to check inside the repository.
        The files are moved into /submission/user and the
        contents are written as appendix to end of feedback.


# Utility commands for grading image Dockerfiles

* `apt_install <package>`

    Calls apt-get update and apt-get install with list of packages.
    Takes care of correct options and cleaning temporary files in the end.
