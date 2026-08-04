@echo off
title Goz Molasi - Masaustu kisayolu

rem  Masaustune, programi tek tikla acan bir kisayol koyar.

set "KLASOR=%~dp0"
set "HEDEF=%KLASOR%Goz Molasi.exe"

if not exist "%HEDEF%" (
  echo HATA: "Goz Molasi.exe" bulunamadi.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$yol = [Environment]::GetFolderPath('Desktop') + '\Goz Molasi.lnk';" ^
  "$s = (New-Object -ComObject WScript.Shell).CreateShortcut($yol);" ^
  "$s.TargetPath = $env:HEDEF;" ^
  "$s.WorkingDirectory = $env:KLASOR.TrimEnd('\');" ^
  "$s.Description = 'Her 20 dakikada 20 saniyelik goz molasi';" ^
  "$s.Save();" ^
  "if (Test-Path $yol) { Write-Host ''; Write-Host '  Masaustune \"Goz Molasi\" kisayolu olusturuldu.'; Write-Host '' } else { Write-Host 'Kisayol olusturulamadi.' }"

pause
