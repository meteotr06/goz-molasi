@echo off
REM Goz Molasi masaustu surumunu derler.
REM Derleme cikitilari proje icinde kalir (masaustu\build), disariya
REM hicbir sey yazilmaz. Cikan dosya: "Goz Molasi.exe"
cd /d "%~dp0"
echo Calisan surum kapatiliyor...
echo 1> "%APPDATA%\GozMolasi\temiz_cikis.bayrak" 2>nul
taskkill /IM "Goz Molasi.exe" /F >nul 2>&1
timeout /t 2 /nobreak >nul

echo Derleniyor...
python -m PyInstaller --noconfirm --onefile --noconsole ^
  --name "Goz Molasi" --icon "%~dp0masaustu\ikon.ico" ^
  --hidden-import pystray._win32 ^
  --distpath "%~dp0." ^
  --workpath "%~dp0masaustu\build" ^
  --specpath "%~dp0masaustu\build" ^
  "%~dp0masaustu\goz_molasi.py"

if errorlevel 1 (
  echo.
  echo DERLEME BASARISIZ.
  pause
  exit /b 1
)

echo.
echo Tamam. Uygulama aciliyor...
start "" "%~dp0Goz Molasi.exe"
