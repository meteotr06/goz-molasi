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

# Bekcinin gizli sozunu tasiyan ortam degiskeni.
#
# OLCULDU (29.08.2026): soz eskiden bekcinin KOMUT SATIRINDA duruyordu
# (`komut += [..., _GIZLI_SOZ]`). Gorev Yoneticisi > Ayrintilar > sutun
# basligina sag tik > "Komut satiri" sutunu acilinca tek adimda
# okunuyordu. Sozu okuyan biri sahte bir "temiz cikis" bayragi yazip
# bekciyi devre disi birakabiliyordu - 27.08'de kapatilan atlatma
# ikinci kapidan geri geliyordu. Koddaki eski yorum "Soz DISKE
# YAZILMIYOR" diyerek guvenli sanmisti; komut satiri guvenli bir yer
# DEGIL.
SOZ_ORTAM_ADI = "GOZMOLASI_BEKCI_SOZU"

# Program ana dongusunu calistirdiginda birakilan bayrak. Bekci
# "zorla kapatildi" ile "acilista coktu"yu bununla ayiriyor.
HAZIR_BAYRAK = "hazir.bayrak"

# Art arda erken olum sayaci ve bekcinin pes ettigini soyleyen not.
ERKEN_SAYAC_DOSYA = "bekci_sayac.json"
BEKCI_NOTU = "bekci_notu.json"
# Not bu kadar sure ekranda gosterilir. Koruma kapandiysa ebeveyn
# bunu ogrenmeli; sessiz kalmak bu projede hata sayiliyor.
NOT_OMRU = 24 * 3600


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
# Windows, Başlangıç KLASÖRÜ kısayolunu AYRI bir anahtarda işaretliyor
# ve değer adı olarak kayıt adını değil KISAYOL DOSYA ADINI kullanıyor
# ("Goz Molasi.lnk"). 29.08.2026'ya kadar bu anahtar hiç okunmuyordu:
# kullanıcı Görev Yöneticisi > Başlangıç'tan kısayolu kapatınca program
# hiç açılmıyor ama ayarlardaki kutu İŞARETLİ kalıyordu — kutu yalan
# söylüyordu. Üstelik OKU.md'nin tarif ettiği ilk kurulum yolu
# ("Windows Acilisinda Baslat.bat") yalnız kısayol koyuyor; yani
# belgelenmiş kurulumun çıktısı tam da kodun göremediği kanattı.
ONAY_KISAYOL_ANAHTARI = (r"Software\Microsoft\Windows\CurrentVersion"
                         r"\Explorer\StartupApproved\StartupFolder")


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


def _onay_bayti(anahtar, ad):
    """StartupApproved altındaki onay baytını okur.

    2/6 = etkin, 3 = kullanıcı Görev Yöneticisi'nden KAPATMIŞ.
    Değer yoksa None döner. "Hiç işaretlenmemiş" ile "kapatılmış"
    aynı şey değil; çağıran ikisini ayırt edebilmeli — 29.08.2026'da
    bu ayrım olmadığı için kullanıcının kapatma kararı, kaydın
    kaybolmasıyla karıştırılıp geri alınıyordu.
    """
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, anahtar) as a:
            deger, _ = winreg.QueryValueEx(a, ad)
        return int(deger[0])
    except Exception:
        return None


def _kisayol_onay_adi():
    """Windows'un kısayol için kullandığı değer adı = kısayolun dosya adı.

    Elle "Goz Molasi.lnk" yazmıyoruz: kısayolun adı değişirse burası
    da kendiliğinden değişsin.
    """
    return os.path.basename(baslangic_kisayolu())


def kayit_etkin_mi():
    """Windows, KAYIT girdimizi 'Başlangıç' listesinden kapatmış mı?

    Görev Yöneticisi -> Başlangıç sekmesinden kapatılan girdiler burada
    işaretleniyor. Kayıt yerinde durur ama Windows çalıştırmaz — kullanıcı
    'kısayol var ama açılmıyor' der.

    DİKKAT: bu yalnızca KAYIT kanadını yanıtlar. Başlangıç klasörü
    kısayolunun cevabı kisayol_etkin_mi()'de.
    """
    b = _onay_bayti(ONAY_ANAHTARI, KAYIT_ADI)
    return b is None or b in (2, 6)     # işaret yoksa engellenmemiş demektir


def kisayol_etkin_mi():
    """Başlangıç KLASÖRÜ kısayolu Görev Yöneticisi'nden kapatılmış mı?

    Kayıt kanadının aynısı, ama Windows'un kısayollar için kullandığı
    anahtarda. Görev Yöneticisi'nden kapatmak .lnk dosyasını SİLMEZ,
    yalnızca bu baytı 3 yapar; dosyaya bakarak anlaşılmaz.
    """
    b = _onay_bayti(ONAY_KISAYOL_ANAHTARI, _kisayol_onay_adi())
    return b is None or b in (2, 6)


def kullanici_windowstan_kapatti_mi():
    """Kullanıcı Windows'un Başlangıç listesinden KENDİ ELİYLE kapattı mı?

    "Kayıt kayboldu" (temizlik programı, Windows güncellemesi) ile
    "kullanıcı kapattı" aynı belirtiyi veriyor ama aynı şey değil:
    birincisinde geri koymak doğru, ikincisinde iradeyi geri almak
    olur. İki kanattan birinde bile 3 varsa bu bir KARARDIR.
    """
    return (_onay_bayti(ONAY_ANAHTARI, KAYIT_ADI) == 3
            or _onay_bayti(ONAY_KISAYOL_ANAHTARI, _kisayol_onay_adi()) == 3)


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
    """İki kanattan BİRİ hem kurulu hem engellenmemişse açılışta başlar.

    29.08.2026'ya kadar burada
        (kayit_var_mi() or kısayol_var) and kayit_etkin_mi()
    yazıyordu. İki yönlü yanlıştı: kısayolun kendi onay baytı hiç
    okunmuyordu (kısayol kapatılmışken "başlar" diyor, ayarlardaki
    kutu işaretli kalıyordu) ve kayıt kanadının kapatılması, açık
    duran bir kısayolu da birlikte gömüyordu. Her kanat kendi
    onayıyla sorulmalı.
    """
    kayit = kayit_var_mi() and kayit_etkin_mi()
    kisayol = os.path.exists(baslangic_kisayolu()) and kisayol_etkin_mi()
    return kayit or kisayol


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

        # Kısayol kanadı da Görev Yöneticisi'nden kapatılmış olabilir;
        # kısayolu koymak tek başına yetmez, Windows yine başlatmaz.
        # Bunu YALNIZCA burada yapıyoruz: buraya kullanıcının kendi
        # "aç" isteğiyle geliniyor. Kendiliğinden onarım yolu artık
        # kullanıcının kapatma kararına dokunmuyor (29.08.2026).
        if not kisayol_etkin_mi():
            try:
                import winreg
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                      ONAY_KISAYOL_ANAHTARI) as a:
                    winreg.SetValueEx(a, _kisayol_onay_adi(), 0,
                                      winreg.REG_BINARY,
                                      bytes([2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
            except Exception:
                pass
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

    Doner: bekcinin PID'i, kurulamadiysa 0.

    NEDEN PID (olculdu 29.08.2026): eskiden True donuyordu, cagiran
    taraf bunu bir kez saklayip bir daha hic bakmiyordu. Bekci Gorev
    Yoneticisi'nden kapatilinca uygulama bunu HIC fark etmiyor, aile
    kipi korumasi sessizce kalkiyordu. PID donunce bekcinin yasayip
    yasamadigi `surec_yasiyor_mu` ile olculebiliyor.
    """
    try:
        os.makedirs(klasor, exist_ok=True)
        # Onceki turdan kalan bayraklar bu bekciyi yaniltmasin.
        for ad in (TEMIZ_CIKIS_DOSYA, HAZIR_BAYRAK):
            y = os.path.join(klasor, ad)
            if os.path.exists(y):
                os.remove(y)

        # GİZLİ SÖZ — temiz çıkış bayrağının taklit edilmesini önler.
        #
        # Bayrak düz bir dosyaydı ve %APPDATA% altında herkes yazabiliyor.
        # Çocuk boş bir dosya oluşturup programı Görev Yöneticisi'nden
        # öldürürse bekçi "düzgün kapandı" sanıp çekiliyordu. Şifre bile
        # gerekmiyordu.
        #
        # SOZ ARTIK KOMUT SATIRINDA DEGIL (29.08.2026). Eski hali
        # `komut += [..., _GIZLI_SOZ]` idi; Gorev Yoneticisi'nin "Komut
        # satiri" sutunu ile tek adimda okunuyordu. Ortam degiskenine
        # tasindi; bekci `bekci_sozu_al` ile okuyup ORTAMDAN SILIYOR.
        #
        # DURUST SINIR: ortam degiskeni de mutlak bir sir degil. Ayni
        # kullanici olarak calisan bir arac (Process Explorer gibi)
        # surecin ortamini okuyabilir. Kazanc gercek ama sinirli:
        # "Gorev Yoneticisi'nde tek tik" -> "ayrica arac indirmek
        # gerekir". Tam cozum ayri bir guvenlik siniri (baska kullanici
        # hesabi) isterdi; bu program yonetici hakki istemiyor ve
        # makineyi rehin almiyor - bilincli bir sinir.
        global _GIZLI_SOZ
        _GIZLI_SOZ = secrets.token_hex(16)

        komut = [sys.executable]
        if not getattr(sys, "frozen", False):
            komut.append(os.path.abspath(sys.argv[0]))
        komut += ["--bekci", str(os.getpid()), klasor]

        ortam = dict(os.environ)
        ortam[SOZ_ORTAM_ADI] = _GIZLI_SOZ

        # CREATE_NO_WINDOW: siyah konsol penceresi açılmasın
        p = subprocess.Popen(komut, creationflags=0x08000000,
                             close_fds=True, env=ortam)
        return p.pid
    except Exception:
        return 0


def bekci_sozu_al():
    """Bekci kipindeki surec gizli sozu ortamdan ALIR ve SILER.

    Silmek sart: bekci, oldurulen programi yeniden acarken kendi
    ortamini miras biraktiriyor. Silinmezse soz once yeni programa,
    oradan da onun baslattigi her alt surece geciyor - bir tanesinin
    ortami okunabilir olsa soz yine disari sizardi.
    """
    try:
        return os.environ.pop(SOZ_ORTAM_ADI, "") or ""
    except Exception:
        return ""


def hazir_isaretle(klasor):
    """Program ana dongusunu calistirdi - bekci bunu bilsin.

    Bekci "zorla kapatilan program" ile "acilista coken program"i bu
    bayrakla ayiriyor (bkz. `erken_olum_karari`). Ayni anda art arda
    erken olum zincirini de kirar: program bir kez ayaga kalktiysa
    onceki cokmeler gecmiste kaldi.
    """
    try:
        os.makedirs(klasor, exist_ok=True)
        with open(os.path.join(klasor, HAZIR_BAYRAK), "w") as f:
            f.write(str(time.time()))
        _erken_olum_sifirla(klasor)
        return True
    except Exception:
        return False


def hazir_mi(klasor, esik_an=0):
    """Program BU bekci dogduktan sonra ayaga kalkti mi?

    `bekci_baslat` bayragi dogmadan once siliyor; esik yine de duruyor
    cunku silme basarisiz olabilir ve eski bir bayrak bekciyi yanlis
    yone (fazla saldirgan yeniden acmaya) iterdi.
    """
    try:
        y = os.path.join(klasor, HAZIR_BAYRAK)
        return os.path.exists(y) and os.path.getmtime(y) >= esik_an
    except Exception:
        return False


def _sayac_yolu(klasor):
    return os.path.join(klasor, ERKEN_SAYAC_DOSYA)


def _erken_olum_artir(klasor):
    """Art arda kacinci erken olum? Sayiyi artirir ve doner."""
    n = 0
    try:
        with open(_sayac_yolu(klasor), "r") as f:
            veri = json.load(f)
        if isinstance(veri, dict):
            okunan = veri.get("art_arda", 0)
            n = int(okunan) if isinstance(okunan, (int, float)) else 0
    except Exception:
        n = 0
    n = max(0, n) + 1
    try:
        os.makedirs(klasor, exist_ok=True)
        with open(_sayac_yolu(klasor), "w") as f:
            json.dump({"art_arda": n, "an": time.time()}, f)
    except Exception:
        pass
    return n


def _erken_olum_sifirla(klasor):
    try:
        os.remove(_sayac_yolu(klasor))
    except Exception:
        pass


def bekci_notu_birak(klasor, sayi):
    """Bekci pes etti - ekranda gorunecek bir iz birak."""
    try:
        os.makedirs(klasor, exist_ok=True)
        with open(os.path.join(klasor, BEKCI_NOTU), "w") as f:
            json.dump({"an": time.time(), "art_arda": sayi}, f)
    except Exception:
        pass


def bekci_notu_var_mi(klasor):
    """Bekci son NOT_OMRU icinde "durdum" notu birakmis mi?

    Dosya JSON olarak OKUNMUYOR, yalnizca varligina ve tarihine
    bakiliyor: bu islev panel her cizildiginde (saniyede dortten fazla)
    cagriliyor.
    """
    try:
        y = os.path.join(klasor, BEKCI_NOTU)
        return os.path.exists(y) and (time.time() - os.path.getmtime(y)) < NOT_OMRU
    except Exception:
        return False


_GIZLI_SOZ = ""


def temiz_cikis_isaretle(klasor):
    """Kullanıcı şifresini girip düzgün kapattı — bekçi karışmasın.

    Bayrağa gizli sözü yazıyoruz; bekçi bunu doğruluyor. Sözü bilmeyen
    biri bayrağı oluştursa da bekçi kanmaz.
    """
    try:
        os.makedirs(klasor, exist_ok=True)
        with open(os.path.join(klasor, TEMIZ_CIKIS_DOSYA), "w") as f:
            f.write(_GIZLI_SOZ or str(time.time()))
    except Exception:
        pass


def temiz_cikis_gecerli_mi(klasor, soz):
    """Bayrak GERÇEKTEN programın kendisi tarafından mı bırakıldı?

    Bekçi bunu soruyor. Söz boşsa (kilit yokken, eski davranış) bayrağın
    varlığı yeterli — orada korunacak bir şey yok. Söz varsa içerik
    tutmalı: taklit bayrak kabul edilmez.
    """
    yol = os.path.join(klasor, TEMIZ_CIKIS_DOSYA)
    if not os.path.exists(yol):
        return False
    if not soz:
        return True
    try:
        with open(yol, "r") as f:
            return f.read().strip() == soz
    except Exception:
        return False


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

# Program acildiktan bu kadar saniye sonra "ayaga kalkti" der ve hazir
# bayragini birakir (bkz. goz_molasi._bekciyi_kur). Ana dongu bu kadar
# donduyse artik bir ACILIS cokmesi degildir.
HAZIR_ESIGI = 12

# Hic ayaga kalkamadan olen program icin en fazla bu kadar deneme.
# Sifir olamazdi (bekci ilk oldurmede pes ederdi), sinirsiz da olamaz
# (acilista gercekten coken program sonsuz dongu uretir).
AZAMI_ERKEN_DENEME = 4
# Denemeler arasi bekleme, gittikce uzuyor: gercek bir cokme dongusu
# bilgisayari mesgul etmesin.
ERKEN_BEKLEME = (5, 15, 45, 120)


def erken_olum_karari(klasor, yasam_sn, hazir):
    """Program oldu. Yeniden acilsin mi, kac saniye sonra?

    Doner: (yeniden_ac, bekleme_sn)

    NEDEN BOYLE - OLCULDU (29.08.2026): eski kural tek satirdi,
    `if time.time() - basladi < ASGARI_YASAM: return 0`. Yani acilistan
    ~22 saniye icinde oldurulen program YENIDEN ACILMIYORDU ve art arda
    iki kez oldurmek bekciyi kalici olarak kaldiriyordu. Aile kipinde bu,
    butun korumanin kalkmasi demek.

    Esigi kaldirmak cozum degil: acilista gercekten coken bir program
    sonsuz dongu uretir. Iki durum AYRILIYOR:
      • Program ana dongusunu calistirabildiyse (hazir bayragi var) bu
        bir ZORLA KAPATMA'dir - kac kez olursa olsun geri aciyoruz.
      • Hic ayaga kalkamadiysa COKME olabilir - sinirli sayida ve
        gittikce uzayan araliklarla deniyoruz, sonra durup NOT
        birakiyoruz. Not ekranda gorunur (`ayar_uyarisi`); koruma
        kapanip kimsenin haberi olmamasi kabul edilmiyor.

    `yasam_sn` MONOTONIK saatle olculur. Duvar saatiyle olcen eski hal,
    sistem saati ileri alinarak "uzun yasadi" gosterilebiliyordu.

    Bilinen sinir: `hazir.bayrak` cocugun da yazabildigi bir klasorde.
    Onu silmek bekciyi ancak bugunku (sinirli deneme) davranisina
    dondurur - yani durumu kotulestirmiyor; olusturmak ise bekciyi
    daha ISRARCI yapar, koruma tarafina duser.
    """
    if hazir or yasam_sn >= ASGARI_YASAM:
        _erken_olum_sifirla(klasor)
        return True, 0
    sira = _erken_olum_artir(klasor)
    if sira > AZAMI_ERKEN_DENEME:
        bekci_notu_birak(klasor, sira)
        return False, 0
    return True, ERKEN_BEKLEME[min(sira, len(ERKEN_BEKLEME)) - 1]


def bekci_calis(izlenen_pid, klasor, soz=""):
    """Bekçi kipi. Programın bittiğini görene kadar bekler.

    `soz`: programın başlatırken verdiği gizli söz. Temiz çıkış bayrağı
    bu sözü içermek zorunda. Eskiden bayrağın VARLIĞI yeterliydi ve
    bayrak %APPDATA% altında herkesin yazabildiği düz bir dosyaydı —
    boş bir dosya oluşturup programı öldüren biri bekçiyi devre dışı
    bırakıyordu, şifre bile gerekmiyordu.

    Soz artik komut satirindan DEGIL, ortam degiskeninden geliyor
    (bkz. `bekci_baslat` ve `bekci_sozu_al`).
    """
    bayrak = os.path.join(klasor, TEMIZ_CIKIS_DOSYA)
    basladi_mono = time.monotonic()
    dogum_ani = time.time()

    def temiz_cikildi():
        if not temiz_cikis_gecerli_mi(klasor, soz):
            return False
        try:
            os.remove(bayrak)
        except Exception:
            pass
        return True

    while surec_yasiyor_mu(izlenen_pid):
        if temiz_cikildi():
            _erken_olum_sifirla(klasor)
            return 0                      # düzgün kapanış: bekçi çekilir
        time.sleep(2)

    # Süreç bitti. Düzgün kapanış bayrağı var mı?
    time.sleep(1.0)
    if temiz_cikildi():
        _erken_olum_sifirla(klasor)
        return 0

    # Cokme mi, zorla kapatma mi? Karar tek yerde: `erken_olum_karari`.
    # 5 saniyelik pay, bayragin yazildigi an ile bekcinin dogdugu an
    # arasindaki olcum gurultusu icin.
    ac, bekle = erken_olum_karari(klasor,
                                  time.monotonic() - basladi_mono,
                                  hazir_mi(klasor, dogum_ani - 5))
    if not ac:
        return 0
    if bekle:
        time.sleep(bekle)

    # Zorla kapatılmış. Programı geri aç.
    try:
        komut = [sys.executable]
        if not getattr(sys, "frozen", False):
            komut.append(os.path.abspath(sys.argv[0]))
        subprocess.Popen(komut, creationflags=0x08000000, close_fds=True)
    except Exception:
        pass
    return 0
