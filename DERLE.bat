@echo off
REM ======================================================================
REM  Goz Molasi masaustu surumunu derler.
REM
REM  ONEMLI: bu betik artik SINAMALARI da calistirir ve sinama gecmezse
REM  uygulamayi ACMAZ. Sebebi: gecmiste "derleme basarili" cikan bir surum
REM  calistirilinca hic acilmadi, bir baskasinda panelde iki kutu ust uste
REM  bindi, bir digerinde pencerenin alti gorev cubugunun altinda kaldi.
REM  Hicbiri derleme ciktisindan anlasilmiyordu. Artik makine bakiyor.
REM
REM  Sira: once UCUZ sinamalar (veri + yerlesim) -> derleme -> ACILIS
REM  sinamasi. Kaynakta hata varsa 2 dakikalik derlemeyi hic baslatmiyoruz.
REM
REM  Derleme ciktilari proje icinde kalir (masaustu\build).
REM  Cikan dosya: "Goz Molasi.exe"
REM ======================================================================
cd /d "%~dp0"

echo.
echo [1/4] Kaynak sinamalari (veri + yerlesim)...
echo ----------------------------------------------------------------------
python "%~dp0masaustu\sinama.py" hizli
if errorlevel 1 (
  echo.
  echo ======================================================================
  echo  SINAMA BASARISIZ - DERLEME YAPILMADI.
  echo  Yukaridaki sorunlari duzeltmeden yayinlama.
  echo ======================================================================
  pause
  exit /b 1
)

echo.
echo [2/4] Calisan surum kapatiliyor...
echo 1> "%APPDATA%\GozMolasi\temiz_cikis.bayrak" 2>nul
taskkill /IM "Goz Molasi.exe" /F >nul 2>&1
rem  timeout.exe girdi yonlendirilince calismiyor ve beklemeyi
rem  atliyordu ("Input redirection is not supported"). O bekleme
rem  onemli: oldurulen surecin exe dosyasini birakmasi lazim.
ping -n 3 127.0.0.1 >nul

echo.
echo [3/4] Derleniyor...
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
echo [4/5] Acilis sinamasi - exe gercekten aciliyor mu...
echo ----------------------------------------------------------------------
python "%~dp0masaustu\sinama_acilis.py"
if errorlevel 1 (
  echo.
  echo ======================================================================
  echo  EXE DERLENDI AMA ACILIS SINAMASINI GECEMEDI.
  echo  Uygulama ACILMIYOR. Bu surumu kimseye verme.
  echo ======================================================================
  pause
  exit /b 1
)

echo.
echo [5/5] Icerik denetimi - bugunku duzeltmeler exe'nin ICINDE mi...
echo ----------------------------------------------------------------------
REM  "Aciliyor" ile "icinde dogru kod var" AYRI seylerdir. Acilis
REM  sinamasi birincisini olcuyor; bu adim ikincisini. Eski bir exe de
REM  sorunsuz acilir - ve kullanici duzeltilmis sandigi hatayi
REM  yasamaya devam eder. Olculdu 29.08.2026: bu adim yoktu.
python "%~dp0masaustu\exe_icerik.py"
if errorlevel 1 (
  echo.
  echo ======================================================================
  echo  EXE ACILIYOR AMA ICERIGI ESKI.
  echo  Kaynaktaki duzeltmeler bu exe'ye girmemis. Derleme eski dosyadan
  echo  yapilmis ya da PyInstaller onbellegi kullanmis olabilir.
  echo  Cozum: build\ ve dist\ klasorlerini silip yeniden derle.
  echo ======================================================================
  pause
  exit /b 1
)

echo.
echo ======================================================================
echo  HEPSI GECTI. Uygulama aciliyor...
echo ======================================================================
start "" "%~dp0Goz Molasi.exe"
