# Bash and GNU commands

- Search string in file content in a directory: `grep --recursive --line-number --word-regexp '<path>' -e '<string pattern>'`

- Randomly remove 90% of files in a directory: `ls | awk 'NR % 10 != 1' | xargs rm`

- Better `history`

```
export HISTFILESIZE=10000
export HISTSIZE=10000
export HISTTIMEFORMAT="[%F %T] "
shopt -s histappend
```

- Turn on/off monitor:

```
DISPLAY=:0 xrandr --output VGA-1 --off
DISPLAY=:0 xrandr --output VGA-1 --auto --mode 1440x900
```
