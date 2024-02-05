# Bash and GNU commands

- Search string in file content in a directory: `grep --recursive --line-number --word-regexp '<path>' -e '<string pattern>'`

- Better `history`

```
export HISTFILESIZE=10000
export HISTSIZE=10000
export HISTTIMEFORMAT="[%F %T] "
shopt -s histappend
```
