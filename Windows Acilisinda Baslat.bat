@echo off
title Goz Molasi - Windows acilisinda baslat

rem ===================================================================
rem  ACMA/KAPAMA dugmesi:
rem    Bir kez calistir  -> Windows her acildiginda Goz Molasi da acilir
rem    Tekrar calistir   -> otomatik acilma kapanir
rem
rem  Windows'un "Baslangic" klasorune kisayol koyar.
rem  Kayit defterine dokunmaz, yonetici yetkisi istemez.
rem ===================================================================

set "KLASOR=%~dp0"
set "HEDEF=%KLASOR%Goz Molasi.exe"

if not exist "%HEDEF%" (
  echo HATA: "Goz Molasi.exe" bulunamadi.
  echo Bu dosya uygulama klasorunde olmali.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$yol = [Environment]::GetFolderPath('Startup') + '\Goz Molasi.lnk';" ^
  "if (Test-Path $yol) {" ^
  "  Remove-Item $yol -Force;" ^
  "  Write-Host '';" ^
  "  Write-Host '  [KAPALI]  Otomatik baslatma kaldirildi.';" ^
  "  Write-Host '  Windows acilisinda artik kendiliginden acilmayacak.';" ^
  "  Write-Host '  Tekrar acmak icin bu dosyayi yeniden calistir.';" ^
  "} else {" ^
  "  $s = (New-Object -ComObject WScript.Shell).CreateShortcut($yol);" ^
  "  $s.TargetPath = $env:HEDEF;" ^
  "  $s.WorkingDirectory = $env:KLASOR.TrimEnd('\');" ^
  "  $s.WindowStyle = 7;" ^
  "  $s.Description = 'Goz Molasi - her 20 dakikada 20 saniye goz molasi';" ^
  "  $s.Save();" ^
  "  Write-Host '';" ^
  "  Write-Host '  [ACIK]  Otomatik baslatma kuruldu.';" ^
  "  Write-Host '';" ^
  "  Write-Host '  Windows her acildiginda Goz Molasi arka planda baslar.';" ^
  "  Write-Host '  Pencere gorunmez; gorev cubugundan ulasabilirsin.';" ^
  "  Write-Host '  Her 20 dakikada bir ekrani 20 saniye kaplar.';" ^
  "  Write-Host '';" ^
  "  Write-Host '  Bilgisayar basinda degilken sayac bosa donmez:';" ^
  "  Write-Host '  90 saniye dokunulmazsa durur, ilk dokunusta devam eder.';" ^
  "  Write-Host '  5 dakikadan uzun uzak kaldiysan bastan sayar.';" ^
  "  Write-Host '';" ^
  "  Write-Host '  Kapatmak icin bu dosyayi tekrar calistir.';" ^
  "}"

echo.
pause
