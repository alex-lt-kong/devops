# Git

## One-liners

- Revert the current commit to a previous commit: `git reset --hard <commit_id>`
- Revert uncommitted changes to the current commit: `git restore <file_path_to_be_reverted>`
- Use a proxy: `git config --global http.proxy 'socks5://127.0.0.1:6666'`

## Make .gitignore effective

```bash
git rm -rf --cached .
git add .
```

## Pull latest change from `master` into my branch

```bash
git fetch origin
git merge origin/master
```

## Store credentials

- `git config [--global] credential.helper <cache/store>`
  - The "cache" mode keeps credentials in memory for a certain period of time. They are purged from
    the cache after 15 minutes.
  - The "store" mode saves the credentials to a plain-text file on disk in home directory, and they never expire.

## Submodules

- Add new submodule: `git submodule add <remote_url> <destination_folder>`
- Pull content of a submodule after `git clone`: `git submodule update --init --recursive`

## Change username and email:

- `git config user.name "FirstName LastName"`
- `git config user.email "email@website.com"`

## Merge two Git repositories without breaking their commit logs

- `cd` into `repo_a`.
- Add `repo_b` to `repo_a`: `git remote add --fetch <name_of_repo_a> <URL_of_repo_a>`
- Merge: `git merge <name_of_repo_a>/<branch_of_repo_a> --allow-unrelated-histories`
- Optional: Move files of `repo_a` into a sub-directory
- Commit: `git commit -m "Move repo_a files into subdir"`
