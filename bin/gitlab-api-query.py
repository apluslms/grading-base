#!/usr/bin/env python
import lib
import requests
try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


SOURCE_FILE = "/submission/user/gitsource"


def main():
    if len(sys.argv) < 1:
        print("Usage: git_host [api_token] [forked_path]")
        sys.exit(1)
    gitlab_api_query(*sys.argv)


def gitlab_api_query(host, token = None, forked = None):
    source = lib.read_file(SOURCE_FILE)
    url = None
    try:
        rid = quote_plus(source[source.index(":") + 1:])
        url = "https://{}/api/v3/projects/{}".format(host, rid)
        qs += "?private_token={}".format(token)

        r = requests.get(url + (qs if token else ''), timeout=3)
        if r.status_code == 200:
            qitlab_api_check(r.json(), forked)
        elif r.status_code == 404:
            if token:
                println("Did not find project: {}".format(url))
                sys.exit(1)
        else:
            r.raise_for_status()
    except Exception:
        println("Failed to check project: {}".format(url))
        sys.exit(1)


def gitlab_api_check(json, forked = None):
    if json.get("public", True):
        println("{} has public access in settings! Remove it to grade exercises.".format(json["web_url"]))
        sys.exit(1)
    if forked:
        if (
            not "forked_from_project" in json
            or json["forked_from_project"]["path_with_namespace"] != forked
        ):
            println("{} is not forked from {}.".format(json("web_url", forked)))
            sys.exit(1)


if __name__ == '__main__':
    main()
