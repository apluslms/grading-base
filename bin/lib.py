#!/usr/bin/env python
import sys, os, cgi, requests


OUT_FILE = "/feedback/out"
ERR_FILE = "/feedback/err"
APPENDIX_FILE = "/feedback/appendix"
POINTS_FILE = "/feedback/points"


def main():
    if len(sys.argv) == 0:
        print('Missing action for lib.py')
        sys.exit(0)
    action = sys.argv[0]
    if action == 'grade':
        parse_and_post_feedback()
    else:
        print('Unknown action: {}'.format(action))


def get_empty_grade_data():
    return {
        "sid": os.environ.get("SID"),
        "points": 0,
        "max_points": 0,
        "feedback": "",
    }


def parse_points_from_out(path, data=None):
    data = data or get_empty_grade_data()
    with open(path, "r") as f:
        feedback = []
        for line in f:
            if line.startswith("TotalPoints: "):
                data["points"] = parse_int(line.strip()[13:], 0)
            elif line.startswith("MaxPoints: "):
                data["max_points"] = parse_int(line.strip()[11:], 0)
            else:
                feedback += line
    data["feedback"] = "".join(feedback)
    return data


def parse_points_file(path, data=None):
    data = data or get_empty_grade_data()
    parts = read_file(path).strip().split("/")
    if len(parts) == 2:
        data["points"] = parse_int(parts[0], 0)
        data["max_points"] = parse_int(parts[1], 0)
    return data


def post_grade_data(data):
    url = os.environ.get("REC") + "/container-post"
    requests.post(url, data)


def parse_and_post_feedback():

    # Check for points and captured stdout.
    if os.path.exists(POINTS_FILE):
        data = parse_points_file(POINTS_FILE)
        data["feedback"] = read_file(OUT_FILE)
    else:
        data = parse_points_from_out(OUT_FILE)

    # Check for captured stderr.
    err = read_file(ERR_FILE).strip()
    if err:
        data["feedback"] += '<pre class="alert alert-danger">{}</pre>'.format(
            escape_html(err)
        )

    post_grade_data(data)


def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r") as f:
        return f.read()


def parse_int(source, default):
    try:
        return int(source)
    except ValueError:
        return default


def escape_html(source):
    return cgi.escape(source)


if __name__ == '__main__':
    main()
