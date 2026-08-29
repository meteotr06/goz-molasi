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
# Mola ekrani acikken panel bulunamaz; varsayilan mola 20 saniye.
# Sure bunu kapsamali, yoksa 'pencere acilmadi' diye yanlis kalir.
BEKLEME_SN = 45


def _kutu(hwnd):
    """Pencerenin gerçek dış kutusu (gölge payı olmadan)."""
    k = wintypes.RECT()
    ctypes.windll.dwmapi.DwmGetWindowAttribute(
        wintypes.HWND(hwnd), ctypes.c_uint(9), ctypes.byref(k), ctypes.sizeof(k))
    return k


def pencereyi_bul(baslik_parcasi="Göz Molası"):
    """Görünür pencereler arasında ANA PANELİ bul.

    TAM EKRAN PENCERELERİ ATLIYOR. Mola ve engel ekranları da aynı
    başlığı taşıyor ve bütün monitörleri kaplıyor. Bir kez bu yüzden
    derleme kaldı: program açılırken kaçırılmış bir molayı hemen verdi,
    sınama 1920x1200'lük mola ekranını panel sanıp "pencere ekrana
    sığmıyor" dedi. Kod doğruydu, sınama yanılıyordu.
    """
    user32 = ctypes.windll.user32
    ekran_g = user32.GetSystemMetrics(0)
    ekran_y = user32.GetSystemMetrics(1)
    bulunan = []

    def geri(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        n = user32.GetWindowTextLengthW(hwnd)
        if n == 0:
            return True
        tampon = ctypes.create_unicode_buffer(n + 1)
        user32.GetWindowTextW(hwnd, tampon, n + 1)
        if baslik_parcasi not in tampon.value:
            return True
        k = _kutu(hwnd)
        # Ekranı kaplayan pencere paneldir DEĞİL: mola/engel ekranı.
        if (k.right - k.left) >= ekran_g - 4 and (k.bottom - k.top) >= ekran_y - 4:
            return True
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


def kayit_kanatlari(hatalar):
    """Açılışta başlatma: her kanat KENDİ onay baytıyla mı okunuyor?

    NİYE VAR (29.08.2026 ölçümü)
      acilista_baslar_mi() şöyle yazıyordu:
          (kayit_var_mi() or kısayol_var) and kayit_etkin_mi()
      kayit_etkin_mi() yalnız "StartupApproved > Run" altını okuyor.
      Windows ise Başlangıç KLASÖRÜ kısayolunu ayrı bir anahtarda
      ("StartupApproved > StartupFolder", değer adı "Goz Molasi.lnk")
      işaretliyor. OKU.md'nin tarif ettiği İLK kurulum yolu
      ("Windows Acilisinda Baslat.bat") yalnız kısayol koyuyor — yani
      belgelenmiş kurulumun çıktısı tam da kodun göremediği kanattı.
      Sonuç: kullanıcı Görev Yöneticisi'nden kapatınca ayarlardaki
      kutu İŞARETLİ kalıyor, program hiç açılmıyor, molalar duruyor.
      Ayrıca "kullanıcı kapattı" ile "kayıt kayboldu" ayrılmadığı için
      uygulama kullanıcının kararını geri koyuyordu.

    KAYIT DEFTERİNE DOKUNMUYOR: kilit.py'nin OKUMA işlevleri geçici
    olarak değiştiriliyor, sonunda geri konuyor. Gerçek anahtarlara
    tek bayt yazılmıyor.
    """
    import tempfile

    print("--- 0) AÇILIŞTA BAŞLATMA KANATLARI ---")

    def kontrol(ad, sart, ayrinti=""):
        if not sart:
            hatalar.append("%s%s" % (ad, (" - " + ayrinti) if ayrinti else ""))
        print("  %-54s %s" % (ad, "TAMAM" if sart else "KALDI"))

    if not hasattr(kl, "_onay_bayti") or not hasattr(kl, "kisayol_etkin_mi"):
        kontrol("kilit.py kısayolun onay baytını okuyor", False,
                "_onay_bayti / kisayol_etkin_mi yok — kısayol kanadı kör")
        return

    gecici = tempfile.mkdtemp(prefix="gm_acilis_")
    lnk_var_yol = os.path.join(gecici, "Goz Molasi.lnk")
    lnk_yok_yol = os.path.join(gecici, "yok", "Goz Molasi.lnk")
    with open(lnk_var_yol, "w", encoding="utf-8") as d:
        d.write("sahte kisayol")

    e_onay = kl._onay_bayti
    e_kayit = kl.kayit_var_mi
    e_yol = kl.baslangic_kisayolu
    try:
        def kur(run_bayt, klasor_bayt, run_var, lnk_var):
            baytlar = {(kl.ONAY_ANAHTARI, kl.KAYIT_ADI): run_bayt,
                       (kl.ONAY_KISAYOL_ANAHTARI, "Goz Molasi.lnk"): klasor_bayt}
            kl._onay_bayti = lambda a, ad: baytlar.get((a, ad))
            kl.kayit_var_mi = lambda: run_var
            kl.baslangic_kisayolu = lambda: (lnk_var_yol if lnk_var
                                             else lnk_yok_yol)

        # (ad, run_bayt, klasor_bayt, run_var, lnk_var, beklenen)
        DURUMLAR = [
            ("kurulu degil",                        None, None, 0, 0, False),
            ("yalniz kisayol, acik",                None, 2,    0, 1, True),
            ("yalniz kisayol, GorevYon KAPATTI",    None, 3,    0, 1, False),
            ("yalniz kayit, acik",                  None, None, 1, 0, True),
            ("yalniz kayit, GorevYon KAPATTI",      3,    None, 1, 0, False),
            ("ikisi var, yalniz kisayol kapali",    2,    3,    1, 1, True),
            ("ikisi var, yalniz kayit kapali",      3,    2,    1, 1, True),
            ("ikisi var, ikisi de kapali",          3,    3,    1, 1, False),
        ]
        for ad, rb, kb, rv, lv, beklenen in DURUMLAR:
            kur(rb, kb, bool(rv), bool(lv))
            sonuc = kl.acilista_baslar_mi()
            kontrol("acilista baslar mi · %-34s -> %s" % (ad, beklenen),
                    sonuc is beklenen, "kod %r dedi" % sonuc)

        # KULLANICI KAPATTI MI: "kayit kayboldu" ile ayni belirtiyi
        # veriyor ama ayni sey degil. Ayrilmazsa kullanicinin karari
        # geri aliniyor ve suc temizlik programina atiliyor.
        for ad, rb, kb, beklenen in [
                ("hicbir isaret yok (gercekten silinmis)", None, None, False),
                ("kayit kanadi kapatilmis",                3,    None, True),
                ("kisayol kanadi kapatilmis",              None, 3,    True),
                ("ikisi de etkin",                         2,    2,    False)]:
            kur(rb, kb, True, True)
            sonuc = kl.kullanici_windowstan_kapatti_mi()
            kontrol("kullanici kapatti mi · %-33s -> %s" % (ad, beklenen),
                    sonuc is beklenen, "kod %r dedi" % sonuc)
    finally:
        kl._onay_bayti = e_onay
        kl.kayit_var_mi = e_kayit
        kl.baslangic_kisayolu = e_yol
        try:
            os.remove(lnk_var_yol)
            os.rmdir(gecici)
        except Exception:
            pass


def main():
    hatalar = []
    iz.dpi_farkindaligi_ac()

    # 0) Açılışta başlatma kanatları — kayıt defterine dokunmaz,
    #    exe olmasa da koşar; o yüzden exe denetiminden ÖNCE.
    kayit_kanatlari(hatalar)
    if hatalar:
        print("BAŞARISIZ — açılışta başlatma kanatları:")
        for h in hatalar:
            print("  -", h)
        return 1

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
        # SIMGE DURUMUNDAKI PENCERE ÖLÇÜLEMEZ.
        #
        # Windows, küçültülmüş pencere için (-32000,-32000) döndürür.
        # Bu sınama onu "ekranın soluna taşıyor" sanıyordu ve
        # ÜÇ KOŞUDAN BİRİNDE yanlış yere KALDI diyordu (ölçüldü,
        # 29.08.2026). Yanlış kırmızı burada pahalı: bu sınama
        # `DERLE.bat`'ı durduruyor — kullanıcı derleyemez ve
        # uygulamayı bozuk sanır.
        #
        # Çözüm: ölçmeden önce pencereyi geri getir. Böylece ölçüm
        # deterministik olur; "ölçemedim" diye geçmek yerine
        # ÖLÇÜLEBİLİR hâle getiriyoruz.
        try:
            if ctypes.windll.user32.IsIconic(wintypes.HWND(hwnd)):
                ctypes.windll.user32.ShowWindow(wintypes.HWND(hwnd), 9)  # RESTORE
                time.sleep(1.2)
        except Exception:
            pass
        k = _kutu(hwnd)
        print("panel açıldı: %dx%d konum (%d,%d)"
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
