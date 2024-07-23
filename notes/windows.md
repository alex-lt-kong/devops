
## PowerShell

- Add a profile file to `$HOME/Document/WindowsPowerShell/profile.ps1`

```
Set-PSReadlineKeyHandler -Key Tab -Function Complete
New-Alias -Name py -Value python
```