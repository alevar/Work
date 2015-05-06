wWshShell.Run "msiexec /x {26A24AE4-039D-4CA4-87B4-2F03217067FF} /q",1,True

IF EXIST "C:\Program Files (x86)" goto both
jre-8u45-windows-i586.exe /s /norestart
exit
:both
jre-8u45-windows-x64.exe /s /norestart
jre-8u45-windows-i586.exe /s /norestart
exit
