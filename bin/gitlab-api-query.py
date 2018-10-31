#!/usr/bin/env python3
import sys, requests, os.path
from urllib.parse import urlencode


SOURCE_FILE = "/submission/user/gitsource"


def main():
    if len(sys.argv) < 2:
        print("Usage: {} git_host [api_token] [forked_path]".format(sys.argv[0]))
        sys.exit(1)
    gitlab_api_query(*sys.argv[1:])


class Gitlab:
    def __init__(self, host, token = None):
        self.host = host
        self.token = token

    def get(self, path, args={}):
        safe_url = "https://{}/api/v4/{}?{}".format(self.host, path, urlencode(args))
        if self.token:
            args['private_token'] = self.token
        url = "https://{}/api/v4/{}?{}".format(self.host, path, urlencode(args))
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return r.json()
        else:
            r.url = safe_url
            r.raise_for_status()

def gitlab_api_query(host, token = None, forked = None):
    source = read_file(SOURCE_FILE).strip()
    gitlab = Gitlab(host, token)
    try:
        rid = source.rpartition(':')[2][:-4]
        username, project_path = rid.split('/', 1)

        users = gitlab.get('users', dict(username=username))
        if len(users) != 1:
            raise RuntimeError("Couldn't find user {!r}".format(username))
        uid = users[0]['id']

        projects = gitlab.get('users/{}/projects'.format(uid))
        projects = [p for p in projects if p['path'] == project_path]
        if len(projects) != 1:
            raise RuntimeError("Couldn't find project {!r} from user {!r}. Do we have access?".format(project_path, username))

        gitlab_api_check(projects[0], forked)
    except Exception as e:
        print("Failed to check project {!r}".format(source), file=sys.stderr)
        print(str(e), file=sys.stderr);
        sys.exit(1)


def gitlab_api_check(json, forked = None):
    if json.get("visibility") != 'private':
        print("{}\nProject is not private! Change visibility to private in project settings for submission to be graded!"
            .format(json["web_url"]), file=sys.stderr)
        sys.exit(1)
    if forked:
        if (
            not "forked_from_project" in json
            or json["forked_from_project"]["path_with_namespace"] != forked
        ):
            print("{}\nis not forked from {}.\nStart from the fork step."
                .format(json["web_url"], forked), file=sys.stderr)
            sys.exit(1)

def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r") as f:
        return f.read()


if __name__ == '__main__':
    main()
