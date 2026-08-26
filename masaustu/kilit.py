# -*- coding: utf-8 -*-
"""
KİLİT — Şifre saklama ve programı ayakta tutan bekçi.

ŞİFRELEME NEDEN BÖYLE?
----------------------
Şifre asla düz metin saklanmaz. Ama düz SHA-256 de yeterli değil:
4 haneli bir şifrede sadece 10.000 ihtimal var; sıradan bir bilgisayar
SHA-256 ile saniyede milyonlarca deneme yapar, yani anında kırar.

Bu yüzden PBKDF2-HMAC-SHA256 kullanıyoruz ve 240.000 tur döndürüyoruz.
Her deneme ~0,1 saniye sürer. 10.000 ihtimal = yaklaşık 17 dakika.
6 haneye çıkarsan 1.000.000 ihtimal = yaklaşık 28 saat.
Tur sayısı dosyada saklanır; ileride artırırsan eski şifreler bozulmaz.

DÜRÜST SINIR
------------
Bu bir dosya şifrelemesi değil, bir kapı kilidi. Dosyayı silen kişi
kilidi de siler. Asıl caydırıcılık bekçi süreçtedir (aşağıda).
"""

import hashlib
import hmac
import json
import os
import secrets
import subprocess
import sys
import time

# OWASP'in PBKDF2-HMAC-SHA256 icin guncel tavsiyesi. 240.000'di,
# 600.000'e cikarildi. Var olan sifreler kendiliginden yukseliyor:
# dogru sifre girilince dogrula() 'yukseltilmeli' der ve cagiran
# taraf ozeti yeni tur sayisiyla yeniden uretir.
TUR_SAYISI = 600_000
TEMIZ_CIKIS_DOSYA = "temiz_cikis.bayrak"


# ----------------------------------------------------------------------
# Şifre
# ----------------------------------------------------------------------
def ozet_uret(sifre, tuz=None, tur=TUR_SAYISI):
    """Şifreden saklanabilir bir özet üretir."""
    tuz = tuz or secrets.token_hex(16)
    ham = hashlib.pbkdf2_hmac("sha256", sifre.encode("utf-8"),
                              bytes.fromhex(tuz), tur)
    return {"yontem": "pbkdf2", "tur": tur, "tuz": tuz, "ozet": ham.hex()}


def dogrula(sifre, kayit):
    """Girilen şifre doğru mu?

    Eski sürümden kalan düz SHA-256 kayıtları da kabul eder;
    doğruysa çağıran taraf yeni yönteme yükseltir.
    """
    if not kayit:
        return False, False           # (dogru_mu, yukseltilmeli_mi)

    if kayit.get("yontem") == "pbkdf2":
        ham = hashlib.pbkdf2_hmac("sha256", sifre.encode("utf-8"),
                                  bytes.fromhex(kayit["tuz"]), kayit["tur"])
        # compare_digest: doğru/yanlış karşılaştırmasının süresi
        # şifreye göre değişmesin diye
        dogru = hmac.compare_digest(ham.hex(), kayit["ozet"])
        return dogru, dogru and kayit["tur"] < TUR_SAYISI

    # Eski biçim: {"tuz": ..., "ozet": sha256(tuz|sifre)}
    if "tuz" in kayit and "ozet" in kayit:
        eski = hashlib.sha256(("%s|%s" % (kayit["tuz"], sifre)).encode("utf-8")).hexdigest()
        dogru = hmac.compare_digest(eski, kayit["ozet"])
        return dogru, dogru
    return False, False


# Saldırganın saniyede kaç deneme yapabildiği.
#
# Buradaki sayı ÖNEMLİ. Eskiden deneme başına 0,1 saniye varsayılıyordu
# — yani saniyede 10 deneme. O rakam, şifreyi UYGULAMANIN EKRANINDAN
# denemenin maliyeti. Ama şifreyi kırmak isteyen kişi ekranı hiç
# kullanmaz: ayarlar.json'u kopyalar, kendi bilgisayarında dener.
# Ekran kartıyla 600.000 turluk PBKDF2-SHA256'da saniyede birkaç bin
# deneme çıkarılabiliyor.
#
# Ölçek farkı bin kat. 4 haneli bir PIN için ekranda "1000 dakika
# dayanır" yazıyordu; gerçekte birkaç saniye. Kullanıcıyı yanlış
# güvene sokmak, hiçbir şey söylememekten kötü.
SANIYEDE_DENEME = 5000


def _alfabe_boyu(sifre):
    """Şifrede hangi karakter türleri var? Deneme uzayı bundan çıkıyor."""
    boy = 0
    if any(c.isdigit() for c in sifre):
        boy += 10
    if any(c.islower() for c in sifre):
        boy += 29          # Türkçe küçük harfler dahil
    if any(c.isupper() for c in sifre):
        boy += 29
    if any(not c.isalnum() for c in sifre):
        boy += 20          # noktalama ve simgeler
    return max(boy, 10)


def sure_metni(saniye):
    if saniye < 60:
        return "%d saniye" % max(1, int(saniye))
    if saniye < 3600:
        return "%d dakika" % (saniye // 60)
    if saniye < 86400:
        return "%d saat" % (saniye // 3600)
    if saniye < 86400 * 365:
        return "%d gün" % (saniye // 86400)
    yil = saniye / (86400 * 365)
    if yil > 1000:
        return "binlerce yıl"
    return "%d yıl" % yil


def sifre_gucu(sifre):
    """Bu şifre kaba kuvvetle ne kadar dayanır?

    Dönen süre KÖTÜMSER tarafta: şifrenin yarısı denendiğinde
    bulunacağı varsayılıyor ve saldırganın ekran kartı olduğu kabul
    ediliyor. Kullanıcıya olduğundan güçlü göstermektense olduğundan
    zayıf göstermek daha az zarar verir.
    """
    if not sifre:
        return None
    ihtimal = _alfabe_boyu(sifre) ** len(sifre)
    # Ortalama olarak uzayın yarısında bulunur
    saniye = (ihtimal / 2.0) / SANIYEDE_DENEME
    return sure_metni(saniye)


# ----------------------------------------------------------------------
# Bekçi süreç
# ----------------------------------------------------------------------
def baslangic_kisayolu():
    """Windows Başlangıç klasöründeki kısayolun tam yolu."""
    return os.path.join(
        os.environ.get("APPDATA", ""),
        r"Microsoft\Windows\Start Menu\Programs\Startup", "Goz Molasi.lnk")


KAYIT_ADI = "GozMolasi"
RUN_ANAHTARI = r"Software\Microsoft\Windows\CurrentVersion\Run"
ONAY_ANAHTARI = (r"Software\Microsoft\Windows\CurrentVersion\Explorer"
                 r"\StartupApproved\Run")


def _hedef_yol():
    """Açılışta çalıştırılacak dosya."""
    if getattr(sys, "frozen", False):
        return sys.executable
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "goz_molasi.py")


def _komut():
    hedef = _hedef_yol()
    if hedef.lower().endswith(".py"):
        # pythonw: konsol penceresi açılmasın
        yorumlayici = sys.executable.replace("python.exe", "pythonw.exe")
        return '"%s" "%s"' % (yorumlayici, hedef)
    return '"%s"' % hedef


def kayit_var_mi():
    """Kayıt defterinde açılış kaydımız var mı?"""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_ANAHTARI) as a:
            winreg.QueryValueEx(a, KAYIT_ADI)
        return True
    except Exception:
        return False


def kayit_etkin_mi():
    """Windows, 'Başlangıç uygulamaları' listesinden kapatmış mı?

    Görev Yöneticisi -> Başlangıç sekmesinden kapatılan girdiler burada
    işaretleniyor. Kayıt yerinde durur ama Windows çalıştırmaz — kullanıcı
    'kısayol var ama açılmıyor' der.
    """
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, ONAY_ANAHTARI) as a:
            deger, _ = winreg.QueryValueEx(a, KAYIT_ADI)
            return deger[0] in (2, 6)      # 2/6 = etkin, 3 = devre dışı
    except Exception:
        return True                         # kayıt yoksa engellenmemiş demektir


def kayit_kur(ac):
    """Kayıt defteri ile açılışta başlatma (yönetici gerekmez).

    Başlangıç klasörü neden tek başına yetmiyor?
      • Bazı temizleyiciler klasörü boşaltıyor
      • Kısayol dosyası bozulabiliyor
      • Program D: sürücüsünde; kısayol hedefi kaybolabiliyor
    Kayıt defteri girdisi bunlardan etkilenmiyor. Görev Zamanlayıcı
    daha da sağlam olurdu ama yönetici yetkisi istiyor — programın
    yönetici olarak çalışması gerekmemeli.
    """
    try:
        import winreg
        if not ac:
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_ANAHTARI, 0,
                                    winreg.KEY_SET_VALUE) as a:
                    winreg.DeleteValue(a, KAYIT_ADI)
            except FileNotFoundError:
                pass
            return True

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_ANAHTARI) as a:
            winreg.SetValueEx(a, KAYIT_ADI, 0, winreg.REG_SZ, _komut())

        # Windows daha önce kapatmışsa tekrar etkinleştir
        if not kayit_etkin_mi():
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, ONAY_ANAHTARI, 0,
                                    winreg.KEY_SET_VALUE) as a:
                    winreg.SetValueEx(a, KAYIT_ADI, 0, winreg.REG_BINARY,
                                      bytes([2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
            except Exception:
                pass
        return kayit_var_mi()
    except Exception:
        return False


def acilista_baslar_mi():
    """İkisinden biri varsa ve engellenmemişse açılışta başlar."""
    return (kayit_var_mi() or os.path.exists(baslangic_kisayolu())) and kayit_etkin_mi()


def acilista_baslat(ac):
    """Windows açılışında otomatik başlatmayı aç/kapat.

    İKİ YÖNTEM BİRDEN kuruyoruz:
      1) Kayıt defteri Run girdisi (asıl — silinmeye dayanıklı)
      2) Başlangıç klasörü kısayolu (yedek)
    İkisi de tetiklense bile ikinci kopya açılmaz; tek örnek koruması
    (tek_ornek_al) devrede.
    """
    kayit_kur(ac)                       # asıl yöntem

    yol = baslangic_kisayolu()
    try:
        if not ac:
            if os.path.exists(yol):
                os.remove(yol)
            return True

        hedef = _hedef_yol()
        klasor = os.path.dirname(hedef)

        # Kısayolu PowerShell'e oluşturtuyoruz; saf Python'da .lnk yazmak
        # COM arayüzü gerektiriyor ve ek kütüphane istiyor.
        betik = (
            "$s = (New-Object -ComObject WScript.Shell).CreateShortcut('%s');"
            "$s.TargetPath = '%s';"
            "$s.WorkingDirectory = '%s';"
            "$s.WindowStyle = 7;"
            "$s.Description = 'Goz Molasi - her 20 dakikada goz molasi';"
            "$s.Save()"
        ) % (yol.replace("'", "''"), hedef.replace("'", "''"),
             klasor.replace("'", "''"))

        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", betik],
            creationflags=0x08000000, timeout=20, check=False)
        return os.path.exists(yol)
    except Exception:
        return False


def acilistan_beri_saniye():
    """Bilgisayar kaç saniyedir açık?

    Program açılışta başlamadıysa, o süre boyunca hiçbir şey
    ölçemedik. Kullanıcıya bunu dürüstçe söylemek için kullanılıyor.
    """
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        k32.GetTickCount64.restype = ctypes.c_ulonglong
        return k32.GetTickCount64() / 1000.0
    except Exception:
        return 0.0


def surec_yasiyor_mu(pid):
    """Süreç GERÇEKTEN çalışıyor mu?

    Dikkat: OpenProcess'in başarılı olması yaşıyor demek DEĞİL. Süreç
    ölse bile başka biri tutamacını açık tuttuğu sürece PID serbest
    kalmaz ve OpenProcess başarılı döner. Bu yüzden ayrıca sürecin
    "işaretli" (signaled = bitmiş) olup olmadığına bakıyoruz.
    """
    try:
        import ctypes
        SYNCHRONIZE = 0x00100000
        WAIT_TIMEOUT = 0x00000102        # hâlâ çalışıyor
        k32 = ctypes.windll.kernel32
        h = k32.OpenProcess(SYNCHRONIZE, False, int(pid))
        if not h:
            return False
        try:
            return k32.WaitForSingleObject(h, 0) == WAIT_TIMEOUT
        finally:
            k32.CloseHandle(h)
    except Exception:
        return False


def bekci_baslat(klasor):
    """Programın kendisini izleyen ikinci bir süreç başlatır.

    Görev Yöneticisi'nden program kapatılırsa bekçi bunu görür ve
    programı yeniden açar. Kullanıcı şifresini girip düzgün kapatırsa
    bir bayrak dosyası bırakılır; bekçi onu görünce sessizce çekilir.
    """
    try:
        os.makedirs(klasor, exist_ok=True)
        bayrak = os.path.join(klasor, TEMIZ_CIKIS_DOSYA)
        if os.path.exists(bayrak):
            os.remove(bayrak)

        komut = [sys.executable]
        if not getattr(sys, "frozen", False):
            komut.append(os.path.abspath(sys.argv[0]))
        komut += ["--bekci", str(os.getpid()), klasor]

        # CREATE_NO_WINDOW: siyah konsol penceresi açılmasın
        subprocess.Popen(komut, creationflags=0x08000000,
                         close_fds=True)
        return True
    except Exception:
        return False


def temiz_cikis_isaretle(klasor):
    """Kullanıcı şifresini girip düzgün kapattı — bekçi karışmasın."""
    try:
        os.makedirs(klasor, exist_ok=True)
        with open(os.path.join(klasor, TEMIZ_CIKIS_DOSYA), "w") as f:
            f.write(str(time.time()))
    except Exception:
        pass


GOSTER_BAYRAK = "goster.bayrak"
_mutex_tutamaci = None


def tek_ornek_al():
    """Program zaten açık mı? Değilse 'benim' de.

    Kullanıcı kısayola iki kez tıklayınca iki kopya açılıyordu; ikisi de
    pencereyi gizlediği için ekranda hiçbir şey görünmüyor, kullanıcı
    "açılmıyor" sanıyordu. Artık ikinci kopya açılmaz; bunun yerine
    zaten açık olana "pencereni göster" der.

    Döner: True = ilk kopya benim, çalışmaya devam et
           False = zaten açık, ben çıkmalıyım
    """
    global _mutex_tutamaci
    try:
        import ctypes
        ERROR_ALREADY_EXISTS = 183
        k32 = ctypes.windll.kernel32
        _mutex_tutamaci = k32.CreateMutexW(None, False, "GozMolasi_TekOrnek_v1")
        return k32.GetLastError() != ERROR_ALREADY_EXISTS
    except Exception:
        return True          # kontrol edilemiyorsa engelleme


def goster_iste(klasor):
    """Çalışan kopyaya 'pencereni aç' mesajı bırak."""
    try:
        os.makedirs(klasor, exist_ok=True)
        with open(os.path.join(klasor, GOSTER_BAYRAK), "w") as f:
            f.write(str(time.time()))
        return True
    except Exception:
        return False


def goster_istendi_mi(klasor):
    """Mesaj var mı? Varsa tüket ve True dön."""
    yol = os.path.join(klasor, GOSTER_BAYRAK)
    if not os.path.exists(yol):
        return False
    try:
        os.remove(yol)
    except Exception:
        pass
    return True


ASGARI_YASAM = 25          # saniye — bundan kısa sürede ölen program çöküyordur


def bekci_calis(izlenen_pid, klasor):
    """Bekçi kipi. Programın bittiğini görene kadar bekler."""
    bayrak = os.path.join(klasor, TEMIZ_CIKIS_DOSYA)
    basladi = time.time()

    while surec_yasiyor_mu(izlenen_pid):
        if os.path.exists(bayrak):
            try:
                os.remove(bayrak)
            except Exception:
                pass
            return 0                      # düzgün kapanış: bekçi çekilir
        time.sleep(2)

    # Süreç bitti. Düzgün kapanış bayrağı var mı?
    time.sleep(1.0)
    if os.path.exists(bayrak):
        try:
            os.remove(bayrak)
        except Exception:
            pass
        return 0

    # Program çok kısa sürede öldüyse bu bir çökmedir, zorla kapatma değil.
    # Yeniden açarsak sonsuz döngüye gireriz — açmıyoruz.
    if time.time() - basladi < ASGARI_YASAM:
        return 0

    # Zorla kapatılmış. Programı geri aç.
    try:
        komut = [sys.executable]
        if not getattr(sys, "frozen", False):
            komut.append(os.path.abspath(sys.argv[0]))
        subprocess.Popen(komut, creationflags=0x08000000, close_fds=True)
    except Exception:
        pass
    return 0
