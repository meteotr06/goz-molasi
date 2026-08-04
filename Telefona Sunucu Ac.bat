@echo off
title Goz Molasi

rem ===================================================================
rem  Uygulamayi kucuk bir yerel sunucuyla baslatir ve tarayicida
rem  "uygulama penceresi" olarak acar.
rem
rem  Neden sunucu? Bildirimler, cevrimdisi calisma ve "ana ekrana ekle"
rem  ozellikleri dosyaya cift tiklayinca (file://) calismaz; sadece
rem  http:// uzerinden calisir.
rem
rem  NOT: Bu dosyanin icinde ve adinda bilerek Turkce karakter yok.
rem  Windows komut satiri (cmd) Turkce karakterli .bat dosyalarinda
rem  kodlama hatasi verebiliyor. Uygulamanin kendisi tamamen Turkce.
rem ===================================================================

set "KLASOR=%~dp0"
set "PORT=8451"
set "ADRES=http://localhost:%PORT%/index.html"

if not exist "%KLASOR%index.html" (
  echo HATA: index.html bulunamadi.
  echo Bu dosya uygulama klasorunde olmali.
  pause
  exit /b 1
)

where python >nul 2>&1
if errorlevel 1 goto :pythonsuz

rem Sunucu zaten acikssa tekrar acma
powershell -NoProfile -Command "$c = New-Object Net.Sockets.TcpClient; try { $c.Connect('127.0.0.1', %PORT%); exit 0 } catch { exit 1 } finally { $c.Close() }" >nul 2>&1
if not errorlevel 1 goto :tarayiciyi_ac

start "Goz Molasi sunucu" /min cmd /c "cd /d "%KLASOR%" && python -m http.server %PORT%"
powershell -NoProfile -Command "Start-Sleep -Milliseconds 1500" >nul

:tarayiciyi_ac
set "TARAYICI="
for %%T in (
  "%ProgramFiles%\Google\Chrome\Application\chrome.exe"
  "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
  "%LocalAppData%\Google\Chrome\Application\chrome.exe"
  "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
  "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
) do if not defined TARAYICI if exist %%T set "TARAYICI=%%~T"

if defined TARAYICI (
  start "" "%TARAYICI%" --app=%ADRES% --window-size=900,780
) else (
  start "" %ADRES%
)
exit /b 0

:pythonsuz
echo.
echo   Python bulunamadi.
echo   Uygulama yine de calisir; ama bildirimler ve cevrimdisi
echo   kullanim devre disi kalir.
echo.
echo   Tam surum icin python.org adresinden Python kurup
echo   bu dosyayi tekrar calistir.
echo.
pause
start "" "%KLASOR%index.html"
exit /b 0
