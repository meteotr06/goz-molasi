# -*- coding: utf-8 -*-
"""AÇILIŞ SINAMASI — derlenen exe GERÇEKTEN açılıyor mu?

NEDEN VAR
  Bir derleme "başarılı" çıktı, exe oluştu, ama çalıştırınca hiç
  açılmadı: panele eklenen bir şeritte parametre hatası vardı ve
  program daha pencereyi kurarken çöküyordu. Derleme çıktısına
  bakıp geçmek yetmiyor — DERLEME BAŞARILI, UYGULAMA AÇILIYOR
  demek DEĞİL.

  Bu sınama exe'yi gerçekten çalıştırır, penceresinin açılmasını
  bekler ve sonra kapatır. Açılmazsa derleme yayına çıkmaz.

NE DENETLER
  1. exe dosyası var mı
  2. çalıştırılınca süreç ayakta kalıyor mu (çökmüyor mu)
  3. "pencereni göster" dendiğinde pencere gerçekten geliyor mu
  4. pencere ekranın dışında kalmıyor mu

ÇALIŞTIRMA
  python sinama_acilis.py
"""
import ctypes
import os
import subprocess
import sys
import time
from ctypes import wintypes

import izleyici as iz
import kilit as kl

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = os.path.join(KOK, "Goz Molasi.exe")
KAYIT_KLASOR = os.path.join(os.environ.get("APPDATA", ""), "GozMolasi")

# Pencerenin gelmesi için tanınan süre. Soğuk açılışta PyInstaller
# tek dosyayı geçici klasöre açıyor, bu birkaç saniye sürebiliyor.
BEKLEME_SN = 25


def pencereyi_bul(baslik_parcasi="Göz Molası"):
    """Görünür pencereler arasında başlığı eşleşeni bul."""
    user32 = ctypes.windll.user32
    bulunan = []

    def geri(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        n = user32.GetWindowTextLengthW(hwnd)
        if n == 0:
            return True
        tampon = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(hwnd, tampon, n + 1)
        if baslik_parcasi in tampon.value:
            bulunan.append(hwnd)
        return True

    TIP = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(TIP(geri), 0)
    return bulunan[0] if bulunan else None


def calisiyor_mu():
    """Şu an açık bir kopya var mı?"""
    try:
        cikti = subprocess.check_output(
            ["tasklist", "/FI", "IMAGENAME eq Goz Molasi.exe"],
            stderr=subprocess.DEVNULL).decode("utf-8", "replace")
        return "Goz Molasi.exe" in cikti
    except Exception:
        return False


def calisan_kopyalari_kapat():
    """Açık kopyaları kapatır.

    TEMİZ ÇIKIŞ BAYRAĞI ÖNCE YAZILIR. Sebebi: programın bir bekçisi
    var ve temiz çıkmadan ölen programı yeniden başlatıyor. Bayrağı
    yazmazsak bekçi sınamayla yarışa giriyor — biri öldürüyor, öbürü
    açıyor — ve sınama neyi ölçtüğünü bilemiyor.
    """
    try:
        os.makedirs(KAYIT_KLASOR, exist_ok=True)
        with open(os.path.join(KAYIT_KLASOR, "temiz_cikis.bayrak"), "w") as f:
            f.write(str(time.time()))
    except Exception:
        pass
    subprocess.call(["taskkill", "/IM", "Goz Molasi.exe", "/F"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)


def main():
    hatalar = []
    iz.dpi_farkindaligi_ac()

    # 1) exe var mı
    if not os.path.exists(EXE):
        print("BAŞARISIZ — exe yok:", EXE)
        return 1
    print("exe bulundu: %.1f MB" % (os.path.getsize(EXE) / 1048576.0))

    # Sınamadan ÖNCE açık mıydı? Sonunda aynı durumu geri kuracağız.
    onceden_calisiyordu = calisiyor_mu()
    if onceden_calisiyordu:
        print("program açıktı — sınama bitince geri açılacak")

    # Temiz başlangıç: açık kopya varsa kapat, yoksa tek örnek kilidi
    # yüzünden yeni kopya hemen çıkar ve sınama yanlış sonuç verir.
    calisan_kopyalari_kapat()

    # 2) çalıştır ve ayakta kalıyor mu
    surec = subprocess.Popen([EXE], cwd=KOK)
    time.sleep(4)
    if surec.poll() is not None:
        hatalar.append("program açılır açılmaz kapandı (çıkış kodu %s)"
                       % surec.returncode)
        print("BAŞARISIZ —", hatalar[-1])
        return 1
    print("süreç ayakta (pid %d)" % surec.pid)

    # 3) pencere geliyor mu
    hwnd = None
    kl.goster_iste(KAYIT_KLASOR)
    basladi = time.time()
    while time.time() - basladi < BEKLEME_SN:
        if surec.poll() is not None:
            hatalar.append("program pencere açmadan çöktü (çıkış kodu %s)"
                           % surec.returncode)
            break
        hwnd = pencereyi_bul()
        if hwnd:
            break
        time.sleep(0.5)
        kl.goster_iste(KAYIT_KLASOR)

    if not hatalar and not hwnd:
        hatalar.append("%d saniyede pencere açılmadı" % BEKLEME_SN)

    # 4) pencere ekranın içinde mi
    if hwnd:
        k = wintypes.RECT()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(
            wintypes.HWND(hwnd), ctypes.c_uint(9), ctypes.byref(k),
            ctypes.sizeof(k))
        print("pencere açıldı: %dx%d konum (%d,%d)"
              % (k.right - k.left, k.bottom - k.top, k.left, k.top))
        a_sol, a_ust, a_gen, a_yuk = iz.calisma_alani()
        if k.bottom > a_ust + a_yuk + 8 or k.right > a_sol + a_gen + 8:
            hatalar.append(
                "pencere çalışma alanının DIŞINA taşıyor: alt kenar %d, "
                "çalışma alanı %d — alttaki düğmeler tıklanamaz"
                % (k.bottom, a_ust + a_yuk))
        if k.top < a_ust - 8 or k.left < a_sol - 8:
            hatalar.append("pencere ekranın soluna/üstüne taşıyor: (%d,%d)"
                           % (k.left, k.top))

    # Temizlik: sınamanın açtığı kopyayı kapat
    calisan_kopyalari_kapat()

    # SINAMA KULLANICININ PROGRAMINI ÖLDÜRMÜŞ HALDE BIRAKMAZ.
    # Bir kez böyle oldu: sınama programı kapattı, kimse geri açmadı ve
    # kullanıcı saatlerce mola almadan çalıştı. Sınamanın görevi hata
    # bulmak, kullanıcıyı korumasız bırakmak değil.
    if onceden_calisiyordu:
        try:
            subprocess.Popen([EXE], cwd=KOK)
            time.sleep(2.5)
            if calisiyor_mu():
                print("program geri açıldı (sınamadan önce açıktı)")
            else:
                hatalar.append("sınama sonrası program geri AÇILAMADI — "
                               "kullanıcı korumasız kaldı")
        except Exception as e:
            hatalar.append("sınama sonrası program geri açılamadı: %r" % e)

    if hatalar:
        print("\nBAŞARISIZ — %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("TAMAM — exe açılıyor, pencere geliyor, ekrana sığıyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
