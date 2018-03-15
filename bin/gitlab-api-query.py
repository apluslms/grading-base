#!/usr/bin/env python3
from __future__ import print_function
import sys, requests, lib
try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


SOURCE_FILE = "/submission/user/gitsource"


def main():
    if len(sys.argv) < 2:
        print("Usage: {} git_host [api_token] [forked_path]".format(sys.argv[0]))
        sys.exit(1)
    gitlab_api_query(*sys.argv[1:])


def gitlab_api_query(host, token = None, forked = None):
    source = lib.read_file(SOURCE_FILE).strip()
    url = None
    try:
        rid = quote_plus(source[source.index(":") + 1:-4])
        url = "https://{}/api/v3/projects/{}".format(host, rid)
        qs = "?private_token={}".format(token)

        r = requests.get(url + (qs if token else ''), timeout=3)
        if r.status_code == 200:
            gitlab_api_check(r.json(), forked)
        elif r.status_code == 404:
            if token:
                print("Did not find project:\n{}".format(url), file=sys.stderr)
                sys.exit(1)
        else:
            r.raise_for_status()
    except Exception as e:
        print("Failed to check project:\n{}".format(url), file=sys.stderr)
        print(str(e), file=sys.stderr);
        sys.exit(1)


def gitlab_api_check(json, forked = None):
    if json.get("public", True):
        print("{}\nhas public access in settings!\n"
            "Remove it to grade exercises."
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


if __name__ == '__main__':
    main()
