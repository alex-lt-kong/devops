
## PowerShell

- Add a profile file to `$HOME/Documents/WindowsPowerShell/profile.ps1`

- Sample profile
```{PowerShell}
# Make PowerShell's tab behavior similar to Bash
Set-PSReadlineKeyHandler -Key Tab -Function Complete
# Bash's alias py=python
New-Alias -Name py -Value python
```
