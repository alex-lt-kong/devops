## PowerShell

- Upgrade to PowerShell version 7 gives you a much similar feeling to bash

- Sample profile

```{PowerShell}
# Make PowerShell's tab behavior similar to Bash
Set-PSReadlineKeyHandler -Key Tab -Function Complete
# Disable the silly autocomplete
# https://stackoverflow.com/questions/75205636/how-to-disable-suggestion-while-typing-in-powersh
Set-PSReadLineOption -PredictionSource None

# Bash's alias py=python
New-Alias -Name py -Value python

# Mimic host
Set-Alias -Name host -Value Resolve-DnsName
```

- Update the profile file

```
cat $PROFILE
mkdir $(Split-Path -Path $PROFILE -Parent)
"" >> $PROFILE
```
