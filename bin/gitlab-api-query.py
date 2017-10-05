#!/usr/bin/env python

#TODO

def gitlabquery(course, exercise, action, submission_dir):
    '''
    Queries gitlab API to check repository properties.
    '''
    if not "require_gitlab" in exercise:
        raise ConfigError("This action needs require_gitlab in exercise.")
    if not "token" in action:
        raise ConfigError("Token missing from configuration for gitlab privacy check.")
    url = None
    err = ""
    try:
        with open(submission_dir + "/user/gitsource") as content:
            source = content.read()
        try:
            from urllib.parse import quote_plus
        except ImportError:
            from urllib import quote_plus
        rid = quote_plus(source[source.index(":") + 1:])
        url = "https://%s/api/v3/projects/%s?private_token=%s" % (exercise["require_gitlab"], rid, action["token"])
        data = get_json(url)
        if "private" in action and action["private"] and data["public"]:
            err = "%s has public access in settings! Remove it to grade exercises." % (data["web_url"])
        if "forks" in action:
            if not "forked_from_project" in data or \
                data["forked_from_project"]["path_with_namespace"] != action["forks"]:
                err = "%s is not forked from %s." % (data["web_url"], action["forks"])
    except Exception:
        LOGGER.exception("Failed to check gitlab URL: %s", url)
    return { "points": 0, "max_points": 0, "out": "", "err": err, "stop": err != "" }
