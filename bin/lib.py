#!/usr/bin/env python
from __future__ import print_function
import sys, os, cgi, requests


OUT_FILE = "/feedback/out"
ERR_FILE = "/feedback/err"
APPENDIX_FILE = "/feedback/appendix"
POINTS_FILE = "/feedback/points"


def main():
    if len(sys.argv) < 1:
        print('Missing action for lib.py')
        sys.exit(1)
    action = sys.argv[1]
    if action == 'grade':
        parse_and_post_feedback(sys.argv[2] if len(sys.argv) > 2 else None)
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
    feedback = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.startswith("TotalPoints: "):
                    data["points"] = parse_int(line.strip()[13:], 0)
                elif line.startswith("MaxPoints: "):
                    data["max_points"] = parse_int(line.strip()[11:], 0)
                else:
                    feedback += line
    data["feedback"] = "".join(feedback)
    return data


def parse_points_string(source, data=None):
    data = data or get_empty_grade_data()
    parts = source.strip().split("/")
    if len(parts) == 2:
        data["points"] = parse_int(parts[0], 0)
        data["max_points"] = parse_int(parts[1], 0)
    return data


def post_grade_data(data):
    rec = os.environ.get("REC")
    if not rec:
        print('The URL for submitting feedback is lost!', file=sys.stderr)
        sys.exit(1)
    requests.post(rec + "/container-post", data)


def parse_and_post_feedback(points=None):

    # Check for points and captured stdout.
    if points:
        data = parse_points_string(points)
        data["feedback"] = read_file(OUT_FILE)
    elif os.path.exists(POINTS_FILE):
        data = parse_points_file(read_file(POINTS_FILE))
        data["feedback"] = read_file(OUT_FILE)
    else:
        data = parse_points_from_out(OUT_FILE)

    # Check for captured stderr.
    err = read_file(ERR_FILE).strip()
    if err:
        data["feedback"] += ('<pre class="alert alert-danger">'
            '{}</pre>'.format(escape_html(err)))

    # Check for appendix.
    if os.path.exists(APPENDIX_FILE):
        data["feedback"] += ('<div class="appendixes"><h4>Appendixes</h4>'
            '{}</div>'.format(read_file(APPENDIX_FILE)))

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
