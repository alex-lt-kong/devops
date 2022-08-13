## Use a proxy

* `git config --global http.proxy 'socks5://127.0.0.1:6666'`

## Merge two Git repositories without breaking their commit logs

* `cd` into `repo_a`.

* Add `repo_b` to `repo_a`: `git remote add --fetch <name_of_repo_a> <URL_of_repo_a>`

* Merge: `git merge <name_of_repo_a>/<branch_of_repo_a> --allow-unrelated-histories`

* Optional: Move files of `repo_a` into a sub-directory

* Commit: `git commit -m "Move repo_a files into subdir"`