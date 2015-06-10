import git
r= git.Repo(".")
for b in r.branches:
    if b!=r.active_branch:
        r.delete_head(b)
