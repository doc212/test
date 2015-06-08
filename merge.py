#!/usr/bin/env python
"""
Merge a git hub pull request by its number
"""
import pygithub3

import sys
import logging
import subprocess
import os
import re
import pygithub3
logging.basicConfig(level=logging.DEBUG)

def shell(cmd, *accepted_codes):
    p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out,err=p.communicate()
    if p.returncode!=0 and p.returncode not in accepted_codes:
        raise RuntimeError, ("shell error",cmd,p.returncode, accepted_codes)
    return out

def githubConfig(key):
    item = shell("git config github."+key, 1)
    if not item:
        logging.error("github."+key+" is not configured")
        sys.exit(1)
    return item.strip()
logging.debug(sys.argv)

login = githubConfig("login")
password = githubConfig("password")
repo = githubConfig("repo")

prNumber = int(sys.argv[1])
msgFile = "/tmp/githubprmsg"
shell("gvim %s"%msgFile)
lines=[]
with open(msgFile) as fh:
    for l in fh:
        if not l.startswith("#"):
            lines.append(l)
msg="".join(lines).strip()
if msg!="":
    g=pygithub3.Github(login=login, password=password, user=login, repo=repo)
    g.pull_requests.merge(prNumber, msg)
else:
    logging.warn("aborting because of empty msg")
    sys.exit(1)
