# -*- coding: utf-8 -*-
"""
GÖZ MOLASI — Windows sürümü

Her 20 dakikada 20 saniyelik göz molası.
Mola ekranı bütün monitörleri kaplar, en üstte durur, kapatılamaz.

Çalıştırma:
    pythonw goz_molasi.py    (konsol penceresi açılmaz — normal kullanım)
    python  goz_molasi.py    (hata ayıklarken)
"""

import math
import hashlib
import json
import os
import random
import math as _math
import re as _re
import secrets
import sys
import time
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import izleyici as iz
import gorunum as gor
import ogeler as og
import kilit as kl
import gecmis as gcm
import egzersiz as egz
import ses
import tepsi
import guncelleme as gnc
import kopru as kpr
from bilgiler import BILGILER, IPUCLARI, MOLA_CUMLELERI
try:
    from dunya import DUNYA        # uretilen dosya (dunya_uret.py)
except Exception:
    DUNYA = []                     # dosya yoksa uygulama yine calissin

def kaynak_yolu(ad):
    """Dosya yolunu bul.

    Program .exe'ye çevrildiğinde (PyInstaller) dosyalar geçici bir
    klasöre açılır ve sys._MEIPASS'te durur. Normal çalışmada ise
    betiğin yanındadır. İkisini de destekliyoruz.
    """
    kok = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(kok, ad)


KAYIT_KLASOR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "GozMolasi")
AYAR_DOSYA = os.path.join(KAYIT_KLASOR, "ayarlar.json")
IST_DOSYA = os.path.join(KAYIT_KLASOR, "istatistik.json")
DURUM_DOSYA = os.path.join(KAYIT_KLASOR, "durum.json")

# Programların dosya adı yerine insanca adı. Grafikte "javaw.exe"
# yazmak kimseye bir şey anlatmıyor. Listede olmayan program, dosya
# uzantısı atılıp baş harfi büyütülerek gösterilir.
PROGRAM_ADLARI = {
    "chrome.exe": "Chrome", "msedge.exe": "Edge", "firefox.exe": "Firefox",
    "brave.exe": "Brave", "opera.exe": "Opera", "vivaldi.exe": "Vivaldi",
    "code.exe": "VS Code", "devenv.exe": "Visual Studio",
    "pycharm64.exe": "PyCharm", "idea64.exe": "IntelliJ",
    "windowsterminal.exe": "Terminal", "cmd.exe": "Komut İstemi",
    "powershell.exe": "PowerShell", "explorer.exe": "Dosya Gezgini",
    "javaw.exe": "Minecraft (Java)", "java.exe": "Java",
    "valorant.exe": "VALORANT", "riotclientux.exe": "Riot Client",
    "steam.exe": "Steam", "steamwebhelper.exe": "Steam",
    "discord.exe": "Discord", "spotify.exe": "Spotify",
    "whatsapp.exe": "WhatsApp", "telegram.exe": "Telegram",
    "excel.exe": "Excel", "winword.exe": "Word",
    "powerpnt.exe": "PowerPoint", "outlook.exe": "Outlook",
    "notepad.exe": "Not Defteri", "photoshop.exe": "Photoshop",
    "vlc.exe": "VLC", "obs64.exe": "OBS", "zoom.exe": "Zoom",
    "teams.exe": "Teams", "claude.exe": "Claude",
    "goz molasi.exe": "Göz Molası", "lively.exe": "Lively",
    "shellexperiencehost.exe": "Windows", "searchhost.exe": "Windows Arama",
    "nvidia overlay.exe": "NVIDIA Overlay",
}


def program_adi(dosya):
    """Dosya adını insanca ada çevir."""
    ad = PROGRAM_ADLARI.get(dosya.lower())
    if ad:
        return ad
    kok = dosya.rsplit(".", 1)[0]
    return kok[:1].upper() + kok[1:] if kok else dosya


# KİPLER — yaptığın işe göre kayıtlı ayar takımı.
# Web sürümündekiyle aynı. Kip yalnızca zamanlama ayarlarını
# değiştirir; tema, canlılık, kilit gibi kişisel tercihler taşınır.
KIPLER = [
    ("calisma", "Çalışma", {
        "calisma_dk": 20, "mola_sn": 20, "uyari_sn": 15,
        "ses": True, "sadece_olc": False}),
    ("ders", "Ders", {
        "calisma_dk": 25, "mola_sn": 30, "uyari_sn": 15,
        "ses": True, "sadece_olc": False}),
    ("toplanti", "Toplantı", {
        "calisma_dk": 60, "mola_sn": 20, "uyari_sn": 0,
        "ses": False, "sadece_olc": False}),
    ("film", "Film · oyun", {
        "calisma_dk": 90, "mola_sn": 20, "uyari_sn": 0,
        "ses": False, "sadece_olc": False}),
]


VARSAYILAN = {
    "calisma_dk": 20,
    "mola_sn": 20,
    "uyari_sn": 15,
    "bosta_esigi_sn": 90,
    "dinlenme_esigi_sn": 300,
    "uzun_mola_esigi_dk": 120,
    "uzun_mola_dk": 5,
    "tam_ekranda_sor": True,
    # Çalışma saatleri: bu aralığın dışında hatırlatma gelmez.
    # Gece 23:00'te ders çalışan biri sabah 9'da mola istemez.
    "saatler_acik": False,
    "bas_saat": "09:00",
    "bit_saat": "18:00",
    "analiz_izni": None,      # None = henüz sorulmadı
    "acilis_izni": None,      # None = henüz sorulmadı (açılışta başlasın mı)
    "ses": True,
    # İlk açılışta beyaz. Mola ekranı her temada koyu kalıyor,
    # yani aydınlık panel gözü dinlendirme amacıyla çelişmiyor.
    "tema": "beyaz",
    "kilit": None,            # {"yontem","tur","tuz","ozet"} — düz metin ASLA
    "bekci": True,
    # KOPRU: tarayici surumu, Windows surumunun sayacini okuyabilsin.
    # Kapatilabilir olmasi onemli - kullanici istemiyorsa bilgisayarinda
    # bir ag ucu acik kalmamali.
    "kopru": True,          # yerel okuma ucu acilsin mi            # kilit açıkken zorla kapatılırsa geri açsın mı
    # SESSİZ ÖLÇÜM: program açık kalır, ekran süresini ve hangi programda
    # ne kadar durduğunu ölçmeye devam eder, ama MOLA VERMEZ ve ekrana
    # hiçbir şey çıkarmaz. Toplantı, oyun, film, sunum için.
    "sadece_olc": False,
    # Renklerin doygunluğu: 0.6 sakin, 1.0 temanın kendisi, 1.5 canlı.
    # Açıklığa dokunulmaz, yani yazı okunaklılığı hiç değişmez.
    "canlilik": 1.0,
    # ================= KİP =================
    # "bireysel": bugünkü davranış — kullanıcı kendi ayarlarını yönetir.
    # "aile":     ebeveyn kural koyar, çocuk değiştiremez.
    #
    # Aile kipi ŞİFRESİZ AÇILAMAZ. Şifresiz bir ebeveyn kilidi,
    # kilidin anahtarını kapının üstünde bırakmak demek.
    "kip": "bireysel",

    # Günlük ekran süresi sınırı, dakika. 0 = sınır yok.
    "gunluk_sinir_dk": 0,
    # AILE KIPI KERTMESI: {"gun": "YYYY-AA-GG", "sn": <gorulen en yuksek>}
    # Ekran suresi gun icinde geri gidemez. Geri giderse istatistik
    # dosyasi kurcalanmis demektir; ebeveyne uyari cikar.
    "ekran_isareti": None,
    # Ebeveynin verdiği ek sürenin bitiş anı (time.time()).
    # Sınır dolduğunda ebeveyn şifreyle ek süre verebiliyor.
    "ek_sure_bitis": 0,

    # Saat yasağı: bu aralıkta bilgisayar kullanılamaz.
    # "calisma saatleri" ayarından FARKLI: o yalnızca molaları
    # susturuyor, bu kullanımı engelliyor.
    "yasak_acik": False,
    "yasak_bas": "21:00",
    "yasak_bit": "07:00",

    # --- eski sürümden kalan alanlar (geriye uyumluluk) ---
    "kilit_ozeti": None,
    "kilit_tuz": None,
}

# Uygulamanın sürümü. GitHub Releases etiketiyle karşılaştırılıyor;
# yeni sürüm çıkınca kullanıcıya haber veriliyor. Sürüm yükseltirken
# BURAYI ve Releases etiketini birlikte güncelle.
SURUM = "1.1"

P = gor.PANEL


# ----------------------------------------------------------------------
# Yardımcılar
# ----------------------------------------------------------------------
def ayarlari_oku():
    """encoding='utf-8-sig': dosyanın başındaki görünmez BOM işareti
    yüzünden ayarların sessizce yok sayılmasını engeller."""
    ayar = dict(VARSAYILAN)
    try:
        with open(AYAR_DOSYA, "r", encoding="utf-8-sig") as f:
            ayar.update(json.load(f))
    except FileNotFoundError:
        pass
    except Exception as hata:
        try:
            os.replace(AYAR_DOSYA, AYAR_DOSYA + ".bozuk")
        except Exception:
            pass
        print("Ayar dosyası okunamadı, varsayılana dönüldü:", hata)
    return ayar


def ayarlari_yaz(ayar):
    try:
        os.makedirs(KAYIT_KLASOR, exist_ok=True)
        with open(AYAR_DOSYA, "w", encoding="utf-8") as f:
            json.dump(ayar, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def simdi_saniye():
    return time.time()


def saat_uygun_mu(ayar, simdi=None):
    """Şu an çalışma saatleri içinde miyiz?

    Bitiş saati başlangıçtan küçükse gece yarısını aşan vardiya sayılır
    (örn. 22:00 — 04:00).
    """
    if not ayar.get("saatler_acik"):
        return True
    simdi = simdi or time.localtime()

    def dakika(metin):
        try:
            saat, dk = str(metin).split(":")
            return int(saat) * 60 + int(dk)
        except Exception:
            return 0

    su = simdi.tm_hour * 60 + simdi.tm_min
    bas = dakika(ayar.get("bas_saat", "09:00"))
    bit = dakika(ayar.get("bit_saat", "18:00"))
    if bas == bit:
        return True                      # 24 saat
    return (bas <= su < bit) if bas < bit else (su >= bas or su < bit)


def yasak_saatinde_mi(ayar, simdi=None):
    """Şu an saat yasağı içinde miyiz?

    saat_uygun_mu ile aynı mantık ama TERS: orada aralık İÇİ çalışma
    saati, burada aralık içi yasak. Ayrı tutuluyor çünkü ikisi farklı
    işler: biri molaları susturur, öbürü kullanımı engeller. Aynı
    ayarı iki işe koşmak, birini değiştirince öbürünü bozar.
    """
    if not ayar.get("yasak_acik"):
        return False
    simdi = simdi or time.localtime()

    def dakika(metin):
        try:
            saat, dk = str(metin).split(":")
            return int(saat) * 60 + int(dk)
        except Exception:
            return 0

    su = simdi.tm_hour * 60 + simdi.tm_min
    bas = dakika(ayar.get("yasak_bas", "21:00"))
    bit = dakika(ayar.get("yasak_bit", "07:00"))
    if bas == bit:
        return False                     # aralık yok
    return (bas <= su < bit) if bas < bit else (su >= bas or su < bit)


def aile_kipinde_mi(ayar):
    """Aile kipi AÇIK ve şifre KURULU mu?

    Şifresiz aile kipi anlamsız — çocuk ayarlardan kipi kapatır.
    O yüzden iki koşul birden aranıyor; biri eksikse kip yok sayılır.
    """
    # OLCULDU (27.08.2026): kip degeri "aile " (sonda bosluk) ya da
    # "AILE" yazilinca esitlik tutmuyor, aile kipi YOK SAYILIYOR ve
    # butun koruma sessizce kalkiyordu. Uygulama bu degeri hep "aile"
    # yaziyor - yani bu yol yalnizca ayar dosyasi ELLE duzenlenince
    # acilir. Aile kipinde o dosya cocugun kendi klasorunde duruyor.
    kip = ayar.get("kip")
    kip = kip.strip().lower() if isinstance(kip, str) else kip
    return bool(kip == "aile" and kilit_kaydi(ayar))


def kilit_kaydi(ayar):
    """Ayarlardan şifre kaydını çıkar. Eski biçimi de anlar."""
    if ayar.get("kilit"):
        return ayar["kilit"]
    if ayar.get("kilit_ozeti") and ayar.get("kilit_tuz"):
        return {"tuz": ayar["kilit_tuz"], "ozet": ayar["kilit_ozeti"]}
    return None


def sure_yazisi(saniye):
    saniye = max(0, int(saniye))
    return "%02d:%02d" % (saniye // 60, saniye % 60)


def sayi_oku(metin, varsayilan=None):
    """Türkçe yazılmış sayıyı okur. Okuyamazsa `varsayilan` döner.

    NEDEN VAR: alanlar `float(metin.replace(",", "."))` ile okunuyordu.
      "90,5"  -> ValueError -> yakalanıyor -> 0 -> SINIR YOK
      "1.500" -> 1.5        -> bin ayıracı ondalık sanılıyor

    İkisi de sessiz. Ebeveyn "günlük 90 dakika" yazdığını sanıp hiç
    sınır koymamış oluyor; kimse fark etmiyor çünkü ekranda hata yok.

    Kurallar:
      • Hem "." hem "," varsa: **SONDAKİ ondalıktır**, öteki binlik.
        1.500,50 -> 1500,50   (Türkçe yazım)
        1,500.50 -> 1500,50   (İngilizce yazım)
        İlk yazımda "nokta hep binliktir" demiştim; İngilizce yazımı
        1,5005 okuyordu — 1000 kat hata, hem de sessiz.
      • Yalnız "," varsa: ondalık                        (90,5)
      • Yalnız "." varsa ve arkasında TAM ÜÇ rakam varsa: binlik
        (1.500 -> 1500). Aksi hâlde ondalık               (90.5)
    """
    if metin is None:
        return varsayilan
    m = str(metin).strip().replace(" ", "").replace("\u00a0", "")
    if not m:
        return varsayilan
    nokta, virgul = "." in m, "," in m
    if nokta and virgul:
        # Hangisi SONDA ise ondalık odur; öteki binlik ayracı.
        if m.rfind(",") > m.rfind("."):
            m = m.replace(".", "").replace(",", ".")
        else:
            m = m.replace(",", "")
    elif virgul:
        m = m.replace(",", ".")
    elif nokta:
        parcalar = m.split(".")
        # 1.500 ya da 1.234.567 gibi: her grup üç rakam -> binlik ayıracı
        if len(parcalar) > 1 and all(len(p) == 3 for p in parcalar[1:]) \
                and parcalar[0].lstrip("-+").isdigit():
            m = "".join(parcalar)
    # float() TEMIZLENMEMIS METNI KABUL EDER: nan, inf, Infinity,
    # 1e3, 1_000. Hicbirini kullanici kastetmez ama hepsi sessizce
    # sayiya donuyordu. nan en kotusu: int(nan) coker ve Kaydet
    # dugmesi sessizce hicbir sey yapmaz; ayrica nan ile yapilan her
    # karsilastirma False doner, yani bir sinir kontrolu nan'a
    # takilirsa sinir HIC uygulanmaz.
    #
    # O yuzden bicimi float()'tan ONCE dogruluyoruz: rakam, en fazla
    # bir ondalik ayraci ve istege bagli isaret. Baska hicbir sey.
    if not _re.match(r"^[+-]?(\d+(\.\d*)?|\.\d+)$", m):
        return varsayilan
    try:
        sonuc = float(m)
    except (ValueError, OverflowError):
        return varsayilan
    # Bicim dogrulamasi "nan"/"inf" metnini eler ama COK UZUN bir rakam
    # dizisi hala tasar: float("9"*400) -> inf. Olculdu, gercek.
    # inf ile yapilan her karsilastirma sinirin sessizce kalkmasina yol acar.
    if not _math.isfinite(sonuc):
        return varsayilan
    return sonuc


def saat_oku(metin):
    r""""SS:DD" biçimindeki saati doğrular. Geçersizse None döner.

    NEDEN VAR: saat alanları `re.match(r"^\d{1,2}:\d{2}$")` ile
    denetleniyordu ve tutmadığında SESSİZCE varsayılana dönüyordu.
    İki sorun:
      • "22.30" ya da "10 pm" yazan ebeveyn, 21:00 kaydedildiğini
        bilmiyor — koyduğunu sandığı yasağı koymamış oluyor.
      • Regex BİÇİME bakıyor, DEĞERE bakmıyor: "25:00" ve "12:75"
        geçiyordu.

    Günlük sınır alanında aynı hatayı düzelttik; sessizce düzeltilen
    girdi, kullanıcıya yalan söylemektir.
    """
    if metin is None:
        return None
    m = str(metin).strip().replace(".", ":")
    parcalar = m.split(":")
    if len(parcalar) != 2:
        return None
    try:
        saat, dakika = int(parcalar[0]), int(parcalar[1])
    except ValueError:
        return None
    if not (0 <= saat <= 23 and 0 <= dakika <= 59):
        return None
    return "%02d:%02d" % (saat, dakika)


def sure_okunakli(saniye):
    saniye = int(saniye)
    if saniye < 60:
        return "%d sn" % saniye
    if saniye < 3600:
        return "%d dk" % (saniye // 60)
    return "%d sa %d dk" % (saniye // 3600, (saniye % 3600) // 60)


def dugme(ana, yazi, komut, ana_mi=False, kucuk=False):
    return tk.Button(
        ana, text=yazi, command=komut,
        font=("Segoe UI", 9 if kucuk else 10, "bold" if ana_mi else "normal"),
        bg=P["vurgu"] if ana_mi else P["kart2"],
        fg=P.get("ana_yazi", "#0d2b28") if ana_mi else P["yazi"],
        activebackground=gor.karistir(P["vurgu"] if ana_mi else P["kart2"], "#ffffff", 0.18),
        activeforeground=P.get("ana_yazi", "#0d2b28") if ana_mi else P["yazi"],
        relief="flat", bd=0, padx=12 if kucuk else 16, pady=6 if kucuk else 9,
        cursor="hand2", highlightthickness=0,
    )


# ======================================================================
# MOLA EKRANI
# ======================================================================
SATIR_AYRAC = chr(10)      # heredoc kaçış dizilerine takılmamak için


class MolaEkrani:
    """Bütün monitörleri kaplayan, kapatılamayan mola ekranı.

    Tamamı tek bir tuvale çizilir — böylece gradyanın üstünde
    dikdörtgen renk lekeleri oluşmaz.
    """

    def __init__(self, uygulama, saniye, uzun=False, egzersiz_sayaci=0):
        self.uyg = uygulama
        self.toplam = float(saniye)
        self.uzun = uzun
        self.egzersiz_sinifi = egz.sec(egzersiz_sayaci, uzun)
        self.egzersiz = None
        self.son_yonerge = None
        self.baslangic = time.time()
        self.bitis = self.baslangic + self.toplam
        self.acil_baslangic = None
        self.acil_sorulyor = False
        self.neden_gosterildi = False

        sol, ust, gen, yuk = iz.sanal_ekran()
        self.gen, self.yuk = gen, yuk

        self.p = tk.Toplevel(uygulama.kok)
        self.p.overrideredirect(True)              # başlık çubuğu yok -> X düğmesi yok
        self.p.geometry("%dx%d+%d+%d" % (gen, yuk, sol, ust))
        self.p.configure(bg=gor.MOLA_GRADYAN[0])
        self.p.attributes("-topmost", True)
        self.p.protocol("WM_DELETE_WINDOW", lambda: None)
        for tus in ("<Alt-F4>", "<Escape>", "<Control-w>", "<Control-W>",
                    "<Control-F4>", "<Alt-Tab>"):
            self.p.bind(tus, lambda e: "break")

        self.t = tk.Canvas(self.p, width=gen, height=yuk, highlightthickness=0, bd=0)
        self.t.pack(fill="both", expand=True)

        self._sahneyi_kur()
        self.p.lift()
        self.p.focus_force()
        self.p.after(60, lambda: iz.one_getir(self.p.winfo_id()))
        self._tik()

    # ---------------- Çizim ----------------
    def _sahneyi_kur(self):
        gen, yuk = self.gen, self.yuk
        gor.gradyan_ciz(self.t, gen, yuk, gor.MOLA_GRADYAN)

        self.orta_x = gen / 2

        # ---- DİKEY YERLEŞİM ----
        # Her şey merkeze göre konumlanıyor: başlık merkezin 132+yarıçap
        # üstünde, "neden?" kartı 262+yarıçap altında bitiyor. Eskiden
        # merkez basitçe ekranın ortasıydı; 768 piksellik bir ekranda kart
        # 761'de bitip ekran dışına taşıyor ve en alttaki acil çıkış
        # yazısının üstüne biniyordu. Artık merkez, üst ve alt ihtiyaç
        # hesaplanarak yerleştiriliyor; sığmazsa önce halka küçülüyor.
        UST_PAY = 150        # başlık + yönerge (yarıçap hariç)
        ALT_PAY = 280        # sayı + "saniye" + neden kartı (yarıçap hariç)
        ALT_NOT = 70         # en alttaki "bu ekran kapatılamaz" yazısı

        self.yaricap = max(70, min(150, int(min(gen, yuk) * 0.15)))
        while self.yaricap > 70 and                 UST_PAY + ALT_PAY + 2 * self.yaricap + ALT_NOT + 20 > yuk:
            self.yaricap -= 5

        ust_ihtiyac = self.yaricap + UST_PAY
        alt_ihtiyac = self.yaricap + ALT_PAY
        self.orta_y = min(max(yuk / 2, ust_ihtiyac + 10),
                          yuk - ALT_NOT - alt_ihtiyac)
        # Ekran gerçekten çok kısaysa (yuk < ~640) yukarıdaki min/max ters
        # dönebilir; o zaman üstü kurtar, alttaki kart kaydırılamaz zaten.
        self.orta_y = max(self.orta_y, ust_ihtiyac + 10)

        self.zemin_renk = gor.gradyan_rengi(gor.MOLA_GRADYAN, self.orta_y / yuk)

        # Başlık = egzersizin adı. Ne yapacağını en üstte söylüyoruz.
        self.t.create_text(
            self.orta_x, self.orta_y - self.yaricap - 132,
            text=("Uzun mola — " if self.uzun else "") + self.egzersiz_sinifi.ad,
            fill=gor.MOLA_YAZI, font=("Segoe UI", 34, "bold"),
        )
        self.yonerge_yazi = self.t.create_text(
            self.orta_x, self.orta_y - self.yaricap - 80,
            text=self.egzersiz_sinifi.yonerge,
            fill=gor.MOLA_SOLUK, font=("Segoe UI", 15),
            width=min(760, gen - 120), justify="center",
        )

        # Nefes parıltısı (her tikte yenilenir)
        self.parilti_etiket = "nefes"

        # Halka izi — geri sayım
        pay = self.yaricap
        self.t.create_oval(self.orta_x - pay, self.orta_y - pay,
                           self.orta_x + pay, self.orta_y + pay,
                           outline=gor.HALKA_IZ, width=9)
        self.yay = self.t.create_arc(
            self.orta_x - pay, self.orta_y - pay,
            self.orta_x + pay, self.orta_y + pay,
            start=90, extent=-359.9, style="arc",
            outline=gor.KEHRIBAR, width=9,
        )

        # Egzersiz animasyonu halkanın İÇİNDE oynar
        self.egzersiz = self.egzersiz_sinifi(
            self.t, self.orta_x, self.orta_y, self.yaricap * 0.78,
            gor.NANE, gor.KEHRIBAR, self.zemin_renk)

        # Geri sayım artık halkanın altında — merkez egzersize ait
        self.sayi = self.t.create_text(
            self.orta_x, self.orta_y + self.yaricap + 42,
            text=str(int(self.toplam)),       # BAŞTAN TAM SAYI: 20
            fill=gor.MOLA_YAZI, font=("Segoe UI", 30, "bold"),
        )
        self.t.create_text(
            self.orta_x, self.orta_y + self.yaricap + 70,
            text="saniye", fill=gor.MOLA_SOLUK, font=("Segoe UI", 10),
        )

        # "Neden?" kartı — molanın ilk beşte birinde belirir
        self.kart_y = self.orta_y + self.yaricap + 112
        # Kart 150 piksel yüksekliğinde; en alttaki uyarı yazısına
        # çarpıyorsa hiç gösterme. Mola yine tam çalışır — kart süs.
        self.kart_sigar = (self.kart_y + 150) <= (yuk - 60)
        self.kart_ogeleri = []

        self.t.create_text(
            self.orta_x, yuk - 40,
            text="Bu ekran kapatılamaz.  Acil durumda Ctrl + Alt + Shift tuşlarını 3 saniye basılı tut.",
            fill=gor.karistir(self.zemin_renk, gor.MOLA_SOLUK, 0.45),
            font=("Segoe UI", 9),
        )

    def _nefes_ciz(self, gecen):
        """10 saniyelik yavaş nefes: 4 sn içeri, 6 sn dışarı."""
        self.t.delete(self.parilti_etiket)
        evre = (gecen % 10.0) / 10.0
        # 0..0.4 büyür, 0.4..1 küçülür (yumuşak)
        if evre < 0.4:
            olcek = 0.86 + 0.22 * (evre / 0.4)
        else:
            olcek = 1.08 - 0.22 * ((evre - 0.4) / 0.6)
        gor.parilti_ciz(self.t, self.orta_x, self.orta_y,
                        self.yaricap * 1.75 * olcek, gor.NANE,
                        self.zemin_renk, katman=20, etiket=self.parilti_etiket,
                        guc=0.35)
        self.t.tag_lower(self.parilti_etiket)
        self.t.tag_lower("gradyan")

    def _neden_goster(self):
        baslik, metin, kaynak = self.uyg.sonraki_kart()
        genislik = min(760, self.gen - 140)

        kart = self.t.create_rectangle(
            self.orta_x - genislik / 2 - 26, self.kart_y - 24,
            self.orta_x + genislik / 2 + 26, self.kart_y + 150,
            fill=gor.karistir(self.zemin_renk, "#ffffff", 0.07),
            outline=gor.karistir(self.zemin_renk, "#ffffff", 0.18),
        )
        b = self.t.create_text(
            self.orta_x - genislik / 2, self.kart_y,
            text="NEDEN? — " + baslik.upper(), anchor="nw",
            fill=gor.KEHRIBAR, font=("Segoe UI", 11, "bold"),
        )
        m = self.t.create_text(
            self.orta_x - genislik / 2, self.kart_y + 28,
            text=metin, anchor="nw", width=genislik,
            fill=gor.MOLA_YAZI, font=("Segoe UI", 12), justify="left",
        )
        alt = self.t.bbox(m)[3]
        k = self.t.create_text(
            self.orta_x - genislik / 2, alt + 10,
            text="Kaynak: " + kaynak, anchor="nw", width=genislik,
            fill=gor.MOLA_SOLUK, font=("Segoe UI", 9), justify="left",
        )
        # Kartı yazıların gerçek boyuna göre kırp
        self.t.coords(kart,
                      self.orta_x - genislik / 2 - 26, self.kart_y - 24,
                      self.orta_x + genislik / 2 + 26, self.t.bbox(k)[3] + 20)
        self.t.tag_raise(b); self.t.tag_raise(m); self.t.tag_raise(k)
        self.kart_ogeleri = [kart, b, m, k]

    # ---------------- Kalp atışı ----------------
    def _tik(self):
        if not self.p.winfo_exists():
            return

        simdi = time.time()
        kalan = self.bitis - simdi
        gecen = simdi - self.baslangic

        # Acil çıkış: Ctrl+Alt+Shift 3 saniye.
        # Şifre konulmuşsa ayrıca şifre de sorulur — yoksa kilit anlamsız olurdu.
        if self.acil_sorulyor:
            self.p.after(200, self._tik)
            return
        if iz.kisayol_basili_mi("ctrl", "alt", "shift"):
            if self.acil_baslangic is None:
                self.acil_baslangic = simdi
            elif simdi - self.acil_baslangic >= 3:
                self.acil_baslangic = None
                self._acil_cikis_iste()
                return
        else:
            self.acil_baslangic = None

        if kalan <= 0:
            self.uyg.mola_bitti()
            return

        # Geri sayım: tam süreden başlar, 1'in altına inmez
        gosterilecek = min(int(self.toplam), int(kalan) + 1)
        self.t.itemconfigure(self.sayi, text=str(gosterilecek))

        # Son üç saniyede haber ver — mola aniden bitince ekrana
        # dönmek sarsıcı oluyordu.
        if kalan <= 3:
            self.t.itemconfigure(self.sayi, fill=gor.KEHRIBAR)
            self.t.itemconfigure(self.yonerge_yazi, text="Az kaldı — hazırlan")
        self.t.itemconfigure(self.yay, extent=-359.9 * max(0.0, kalan / self.toplam))

        self._nefes_ciz(gecen)

        # Rehberli egzersiz animasyonu
        if self.egzersiz:
            try:
                self.egzersiz.guncelle(gecen, self.toplam)
                yeni = self.egzersiz.anlik_yonerge(gecen, self.toplam)
                if yeni != self.son_yonerge:
                    self.son_yonerge = yeni
                    self.t.itemconfigure(self.yonerge_yazi, text=yeni)
            except Exception:
                self.egzersiz = None      # egzersiz çökse bile mola sürsün

        if (not self.neden_gosterildi and self.kart_sigar
                and gecen >= min(4.0, self.toplam * 0.2)):
            self.neden_gosterildi = True
            self._neden_goster()

        # Başka pencere öne geçtiyse geri al
        self.p.attributes("-topmost", True)
        self.p.lift()

        self.p.after(200, self._tik)

    def _acil_cikis_iste(self):
        """Acil çıkış istendi.

        Bireysel kipte şifre sorulmaz — şifre yalnızca programı
        kapatırken sorulur; molayı atlamak kişinin kendi bileceği iş.

        AİLE KİPİNDE şifre sorulur. Ebeveynin koyduğu 20 saniyeyi
        çocuğun üç tuşla geçebilmesi, kuralı kural olmaktan çıkarır.
        """
        if aile_kipinde_mi(self.uyg.ayar):
            self.acil_sorulyor = True
            self.p.attributes("-topmost", False)
            try:
                tamam = self.uyg.izin_al(
                    "Aile kipi açık. Molayı geçmek için ebeveyn şifresi.",
                    ust=self.p)
            finally:
                self.p.attributes("-topmost", True)
                self.acil_sorulyor = False
            if not tamam:
                return
        self.uyg.mola_bitti(iptal=True)

    def kapat(self):
        try:
            self.p.destroy()
        except Exception:
            pass


class EngelEkrani:
    """Aile kipinde kullanımı durduran tam ekran.

    NE ZAMAN ÇIKAR
      • Günlük ekran süresi dolduğunda
      • Saat yasağı içinde

    NEDEN MOLA EKRANI DEĞİL
      Mola ekranı 20 saniye sürer ve kendi kapanır. Bu ekran koşul
      sürdüğü sürece durur. İkisini aynı sınıfa sıkıştırmak, mola
      mantığını da bunu da karmaşıklaştırırdı.

    DÜRÜSTLÜK NOTU
      Bu bir güvenlik duvarı DEĞİL. Görev yöneticisinden süreç
      öldürülebilir. Bekçi süreci geri açıyor ama kararlı biri yine
      de aşar. Ekranda bunu gizlemiyoruz — "kırılmaz" demek yalan
      olurdu ve ebeveyni yanlış güvene sokardı.
    """

    def __init__(self, uygulama, baslik, aciklama):
        self.uyg = uygulama
        self.baslik_metni = baslik
        self.aciklama_metni = aciklama
        self.kapandi = False

        sol, ust, gen, yuk = iz.sanal_ekran()
        self.gen, self.yuk = gen, yuk

        self.p = tk.Toplevel(uygulama.kok)
        self.p.overrideredirect(True)
        self.p.geometry("%dx%d+%d+%d" % (gen, yuk, sol, ust))
        self.p.configure(bg=gor.MOLA_GRADYAN[0])
        self.p.attributes("-topmost", True)
        self.p.protocol("WM_DELETE_WINDOW", lambda: None)
        for tus in ("<Alt-F4>", "<Escape>", "<Control-w>", "<Control-W>",
                    "<Control-F4>", "<Alt-Tab>"):
            self.p.bind(tus, lambda e: "break")

        self.t = tk.Canvas(self.p, width=gen, height=yuk,
                           highlightthickness=0, bd=0)
        self.t.pack(fill="both", expand=True)
        self._sahne()
        self.p.lift()
        self.p.focus_force()
        self.p.after(60, lambda: iz.one_getir(self.p.winfo_id()))
        self._tik()
        self._koru()

    def _koru(self):
        """Ekranı önde tutar.

        Ayrı ve HIZLI bir döngü: metin saniyede bir tazelense yeter ama
        önde kalmak yetmiyor — Alt+Tab ile arkaya atılan ekran bir
        saniye boyunca arkada kalıyordu, o bir saniye kaçmaya yetiyor.
        400 ms'de bir öne alınıyor.
        """
        if self.kapandi:
            return
        try:
            self.p.attributes("-topmost", True)
            self.p.lift()
            # Odak başka pencereye kaçtıysa geri al
            if self.p.focus_displayof() is None:
                self.p.focus_force()
                iz.one_getir(self.p.winfo_id())
        except Exception:
            pass
        self.p.after(400, self._koru)

    def _sahne(self):
        gen, yuk = self.gen, self.yuk
        gor.gradyan_ciz(self.t, gen, yuk, gor.MOLA_GRADYAN)
        mx = gen / 2
        my = yuk / 2

        self.baslik = self.t.create_text(
            mx, my - 130, text=self.baslik_metni, fill=gor.MOLA_YAZI,
            font=("Segoe UI", 34, "bold"))
        self.aciklama = self.t.create_text(
            mx, my - 60, text=self.aciklama_metni, fill=gor.MOLA_SOLUK,
            font=("Segoe UI", 14), width=min(760, gen - 120), justify="center")
        self.alt_yazi = self.t.create_text(
            mx, my + 20, text="", fill=gor.KEHRIBAR,
            font=("Segoe UI", 16, "bold"))
        # Boş açılmasın; _tik bir saniye sonra gelir
        try:
            self.t.itemconfigure(self.alt_yazi,
                                 text=self.uyg.engel_kalan_metni())
        except Exception:
            pass

        # Ebeveyn düğmesi — şifreyle ek süre verir
        self.dugmeler = [
            og.Dugme(self.t, mx - 130, my + 80, 260, 46,
                     "Ebeveyn: ek süre ver", self._ek_sure,
                     gor.MOLA_GRADYAN[0], gor.KEHRIBAR, "#2a1f08",
                     "Segoe UI", kalin=True),
        ]

        # NOT: burada eskiden "bu ekran görev yöneticisinden kapatılabilir"
        # yazan bir satır vardı. Kaldırıldı — o yazı, engellemeye
        # çalıştığımız kişiye kaçış yolunu tarif ediyordu. Sınırın
        # dürüstçe yazılacağı yer AYARLAR penceresi; orayı yalnızca
        # şifreyi bilen ebeveyn açabiliyor.

    def _ek_sure(self):
        """Ebeveyn şifresiyle ek süre. Şifre yoksa kip zaten geçersiz."""
        kayit = kilit_kaydi(self.uyg.ayar)
        if kayit is None:
            return
        self.p.attributes("-topmost", False)
        try:
            tamam = SifreSor(self.p, "Ek süre vermek için ebeveyn şifresi.",
                             kayit, self.uyg._kilidi_yukselt).bekle()
        finally:
            self.p.attributes("-topmost", True)
        if not tamam:
            return
        cevap = Soru(
            self.p, "Ne kadar ek süre?",
            "Bu süre boyunca engel kalkar. Süre bitince ekran geri gelir.",
            evet_yazi="30 dakika", hayir_yazi="15 dakika",
            # geri_sayim=0 aninda varsayilani uyguluyor. Ebeveyn
            # ekranin basinda, dusunmesi icin sure verelim.
            geri_sayim=30, varsayilan=False).bekle()
        dakika = 30 if cevap else 15
        self.uyg.ayar["ek_sure_bitis"] = time.time() + dakika * 60
        ayarlari_yaz(self.uyg.ayar)
        self.uyg.engeli_kaldir()

    def _tik(self):
        if self.kapandi:
            return
        # Koşul kalktıysa kendini kapat
        yeni = self.uyg.engel_sebebi()
        if not yeni:
            self.uyg.engeli_kaldir()
            return

        # Sebep değiştiyse (yasak bitti ama süre sınırı doldu gibi)
        # başlığı ve açıklamayı tazele. Eskiden yalnızca alt satır
        # güncelleniyordu ve başlık yanlış sebebi gösteriyordu.
        if yeni[1] != self.baslik_metni:
            self.baslik_metni = yeni[1]
            self.aciklama_metni = yeni[2]
            self.t.itemconfigure(self.baslik, text=yeni[1])
            self.t.itemconfigure(self.aciklama, text=yeni[2])

        # Alt satır CANLI geri sayım — açıklamanın kopyası değil.
        # İlk yazımda buraya da açıklama konuyordu ve ekranda aynı
        # cümle iki kez görünüyordu.
        try:
            self.t.itemconfigure(self.alt_yazi,
                                 text=self.uyg.engel_kalan_metni())
        except Exception:
            pass

        self.p.after(1000, self._tik)

    def kapat(self):
        self.kapandi = True
        try:
            self.p.destroy()
        except Exception:
            pass


# ======================================================================
# SORU KUTUSU — "gerekirse izin istesin" kısmı
# ======================================================================
class Soru:
    """Cevap gelmezse GÜVENLİ seçenek uygulanır.
    Güvenli seçenek her zaman 'molayı ver' tarafıdır."""

    def __init__(self, kok, baslik, metin, evet_yazi, hayir_yazi,
                 geri_sayim=12, varsayilan=False):
        self.sonuc = varsayilan
        self.varsayilan = varsayilan
        self.bitis = time.time() + geri_sayim

        self.p = tk.Toplevel(kok)
        self.p.title(baslik)
        self.p.configure(bg=P["kart"])
        self.p.attributes("-topmost", True)
        self.p.resizable(False, False)
        self.p.protocol("WM_DELETE_WINDOW", self._hayir)

        tk.Label(self.p, text=baslik, font=("Segoe UI", 14, "bold"),
                 fg=P["yazi"], bg=P["kart"], wraplength=400,
                 justify="left").pack(padx=26, pady=(22, 8), anchor="w")
        tk.Label(self.p, text=metin, font=("Segoe UI", 10), fg=P["soluk"],
                 bg=P["kart"], wraplength=400, justify="left").pack(padx=26, anchor="w")

        self.sayac = tk.Label(self.p, text="", font=("Segoe UI", 9),
                              fg=P["sicak"], bg=P["kart"])
        self.sayac.pack(pady=(12, 0))

        sira = tk.Frame(self.p, bg=P["kart"])
        sira.pack(padx=26, pady=20)
        dugme(sira, hayir_yazi, self._hayir).pack(side="left", padx=6)
        dugme(sira, evet_yazi, self._evet, ana_mi=True).pack(side="left", padx=6)

        self.p.update_idletasks()
        g, y = self.p.winfo_width(), self.p.winfo_height()
        self.p.geometry("+%d+%d" % ((self.p.winfo_screenwidth() - g) // 2,
                                    (self.p.winfo_screenheight() - y) // 3))
        self.p.lift()
        self.p.focus_force()
        self._tik()

    def _tik(self):
        if not self.p.winfo_exists():
            return
        kalan = self.bitis - time.time()
        if kalan <= 0:
            self.sonuc = self.varsayilan
            self.p.destroy()
            return
        self.sayac.configure(text="%d saniye içinde cevap vermezsen mola başlar."
                                  % (int(kalan) + 1))
        self.p.after(250, self._tik)

    def _evet(self):
        self.sonuc = True
        self.p.destroy()

    def _hayir(self):
        self.sonuc = False
        self.p.destroy()

    def bekle(self):
        self.p.wait_window()
        return self.sonuc


# ======================================================================
# ŞİFRE SORMA
# ======================================================================
class SifreSor:
    def __init__(self, kok, aciklama, kayit, yukseltme_geri_cagri=None):
        self.tamam = False
        self.kayit = kayit
        self.yukselt = yukseltme_geri_cagri
        self.yanlis = 0
        self.bekleme_bitis = 0

        self.p = tk.Toplevel(kok)
        self.p.title("Şifre gerekli")
        self.p.configure(bg=P["kart"])
        self.p.attributes("-topmost", True)
        self.p.resizable(False, False)

        tk.Label(self.p, text="Şifre gerekli", font=("Segoe UI", 14, "bold"),
                 fg=P["yazi"], bg=P["kart"]).pack(padx=26, pady=(22, 6))
        tk.Label(self.p, text=aciklama, font=("Segoe UI", 10), fg=P["soluk"],
                 bg=P["kart"], wraplength=340).pack(padx=26)

        self.alan = tk.Entry(self.p, show="●", font=("Segoe UI", 18), justify="center",
                             bg=P["zemin"], fg=P["yazi"], insertbackground=P["yazi"],
                             relief="flat", width=12)
        self.alan.pack(pady=16, ipady=8)
        self.alan.bind("<Return>", lambda e: self._onayla())

        self.hata = tk.Label(self.p, text="", font=("Segoe UI", 9),
                             fg="#ff8f7a", bg=P["kart"])
        self.hata.pack()

        sira = tk.Frame(self.p, bg=P["kart"])
        sira.pack(padx=26, pady=18)
        dugme(sira, "Vazgeç", self.p.destroy).pack(side="left", padx=6)
        dugme(sira, "Onayla", self._onayla, ana_mi=True).pack(side="left", padx=6)

        self.p.update_idletasks()
        g, y = self.p.winfo_width(), self.p.winfo_height()
        self.p.geometry("+%d+%d" % ((self.p.winfo_screenwidth() - g) // 2,
                                    (self.p.winfo_screenheight() - y) // 3))
        self.alan.focus_force()

    def _onayla(self):
        if time.time() < self.bekleme_bitis:
            return
        girilen = self.alan.get()
        self.hata.configure(text="Kontrol ediliyor…", fg=P["soluk"])
        self.p.update_idletasks()

        dogru, yukseltilmeli = kl.dogrula(girilen, self.kayit)
        if dogru:
            if yukseltilmeli and callable(self.yukselt):
                self.yukselt(girilen)      # eski özeti yeni yönteme taşı
            self.tamam = True
            self.p.destroy()
            return

        self.yanlis += 1
        self.alan.delete(0, "end")
        if self.yanlis % 3 == 0:
            # Her 3 yanlışta bekletme uzuyor: 15, 30, 45 saniye...
            bekleme = 15 * (self.yanlis // 3)
            self.bekleme_bitis = time.time() + bekleme
            self.alan.configure(state="disabled")
            self.hata.configure(text="%d yanlış deneme — %d saniye bekle."
                                     % (self.yanlis, bekleme), fg="#ff8f7a")
            self.p.after(bekleme * 1000, self._beklemeyi_bitir)
        else:
            self.hata.configure(text="Şifre yanlış. (%d. deneme)" % self.yanlis,
                                fg="#ff8f7a")

    def _beklemeyi_bitir(self):
        try:
            self.alan.configure(state="normal")
            self.hata.configure(text="")
            self.alan.focus_force()
        except Exception:
            pass

    def bekle(self):
        self.p.wait_window()
        return self.tamam


# ======================================================================
# UYARI BALONU
# ======================================================================
class Balon:
    def __init__(self, kok, metin):
        self.p = tk.Toplevel(kok)
        self.p.overrideredirect(True)
        self.p.attributes("-topmost", True)
        self.p.configure(bg=gor.KEHRIBAR)

        ic = tk.Frame(self.p, bg=P["kart"], padx=26, pady=14)
        ic.pack(padx=2, pady=2)
        self.yazi = tk.Label(ic, text=metin, font=("Segoe UI", 12, "bold"),
                             fg=P["yazi"], bg=P["kart"], width=26)
        self.yazi.pack()

        self.p.update_idletasks()
        g = self.p.winfo_width()
        self.p.geometry("+%d+%d" % ((self.p.winfo_screenwidth() - g) // 2,
                                    self.p.winfo_screenheight() - 170))

    def guncelle(self, metin):
        try:
            self.yazi.configure(text=metin)
            self.p.attributes("-topmost", True)
        except Exception:
            pass

    def kapat(self):
        try:
            self.p.destroy()
        except Exception:
            pass


class TelafiKarti:
    """Mola atlanınca çıkan, kendiliğinden kapanan bilgi kartı.

    NEDEN SORU KUTUSU DEĞİL: molayı atlayan kişi meşgul. Karşısına
    cevap bekleyen bir pencere çıkarmak, atlamanın sebebini görmezden
    gelmek olur. Bu kart hiçbir şey sormaz, birkaç saniye durur ve
    kendi kapanır. Tıklanırsa hemen kapanır.

    NEDEN GÖSTERİLİYOR: atlamayı sessizce geçiştirmek "atlamak
    önemsizdi" mesajı veriyor. Oysa asıl anlatılacak şey tam da o an
    lazım — neyi atladığı.
    """

    SANIYE = 9

    def __init__(self, kok, baslik, metin, kaynak, plan, eylem=None):
        self.p = tk.Toplevel(kok)
        self.p.overrideredirect(True)
        self.p.attributes("-topmost", True)
        self.p.configure(bg=gor.KEHRIBAR)

        ic = tk.Frame(self.p, bg=P["kart"], padx=22, pady=16)
        ic.pack(padx=2, pady=2)

        tk.Label(ic, text=baslik, font=("Segoe UI", 12, "bold"),
                 fg=P["yazi"], bg=P["kart"], anchor="w",
                 justify="left", wraplength=440).pack(anchor="w")
        tk.Label(ic, text=metin, font=("Segoe UI", 10),
                 fg=P["yazi"], bg=P["kart"], anchor="w",
                 justify="left", wraplength=440).pack(anchor="w", pady=(6, 0))
        if kaynak:
            tk.Label(ic, text=kaynak, font=("Segoe UI", 8),
                     fg=P["soluk"], bg=P["kart"], anchor="w",
                     justify="left", wraplength=440).pack(anchor="w", pady=(4, 0))
        tk.Label(ic, text=plan, font=("Segoe UI", 10, "bold"),
                 fg=gor.KEHRIBAR, bg=P["kart"], anchor="w",
                 justify="left", wraplength=440).pack(anchor="w", pady=(10, 0))

        # Tıklanınca: eylem varsa onu çalıştır (ör. indirme sayfasını aç),
        # sonra kapan. Eylem yoksa sadece kapan.
        def _tik(_e=None):
            if eylem:
                try:
                    eylem()
                except Exception:
                    pass
            self.kapat()

        for w in (self.p, ic):
            w.bind("<Button-1>", _tik)
        for c in ic.winfo_children():
            c.bind("<Button-1>", _tik)

        self.p.update_idletasks()
        g, y = self.p.winfo_width(), self.p.winfo_height()
        try:
            a_sol, a_ust, a_gen, a_yuk = iz.calisma_alani()
        except Exception:
            a_sol, a_ust = 0, 0
            a_gen = self.p.winfo_screenwidth()
            a_yuk = self.p.winfo_screenheight()
        self.p.geometry("+%d+%d" % (a_sol + (a_gen - g) // 2,
                                    a_ust + a_yuk - y - 60))
        self.p.after(int(self.SANIYE * 1000), self.kapat)

    def kapat(self):
        try:
            self.p.destroy()
        except Exception:
            pass


# ======================================================================
# ANA UYGULAMA
# ======================================================================
class Uygulama:
    def __init__(self):
        # Pencere açılmadan ÖNCE çağrılmalı
        iz.dpi_farkindaligi_ac()
        # Ayar dosyası yoksa bu ilk açılış demektir
        self.ilk_acilis = not os.path.exists(AYAR_DOSYA)
        self.ayar = ayarlari_oku()
        gor.tema_uygula(self.ayar.get("tema", "gece"),
                        self.ayar.get("canlilik", 1.0))
        self.durum = "calisiyor"
        # Sayacı kaldığı yerden sürdür. Eskiden her açılışta sıfırdan
        # başlıyordu: programı aç-kapa yapan biri hiç mola almıyordu.
        self.hedef = self._sayaci_geri_yukle()
        self.dondurulmus = None
        self.mola_ekrani = None
        self.balon = None
        self.uzun_mola_mi = False
        # Atlanan molanın telafisi: kaç kez üst üste atlandı ve bir
        # sonraki mola kaç saniye olacak
        self.telafi_sayisi = 0
        self.telafi_suresi = None
        # Aile kipi engel ekrani (gunluk sinir / saat yasagi)
        self.engel_ekrani = None
        self.baslangic_ani = time.time()
        self.kilit_gorundu = False
        self.kart_sirasi = 0
        self.bilgi_no = random.randrange(len(BILGILER) or 1)
        self.dunya_no = random.randrange(len(DUNYA) or 1)
        self.ipucu_no = 0
        self.son_bosta = 0.0
        self.duraklama_bitis = 0
        self.tepsi = None

        self.ist = {
            "gun": time.strftime("%Y-%m-%d"),
            "tamamlanan": 0, "ertelenen": 0, "uzun_mola": 0,
            "ekran_sn": 0.0, "kesintisiz_sn": 0.0, "programlar": {},
        }
        self._istatistik_oku()

        self.kok = tk.Tk()
        self.kok.title("Göz Molası")
        self.kok.configure(bg=P["zemin"])

        # Ekran büyütmesi (%125, %150...) — tasarımı buna göre ölçekliyoruz.
        self.o = iz.olcek()

        # ...ama ekrana SIĞMASI şart. Panel 580x888 tasarım ölçüsünde ve
        # resizable(False, False); eskiden yalnızca DPI ile çarpılıyordu.
        # 1366x768 bir dizüstünde %125 ölçekte panel 1000px oluyor, 232px'i
        # ekranın dışında kalıyor ve kullanıcı pencereyi büyütemediği için
        # alttaki düğmelere hiç ulaşamıyordu. Ölçeği ekrana göre kısıyoruz.
        # Windows'un bildirdiği ÇALIŞMA ALANI'na sığdırıyoruz. Eskiden
        # "ekran yüksekliği - 80" yazıyordu: 80 uydurma bir sayıydı ve
        # başlık çubuğunu hiç saymıyordu. 1920x1200 / %125 ölçekli bir
        # makinede pencere 1143 piksel istiyor, çalışma alanı ise 1140 —
        # alttaki "Programı kapat" düğmesi görev çubuğunun altında
        # kalıyordu. Artık tahmin yok, ölçülen değer var.
        try:
            _, _, kul_g, kul_y = iz.calisma_alani()
            baslik, kenar = iz.pencere_cercevesi()
            # Tk yalnızca İÇERİĞİ ölçer; başlık çubuğu ve kenarlar ayrıca yer kaplar
            ic_y = kul_y - baslik - 2 * kenar
            ic_g = kul_g - 2 * kenar
            self.o = min(self.o, ic_y / 888.0, ic_g / 580.0)
            self.o = max(0.62, self.o)                   # okunmaz kadar küçülmesin
        except Exception:
            pass
        # Yazı tipleri punto cinsinden; tk'ye de aynı ölçeği bildiriyoruz
        try:
            self.kok.tk.call("tk", "scaling", self.o * 96.0 / 72.0)
        except Exception:
            pass

        self.G, self.Y = self.ol(580), self.ol(888)
        # Pencereyi çalışma alanının İÇİNE yerleştir. Boyut doğru olsa
        # bile Windows pencereyi y=32 gibi bir yere koyuyordu ve alt
        # kenar görev çubuğunun altında kalıyordu.
        try:
            a_sol, a_ust, a_gen, a_yuk = iz.calisma_alani()
            baslik, kenar = iz.pencere_cercevesi()
            tam_y = self.Y + baslik + 2 * kenar
            x = a_sol + max(0, (a_gen - self.G) // 2)
            y = a_ust + max(0, (a_yuk - tam_y) // 2)
            self.kok.geometry("%dx%d+%d+%d" % (self.G, self.Y, x, y))
        except Exception:
            self.kok.geometry("%dx%d" % (self.G, self.Y))
        self.kok.resizable(False, False)
        self.yt = og.yazi_tipi_sec(self.kok)
        self.kok.protocol("WM_DELETE_WINDOW", self.gizle)
        try:
            self.kok.iconbitmap(kaynak_yolu("ikon.ico"))
        except Exception:
            pass

        self._panel_kur()

        # Beyaz başlık çubuğu koyu bir uygulamanın üstünde yamalı duruyor.
        # Windows'a başlık çubuğunu uygulamanın rengine boyamasını söylüyoruz.
        # Pencere gerçekten oluşana kadar hwnd hazır olmaz, o yüzden update sonrası.
        self.kok.update_idletasks()
        try:
            iz.pencereyi_koyulastir(self.kok.winfo_id(), P["zemin"], P["yazi"])
        except Exception:
            pass

        self._sekme_sec("programlar")
        self._analiz_izni_sor_gerekirse()
        self._acilis_izni_sor_gerekirse()
        # İzin pencerelerinden sonra: sürüm/kayıt/ölçüm denetimi.
        # 5 saniye, izin soruları (1,5 ve 2,6 sn) kapandıktan sonrası.
        self.kok.after(5000, self._surum_denetimini_baslat)
        self._bekciyi_kur()
        self._kopruyu_kur()
        ses.onceden_hazirla()

        # Tepsi simgesi. Kurulamazsa pencere görev çubuğunda kalır —
        # kullanıcının programa ulaşamaması olmaz.
        try:
            self.tepsi = tepsi.Tepsi(self, kaynak_yolu("ikon.ico"))
            if not self.tepsi.baslat():
                self.tepsi = None
        except Exception:
            self.tepsi = None

        # Tepsi yoksa pencere görev çubuğunda kalacak; alt yazıyı ona göre yaz
        if not self.tepsi:
            self.t.itemconfigure(
                self.alt_bilgi,
                text="Pencereyi kapatmak programı kapatmaz — görev çubuğunda durur.")

        self.kok.after(200, self._tik)

        # İLK AÇILIŞTA PENCEREYİ GÖSTER.
        # Eskiden program açılır açılmaz kendini gizliyordu; tepsi simgesi de
        # Windows'un "gizli simgeler" okunun altına düştüğü için kullanıcı
        # ekranda hiçbir şey görmüyor ve "açılmıyor" sanıyordu.
        if self.ilk_acilis:
            self.pencereyi_goster()
            ayarlari_yaz(self.ayar)      # bir daha ilk açılış sayılmasın
        else:
            self.gizle()

    def ol(self, deger):
        """Tasarım ölçüsünü ekranın büyütmesine çevir."""
        return int(round(deger * self.o))

    def _panel_yenile(self):
        """Paneli baştan çiz. Renkler çizim ANINDA okunuyor; var olan
        şekillerin rengi kendiliğinden değişmiyor, o yüzden tuvali
        komple yeniliyoruz. Tema ve canlılık değişince çağrılır."""
        gorunur = self.kok.state() == "normal"
        try:
            self.t.destroy()
        except Exception:
            pass
        self.kok.configure(bg=P["zemin"])
        self._panel_kur()
        self._sekme_sec(self.grafik_sekmesi if hasattr(self, "grafik_sekmesi")
                        else "programlar")
        self.grafik_imza = None
        self.nokta_imza = None
        self.oneri_imza = None
        try:
            iz.pencereyi_koyulastir(self.kok.winfo_id(), P["zemin"], P["yazi"])
        except Exception:
            pass
        if gorunur:
            self._ciz(self.hedef - time.time())

    def canliligi_degistir(self, deger):
        """Renklerin doygunluğunu değiştir ve paneli baştan çiz.
        Renkler çizim ANINDA okunuyor; var olan şekiller kendiliğinden
        değişmez, o yüzden tuvali komple yeniliyoruz."""
        yeni = max(0.6, min(1.5, round(float(deger), 2)))
        if abs(yeni - float(self.ayar.get("canlilik", 1.0))) < 0.01:
            return
        self.ayar["canlilik"] = yeni
        gor.tema_uygula(self.ayar.get("tema", "gece"), yeni)
        ayarlari_yaz(self.ayar)
        self._panel_yenile()

    def temayi_degistir(self, ad):
        """Temayı değiştir ve paneli baştan çiz.

        Renkler çizim ANINDA okunuyor; var olan şekillerin rengi kendiliğinden
        değişmez. Bu yüzden tuvali komple yenilemek gerekiyor.
        """
        if ad == self.ayar.get("tema"):
            return
        self.ayar["tema"] = ad
        gor.tema_uygula(ad, self.ayar.get("canlilik", 1.0))
        ayarlari_yaz(self.ayar)

        self._panel_yenile()

    # ---------------- Kayıt ----------------
    def _sayaci_geri_yukle(self):
        """Program kapanırken kalan süreyi geri yükler.

        Eskiden her açılışta sayaç sıfırdan başlıyordu; programı aç-kapa
        yapan biri hiç mola almıyordu. Kurallar:
          • Kapalı kaldığı süre dinlenme eşiğinden uzunsa (varsayılan 5 dk)
            gözler zaten dinlenmiştir — temiz bir süre başlar.
          • Hedef henüz geçmemişse kaldığı yerden devam eder.
          • Hedef kapalıyken geçtiyse: kısa süre kapalıydıysa kaçırılan
            molayı kısa bir payla verir, uzun kapalıydıysa temiz başlar.
        """
        tam = time.time() + self.ayar["calisma_dk"] * 60
        try:
            with open(DURUM_DOSYA, "r", encoding="utf-8-sig") as f:
                d = json.load(f)
        except Exception:
            return tam

        kapali_kalan = time.time() - float(d.get("kayit_ani", 0))

        # ÖLÇÜLEMEYEN SÜRE — kullanıcıya dürüst olmak için.
        # Program kapalıyken hiçbir şey ölçemiyoruz. Ama bilgisayarın
        # ne zaman açıldığını Windows biliyor; kapalı geçen sürenin ne
        # kadarında makinenin AÇIK olduğunu buradan sınırlayabiliyoruz.
        # "Saymadım" demek, hiç söylememekten iyi.
        try:
            acik_kalan = kl.acilistan_beri_saniye()
            self.olculemeyen_sn = max(0.0, min(kapali_kalan, acik_kalan))
        except Exception:
            self.olculemeyen_sn = 0.0

        if kapali_kalan < 0 or kapali_kalan > self.ayar["dinlenme_esigi_sn"]:
            return tam

        # `float()` burada cokuyordu: durum.json'a "cok sonra" gibi bir
        # metin yazilinca ValueError dusuyor ve UYGULAMA HIC ACILMIYOR.
        # Acilmayan uygulamada aile kipi de dahil hicbir koruma yok -
        # cokme, en sessiz atlatmadir.
        kalan = sayi_oku(d.get("hedef"), 0.0) - time.time()
        if 0 < kalan <= self.ayar["calisma_dk"] * 60:
            return time.time() + kalan

        # Hedef kapalıyken geçmiş. Ölçtüm: sayaç -45 saniyedeyken program
        # açılınca o mola sessizce düşüyor ve 20 dakika baştan başlıyordu.
        # Kısa bir kapanmaydıysa (güncelleme, çökme, yeniden başlatma)
        # kullanıcı ekranın başındaydı ve molayı hak ediyor — kısa bir
        # pay bırakıp veriyoruz. Uzun kapanmada temiz başlıyoruz ki
        # açılır açılmaz mola ekranı yüzüne çarpmasın.
        if kalan <= 0 and kapali_kalan <= 60:
            return time.time() + 25
        return tam

    def _sayaci_kaydet(self):
        try:
            os.makedirs(KAYIT_KLASOR, exist_ok=True)
            with open(DURUM_DOSYA, "w", encoding="utf-8") as f:
                json.dump({"hedef": self.hedef, "kayit_ani": time.time(),
                           "durum": self.durum}, f)
        except Exception:
            pass

    def _istatistik_oku(self):
        try:
            with open(IST_DOSYA, "r", encoding="utf-8-sig") as f:
                veri = json.load(f)
            if veri.get("gun") == time.strftime("%Y-%m-%d"):
                self.ist.update(veri)
        except Exception:
            pass
        # Dosya okundu; simdi GUVENILIR MI diye sor.
        self._sayac_isaretini_dogrula()

    # Kertme toleransi: isaret ile istatistik AYRI dosyalara, AYRI
    # anlarda yaziliyor. Program tam aralarinda kapanirsa isaret bir
    # kayit araligi (30 sn) kadar ileride kalabilir. 90 sn, bunu rahatca
    # kapsar ve gercek bir geri almayi (dakikalar/saatler) kacirmaz.
    ISARET_TOLERANSI_SN = 90

    def _sayac_isaretini_dogrula(self):
        """Ekran suresi gun icinde geri gitmis mi? Aile kipinde onemli.

        Bireysel kipte hicbir sey yapmaz: orada kullanici kendi
        verisinin sahibidir, sifirlamak mesrudur.
        """
        self.sayac_oynanmis = False
        if not aile_kipinde_mi(self.ayar):
            return
        bugun = time.strftime("%Y-%m-%d")
        simdiki = sayi_oku(self.ist.get("ekran_sn"), None)
        if simdiki is None:
            return                      # bozuk deger: ayar_uyarisi ilgileniyor

        isaret = self.ayar.get("ekran_isareti")
        if isinstance(isaret, dict) and isaret.get("gun") == bugun:
            onceki = sayi_oku(isaret.get("sn"), None)
            if onceki is not None and simdiki < onceki - self.ISARET_TOLERANSI_SN:
                # Dusuk degere GUVENMIYORUZ. Sessizce duzeltmek de
                # yanlis olurdu - ebeveyn bilmeli.
                self.ist["ekran_sn"] = onceki
                self.sayac_oynanmis = True
                return
        self._sayac_isaretini_tazele()

    def _sayac_isaretini_tazele(self):
        """Gorulen en yuksek degeri isaretler. Yalnizca ileri gider."""
        if not aile_kipinde_mi(self.ayar):
            return
        bugun = time.strftime("%Y-%m-%d")
        simdiki = sayi_oku(self.ist.get("ekran_sn"), None)
        if simdiki is None:
            return
        isaret = self.ayar.get("ekran_isareti")
        onceki = 0.0
        if isinstance(isaret, dict) and isaret.get("gun") == bugun:
            onceki = sayi_oku(isaret.get("sn"), 0.0)
        if simdiki >= onceki:
            self.ayar["ekran_isareti"] = {"gun": bugun, "sn": float(simdiki)}

    def _istatistik_yaz(self):
        self._sayac_isaretini_tazele()
        try:
            os.makedirs(KAYIT_KLASOR, exist_ok=True)
            with open(IST_DOSYA, "w", encoding="utf-8") as f:
                json.dump(self.ist, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        self._sayaci_kaydet()
        # Günün özetini kalıcı geçmişe de yaz (7 gün grafiği ve seri için)
        try:
            gcm.gunu_isle(KAYIT_KLASOR, self.ist.get("gun", time.strftime("%Y-%m-%d")),
                          self.ist)
        except Exception:
            pass

    # ---------------- Kilit ----------------
    def kilitli_mi(self):
        return kilit_kaydi(self.ayar) is not None

    def _kilidi_yukselt(self, sifre):
        """Eski SHA-256 kaydı doğrulandı — yeni, kırılması zor yönteme taşı."""
        self.ayar["kilit"] = kl.ozet_uret(sifre)
        self.ayar["kilit_ozeti"] = None
        self.ayar["kilit_tuz"] = None
        ayarlari_yaz(self.ayar)

    def izin_al(self, aciklama, ust=None):
        kayit = kilit_kaydi(self.ayar)
        if kayit is None:
            return True
        return SifreSor(ust or self.kok, aciklama, kayit,
                        self._kilidi_yukselt).bekle()

    # ---------------- Panel ----------------
    def _panel_kur(self):
        """Panelin tamamı tek bir tuvale çizilir.

        Sebep: tkinter'ın hazır düğme ve çerçeveleri keskin köşeli ve
        gölgesiz. Tuvale çizince yuvarlak kartlar, gradyan zemin ve
        üstüne gelince renk değiştiren düğmeler yapabiliyoruz.
        """
        o = self.ol                      # tasarım ölçüsü -> ekran pikseli
        G, Y = self.G, self.Y
        self.t = tk.Canvas(self.kok, width=G, height=Y, highlightthickness=0, bd=0)
        self.t.pack(fill="both", expand=True)
        yt = self.yt

        gor.gradyan_ciz(self.t, G, Y, [P["zemin"], P["zemin2"], P["zemin"]])
        # Üst köşelerde yumuşak renk lekeleri — düz zemin cansız duruyordu
        gor.parilti_ciz(self.t, o(60), o(40), o(190), P["vurgu"], P["zemin"], katman=16)
        gor.parilti_ciz(self.t, G - o(50), o(90), o(210), P["sicak"], P["zemin"], katman=16)

        ke = o(24)                       # kenar boşluğu

        # ---------- Başlık ----------
        og.goz_simgesi(self.t, ke + o(15), o(42), o(30), P["vurgu"], P["zemin2"])
        self.t.create_text(ke + o(40), o(34), anchor="w", text="Göz Molası",
                           fill=P["yazi"], font=(yt, 19, "bold"))
        self.t.create_text(ke + o(40), o(56), anchor="w",
                           text="20 DAKİKA · 20 SANİYE · 6 METRE",
                           fill=P["soluk"], font=(yt, 8))
        self.kilit_rozet = self.t.create_text(G - ke, o(56), anchor="e", text="",
                                              fill=P["sicak"], font=(yt, 8, "bold"))
        self.seri_rozet = self.t.create_text(G - ke, o(34), anchor="e", text="",
                                             fill=P["vurgu"], font=(yt, 11, "bold"))

        # "ARKA PLANDA ÇALIŞIYORUM" ŞERİDİ
        # Kullanıcının haklı şikâyeti: program saatlerdir çalışıp ölçüyor
        # ama hiçbir yerde göründüğüne dair iz yok — Windows 11 yeni tepsi
        # simgelerini taşma okunun altına saklıyor. Pencere açıldığında ilk
        # görülecek şey, arka planda ne kadar ölçtüğü olmalı.
        #
        # YERLEŞİM — bu bir kez bozuldu, bir daha bozulmasın:
        # Şerit KENDİ satırında durur (78-140). Önce 92-142 arasına
        # çizilmişti, ama sayaç kartı 78'de başlıyordu; şerit kartın
        # tepesine biniyordu. Artık kart 148'de başlıyor ve şeridin
        # altındaki HER ŞEY 70 birim aşağıda. Tasarım yüksekliği de
        # 800'den 888'e çıktı, yoksa alttaki düğmeler pencerenin
        # dışına taşardı. sinama_yerlesim.py bunu otomatik denetliyor.
        #
        # yuvarlak() genişlik/yükseklik değil KÖŞE KOORDİNATLARI alıyor
        # ve rengi fill= ile istiyor.
        og.yuvarlak(self.t, ke, o(78), G - ke, o(140),
                    r=o(12), fill=gor.karistir(P["zemin"], P["vurgu"], 0.14),
                    outline="")
        self.arka_serit = self.t.create_text(
            ke + o(16), o(95), anchor="w", text="",
            fill=P["yazi"], font=(yt, 9, "bold"))
        self.arka_serit_alt = self.t.create_text(
            ke + o(16), o(118), anchor="w", text="",
            fill=P["soluk"], font=(yt, 8),
            width=G - 2 * ke - o(32))

        # ---------- Sayaç kartı ----------
        og.kart(self.t, ke, o(148), G - ke, o(422), P["zemin"], P["kart"], r=o(22))
        mx, my = G / 2, o(266)
        self.halka_r = o(78)
        self.halka_kalinlik = o(12)
        gor.parilti_ciz(self.t, mx, my, self.halka_r * 1.5, P["vurgu"], P["kart"], katman=14)
        self.t.create_oval(mx - self.halka_r, my - self.halka_r,
                           mx + self.halka_r, my + self.halka_r,
                           outline=P["cizgi"], width=self.halka_kalinlik)
        self.halka_yay = self.t.create_arc(
            mx - self.halka_r, my - self.halka_r, mx + self.halka_r, my + self.halka_r,
            start=90, extent=-359.9, style="arc", outline=P["vurgu"],
            width=self.halka_kalinlik)
        self.halka_orta = (mx, my)
        self.uc_noktalari = []            # yayın yuvarlak uçları
        self.sure_yazi = self.t.create_text(mx, my - o(6), text="20:00", fill=P["yazi"],
                                            font=(yt, 32, "bold"))
        self.durum_yazi = self.t.create_text(mx, my + o(32), text="Çalışıyor",
                                             fill=P["soluk"], font=(yt, 9))

        # Kartın altında: bugünkü molalar nokta nokta + sonraki mola bilgisi
        self.nokta_y = o(370)
        self.nokta_x = ke + o(22)
        self.nokta_cap = o(9)
        self.nokta_ara = o(6)
        self.nokta_adet = 12
        self.t.create_text(self.nokta_x, o(358), anchor="w", text="BUGÜNKÜ MOLALAR",
                           fill=gor.karistir(P["kart"], P["soluk"], 0.75), font=(yt, 7, "bold"))
        self.ipucu_yazi = self.t.create_text(G - ke - o(22), o(374), anchor="e", text="",
                                             fill=P["soluk"], font=(yt, 9))

        # ---------- Düğmeler ----------
        dy, dyu = o(444), o(46)
        ara = o(10)
        kalan_g = G - 2 * ke - 2 * ara
        g1, g2 = int(kalan_g * 0.42), int(kalan_g * 0.29)
        g3 = kalan_g - g1 - g2
        self.dugmeler = [
            og.Dugme(self.t, ke, dy, g1, dyu, "Şimdi mola ver", self.hemen_mola,
                     P["zemin"], P["vurgu"], P.get("ana_yazi", "#0d2b28"), yt, kalin=True),
            og.Dugme(self.t, ke + g1 + ara, dy, g2, dyu, "Ayarlar", self.ayarlari_ac,
                     P["zemin"], P["kart2"], P["yazi"], yt),
            og.Dugme(self.t, ke + g1 + g2 + 2 * ara, dy, g3, dyu, "Gizle", self.gizle,
                     P["zemin"], P["kart2"], P["yazi"], yt),
        ]

        # ---------- Bugün kutucukları ----------
        self.t.create_text(ke, o(516), anchor="w", text="BUGÜN",
                           fill=P["soluk"], font=(yt, 8, "bold"))
        ky, kyu = o(530), o(80)
        kutu_g = (G - 2 * ke - 3 * ara) / 4
        self.kutu_yazilari = {}
        for i, (anahtar, etiket, vurgu) in enumerate((
                ("tamamlanan", "mola", P["vurgu"]),
                ("uzun_mola", "uzun mola", gor.GRAFIK_RENKLERI[2]),
                ("ekran_sn", "ekran", P["sicak"]),
                ("kesintisiz_sn", "kesintisiz", gor.GRAFIK_RENKLERI[3]))):
            x = ke + i * (kutu_g + ara)
            og.kart(self.t, x, ky, x + kutu_g, ky + kyu, P["zemin"], P["kart"],
                    r=o(16), golge=2)
            # Üstte ince renkli şerit — kutucuklar birbirinden ayrışsın
            og.yuvarlak(self.t, x + o(16), ky + o(7), x + kutu_g - o(16), ky + o(10),
                        r=o(2), fill=vurgu, outline="")
            self.kutu_yazilari[anahtar] = self.t.create_text(
                x + kutu_g / 2, ky + o(34), text="0", fill=P["yazi"], font=(yt, 16, "bold"))
            self.t.create_text(x + kutu_g / 2, ky + o(60), text=etiket,
                               fill=P["soluk"], font=(yt, 8))

        # ---------- Grafik kartı ----------
        self.grafik_ust = o(632)
        self.grafik_alt = o(786)
        og.kart(self.t, ke, self.grafik_ust, G - ke, self.grafik_alt,
                P["zemin"], P["kart"], r=o(20))
        self.grafik_baslik = self.t.create_text(
            ke + o(20), self.grafik_ust + o(22), anchor="w", text="EN ÇOK KULLANDIKLARIN",
            fill=P["soluk"], font=(yt, 8, "bold"))
        self.grafik_imza = None

        # Sekme: PROGRAMLAR | 7 GÜN
        self.grafik_sekmesi = "programlar"
        sek_g, sek_y = o(78), o(22)
        sek_x = G - ke - o(20) - 2 * sek_g - o(4)
        self.sekme_dugmeleri = {}
        for i, (anahtar, etiket) in enumerate((("programlar", "Programlar"),
                                               ("hafta", "7 gün"))):
            x = sek_x + i * (sek_g + o(4))
            d = og.Dugme(self.t, x, self.grafik_ust + o(11), sek_g, sek_y, etiket,
                         (lambda a=anahtar: self._sekme_sec(a)),
                         P["kart"], P["kart2"], P["soluk"], yt, r=o(11))
            self.sekme_dugmeleri[anahtar] = d

        # ---------- Öneri şeridi ----------
        self.oneri_ust = o(800)
        self.oneri_imza = None

        # ---------- Alt ----------
        self.alt_bilgi = self.t.create_text(
            ke, o(865), anchor="w",
            text="Pencereyi kapatmak programı kapatmaz — saatin yanında çalışır.   "
                 "Kısayollar için F1",
            fill=gor.karistir(P["zemin"], P["soluk"], 0.7), font=(yt, 8))

        kapat_g = o(130)
        self.dugmeler.append(
            og.Dugme(self.t, G - ke - kapat_g, o(850), kapat_g, o(30), "Programı kapat",
                     self.cik, P["zemin"], gor.karistir(P["zemin"], P["kart2"], 0.7),
                     P["soluk"], yt))

        # Şeridin metnini HEMEN doldur. Eskiden yalnızca pencereyi_goster()
        # dolduruyordu; program ilk açılışta pencereyi doğrudan gösterdiği
        # için şerit boş bir kutu olarak görünüyordu. Tema değişiminde panel
        # baştan çizildiği için de buraya konması gerekiyor.
        self._arka_seridi_tazele()
        self._kisayollari_kur()

        # ---------- YERLEŞİM KAYDI ----------
        # Panelin satırları burada tek listede duruyor. sinama_yerlesim.py
        # bu listeyi okuyup İKİ ŞEYİ denetliyor:
        #   1) hiçbir kutu bir başkasının üstüne binmiyor,
        #   2) hiçbir kutu pencerenin dışına taşmıyor.
        #
        # NEDEN VAR: "arka planda çalışıyorum" şeridi sonradan eklenmiş
        # ama kendine yer açılmamıştı; doğrudan sayaç kartının içine
        # düşüyordu. Öneri şeridi de kapat düğmesinin üstüne biniyordu.
        # İkisi de gözle fark edilene kadar sürdü.
        #
        # PANELE YENİ SATIR EKLERSEN BURAYA DA EKLE.
        self.yerlesim_kutulari = [
            ("arka plan şeridi",  ke,                o(78),
                                  G - ke,            o(140)),
            ("sayaç kartı",       ke,                o(148),
                                  G - ke,            o(422)),
            ("ana düğmeler",      ke,                dy,
                                  G - ke,            dy + dyu),
            ("bugün kutucukları", ke,                ky,
                                  G - ke,            ky + kyu),
            ("grafik kartı",      ke,                self.grafik_ust,
                                  G - ke,            self.grafik_alt),
            ("öneri şeridi",      ke,                self.oneri_ust,
                                  G - ke,            self.oneri_ust + o(42)),
            ("kapat düğmesi",     G - ke - kapat_g,  o(850),
                                  G - ke,            o(880)),
        ]

    # ---------------- İzin ----------------
    def _acilis_izni_sor_gerekirse(self):
        """Windows açılışında başlamak için İZİN ister.

        Eskiden bu ayrı bir .bat ile, kullanıcıya hiç sorulmadan
        yapılıyordu. Kendi başına başlayan bir program, kullanıcının
        haberi olmadan başlamamalı.
        """
        if self.ayar.get("acilis_izni") is not None:
            return
        # Zaten kuruluysa sorma; sorup cevap alamazsak var olanı bozarız
        if kl.acilista_baslar_mi():
            self.ayar["acilis_izni"] = True
            ayarlari_yaz(self.ayar)
            return

        def sor():
            gecen = kl.acilistan_beri_saniye()
            ek = ""
            if gecen > 600:
                ek = ("\n\nBu arada: bilgisayarın %s açık ama ben yeni başladım. "
                      "O süre sayılmadı — kapalıyken hiçbir şey ölçemem, "
                      "açılışta başlamamın sebebi bu."
                      % sure_okunakli(gecen))

            cevap = Soru(
                self.kok, "Bilgisayar açılınca başlayayım mı?",
                "Molaların düzenli gelmesi için programın açık olması gerekiyor. "
                "İzin verirsen Windows her açıldığında arka planda kendim başlarım "
                "— pencere açılmaz, sadece saatin yanında simge durur." + ek +
                "\n\nHayır dersen molalar yalnızca programı elle açtığında çalışır. "
                "Bu ayarı istediğin an değiştirebilirsin.",
                evet_yazi="İzin veriyorum", hayir_yazi="Hayır, elle açarım",
                geri_sayim=90, varsayilan=False)
            izin = bool(cevap.bekle())
            self.ayar["acilis_izni"] = izin
            # Sadece EVET denince kur. Hayır/cevapsızda hiçbir şey silme —
            # daha önce kurulmuş bir ayarı bozmamalıyız.
            if izin:
                kl.acilista_baslat(True)
            ayarlari_yaz(self.ayar)

        self.kok.after(2600, sor)      # analiz izninden sonra sorsun

    def _analiz_izni_sor_gerekirse(self):
        if self.ayar.get("analiz_izni") is not None:
            return

        def sor():
            cevap = Soru(
                self.kok, "Kullanımını analiz edeyim mi?",
                "İzin verirsen hangi programda ne kadar vakit geçirdiğini sayar ve "
                "sana günlük özet çıkarırım.\n\n"
                "• Sadece program adı ve süre tutulur (örn. \"chrome.exe — 42 dk\").\n"
                "• Pencere başlıkları, yazdıkların, gezdiğin siteler KAYDEDİLMEZ.\n"
                "• Her şey bu bilgisayarda kalır, hiçbir yere gönderilmez.\n"
                "• Ayarlardan istediğin an kapatabilirsin.\n\n"
                "Hayır dersen molalar aynen çalışır, sadece özet çıkmaz.",
                evet_yazi="İzin veriyorum", hayir_yazi="Hayır, sayma",
                geri_sayim=90, varsayilan=False)
            self.ayar["analiz_izni"] = bool(cevap.bekle())
            ayarlari_yaz(self.ayar)

        self.kok.after(1500, sor)

    # ---------------- Kontrol ----------------
    def gizle(self):
        """Tepsi simgesi varsa pencereyi tamamen gizle (görev çubuğundan da).
        Yoksa simge durumuna küçült — yoksa kullanıcı programa ulaşamaz."""
        if self.tepsi and self.tepsi.acik:
            self.kok.withdraw()
        else:
            self.kok.iconify()

    def _arka_seridi_tazele(self):
        """Pencere açıldığında "arka planda ne kadar süredir ölçüyorum"
        bilgisini yaz. Kullanıcı programın çalıştığını başka türlü
        göremiyor; Windows tepsi simgesini saklıyor."""
        try:
            self.t.itemconfigure(
                self.arka_serit,
                text="Arka planda çalışıyorum — bugün %s ölçtüm"
                     % sure_okunakli(self.ist.get("ekran_sn", 0)))
            if self.tepsi_gizli_mi():
                alt = ("Simge Windows tarafından gizleniyor. Saatin yanındaki "
                       "^ okuna tıklayıp simgeyi aşağı sürüklersen hep görünür.")
            else:
                acik = time.time() - getattr(self, "baslangic_ani", time.time())
                alt = ("%s önce açıldım · pencereyi kapatsan da saymaya "
                       "devam ediyorum" % sure_okunakli(acik))
            self.t.itemconfigure(self.arka_serit_alt, text=alt)
        except Exception:
            pass

    def tepsi_gizli_mi(self):
        """Windows tepsi simgesini gizliyor mu?

        Windows 11 yeni simgeleri varsayılan olarak taşma okunun altına
        koyuyor; IsPromoted=1 olmadıkça görünmüyorlar.
        """
        try:
            import winreg
            yol = "Control Panel" + chr(92) + "NotifyIconSettings"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, yol) as k:
                for i in range(winreg.QueryInfoKey(k)[0]):
                    with winreg.OpenKey(k, winreg.EnumKey(k, i)) as alt:
                        try:
                            p = winreg.QueryValueEx(alt, "ExecutablePath")[0]
                        except FileNotFoundError:
                            continue
                        if "Goz Molasi" not in p:
                            continue
                        try:
                            return winreg.QueryValueEx(alt, "IsPromoted")[0] != 1
                        except FileNotFoundError:
                            return True          # ayarlanmamis = gizli
        except Exception:
            pass
        return False

    def pencereyi_goster(self):
        self._arka_seridi_tazele()
        try:
            self.kok.deiconify()
            self.kok.state("normal")
            self.kok.lift()
            self.kok.focus_force()
        except Exception:
            pass

    def duraklatildi_mi(self):
        return time.time() < getattr(self, "duraklama_bitis", 0)

    def duraklat(self, dakika):
        """Belirli bir süre mola verme (film, sunum, toplantı).
        Şifre sorulmaz: şifre yalnızca kapatırken sorulur."""
        self.duraklama_bitis = time.time() + dakika * 60
        self.durum = "duraklatildi"
        if self.balon:
            self.balon.kapat()
            self.balon = None
        if self.tepsi:
            self.tepsi.menuyu_tazele()

    def devam_et(self):
        self.duraklama_bitis = 0
        self.durum = "calisiyor"
        self.hedef = time.time() + self.ayar["calisma_dk"] * 60
        self._sayaci_kaydet()
        if self.tepsi:
            self.tepsi.menuyu_tazele()

    def acik_kip(self):
        """Şu anki ayarlar hangi kipe uyuyor? Hiçbirine uymuyorsa None —
        kullanıcı elle ayar yaptıysa kip seçili görünmemeli."""
        for anahtar, _ad, ayar in KIPLER:
            if all(self.ayar.get(k) == v for k, v in ayar.items()):
                return anahtar
        return None

    def kipe_gec(self, anahtar):
        """Kipi uygula ve sayacı yeni süreyle baştan başlat."""
        for a, ad, ayar in KIPLER:
            if a != anahtar:
                continue
            self.ayar.update(ayar)
            ayarlari_yaz(self.ayar)
            if self.balon:
                self.balon.kapat()
                self.balon = None
            self.durum = "calisiyor"
            self.hedef = time.time() + self.ayar["calisma_dk"] * 60
            self._sayaci_kaydet()
            if self.tepsi:
                self.tepsi.ipucu_yaz("Göz Molası — %s kipi" % ad)
                self.tepsi.menuyu_tazele()
            self._panel_yenile()
            return

    def sonraki_kart(self):
        """Mola ekranında gösterilecek sıradaki kart.

        Eskiden random.choice(BILGILER) ile seçiliyordu; aynı bilgi üst
        üste iki molada çıkabiliyordu. Artık sıra dönüyor ve TÜRÜ de
        değişiyor: neden → ipucu → neden → durumun → ...

          neden  : göz sağlığı bilgisi, kaynaklı
          ipucu  : molada YAPILACAK şey
          durumun: kişinin kendi geçmişi

        Sürekli aynı türde kart okumak sıkıcı; ayrıca "neden" bilmek
        yetmiyor, "ne yapacağını" da söylemek gerekiyor.
        """
        # Sekizli dizi. "durumun" kartı dört molada bir gelince fazla
        # sık tekrarlıyordu; "dunya" ise sonradan eklendi.
        #
        # NEDEN "dunya" VAR: bütün kartlar göz sağlığı üzerineydi ve
        # hepsi aynı yöne bakıyordu — "ekran gözünü yoruyor". Günde
        # 20-30 mola veren biri için bu tekrara düşüyor ve kart
        # okunmamaya başlıyor. Dünyadan genel kültür kartları araya
        # girince mola birkaç saniyeliğine merak edilecek bir şeye
        # dönüşüyor. Göz bilgisi hâlâ BASKIN: sekizin üçü "neden".
        SIRA = ("neden", "ipucu", "neden", "dunya",
                "neden", "durumun", "ipucu", "dunya")
        for _ in range(len(SIRA)):
            tur = SIRA[self.kart_sirasi % len(SIRA)]
            self.kart_sirasi += 1
            if tur == "neden" and BILGILER:
                k = BILGILER[self.bilgi_no % len(BILGILER)]
                self.bilgi_no += 1
                return k
            if tur == "ipucu" and IPUCLARI:
                k = IPUCLARI[self.ipucu_no % len(IPUCLARI)]
                self.ipucu_no += 1
                return k
            if tur == "dunya" and DUNYA:
                k = DUNYA[self.dunya_no % len(DUNYA)]
                self.dunya_no += 1
                return k
            if tur == "durumun":
                k = self._durum_karti()
                if k:
                    return k
        return BILGILER[0]

    def _durum_karti(self):
        """Kişinin kendi geçmişi. Hiç mola yoksa gösterilmez —
        "bugün 0 mola" demek moral bozar."""
        bugun = int(self.ist.get("tamamlanan", 0))
        try:
            gunler = gcm.son_gunler(KAYIT_KLASOR, 7, self.ist)
            hafta = sum(sayi for _, sayi, _ in gunler)
            seri = gcm.seri(KAYIT_KLASOR, self.ist)
        except Exception:
            hafta, seri = bugun, 0
        if bugun == 0 and hafta == 0:
            return None

        parca = ["Bugün %d mola tamamladın." % bugun]
        if hafta > bugun:
            parca.append("Son yedi günde toplam %d mola." % hafta)
        if seri >= 2:
            parca.append("%d gündür üst üste günlük hedefi tutturuyorsun." % seri)
        dk = round(hafta * self.ayar["mola_sn"] / 60.0)
        if dk >= 1:
            parca.append("Bu, yaklaşık %d dakikalık toplam göz dinlenmesi demek." % dk)
        return ("Senin durumun", " ".join(parca),
                "Kendi geçmişin · yalnızca bu cihazda saklanır")

    def sadece_olc_degistir(self):
        """Sessiz ölçüm modunu aç/kapat.

        Açıkken: program çalışmaya ve ölçmeye devam eder (ekran süresi,
        kesintisiz süre, hangi programda ne kadar durulduğu) ama mola
        vermez, uyarı balonu çıkarmaz, ekranı kaplamaz.
        Kapanınca sayaç sıfırdan başlar — mod kapanır kapanmaz mola
        gelmesi kimseyi memnun etmez."""
        yeni = not self.ayar.get("sadece_olc")
        self.ayar["sadece_olc"] = yeni
        ayarlari_yaz(self.ayar)
        if self.balon:
            self.balon.kapat()
            self.balon = None
        self.durum = "olcuyor" if yeni else "calisiyor"
        self.hedef = time.time() + self.ayar["calisma_dk"] * 60
        self._sayaci_kaydet()
        if self.tepsi:
            self.tepsi.menuyu_tazele()

    def hemen_mola(self):
        self.uzun_mola_mi = False
        self._molayi_baslat(self.ayar["mola_sn"])

    # ---------------- Köprü (tarayıcı sürümüyle bağlantı) ----------------
    def _kopruyu_kur(self):
        """Tarayıcı sürümünün sayacı okuyabileceği yerel ucu açar.

        NEDEN: İki sürüm iki ayrı yere yazıyor — Windows dosyaya,
        tarayıcı kendi deposuna. Biri 8 dakikadayken öbürü 20:00
        gösteriyordu. Tarayıcı bilgisayardaki dosyayı okuyamaz
        (güvenlik duvarı, izinle aşılmaz), o yüzden BİZ anlatıyoruz.

        Açılmazsa uygulama normal çalışır; köprü bir kolaylıktır.
        """
        self.kopru = None
        # DÜRÜSTLÜK NOTU: bu alan şu an HİÇBİR YERDE gösterilmiyor.
        # Eskiden yanındaki yorumda "Bilgiler sekmesi bunu gösteriyor"
        # yazıyordu — masaüstü sürümünde öyle bir sekme yok (sekmeler:
        # Programlar, 7 gün). Yorum yanlıştı; kaldırmak yerine gerçeği
        # yazıyoruz. Köprü açılmazsa kullanıcı bunu ancak tarayıcıda
        # eşitleme notunun ÇIKMAMASINDAN anlar. Eksik, ama artık
        # "gösteriliyor" diye yanlış bir güven vermiyor.
        self.kopru_hatasi = None
        if not self.ayar.get("kopru", True):
            return
        try:
            self.kopru = kpr.Kopru(self._kopru_verisi)
            if not self.kopru.baslat():
                self.kopru_hatasi = self.kopru.hata
                self.kopru = None
        except Exception as e:
            self.kopru_hatasi = str(e)
            self.kopru = None

    def _kopru_verisi(self):
        """Köprünün her istekte döndürdüğü anlık durum.

        Yalnızca sayaçla ilgili alanlar. Şifre, kilit özeti, program
        listesi ve ayarlar BİLEREK dışarıda — köprü sayacı anlatmak
        için var, uygulamayı dışa açmak için değil.
        """
        def tam(deger, varsayilan=0):
            # nan/inf/metin buradan geçerse JSON bozulur ya da tarayıcı
            # tarafında sessizce yanlış sayı olur. Bu sınıf hatayı
            # bu projede zaten yaşadık.
            try:
                s = float(deger)
            except (TypeError, ValueError):
                return varsayilan
            if s != s or s in (float("inf"), float("-inf")):
                return varsayilan
            return int(s)

        donmus = self.durum in ("bosta", "duraklatildi", "saat_disi")
        return {
            "kaynak": "windows",
            # Tarayici bu iki alani OKUMAK ZORUNDA. Eskiden pakete
            # konuyor ama hic okunmuyordu; butun hayalet mola hatasi
            # buradan cikti - veri gonderilmis, karar verilmemisti.
            "sayiyor": self.durum in ("calisiyor", "uyari"),
            "donmus": donmus,
            "surum": SURUM,
            "an": time.time(),
            "durum": self.durum,
            # DONMUS DURUMLAR: bosta / duraklatildi / saat_disi iken
            # `hedef` ILERLEMIYOR, yalnizca cizim `dondurulmus` ile
            # donuyor. Ham `hedef - now` yayinlamak sayiyi sifira
            # indiriyordu ve tarayici bos yere molaya giriyordu -
            # ogle molasinda ~50 sahte mola, hepsi istatistige yazili.
            # Kopru EKRANDA YAZAN sayiyi soyler.
            "kalan_sn": max(0, tam(self._kopru_kalan())),
            "calisma_dk": tam(self.ayar.get("calisma_dk"), 20),
            "mola_sn": tam(self.ayar.get("mola_sn"), 20),
            "gun": time.strftime("%Y-%m-%d"),
            "tamamlanan": tam(self.ist.get("tamamlanan")),
            "ekran_sn": tam(self.ist.get("ekran_sn")),
        }

    def _kopru_kalan(self):
        """Ekranda yazan kalan sureyi verir - koprunun tek dogru kaynagi.

        `_tik` icindeki cizim mantiginin aynisi:
          donmus durumlar   -> self.dondurulmus
          sadece_olc        -> hedef her tikte tazeleniyor, tam sure
          normal            -> hedef - simdi
        """
        if self.durum in ("bosta", "duraklatildi", "saat_disi"):
            return float(self.dondurulmus or 0)
        return self.hedef - time.time()

    def cik(self):
        if not self.izin_al("Programı kapatmak için şifreni gir."):
            return
        self._istatistik_yaz()
        self._sayaci_kaydet()
        ayarlari_yaz(self.ayar)
        # Bekçiye "bu kapanış düzgün, karışma" de
        kl.temiz_cikis_isaretle(KAYIT_KLASOR)
        if self.tepsi:
            self.tepsi.durdur()
        if getattr(self, "kopru", None):
            self.kopru.durdur()
        self.kok.destroy()

    def _bekciyi_kur(self):
        """Kilit açıksa programı izleyen ikinci bir süreç başlatır.

        Görev Yöneticisi'nden kapatılırsa bekçi programı geri açar.
        Şifreyle düzgün kapatılırsa bekçi sessizce çekilir.
        """
        if not (self.kilitli_mi() and self.ayar.get("bekci")):
            return
        # Ortam değişkeni KULLANMIYORUZ: alt süreçlere miras kalıyor ve
        # bekçinin yeniden açtığı program kendi bekçisini kuramıyordu.
        if getattr(self, "_bekci_var", False):
            return
        self._bekci_var = kl.bekci_baslat(KAYIT_KLASOR)

    # ---------------- Mola ----------------
    def _molayi_baslat(self, saniye):
        if self.mola_ekrani:
            return
        if self.balon:
            self.balon.kapat()
            self.balon = None
        self.durum = "mola"
        ses.cal("mola_basi", self.ayar.get("ses", True))
        # Egzersiz sayacı: her molada sıradaki egzersize geçilsin
        sayac = self.ist["tamamlanan"] + self.ist["uzun_mola"] + self.ist["ertelenen"]
        self.mola_ekrani = MolaEkrani(self, saniye, uzun=self.uzun_mola_mi,
                                      egzersiz_sayaci=sayac)

    def mola_bitti(self, iptal=False):
        if self.mola_ekrani:
            self.mola_ekrani.kapat()
            self.mola_ekrani = None

        if not iptal:
            ses.cal("mola_sonu", self.ayar.get("ses", True))
            if self.uzun_mola_mi:
                self.ist["uzun_mola"] += 1
                self.ist["kesintisiz_sn"] = 0.0
            else:
                self.ist["tamamlanan"] += 1
            # Mola tamamlandı: telafi zinciri sıfırlanır
            self.telafi_sayisi = 0
            self.telafi_suresi = None
        self.uzun_mola_mi = False
        self._istatistik_yaz()

        self.durum = "calisiyor"
        self.hedef = time.time() + self.ayar["calisma_dk"] * 60

        # Atlandıysa: nedenini söyle ve DAHA KISA bir molayı yakına al.
        # Yukarıdaki tam süreli hedefin üstüne yazar.
        if iptal:
            self._molayi_atladi()
        # Hedef DEĞİŞTİKTEN sonra kaydet. Önce kaydedersek diske eski
        # hedef yazılıyor ve program o anda kapatılırsa sayaç yanlış
        # (geçmiş) bir değerle geri yükleniyordu.
        self._sayaci_kaydet()

        if not iptal and self.ist["kesintisiz_sn"] >= self.ayar["uzun_mola_esigi_dk"] * 60:
            self.kok.after(400, self._uzun_mola_sor)

    # Atlanan mola kaç dakika sonra yeniden önerilsin
    TELAFI_DK = 4
    # Telafi molası bu saniyenin altına inmez — daha kısası gözün
    # odağını uzağa alması için yetmiyor
    TELAFI_ASGARI_SN = 8

    # Duvar saatinin bu kadar sapmasi "saat oynadi" sayilir. Normal bir
    # tik 0,25-1 saniye; 2 saniye pay yeterli ve NTP'nin milisaniyelik
    # duzeltmelerini yanlislikla sicrama saymiyor.
    SICRAMA_ESIGI = 2.0

    def _gunu_tazele(self):
        """Gece yarısı geçildiyse günlük sayaçları sıfırla.

        Eskiden `ist["gun"]` yalnızca açılışta belirleniyordu ve _tik
        içinde hiç denetlenmiyordu. Bilgisayarı gece yarısını geçerek
        açık bırakan biri için:
          • ekran süresi DÜNKÜ kovaya yazılmaya devam ediyordu,
          • aile kipi günlük sınırı sıfırlanmıyordu — çocuk ertesi gün
            de kilitli kalıyordu,
          • engel ekranındaki "gece yarısı sıfırlanır" yazısı yalandı.
        """
        bugun = time.strftime("%Y-%m-%d")
        if self.ist.get("gun") == bugun:
            return False
        # Biten günü kalıcı geçmişe yaz, SONRA sıfırla — sırası önemli,
        # tersi olursa o günün verisi kaybolur.
        try:
            gcm.gunu_isle(KAYIT_KLASOR, self.ist.get("gun", bugun), self.ist)
        except Exception:
            pass
        self.ist.update({
            "gun": bugun,
            "tamamlanan": 0, "ertelenen": 0, "uzun_mola": 0,
            "ekran_sn": 0.0, "kesintisiz_sn": 0.0, "programlar": {},
        })
        # Ebeveynin dünkü ek süresi yeni güne devretmez
        self.ayar["ek_sure_bitis"] = 0
        try:
            ayarlari_yaz(self.ayar)
        except Exception:
            pass
        self._istatistik_yaz()
        return True

    def _saat_sicramasini_yakala(self, simdi):
        """Duvar saati oynadıysa sayacı koru ve olayı kaydet.

        Sayaç `hedef` olarak bir duvar saati anı tutuyor. Saat geri
        alınırsa kalan süre uzuyor, ileri alınırsa mola aniden geliyor.
        Bu yalnızca kötü niyet değil: yaz/kış saati değişimi ve NTP
        eşitlemesi de aynı etkiyi yapıyor.

        Monotonik saat duvar saatinden bağımsız ilerler. İkisinin farkı
        sıçramanın miktarını veriyor; `hedef`i o kadar kaydırınca KALAN
        SÜRE değişmiyor.
        """
        mono = time.monotonic()
        onceki_duvar = getattr(self, "_son_duvar", None)
        onceki_mono = getattr(self, "_son_mono", None)
        self._son_duvar, self._son_mono = simdi, mono
        if onceki_duvar is None:
            self._en_ileri_an = max(getattr(self, "_en_ileri_an", 0), simdi)
            return 0.0

        sapma = (simdi - onceki_duvar) - (mono - onceki_mono)
        if abs(sapma) < self.SICRAMA_ESIGI:
            self._en_ileri_an = max(getattr(self, "_en_ileri_an", 0), simdi)
            return 0.0

        # Sayacı koru: kalan süre saat oyunundan etkilenmesin
        self.hedef += sapma
        if getattr(self, "duraklama_bitis", 0):
            self.duraklama_bitis += sapma
        if self.ayar.get("ek_sure_bitis"):
            self.ayar["ek_sure_bitis"] += sapma

        # Saat GERİ alındıysa bunu unutma. Aile kipinde yasak saatini
        # atlatmanın en kolay yolu bu; kanmamak için en ileri görülen
        # anı saklıyoruz.
        self._en_ileri_an = max(getattr(self, "_en_ileri_an", 0), onceki_duvar)
        if sapma < 0:
            self._saat_geri_alindi = True
        return sapma

    def saat_oynanmis_mi(self):
        """Sistem saati geriye alınmış mı? (aile kipi için)"""
        if not getattr(self, "_saat_geri_alindi", False):
            return False
        # Saat düzeltilip en ileri ana yetiştiyse affediyoruz — kullanıcı
        # yanlış saati düzeltmiş olabilir, sonsuza kadar suçlu saymayız.
        if time.time() >= getattr(self, "_en_ileri_an", 0) - 60:
            self._saat_geri_alindi = False
            return False
        return True

    # Ebeveyn arayuzden en fazla 30 dk ek sure veriyor (bkz. EngelEkrani).
    # Bu esik onun sekiz kati; asan deger elle yazilmis demektir.
    EK_SURE_AZAMI_SN = 4 * 3600

    def ek_sure_supheli_mi(self):
        """Ek sure makul bir tarihe mi kurulmus?

        Hem `engel_sebebi` hem `ayar_uyarisi` bunu ayri ayri
        CAGIRIYOR - biri otekinin yan etkisine bagli DEGIL. Onceki hali
        bayrak kullaniyordu ve arayuz uyariyi once sorarsa uyari hic
        cikmiyordu. Kendi sinamam yakaladi.
        """
        ham = self.ayar.get("ek_sure_bitis", 0) or 0
        ek = sayi_oku(ham, None)
        if ek is None:
            return False
        return (ek - time.time()) > self.EK_SURE_AZAMI_SN

    def engel_sebebi(self):
        """Şu an kullanımı engellemek gerekiyor mu?

        Döner: (tur, baslik, aciklama) ya da None.

        Sıra önemli: saat yasağı süre sınırından ÖNCE bakılıyor.
        Gece 23:00'te süre sınırı dolmuş olsa bile asıl sebep yasak;
        ebeveynin verdiği ek süre yasağı da açar, bu kasıtlı — "bu
        akşam biraz daha" diyebilmek gerekiyor.
        """
        if not aile_kipinde_mi(self.ayar):
            return None
        # Ebeveyn ek süre verdiyse hiçbir engel yok.
        # `float(...)` burada da coker: "abc" -> ValueError, [1] -> TypeError.
        # `inf` cokmez ama ek sureyi HIC bitirmez -> sinir kalici kapali.
        # Kullanici karari (27.08.2026): bozuk ayarda engelleme, uyar.
        # Yani bozuk ek sure "ek sure surüyor" sayilir (yeni engel eklemiyoruz)
        # ve `ayar_uyarisi()` bunu ekranda soyler.
        ham_ek = self.ayar.get("ek_sure_bitis", 0) or 0
        ek = sayi_oku(ham_ek, None)
        if ek is None:
            return None
        # MAKUL SINIR - bozukluk denetimi bunu yakalayamaz.
        # Olculdu (27.08.2026): `ek_sure_bitis` = simdi + 10 yil
        # yazilinca gunluk sinir KALICI olarak kalkiyordu. Deger bozuk
        # DEGIL, gayet gecerli bir sayi; o yuzden "bozuk ayar"
        # denetimlerinin hicbiri gormuyordu. Sessiz ve kalici bir
        # atlatma.
        #
        # Ebeveyn arayuzden en fazla 30 dakika veriyor. 4 saat, mesru
        # kullanimin sekiz kati - bu esigi asan bir deger elle
        # yazilmistir. Guvenmiyoruz ve sebebini soyluyoruz.
        # Yanlis tarafa dusme yonu bilincli: kurcalamaya kanmaktansa
        # ebeveynin ek suresini bir kez daha vermesi iyidir.
        if self.ek_sure_supheli_mi():
            pass                       # guvenmiyoruz: ek sure yokmus gibi
        elif time.time() < ek:
            return None

        # SAAT OYUNU — yasak saatini atlatmanın en kolay yolu sistem
        # saatini değiştirmek. Engelleyemiyoruz ama kanmıyoruz: saat
        # geri alınmışsa yasağı kaldırmıyoruz ve sebebini yazıyoruz.
        if self.saat_oynanmis_mi() and self.ayar.get("yasak_acik"):
            return ("saat", "Sistem saati değiştirilmiş",
                    "Bilgisayarın saati geri alınmış. Saat yasağı bu yüzden "
                    "kaldırılmadı. Saati doğru değere getirince engel kalkar.")

        if yasak_saatinde_mi(self.ayar):
            return ("yasak", "Şimdi bilgisayar zamanı değil",
                    "Ailen %s ile %s arasını kapalı zaman olarak ayarladı."
                    % (self.ayar.get("yasak_bas", "21:00"),
                       self.ayar.get("yasak_bit", "07:00")))

        # BOZUK AYAR KORUMAYI SESSIZCE KAPATMASIN.
        #
        # Olculdu (27.08.2026, capraz denetim):
        #   ekran_sn = nan        -> `nan >= sinir*60` HER ZAMAN False,
        #                            gunluk sinir hic devreye girmiyor.
        #                            Ebeveyn siniri acik saniyor. Sessiz.
        #   gunluk_sinir_dk bozuk -> int() COKUYOR (ValueError/OverflowError).
        #                            Cokme `engeli_uygula` icinde olunca HICBIR
        #                            engel uygulanmiyor (saat yasagi dahil) ve
        #                            hata yalnizca konsola gidiyor; arayuz
        #                            kullanicisi konsolu gormez.
        # Ikisi de ayni sonuca cikiyordu: koruma kapali, kimse haberdar degil.
        #
        # KULLANICI KARARI (27.08.2026): bozuk ayarda ENGELLEME, ama UYAR.
        # Engellemek secilmedi -- bu uygulama bir kez gercek ekrani kilitledi,
        # bozuk bir dosya yuzunden ekranin kilitlenmesi kabul edilmedi.
        # Sessiz kalmak da kabul edilmedi. Uyari: `ayar_uyarisi()`.
        # TEK cozumleyici: sayi_oku. Bu dosyaya ikinci bir tane EKLEME —
        # 04 Muhasebe'de tam boyle uc ayri cozumleyici birikmisti, ikisi bozuktu.
        sinir = sayi_oku(self.ayar.get("gunluk_sinir_dk"), 0)
        gecen = sayi_oku(self.ist.get("ekran_sn"), None)
        if sinir > 0 and gecen is not None:
            if gecen >= sinir * 60:
                return ("sinir", "Bugünlük ekran süren doldu",
                        "Günlük sınır %d dakika. Bugün %s kullandın."
                        % (sinir, sure_okunakli(gecen)))
        return None

    def ayar_uyarisi(self):
        """Koruma uygulanmiyorsa ekranda SOYLE.

        Kullanici karari (27.08.2026): bozuk/kurcalanmis ayarda
        ENGELLEME, ama UYAR. Burada hicbir engel uygulanmaz.

        METIN NEDEN KISA: bu uyari `ipucu_yazi` tuval metnini eziyor.
        Orada satir kirma yok ve metin saga yasli - uzun bir uyari
        panelin SOL kenarindan tasiyor. Olculdu: 704 px'lik bir uyari
        540 px'lik alana yaziliyordu. Kirpilan uyari, hic olmayan
        uyaridir. Ayrinti ayar ekranina ait; ebeveyn zaten orada
        duzeltecek. Burada: sorunu adlandir + nereye gidilecegini soyle.

        Sinama: sinama_yerlesim.py her uyariyi olcuyor.
        """
        # SIRALAMA ONEMLI: "aile secili ama sifre yok" durumunda
        # aile_kipinde_mi() False doner. Bu denetim asagida olsaydi hic
        # calismazdi - oysa tam da uyarilmasi gereken an burasi.
        # Olculdu: `kilit` bosaltilinca kip sessizce uygulanmiyor ama
        # ayar ekraninda hala "Aile" SECILI gorunuyor.
        kip = self.ayar.get("kip")
        kip = kip.strip().lower() if isinstance(kip, str) else kip
        if kip == "aile" and not kilit_kaydi(self.ayar):
            return "⚠ Aile kipi şifresiz — ayarlardan şifre koyun"
        if not aile_kipinde_mi(self.ayar):
            return None

        ham = self.ayar.get("gunluk_sinir_dk")
        # Bos ya da 0 sinir BOZUK DEGILDIR - o, "sinir yok" demektir.
        if ham not in (None, "", 0, "0") and sayi_oku(ham) is None:
            return "⚠ Günlük sınır okunamadı — sınır uygulanmıyor"
        if sayi_oku(ham, 0) > 0 and sayi_oku(self.ist.get("ekran_sn"), None) is None:
            return "⚠ Ekran süresi sayacı bozuk — sınır uygulanmıyor"

        # GECERLI GORUNEN AMA ANLAMSIZ DEGERLER.
        # Bozukluk denetimi bunlari yakalayamaz: hepsi gayet gecerli
        # sayilar. Bir gunde 1440 dakika var; ustu "sinir yok" demek.
        if sayi_oku(ham, 0) > 1440:
            return "⚠ Sınır bir günden uzun — ayarlardan düzeltin"
        if sayi_oku(ham, 0) < 0:
            return "⚠ Sınır negatif — ayarlardan düzeltin"
        if self.ek_sure_supheli_mi():
            return "⚠ Ek süre çok ileri bir tarihte — yok sayılıyor"
        if getattr(self, "sayac_oynanmis", False):
            return "⚠ Ekran süresi geri alınmış — son değerden devam"

        ham_ek = self.ayar.get("ek_sure_bitis", 0) or 0
        if ham_ek and sayi_oku(ham_ek, None) is None:
            return "⚠ Ek süre ayarı bozuk — sınır uygulanmıyor"
        return None

    # Klavye kısayolları. Web sürümüyle AYNI harfler — aynı uygulamanın
    # iki sürümünün farklı davranması, kullanıcıyı her geçişte yeniden
    # öğrenmeye zorluyor.
    KISAYOLLAR = (
        ("M", "Şimdi mola ver"),
        ("A", "Ayarlar"),
        ("T", "Temayı değiştir"),
        ("H", "Pencereyi gizle (program çalışmaya devam eder)"),
        ("F1", "Bu liste"),
    )

    def _kisayollari_kur(self):
        """Kısayolları ana pencereye bağlar.

        Mola ve engel ekranları ayrı pencereler ve odağı onlar alıyor;
        bu bağlamalar oralarda çalışmaz. Kasıtlı: 20 saniyelik molayı
        tek tuşla geçebilmek molayı mola olmaktan çıkarır.
        """
        def bagla(tus, islev):
            try:
                self.kok.bind(tus, lambda e: (islev(), "break")[1])
            except Exception:
                pass

        for buyuk, kucuk, islev in (
                ("<M>", "<m>", self.hemen_mola),
                ("<A>", "<a>", self.ayarlari_ac),
                ("<T>", "<t>", self._temayi_dondur),
                ("<H>", "<h>", self.gizle)):
            bagla(buyuk, islev)
            bagla(kucuk, islev)
        bagla("<F1>", self._kisayollari_goster)
        bagla("<question>", self._kisayollari_goster)

    def _temayi_dondur(self):
        """Sıradaki temaya geç. Web'deki T tuşunun karşılığı."""
        try:
            adlar = list(gor.TEMALAR.keys())
            su = self.ayar.get("tema", gor.VARSAYILAN_TEMA)
            yeni = adlar[(adlar.index(su) + 1) % len(adlar)] if su in adlar else adlar[0]
            self.ayar["tema"] = yeni
            ayarlari_yaz(self.ayar)
            gor.tema_uygula(yeni, self.ayar.get("canlilik", 1.0))
            self._panel_yenile()
        except Exception:
            pass

    def _kisayollari_goster(self):
        satirlar = SATIR_AYRAC.join(
            "  %-4s  %s" % (t, a) for t, a in self.KISAYOLLAR)
        try:
            TelafiKarti(
                self.kok, "Klavye kısayolları", satirlar, "",
                "Mola ekranındayken kısayollar çalışmaz — 20 saniye "
                "tuşla geçilebilseydi mola olmazdı.")
        except Exception:
            pass

    def engel_kalan_metni(self):
        """Engel ne zaman kalkacak? Canlı metin.

        "Ne kadar bekleyeceğim" sorusunun cevabı olmadan engel ekranı
        sadece bir duvar. Cevapla birlikte anlaşılır bir kural oluyor.
        """
        sebep = self.engel_sebebi()
        if not sebep:
            return ""
        simdi = time.localtime()
        su = simdi.tm_hour * 3600 + simdi.tm_min * 60 + simdi.tm_sec

        if sebep[0] == "yasak":
            try:
                s, d = str(self.ayar.get("yasak_bit", "07:00")).split(":")
                hedef = int(s) * 3600 + int(d) * 60
            except Exception:
                hedef = 7 * 3600
            kalan = hedef - su
            if kalan <= 0:
                kalan += 86400
            return "Saat %s'de kalkacak — %s kaldı" % (
                self.ayar.get("yasak_bit", "07:00"), sure_okunakli(kalan))

        # Sınır: gece yarısı sıfırlanıyor
        kalan = 86400 - su
        return "Sayaç gece yarısı sıfırlanır — %s kaldı" % sure_okunakli(kalan)

    def _aile_kipini_saglamlastir(self):
        """Aile kipi açıkken bekçi ZORUNLU.

        Bekçi kapalıyken çocuk programı görev yöneticisinden öldürüyor
        ve o gün bir daha açılmıyor — kural da kalkmış oluyor. Aile
        kipinde bu ayar kullanıcıya bırakılmaz.
        """
        if aile_kipinde_mi(self.ayar) and not self.ayar.get("bekci"):
            self.ayar["bekci"] = True
            ayarlari_yaz(self.ayar)
            self._bekciyi_kur()

    def engeli_uygula(self):
        self._aile_kipini_saglamlastir()
        """Engel gerekiyorsa ekranı aç, gerekmiyorsa kapat."""
        sebep = self.engel_sebebi()
        if sebep and self.engel_ekrani is None:
            # Mola ekranı açıkken engel açmıyoruz — üst üste iki tam
            # ekran, ikisi de topmost, sonsuz döngüye giriyor.
            if self.mola_ekrani:
                return
            self.engel_ekrani = EngelEkrani(self, sebep[1], sebep[2])
        elif not sebep and self.engel_ekrani is not None:
            self.engeli_kaldir()

    def engeli_kaldir(self):
        if self.engel_ekrani is not None:
            self.engel_ekrani.kapat()
            self.engel_ekrani = None

    def _molayi_atladi(self):
        """Mola atlandı.

        Eskiden burada hiçbir şey olmuyordu: mola sessizce düşüyor ve
        sayaç 20 dakika baştan başlıyordu. İki sorun vardı —
          1. Kişi NEYİ atladığını hiç öğrenmiyordu.
          2. Atlanan mola tamamen kayboluyordu; yoğun bir günde üst
             üste atlayan biri hiç mola almıyordu.

        Yeni davranış: nedenini söyleyen bir kart çıkar ve mola birkaç
        dakika sonraya, DAHA KISA olarak yeniden konur. Her üst üste
        atlamada süre yarıya iner. Neden kısalıyor: atlayan kişi
        meşgul, aynı süreyi dayatmak ikinci kez atlanmasına yol
        açıyor. Kısa mola, hiç moladan iyi.
        """
        self.ist["ertelenen"] += 1
        self.telafi_sayisi = getattr(self, "telafi_sayisi", 0) + 1

        tam = int(self.ayar["mola_sn"])
        kisa = int(round(tam / float(2 ** self.telafi_sayisi)))
        if kisa >= tam:                      # ayar zaten çok kısaysa
            kisa = tam // 2
        kisa = max(self.TELAFI_ASGARI_SN, kisa)
        self.telafi_suresi = kisa

        self.hedef = time.time() + self.TELAFI_DK * 60
        self._sayaci_kaydet()
        self._istatistik_yaz()

        # Neden önemliydi — kaynaklı bilgi, sırayla
        try:
            baslik, metin, kaynak = BILGILER[self.bilgi_no % len(BILGILER)]
            self.bilgi_no += 1
        except Exception:
            baslik = "Gözün kırpmayı unutuyor"
            metin = ("Ekrana bakarken göz kırpma sayısı dakikada 15'ten "
                     "5-7'ye düşer; kuruluk ve batma buradan gelir.")
            kaynak = "American Academy of Ophthalmology"

        plan = ("%d dakika sonra %d saniyelik kısa bir mola vereceğim."
                % (self.TELAFI_DK, kisa))
        try:
            TelafiKarti(self.kok, "Molayı atladın — " + baslik,
                        metin, kaynak, plan)
        except Exception:
            pass

    def _acilis_denetimi(self):
        """Açılışta kendini denetler ve TEK bir kartla durumu söyler.

        NEDEN TEK KART: üç ayrı bildirim üst üste çıkarsa kullanıcı
        hepsini kapatır ve hiçbirini okumaz. Sırayla en önemlisi
        gösteriliyor; diğerleri bir sonraki açılışa kalıyor.

        Sıra:
          1. Yeni sürüm — kullanıcı düzelttiğimiz hatayı görmeye
             devam ediyor olabilir, en acili bu.
          2. Açılışta başlatma kaydı silinmiş — program bir daha
             kendiliğinden açılmaz, molalar tamamen durur.
          3. Ölçülemeyen süre — bilgi amaçlı.
        """
        if getattr(self, "_acilis_karti_cikti", False):
            return
        self._acilis_karti_cikti = True

        # --- 1) Yeni sürüm var mı ---
        # Ağ işi ARKA PLANDA yapıldı (_surum_denetimini_baslat); burada
        # sadece sonucu okuyoruz. Bu yöntem tkinter'ın kuralı: ağ arka
        # planda, ekrana yazma ana thread'de.
        try:
            etiket, adres = getattr(self, "_yeni_surum", (None, None))
            if etiket:
                import webbrowser

                def indir():
                    webbrowser.open(adres)
                    # Açtıysa bir daha sorma
                    self.ayar["gormezden_gelinen_surum"] = etiket
                    ayarlari_yaz(self.ayar)

                TelafiKarti(
                    self.kok,
                    "Yeni sürüm çıktı — %s" % etiket,
                    "Şu an %s sürümünü kullanıyorsun. Yeni sürümde "
                    "düzeltmeler ve yeni özellikler var." % SURUM,
                    "github.com/meteotr06/goz-molasi",
                    "İndirme sayfasını açmak için buraya tıkla.",
                    eylem=indir)
                return
        except Exception:
            pass

        # --- 2) Açılışta başlatma kaydı duruyor mu ---
        try:
            if self.ayar.get("acilis_izni") and not kl.acilista_baslar_mi():
                # Kullanıcı izin vermişti ama kayıt kaybolmuş (Windows
                # güncellemesi, temizlik programı, başka bir kurulum).
                # İzin ZATEN VERİLMİŞ; yeniden sormuyoruz, geri koyup
                # haber veriyoruz.
                kl.acilista_baslat(True)
                TelafiKarti(
                    self.kok,
                    "Açılışta başlatma kaydı geri kondu",
                    "Windows açıldığında kendim başlamam için verdiğin izin "
                    "kaybolmuştu — büyük ihtimalle bir Windows güncellemesi "
                    "ya da temizlik programı sildi. Geri koydum.",
                    "",
                    "Bir şey yapmana gerek yok.")
                return
        except Exception:
            pass

        # --- 3) Ölçülemeyen süre ---
        try:
            olculemeyen = getattr(self, "olculemeyen_sn", 0.0)
            if olculemeyen >= 600:          # 10 dakikadan azını söylemeye değmez
                TelafiKarti(
                    self.kok,
                    "Kapalıyken %s ölçemedim" % sure_okunakli(olculemeyen),
                    "Bu süre boyunca bilgisayar açıktı ama ben kapalıydım. "
                    "Program çalışmıyorken hiçbir şey ölçemiyorum — o yüzden "
                    "bu süre bugünkü toplama girmedi.",
                    "",
                    "Hep açık kalmam için pencereyi kapatman yeterli; "
                    "kapatmak programı kapatmaz.")
        except Exception:
            pass

    def _surum_denetimini_baslat(self):
        """Sürüm denetimini arka planda yapar, sonucu ana thread'e taşır.

        İnternet yoksa ya da GitHub yavaşsa açılış beklemesin diye.
        Sonuç gelmezse 9 saniye sonra kart yine gösterilir — o zaman
        yerel denetimlerden biri çıkar."""
        import threading

        self._yeni_surum = (None, None)

        def calis():
            try:
                sonuc = gnc.denetle(self.ayar, SURUM)
            except Exception:
                sonuc = (None, None)
            self._yeni_surum = sonuc
            try:
                ayarlari_yaz(self.ayar)
            except Exception:
                pass
            # Ekrana yazma ana thread'de olmalı
            try:
                self.kok.after(0, self._acilis_denetimi)
            except Exception:
                pass

        threading.Thread(target=calis, daemon=True).start()
        # Ağ hiç cevap vermezse kart yine de çıksın
        self.kok.after(9000, self._acilis_denetimi)

    def _uzun_mola_sor(self):
        cevap = Soru(
            self.kok, "%s kesintisiz çalıştın" % sure_okunakli(self.ist["kesintisiz_sn"]),
            "Amerikan Optometri Birliği, riskin günde 2 saati aşan kesintisiz ekran "
            "kullanımında başladığını söylüyor.\n\n"
            "%d dakikalık uzun bir mola vereyim mi? Uygun değilse hayır de, "
            "20 saniyelik molalar devam eder." % self.ayar["uzun_mola_dk"],
            evet_yazi="Uzun mola ver", hayir_yazi="Şimdi olmaz",
            geri_sayim=25, varsayilan=False).bekle()
        if cevap:
            self.uzun_mola_mi = True
            self._molayi_baslat(self.ayar["uzun_mola_dk"] * 60)
        else:
            self.ist["kesintisiz_sn"] = self.ayar["uzun_mola_esigi_dk"] * 60 * 0.5

    def _mola_zamani(self):
        if self.ayar.get("tam_ekranda_sor"):
            toplantida, kim = iz.toplantida_mi()
            tam_ekran = iz.tam_ekran_mi()

            if toplantida or tam_ekran:
                if toplantida:
                    baslik = "Görüşmede gibisin"
                    metin = ("Şu anda %s açık. Toplantı ya da görüntülü görüşme "
                             "olabilir.\n\nMolayı 5 dakika erteleyeyim mi?" % kim)
                else:
                    _, program = iz.on_pencere()
                    baslik = "Tam ekran bir şey açık"
                    metin = ("Şu anda %s tam ekran çalışıyor. Sunum, video ya da "
                             "oyun olabilir.\n\nMolayı 5 dakika erteleyeyim mi?"
                             % (program or "bir program"))

                # Cevap gelmezse MOLA VERİLİR — varsayılan hep molanın lehine
                if Soru(self.kok, baslik, metin, evet_yazi="5 dk ertele",
                        hayir_yazi="Hayır, molayı ver",
                        geri_sayim=12, varsayilan=False).bekle():
                    self.ist["ertelenen"] += 1
                    self.durum = "calisiyor"
                    self.hedef = time.time() + 5 * 60
                    return

        self.uzun_mola_mi = False
        # Bir önceki mola atlandıysa bu sefer daha kısa mola veriyoruz.
        # Elle istenen mola (hemen_mola) bundan etkilenmez — orada
        # kişi molayı bilerek istiyor, kısaltmak saygısızlık olur.
        sure = getattr(self, "telafi_suresi", None) or self.ayar["mola_sn"]
        self._molayi_baslat(sure)

    # ---------------- Kalp atışı ----------------
    def _tik(self):
        simdi = time.time()

        # Saat oynadıysa sayacı koru; gece yarısı geçildiyse günü çevir.
        # İkisi de _tik'in EN BAŞINDA: aşağıdaki bütün kararlar doğru
        # zamana ve doğru güne dayansın.
        self._saat_sicramasini_yakala(simdi)
        if self._gunu_tazele():
            self.engeli_uygula()

        # Kullanıcı kısayola tekrar tıkladıysa ikinci kopya bize
        # "pencereni göster" mesajı bırakmıştır
        if kl.goster_istendi_mi(KAYIT_KLASOR):
            self.pencereyi_goster()

        # AİLE KİPİ — engel gerekiyor mu?
        # Mola durumundan ÖNCE bakılıyor: molanın bitmesini beklemek
        # yasak saatinin 20 saniye gecikmesi demek olurdu.
        if aile_kipinde_mi(self.ayar) or self.engel_ekrani is not None:
            self.engeli_uygula()
            if self.engel_ekrani is not None:
                # Engel ekranı açıkken ekran süresi SAYILMIYOR — kişi
                # zaten kullanamıyor. Saymak, ertesi günün sınırını da
                # yiyip bitirirdi.
                self.kok.after(500, self._tik)
                return

        if self.durum == "mola":
            self.kok.after(250, self._tik)
            return

        # Çalışma saatleri dışındaysak sayaç işlemez
        if not saat_uygun_mu(self.ayar):
            if self.durum != "saat_disi":
                self.durum = "saat_disi"
            self._ciz(self.ayar["calisma_dk"] * 60)
            self.kok.after(1000, self._tik)
            return
        if self.durum == "saat_disi":
            self.durum = "calisiyor"
            self.hedef = simdi + self.ayar["calisma_dk"] * 60

        # Kullanıcı elle duraklattıysa (film, sunum) sayaç işlemez
        if self.duraklatildi_mi():
            self._ciz(self.ayar["calisma_dk"] * 60)
            self.kok.after(500, self._tik)
            return
        if getattr(self, "duraklama_bitis", 0) and not self.duraklatildi_mi():
            self.devam_et()

        bosta = iz.bosta_saniye()

        if bosta > self.ayar["bosta_esigi_sn"]:
            if self.durum != "bosta":
                self.dondurulmus = self.hedef - simdi
                self.durum = "bosta"
                self.kilit_gorundu = False
            self.son_bosta = bosta
            # Ekran kilitlendiyse kişi GERÇEKTEN uzaklaşmıştır.
            # Bunu ayrıca izliyoruz çünkü "klavyeye dokunmadı" ile
            # "makineden uzaklaştı" aynı şey değil.
            if not self.kilit_gorundu and iz.ekran_kilitli_mi():
                self.kilit_gorundu = True
            self._ciz(self.dondurulmus or 0)
            self.kok.after(400, self._tik)
            return

        if self.durum == "bosta":
            # Sayacı sıfırlamak, "gözlerin dinlendi, baştan başla"
            # demektir. Bunu YALNIZCA gerçekten uzaklaşıldıysa yapmalı:
            #   • ekran kilitlendiyse — kesin kanıt, ya da
            #   • girdi eşiğin epey üstünde bir süre gelmediyse.
            # Eskiden tek ölçüt 5 dakika girdisizlikti; uzun bir metni
            # okuyan biri ekrana baktığı hâlde sayacı sıfırlanıyordu.
            # Ölçtüm: 132 dakika ekran süresine karşılık 0 mola.
            uzun_esik = max(self.ayar["dinlenme_esigi_sn"], 900)
            gercekten_uzaklasti = (self.kilit_gorundu
                                   or self.son_bosta > uzun_esik)
            if gercekten_uzaklasti:
                self.ist["kesintisiz_sn"] = 0.0
                self.hedef = simdi + self.ayar["calisma_dk"] * 60
            else:
                self.hedef = simdi + max(1, self.dondurulmus or 0)
            self.durum = "calisiyor"
            self.dondurulmus = None
            self.kilit_gorundu = False

        self.ist["ekran_sn"] += 0.25
        self.ist["kesintisiz_sn"] += 0.25

        if self.ayar.get("analiz_izni"):
            _, program = iz.on_pencere()
            if program:
                self.ist["programlar"][program] = self.ist["programlar"].get(program, 0) + 0.25

        # SESSİZ ÖLÇÜM: yukarıdaki sayaçlar işledi, aşağıdaki mola/uyarı
        # mantığı hiç çalışmıyor. Program açık kalır, ekrana bir şey
        # çıkmaz, mola verilmez — ama ölçüm sürer.
        if self.ayar.get("sadece_olc"):
            if self.balon:
                self.balon.kapat()
                self.balon = None
            self.durum = "olcuyor"
            # Sayaç ilerlemesin ki mod kapanınca aniden mola gelmesin
            self.hedef = simdi + self.ayar["calisma_dk"] * 60
            self._ciz(self.hedef - simdi)
            if int(simdi) % 30 == 0:
                self._istatistik_yaz()
                self._sayaci_kaydet()
            self.kok.after(250, self._tik)
            return

        kalan = self.hedef - simdi

        if 0 < kalan <= self.ayar["uyari_sn"]:
            mesaj = "%d saniye sonra göz molası" % (int(kalan) + 1)
            if self.durum != "uyari":
                self.durum = "uyari"
                ses.cal("uyari", self.ayar.get("ses", True))
                self.balon = Balon(self.kok, mesaj)
            elif self.balon:
                self.balon.guncelle(mesaj)
        elif self.balon and kalan > self.ayar["uyari_sn"]:
            self.balon.kapat()
            self.balon = None
            self.durum = "calisiyor"

        if kalan <= 0:
            if self.balon:
                self.balon.kapat()
                self.balon = None
            self._mola_zamani()
            self.kok.after(250, self._tik)
            return

        self._ciz(kalan)
        # Sayacı da düzenli kaydet. Eskiden yalnızca durum değişince
        # (mola bitince, duraklatınca) yazılıyordu. Program zorla
        # kapatılırsa — çökme, taskkill, elektrik — diskteki kayıt
        # eskide kalıyor, açılışta "5 dakikadan uzun kapalıydı" hesabı
        # çıkıyor ve 20 dakika BAŞTAN başlıyordu. 30 saniyede bir
        # yazmak bunu en fazla 30 saniyelik kayba indiriyor.
        if int(simdi) % 30 == 0:
            self._istatistik_yaz()
            self._sayaci_kaydet()
        self.kok.after(250, self._tik)

    # ---------------- Çizim ----------------
    def _yay_uclarini_ciz(self, oran, renk):
        """Yayın iki ucuna küçük daire koyar — böylece uçlar yuvarlak görünür.
        Tkinter'ın create_arc'ında yuvarlak uç seçeneği yok."""
        import math
        for oge in self.uc_noktalari:
            self.t.delete(oge)
        self.uc_noktalari = []
        if oran <= 0:
            return
        mx, my = self.halka_orta
        kalinlik = self.halka_kalinlik
        for aci_derece in (90, 90 - 359.9 * oran):
            a = math.radians(aci_derece)
            x = mx + self.halka_r * math.cos(a)
            y = my - self.halka_r * math.sin(a)
            self.uc_noktalari.append(self.t.create_oval(
                x - kalinlik / 2, y - kalinlik / 2, x + kalinlik / 2, y + kalinlik / 2,
                fill=renk, outline=""))

    def _ciz(self, kalan):
        if self.kok.state() == "iconic":
            return

        yt = self.yt
        toplam = self.ayar["calisma_dk"] * 60
        oran = max(0.0, min(1.0, kalan / toplam))
        renk = {"calisiyor": P["vurgu"], "uyari": P["sicak"],
                "bosta": P["soluk"]}.get(self.durum, P["vurgu"])

        self.t.itemconfigure(self.sure_yazi, text=sure_yazisi(kalan))
        self.t.itemconfigure(self.halka_yay, extent=-359.9 * oran, outline=renk)
        self._yay_uclarini_ciz(oran, renk)

        if self.durum == "saat_disi":
            self.t.itemconfigure(self.sure_yazi, text="—")
            self.t.itemconfigure(self.durum_yazi, text="Çalışma saati dışı", fill=P["soluk"])
            self.t.itemconfigure(self.halka_yay, extent=-359.9, outline=P["cizgi"])
            self._yay_uclarini_ciz(0, P["cizgi"])
            self.t.itemconfigure(self.ipucu_yazi,
                                 text="%s–%s arasında hatırlatır"
                                      % (self.ayar["bas_saat"], self.ayar["bit_saat"]))
        elif self.ayar.get("sadece_olc"):
            self.t.itemconfigure(self.sure_yazi, text="—")
            self.t.itemconfigure(self.durum_yazi, text="Sadece ölçüyor",
                                 fill=P["sicak"])
            self.t.itemconfigure(self.halka_yay, extent=-359.9, outline=P["cizgi"])
            self._yay_uclarini_ciz(0, P["cizgi"])
            self.t.itemconfigure(
                self.ipucu_yazi,
                text="Mola vermez, ekrana çıkmaz — ölçmeye devam eder")
        elif self.duraklatildi_mi():
            kalan_dk = max(1, int((self.duraklama_bitis - time.time()) / 60) + 1)
            self.t.itemconfigure(self.sure_yazi, text="—")
            self.t.itemconfigure(self.durum_yazi, text="Duraklatıldı", fill=P["sicak"])
            self.t.itemconfigure(self.halka_yay, extent=-359.9, outline=P["cizgi"])
            self._yay_uclarini_ciz(0, P["cizgi"])
            self.t.itemconfigure(self.ipucu_yazi,
                                 text="%d dakika sonra devam eder" % kalan_dk)
        else:
            adlar = {"calisiyor": "Çalışıyor", "uyari": "Mola geliyor",
                     "bosta": "Boşta — sayaç durdu"}
            self.t.itemconfigure(self.durum_yazi, text=adlar.get(self.durum, ""),
                                 fill=renk if self.durum != "calisiyor" else P["soluk"])
            self.t.itemconfigure(
                self.ipucu_yazi,
                text="Dokununca devam eder" if self.durum == "bosta"
                else "%d saniye sürecek" % self.ayar["mola_sn"])

        # Bozuk ayar uyarisi ipucu satirini EZER: sinir uygulanmadigi hâlde
        # ebeveynin "koruma acik" sanmasi, bu uygulamadaki en pahali hata.
        # Uyari yokken rengi geri almak sart, yoksa duzeltildikten sonra da
        # kirmizi kaliyor.
        uyari = self.ayar_uyarisi()
        self.t.itemconfigure(self.ipucu_yazi, fill=P["sicak"] if uyari else P["soluk"])
        if uyari:
            self.t.itemconfigure(self.ipucu_yazi, text=uyari)

        # Tepsi simgesinin üstüne gelince görünen yazı
        if self.tepsi and self.tepsi.acik and int(simdi_saniye()) % 5 == 0:
            if self.ayar.get("sadece_olc"):
                self.tepsi.ipucu_yaz("Göz Molası — sadece ölçüyor, mola vermiyor")
            elif self.duraklatildi_mi():
                self.tepsi.ipucu_yaz("Göz Molası — duraklatıldı")
            else:
                self.tepsi.ipucu_yaz("Göz Molası — sonraki mola %s"
                                     % sure_yazisi(kalan))

        # Bugünkü molalar — nokta şeridi
        dolu = self.ist["tamamlanan"] + self.ist["uzun_mola"]
        imza = min(dolu, self.nokta_adet)
        if imza != getattr(self, "nokta_imza", None):
            self.nokta_imza = imza
            self.t.delete("noktalar")
            og.nokta_seridi(self.t, self.nokta_x, self.nokta_y, self.nokta_adet, imza,
                            self.nokta_cap, self.nokta_ara, P["vurgu"],
                            gor.karistir(P["kart"], P["cizgi"], 0.9), etiket="noktalar")
            if dolu > self.nokta_adet:
                self.t.create_text(
                    self.nokta_x + self.nokta_adet * (self.nokta_cap + self.nokta_ara) + self.ol(6),
                    self.nokta_y + self.nokta_cap / 2, anchor="w", text="+%d" % (dolu - self.nokta_adet),
                    fill=P["vurgu"], font=(yt, 8, "bold"), tags="noktalar")

        self.t.itemconfigure(self.kilit_rozet,
                             text="🔒 KİLİTLİ" if self.kilitli_mi() else "")

        # Seri: her 30 saniyede bir hesapla, her çeyrek saniyede değil
        if simdi_saniye() - getattr(self, "_seri_zaman", 0) > 30:
            self._seri_zaman = simdi_saniye()
            self._seri = gcm.seri(KAYIT_KLASOR, self.ist)
        s = getattr(self, "_seri", 0)
        self.t.itemconfigure(
            self.seri_rozet,
            text=("🔥 %d gün üst üste" % s) if s > 0 else "")

        self.t.itemconfigure(self.kutu_yazilari["tamamlanan"], text=str(self.ist["tamamlanan"]))
        self.t.itemconfigure(self.kutu_yazilari["uzun_mola"], text=str(self.ist["uzun_mola"]))
        self.t.itemconfigure(self.kutu_yazilari["ekran_sn"],
                             text=sure_okunakli(self.ist["ekran_sn"]))
        self.t.itemconfigure(self.kutu_yazilari["kesintisiz_sn"],
                             text=sure_okunakli(self.ist["kesintisiz_sn"]))

        self._grafik_ciz()
        self._oneri_ciz()

    def _sekme_sec(self, anahtar):
        self.grafik_sekmesi = anahtar
        self.grafik_imza = None
        for a, d in self.sekme_dugmeleri.items():
            secili = (a == anahtar)
            d.renk = P["vurgu"] if secili else P["kart2"]
            d.uzerinde = gor.karistir(d.renk, "#ffffff", 0.14)
            d.basili = gor.karistir(d.renk, "#000000", 0.12)
            d._boya(d.renk)
            self.t.itemconfigure(d.yazi, fill=P.get("ana_yazi", "#0d2b28") if secili else P["soluk"])
        self._grafik_ciz()

    def _grafik_ciz(self):
        """Grafik yalnızca veri değiştiğinde yeniden çizilir.
        Her çeyrek saniyede baştan çizmek titremeye yol açardı."""
        if self.grafik_sekmesi == "hafta":
            self._hafta_ciz()
            return

        sirali = sorted(self.ist["programlar"].items(), key=lambda x: -x[1])[:5]
        imza = ("prog", self.ayar.get("analiz_izni"),
                tuple((a, int(s / 15)) for a, s in sirali))
        if imza == self.grafik_imza:
            return
        self.grafik_imza = imza

        self.t.delete("grafik")
        yt = self.yt
        o = self.ol
        ke = o(24)
        ic_x = ke + o(20)
        ic_y = self.grafik_ust + o(46)

        if self.ayar.get("analiz_izni") is False:
            self.t.itemconfigure(self.grafik_baslik, text="PROGRAM ANALİZİ KAPALI")
            self.t.create_text(ic_x, ic_y, anchor="nw", width=self.G - 2 * ic_x,
                               tags="grafik",
                               text="Hangi programda ne kadar vakit geçirdiğini görmek "
                                    "istersen Ayarlar'dan açabilirsin.\n"
                                    "Sadece program adı ve süre tutulur; pencere "
                                    "başlıkları asla kaydedilmez.",
                               fill=P["soluk"], font=(yt, 9))
            return

        olculen = sum(self.ist["programlar"].values())
        if olculen:
            self.t.itemconfigure(
                self.grafik_baslik,
                text="EN ÇOK KULLANDIKLARIN   ·   TOPLAM %s ÖLÇÜLDÜ"
                     % sure_okunakli(olculen).upper())
        else:
            self.t.itemconfigure(self.grafik_baslik, text="EN ÇOK KULLANDIKLARIN")
        if not sirali:
            self.t.create_text(ic_x, ic_y, anchor="nw", tags="grafik",
                               text="Henüz veri yok — birkaç dakika sonra dolacak.",
                               fill=P["soluk"], font=(yt, 9))
            return

        enb = max(s for _, s in sirali) or 1
        etiket_g = o(116)
        cubuk_g = self.G - ic_x - etiket_g - o(24) - o(20) - o(56)
        yuk, bosluk = o(14), o(9)

        for i, (ad, sn) in enumerate(sirali):
            y = ic_y + i * (yuk + bosluk)
            insanca = program_adi(ad)
            kisa = insanca if len(insanca) <= 16 else insanca[:15] + "…"
            self.t.create_text(ic_x, y + yuk / 2, anchor="w", text=kisa,
                               fill=P["yazi"], font=(yt, 9), tags="grafik")
            og.cubuk(self.t, ic_x + etiket_g, y, cubuk_g, yuk, sn / enb,
                     P["kart2"], gor.GRAFIK_RENKLERI[i % len(gor.GRAFIK_RENKLERI)],
                     etiket="grafik")
            yuzde = round(100.0 * sn / olculen) if olculen else 0
            self.t.create_text(ic_x + etiket_g + cubuk_g + o(10), y + yuk / 2, anchor="w",
                               text="%s  ·  %%%d" % (sure_okunakli(sn), yuzde),
                               fill=P["soluk"], font=(yt, 9), tags="grafik")
        # Çubuklar kartın üstüne çizildi; etiketleri öne al
        for oge in self.t.find_withtag("grafik"):
            self.t.tag_raise(oge)

    def _hafta_ciz(self):
        """Son 7 günün mola sayısı — dikey çubuklar."""
        gunler = gcm.son_gunler(KAYIT_KLASOR, 7, self.ist)
        imza = ("hafta", tuple(s for _, s, _ in gunler))
        if imza == self.grafik_imza:
            return
        self.grafik_imza = imza

        self.t.delete("grafik")
        o, yt, ke = self.ol, self.yt, self.ol(24)

        toplam = sum(sayi for _, sayi, _ in gunler)
        if toplam:
            ortalama = round(toplam / 7.0, 1)
            self.t.itemconfigure(
                self.grafik_baslik,
                text="SON 7 GÜN   ·   %d MOLA, GÜNDE ORTALAMA %s"
                     % (toplam, str(ortalama).replace(".", ",")))
        else:
            self.t.itemconfigure(self.grafik_baslik, text="SON 7 GÜN")

        ic_x = ke + o(20)
        taban = self.grafik_alt - o(30)
        tepe = self.grafik_ust + o(48)
        yukseklik = taban - tepe
        alan = self.G - 2 * ic_x
        cubuk_g = alan / 7 * 0.52
        ara = alan / 7

        # Hiç mola yokken yedi tane sıfır çubuğu ve yedi tane "0" yazısı
        # bozuk duruyor — yeni kullanıcının gördüğü ilk şey bu.
        if not toplam:
            self.t.create_text(
                self.G / 2, (taban + tepe) / 2,
                text=SATIR_AYRAC.join(["Henüz mola yok.",
                                      "İlk molanı tamamladığında buraya",
                                      "günlük çubuğun düşecek."]),
                fill=P["soluk"], font=(yt, 9), justify="center", tags="grafik")
            for oge in self.t.find_withtag("grafik"):
                self.t.tag_raise(oge)
            return

        enb = max([s for _, s, _ in gunler] + [gcm.GUNLUK_HEDEF])

        # Hedef çizgisi
        hy = taban - yukseklik * (gcm.GUNLUK_HEDEF / enb)
        for x in range(int(ic_x), int(ic_x + alan), o(7)):
            self.t.create_line(x, hy, x + o(3), hy,
                               fill=gor.karistir(P["kart"], P["soluk"], 0.6),
                               tags="grafik")
        self.t.create_text(ic_x, hy - o(9), anchor="w",
                           text="günlük hedef: %d mola" % gcm.GUNLUK_HEDEF,
                           fill=gor.karistir(P["kart"], P["soluk"], 0.8),
                           font=(yt, 7), tags="grafik")

        for i, (ad, sayi, bugun_mu) in enumerate(gunler):
            x = ic_x + i * ara + (ara - cubuk_g) / 2
            y = taban - (yukseklik * (sayi / enb) if enb else 0)
            renk = P["vurgu"] if sayi >= gcm.GUNLUK_HEDEF else P["kart2"]
            if bugun_mu and sayi < gcm.GUNLUK_HEDEF:
                renk = P["sicak"]
            og.dikey_cubuk(self.t, x, taban, cubuk_g, taban - y, renk,
                           r=o(5), etiket="grafik")
            if sayi:                       # sıfır günde "0" yazmak gürültü
                self.t.create_text(x + cubuk_g / 2, y - o(9), text=str(sayi),
                                   fill=P["vurgu"] if sayi >= gcm.GUNLUK_HEDEF
                                        else P["yazi"],
                                   font=(yt, 8, "bold"), tags="grafik")
            self.t.create_text(x + cubuk_g / 2, taban + o(12),
                               text="Bugün" if bugun_mu else ad,
                               fill=P["yazi"] if bugun_mu else P["soluk"],
                               font=(yt, 8, "bold" if bugun_mu else "normal"),
                               tags="grafik")

    def _oneri_ciz(self):
        kesintisiz = self.ist["kesintisiz_sn"]
        esik = self.ayar["uzun_mola_esigi_dk"] * 60
        if kesintisiz >= esik:
            metin = ("⚠  %s kesintisiz çalışıyorsun. Bir sonraki moladan sonra "
                     "uzun mola önereceğim." % sure_okunakli(kesintisiz))
            vurgu = P["uyari"]
        elif kesintisiz >= esik * 0.75:
            metin = "%s kesintisiz. 2 saate yaklaşıyorsun." % sure_okunakli(kesintisiz)
            vurgu = P["sicak"]
        else:
            metin = ""
            vurgu = None

        if metin == self.oneri_imza:
            return
        self.oneri_imza = metin
        self.t.delete("oneri")
        if not metin:
            return

        o = self.ol
        ke = o(24)
        og.kart(self.t, ke, self.oneri_ust, self.G - ke, self.oneri_ust + o(42),
                P["zemin"], gor.karistir(P["kart"], vurgu, 0.13), r=o(14), golge=2,
                etiket="oneri")
        self.t.create_text(ke + o(16), self.oneri_ust + o(21), anchor="w", text=metin,
                           fill=P["yazi"], font=(self.yt, 9), tags="oneri",
                           width=self.G - 2 * ke - o(32))

    # ---------------- Ayarlar penceresi ----------------
    def ayarlari_ac(self):
        # AİLE KİPİ: ayarlar ebeveyn şifresiyle korunuyor. Bu olmadan
        # kip anlamsız — çocuk ayarlara girip kipi kapatırdı.
        if aile_kipinde_mi(self.ayar):
            if not self.izin_al("Aile kipi açık. Ayarlar için ebeveyn şifresi."):
                return
        return self._ayarlari_ac()

    def _ayarlari_ac(self):
        # Şifre sorulmaz. Kilidin tek görevi programın kapatılmasını
        # engellemek; "şifreyi kaldır" zaten ayrıca şifre ister.

        pencere = tk.Toplevel(self.kok)
        pencere.title("Ayarlar")
        pencere.configure(bg=P["kart"])
        pencere.attributes("-topmost", True)

        # ---------------------------------------------------------------
        # KAYDIRILABİLİR GÖVDE
        # Ayarlar büyüdükçe pencere 1490 piksele çıktı, ekran ise 1200.
        # Kaydet düğmesi ekranın altında kalıyor ve tıklanamıyordu:
        # kullanıcı değeri değiştiriyor ama kaydedemiyordu.
        # Çözüm: içerik kayar, düğmeler altta SABİT durur.
        # ---------------------------------------------------------------
        alt_cerceve = tk.Frame(pencere, bg=P["kart"])
        alt_cerceve.pack(side="bottom", fill="x")

        dis = tk.Frame(pencere, bg=P["kart"])
        dis.pack(side="top", fill="both", expand=True)

        tuval = tk.Canvas(dis, bg=P["kart"], highlightthickness=0, bd=0)
        cubuk = tk.Scrollbar(dis, orient="vertical", command=tuval.yview)
        tuval.configure(yscrollcommand=cubuk.set)
        cubuk.pack(side="right", fill="y")
        tuval.pack(side="left", fill="both", expand=True)

        p = tk.Frame(tuval, bg=P["kart"])          # içerik buraya paketlenir
        ic_pencere = tuval.create_window((0, 0), window=p, anchor="nw")

        def _govde_olcu(_=None):
            tuval.configure(scrollregion=tuval.bbox("all"))
            tuval.itemconfigure(ic_pencere, width=tuval.winfo_width())
        p.bind("<Configure>", _govde_olcu)
        tuval.bind("<Configure>", _govde_olcu)

        def _tekerlek(olay):
            tuval.yview_scroll(int(-olay.delta / 120), "units")
        pencere.bind_all("<MouseWheel>", _tekerlek)
        pencere.bind("<Destroy>", lambda e: pencere.unbind_all("<MouseWheel>"))

        tk.Label(p, text="Ayarlar", font=("Segoe UI", 15, "bold"),
                 fg=P["yazi"], bg=P["kart"]).pack(padx=26, pady=(20, 10), anchor="w")

        # ---------- Tema seçimi ----------
        tk.Label(p, text="Renk teması", font=("Segoe UI", 10), fg=P["yazi"],
                 bg=P["kart"]).pack(padx=26, anchor="w")
        tk.Label(p, text="Seçince hemen uygulanır", font=("Segoe UI", 8),
                 fg=P["soluk"], bg=P["kart"]).pack(padx=26, anchor="w")

        # Tema sayısı arttı; tek sıraya sığmıyor, satırlara bölüyoruz
        SUTUN = 5
        satir_sayisi = (len(gor.tema_listesi()) + SUTUN - 1) // SUTUN
        tema_seridi = tk.Canvas(p, height=56 * satir_sayisi, bg=P["kart"],
                                highlightthickness=0)
        tema_seridi.pack(fill="x", padx=26, pady=(8, 4))

        def temayi_sec(ad):
            pencere.destroy()
            self.temayi_degistir(ad)
            self.kok.after(60, self.ayarlari_ac)   # yeni renklerle tekrar aç

        for i, (anahtar, gorunen_ad) in enumerate(gor.tema_listesi()):
            t = gor.TEMALAR[anahtar]
            x = 6 + (i % SUTUN) * 60
            y = 2 + (i // SUTUN) * 56
            secili = (anahtar == self.ayar.get("tema"))
            etiket = "tema_%s" % anahtar
            if secili:
                tema_seridi.create_oval(x - 4, y, x + 44, y + 48,
                                        outline=t["panel"]["vurgu"], width=2)
            # Temanın üç ana rengini gösteren küçük daire
            tema_seridi.create_oval(x, y + 4, x + 40, y + 44, fill=t["panel"]["zemin"],
                                    outline=t["panel"]["cizgi"], tags=etiket)
            tema_seridi.create_oval(x + 8, y + 12, x + 24, y + 28, fill=t["panel"]["vurgu"],
                                    outline="", tags=etiket)
            tema_seridi.create_oval(x + 20, y + 22, x + 32, y + 34, fill=t["panel"]["sicak"],
                                    outline="", tags=etiket)
            tema_seridi.tag_bind(etiket, "<Button-1>",
                                 lambda e, a=anahtar: temayi_sec(a))
            tema_seridi.tag_bind(etiket, "<Enter>",
                                 lambda e: tema_seridi.configure(cursor="hand2"))
            tema_seridi.tag_bind(etiket, "<Leave>",
                                 lambda e: tema_seridi.configure(cursor=""))

        tk.Label(p, text=gor.TEMALAR[self.ayar.get("tema", "gece")]["ad"],
                 font=("Segoe UI", 9, "bold"), fg=P["vurgu"],
                 bg=P["kart"]).pack(padx=26, anchor="w", pady=(0, 6))

        # ---------- Canlılık ----------
        # Renklerin doygunluğu. OKLab'da yalnızca doygunluk değişiyor,
        # algılanan açıklık sabit kalıyor — yani yazı okunaklılığı hiç
        # etkilenmiyor. Web sürümündeki kaydırıcının aynısı.
        canli_satir = tk.Frame(p, bg=P["kart"])
        canli_satir.pack(fill="x", padx=26, pady=(2, 2))
        tk.Label(canli_satir, text="Canlılık", font=("Segoe UI", 9, "bold"),
                 fg=P["yazi"], bg=P["kart"]).pack(side="left")
        canli_yazi = tk.Label(canli_satir, text="", font=("Segoe UI", 8),
                              fg=P["soluk"], bg=P["kart"])
        canli_yazi.pack(side="right")

        def canli_ad(v):
            return "Sakin" if v <= 0.75 else ("Canlı" if v >= 1.3 else "Dengeli")

        def canli_degisti(deger):
            v = round(float(deger), 2)
            canli_yazi.configure(text="%s  ·  %%%d" % (canli_ad(v), round(v * 100)))

        canli_kaydirici = tk.Scale(
            p, from_=0.6, to=1.5, resolution=0.05, orient="horizontal",
            showvalue=False, command=canli_degisti,
            bg=P["kart"], fg=P["yazi"], troughcolor=P["zemin2"],
            activebackground=P["vurgu"], highlightthickness=0, bd=0,
            sliderrelief="flat", length=10)
        canli_kaydirici.set(float(self.ayar.get("canlilik", 1.0)))
        canli_degisti(canli_kaydirici.get())
        canli_kaydirici.pack(fill="x", padx=26, pady=(0, 2))

        tk.Label(p, text="Renklerin doygunluğu. Yazı okunaklılığı değişmez.",
                 font=("Segoe UI", 8), fg=P["soluk"], bg=P["kart"]).pack(
            padx=26, anchor="w", pady=(0, 4))

        def canliligi_uygula():
            pencere.destroy()
            self.canliligi_degistir(canli_kaydirici.get())
            self.kok.after(60, self.ayarlari_ac)   # yeni renklerle tekrar aç

        dugme(p, "Canlılığı uygula", canliligi_uygula, kucuk=True).pack(
            padx=26, anchor="w", pady=(0, 8))

        tk.Frame(p, bg=P["cizgi"], height=1).pack(fill="x", padx=26, pady=(4, 10))

        alanlar = {}

        # ---------- Hazır süreler ----------
        # Sayı kutusuna elle yazmak yerine tek tıkla seçim.
        SURELER = [
            (20, 20, "20 dk · 20 sn", "Klasik 20-20-20 kuralı"),
            (10, 20, "10 dk · 20 sn", "2023 çalışması bunu öneriyor"),
            (30, 30, "30 dk · 30 sn", "Daha seyrek, daha uzun"),
            (45, 60, "45 dk · 1 dk", "Odak bloğu sevenler için"),
        ]
        tk.Label(p, text="Hazır süreler", font=("Segoe UI", 10), fg=P["yazi"],
                 bg=P["kart"]).pack(padx=26, anchor="w")
        tk.Label(p, text="Kendine uyanı seç, istersen aşağıdan elle değiştir",
                 font=("Segoe UI", 8), fg=P["soluk"], bg=P["kart"]).pack(padx=26, anchor="w")

        izgara = tk.Frame(p, bg=P["kart"])
        izgara.pack(fill="x", padx=26, pady=(8, 6))
        sure_dugmeleri = []

        def sure_uygula(dk, sn):
            alanlar["calisma_dk"].delete(0, "end"); alanlar["calisma_dk"].insert(0, dk)
            alanlar["mola_sn"].delete(0, "end"); alanlar["mola_sn"].insert(0, sn)
            alanlar["uyari_sn"].delete(0, "end")
            alanlar["uyari_sn"].insert(0, max(5, min(15, int(dk * 60 * 0.02))))
            sureleri_tazele()

        def sureleri_tazele():
            try:
                dk = int(float(alanlar["calisma_dk"].get()))
                sn = int(float(alanlar["mola_sn"].get()))
            except (ValueError, KeyError):
                return
            for d, (sdk, ssn, _, _) in zip(sure_dugmeleri, SURELER):
                secili = (sdk == dk and ssn == sn)
                d.configure(bg=gor.karistir(P["kart2"], P["vurgu"], 0.28) if secili
                            else P["kart2"],
                            fg=P["yazi"])

        for i, (dk, sn, ad, notu) in enumerate(SURELER):
            d = tk.Button(izgara, text="%s\n%s" % (ad, notu), justify="left",
                          font=("Segoe UI", 9), bg=P["kart2"], fg=P["yazi"],
                          activebackground=gor.karistir(P["kart2"], "#ffffff", 0.12),
                          relief="flat", bd=0, padx=10, pady=8, cursor="hand2",
                          anchor="w", width=22,
                          command=(lambda a=dk, b=sn: sure_uygula(a, b)))
            d.grid(row=i // 2, column=i % 2, sticky="ew", padx=3, pady=3)
            sure_dugmeleri.append(d)
        izgara.columnconfigure(0, weight=1)
        izgara.columnconfigure(1, weight=1)

        def satir(etiket, aciklama, anahtar):
            f = tk.Frame(p, bg=P["kart"])
            f.pack(fill="x", padx=26, pady=5)
            sol = tk.Frame(f, bg=P["kart"])
            sol.pack(side="left", fill="x", expand=True)
            tk.Label(sol, text=etiket, font=("Segoe UI", 10), fg=P["yazi"],
                     bg=P["kart"]).pack(anchor="w")
            tk.Label(sol, text=aciklama, font=("Segoe UI", 8), fg=P["soluk"],
                     bg=P["kart"]).pack(anchor="w")
            e = tk.Entry(f, width=6, font=("Segoe UI", 11), justify="center",
                         bg=P["zemin"], fg=P["yazi"], insertbackground=P["yazi"],
                         relief="flat")
            e.insert(0, str(self.ayar[anahtar]))
            e.pack(side="right", ipady=5, padx=(10, 0))
            e.bind("<KeyRelease>", lambda ev: sureleri_tazele())
            alanlar[anahtar] = e

        satir("Çalışma süresi", "Kaç dakikada bir mola verilsin", "calisma_dk")
        satir("Mola süresi", "Saniye cinsinden", "mola_sn")
        satir("Ön uyarı", "Molaya kaç saniye kala haber verilsin", "uyari_sn")
        sureleri_tazele()          # açılışta hangi hazır süre seçili göster
        satir("Uzun mola eşiği", "Kaç dakika kesintisizden sonra uzun mola önerilsin", "uzun_mola_esigi_dk")
        satir("Uzun mola süresi", "Dakika", "uzun_mola_dk")

        tam_ekran = tk.BooleanVar(value=bool(self.ayar["tam_ekranda_sor"]))
        analiz = tk.BooleanVar(value=bool(self.ayar.get("analiz_izni")))
        sesli = tk.BooleanVar(value=bool(self.ayar.get("ses", True)))
        bekci = tk.BooleanVar(value=bool(self.ayar.get("bekci", True)))

        def kutu(metin, aciklama, degisken):
            f = tk.Frame(p, bg=P["kart"])
            f.pack(fill="x", padx=26, pady=6)
            tk.Checkbutton(f, text=metin, variable=degisken, font=("Segoe UI", 10),
                           fg=P["yazi"], bg=P["kart"], selectcolor=P["zemin"],
                           activebackground=P["kart"], activeforeground=P["yazi"],
                           relief="flat", highlightthickness=0).pack(anchor="w")
            tk.Label(f, text=aciklama, font=("Segoe UI", 8), fg=P["soluk"],
                     bg=P["kart"], wraplength=380, justify="left").pack(anchor="w", padx=24)

        # ---------- Çalışma saatleri ----------
        saatler = tk.BooleanVar(value=bool(self.ayar.get("saatler_acik")))
        sf2 = tk.Frame(p, bg=P["kart"])
        sf2.pack(fill="x", padx=26, pady=(10, 2))
        tk.Checkbutton(sf2, text="Çalışma saatleri", variable=saatler,
                       font=("Segoe UI", 10), fg=P["yazi"], bg=P["kart"],
                       selectcolor=P["zemin"], activebackground=P["kart"],
                       activeforeground=P["yazi"], relief="flat",
                       highlightthickness=0).pack(anchor="w")
        tk.Label(sf2, text="Bu aralığın dışında hatırlatma gelmez (22:00–04:00 gibi "
                           "gece vardiyası da olur)",
                 font=("Segoe UI", 8), fg=P["soluk"], bg=P["kart"],
                 wraplength=380, justify="left").pack(anchor="w", padx=24)
        saat_satiri = tk.Frame(p, bg=P["kart"])
        saat_satiri.pack(fill="x", padx=50, pady=(4, 6))
        bas_alan = tk.Entry(saat_satiri, width=7, font=("Segoe UI", 11), justify="center",
                            bg=P["zemin"], fg=P["yazi"], insertbackground=P["yazi"],
                            relief="flat")
        bas_alan.insert(0, self.ayar.get("bas_saat", "09:00"))
        bas_alan.pack(side="left", ipady=4)
        tk.Label(saat_satiri, text="  —  ", fg=P["soluk"], bg=P["kart"]).pack(side="left")
        bit_alan = tk.Entry(saat_satiri, width=7, font=("Segoe UI", 11), justify="center",
                            bg=P["zemin"], fg=P["yazi"], insertbackground=P["yazi"],
                            relief="flat")
        bit_alan.insert(0, self.ayar.get("bit_saat", "18:00"))
        bit_alan.pack(side="left", ipady=4)

        # ---------- Açılışta başlatma ----------
        acilis = tk.BooleanVar(value=kl.acilista_baslar_mi())
        af2 = tk.Frame(p, bg=P["kart"])
        af2.pack(fill="x", padx=26, pady=(10, 2))
        tk.Checkbutton(af2, text="Windows açılınca kendim başla", variable=acilis,
                       font=("Segoe UI", 10), fg=P["yazi"], bg=P["kart"],
                       selectcolor=P["zemin"], activebackground=P["kart"],
                       activeforeground=P["yazi"], relief="flat",
                       highlightthickness=0).pack(anchor="w")
        gecen_sure = kl.acilistan_beri_saniye()
        acilis_not = ("Arka planda başlar, pencere açılmaz. Program KAPALIYKEN "
                      "hiçbir şey ölçemez — açılışta başlamasının sebebi bu.")
        if gecen_sure > 600 and not kl.acilista_baslar_mi():
            acilis_not += ("\nBilgisayarın %s açık; bu sürenin tamamı sayılmadı."
                           % sure_okunakli(gecen_sure))
        tk.Label(af2, text=acilis_not, font=("Segoe UI", 8), fg=P["soluk"],
                 bg=P["kart"], wraplength=380, justify="left").pack(anchor="w", padx=24)

        kutu("Uyarı sesi", "Mola başında ve sonunda yumuşak bir çan sesi", sesli)
        kutu("Tam ekranda izin iste", "Sunum/video varsa molayı ertelemeyi teklif eder", tam_ekran)
        kutu("Program analizi", "Hangi programda ne kadar kaldığını sayar. Pencere "
                                "başlıkları kaydedilmez, veriler bu bilgisayarda kalır.", analiz)

        # --- Şifre ---
        tk.Frame(p, bg=P["cizgi"], height=1).pack(fill="x", padx=26, pady=(14, 10))
        kf = tk.Frame(p, bg=P["kart"])
        kf.pack(fill="x", padx=26)
        tk.Label(kf, text="Kilit şifresi", font=("Segoe UI", 10), fg=P["yazi"],
                 bg=P["kart"]).pack(anchor="w")
        kilit_durum = tk.Label(
            kf, font=("Segoe UI", 8), fg=P["soluk"], bg=P["kart"],
            wraplength=380, justify="left",
            text=("Açık — ayarlar ve programı kapatma şifreli"
                  if self.kilitli_mi() else
                  "Kapalı — herkes programı kapatabilir"))
        kilit_durum.pack(anchor="w")

        sf = tk.Frame(p, bg=P["kart"])
        sf.pack(fill="x", padx=26, pady=8)
        sifre_alan = tk.Entry(sf, show="●", width=12, font=("Segoe UI", 11),
                              justify="center", bg=P["zemin"], fg=P["yazi"],
                              insertbackground=P["yazi"], relief="flat")
        sifre_alan.pack(side="left", ipady=5)

        def kilit_metni():
            if not self.kilitli_mi():
                return "Kapalı — program herkes tarafından kapatılabilir"
            return ("Açık — program YALNIZCA şifreyle kapatılır. Ayarlar, "
                    "duraklatma ve molayı erken bitirme serbest.")

        def sifre_kur():
            yeni = sifre_alan.get().strip()
            if not (yeni.isdigit() and 4 <= len(yeni) <= 12):
                kilit_durum.configure(text="Şifre 4–12 rakam olmalı.")
                return
            if self.kilitli_mi() and not self.izin_al(
                    "Şifreyi değiştirmek için önce mevcut şifreni gir.", ust=pencere):
                return
            kilit_durum.configure(text="Şifre hazırlanıyor…")
            pencere.update_idletasks()
            self.ayar["kilit"] = kl.ozet_uret(yeni)
            self.ayar["kilit_ozeti"] = None
            self.ayar["kilit_tuz"] = None
            ayarlari_yaz(self.ayar)
            sifre_alan.delete(0, "end")
            self._bekciyi_kur()
            kilit_durum.configure(
                text=kilit_metni() + "\nKaba kuvvetle kırma süresi: yaklaşık %s"
                     % (kl.sifre_gucu(yeni) or "?"))

        def sifre_kaldir():
            if not self.izin_al("Kilidi kaldırmak için şifreni gir.", ust=pencere):
                return
            self.ayar["kilit"] = None
            self.ayar["kilit_ozeti"] = None
            self.ayar["kilit_tuz"] = None
            ayarlari_yaz(self.ayar)
            kilit_durum.configure(text=kilit_metni())

        dugme(sf, "Şifreyi koy", sifre_kur, kucuk=True).pack(side="left", padx=8)
        dugme(sf, "Kaldır", sifre_kaldir, kucuk=True).pack(side="left")

        kutu("Zorla kapatılırsa geri aç",
             "Kilit açıkken, Görev Yöneticisi'nden kapatılırsa program kendini "
             "yeniden başlatır. Şifreyle düzgün kapattığında bu olmaz."
             + (" AİLE KİPİNDE bu ayar kapatılamaz — kapalıyken kural "
                "tek bir kapatmayla kalkardı."
                if aile_kipinde_mi(self.ayar) else ""), bekci)

        tk.Label(p, text="Şifre düz metin saklanmaz. PBKDF2-HMAC-SHA256 ile 600.000 tur "
                         "döndürülür (OWASP'ın güncel tavsiyesi) ve her şifreye özel "
                         "rastgele bir tuz eklenir. Yine de bu bir cihaz güvenliği "
                         "değildir: ayar dosyasını silen kişi kilidi de siler. "
                         "Kısa rakam şifreler hızlı kırılır — yukarıdaki süre tahmini "
                         "ekran kartıyla saldıran birini varsayar.",
                 font=("Segoe UI", 8), fg=P["soluk"], bg=P["kart"],
                 wraplength=400, justify="left").pack(padx=26, pady=(8, 0), anchor="w")

        # ================= AİLE KİPİ =================
        # Ebeveyn kural koyar, çocuk değiştiremez. Şifre ZORUNLU:
        # şifresiz aile kipi, kilidin anahtarını kapının üstünde
        # bırakmak demek — çocuk ayarlara girip kipi kapatır.
        tk.Frame(p, bg=P["cizgi"], height=1).pack(fill="x", padx=26, pady=(14, 10))
        akf = tk.Frame(p, bg=P["kart"])
        akf.pack(fill="x", padx=26)
        tk.Label(akf, text="Kip", font=("Segoe UI", 10, "bold"), fg=P["yazi"],
                 bg=P["kart"]).pack(anchor="w")

        kip_secim = tk.StringVar(value=self.ayar.get("kip", "bireysel"))
        for deger, ad, aciklama in (
                ("bireysel", "Bireysel",
                 "Ayarları sen yönetirsin, molayı istersen geçersin."),
                ("aile", "Aile (ebeveyn kontrolü)",
                 "Ayarlar ve molayı geçme şifreli. Günlük süre sınırı ve "
                 "saat yasağı konabilir.")):
            kr = tk.Frame(p, bg=P["kart"])
            kr.pack(fill="x", padx=26, pady=(4, 0))
            tk.Radiobutton(kr, text=ad, variable=kip_secim, value=deger,
                           font=("Segoe UI", 10), fg=P["yazi"], bg=P["kart"],
                           activebackground=P["kart"], activeforeground=P["yazi"],
                           selectcolor=P["zemin"], highlightthickness=0,
                           anchor="w").pack(anchor="w")
            tk.Label(kr, text=aciklama, font=("Segoe UI", 8), fg=P["soluk"],
                     bg=P["kart"], wraplength=380, justify="left").pack(
                anchor="w", padx=24)

        aile_uyari = tk.Label(p, text="", font=("Segoe UI", 8), fg="#ff8f7a",
                              bg=P["kart"], wraplength=400, justify="left")
        aile_uyari.pack(anchor="w", padx=26, pady=(6, 0))

        # --- Aile ayarları (yalnızca aile kipinde anlamlı) ---
        agf = tk.Frame(p, bg=P["kart"])
        agf.pack(fill="x", padx=26, pady=(8, 0))

        sinir_satir = tk.Frame(agf, bg=P["kart"])
        sinir_satir.pack(fill="x", pady=(4, 0))
        tk.Label(sinir_satir, text="Günlük ekran süresi sınırı (dakika, 0 = sınırsız)",
                 font=("Segoe UI", 9), fg=P["yazi"], bg=P["kart"]).pack(anchor="w")
        sinir_alan = tk.Entry(sinir_satir, width=8, font=("Segoe UI", 11),
                              justify="center", bg=P["zemin"], fg=P["yazi"],
                              insertbackground=P["yazi"], relief="flat")
        sinir_alan.insert(0, str(int(self.ayar.get("gunluk_sinir_dk", 0) or 0)))
        sinir_alan.pack(anchor="w", ipady=4, pady=(3, 0))

        yasak_acik = tk.BooleanVar(value=bool(self.ayar.get("yasak_acik")))
        kutu("Saat yasağı",
             "Bu aralıkta tam ekran uyarı çıkar ve kapanmaz. “Çalışma "
             "saatleri” ayarından farklı: o yalnızca molaları susturur, "
             "bu kullanımı engeller.", yasak_acik)

        ysf = tk.Frame(p, bg=P["kart"])
        ysf.pack(fill="x", padx=50, pady=(0, 4))
        tk.Label(ysf, text="Yasak başlangıcı", font=("Segoe UI", 8),
                 fg=P["soluk"], bg=P["kart"]).pack(side="left")
        yasak_bas_alan = tk.Entry(ysf, width=6, font=("Segoe UI", 10),
                                  justify="center", bg=P["zemin"], fg=P["yazi"],
                                  insertbackground=P["yazi"], relief="flat")
        yasak_bas_alan.insert(0, self.ayar.get("yasak_bas", "21:00"))
        yasak_bas_alan.pack(side="left", padx=6, ipady=3)
        tk.Label(ysf, text="bitişi", font=("Segoe UI", 8),
                 fg=P["soluk"], bg=P["kart"]).pack(side="left")
        yasak_bit_alan = tk.Entry(ysf, width=6, font=("Segoe UI", 10),
                                  justify="center", bg=P["zemin"], fg=P["yazi"],
                                  insertbackground=P["yazi"], relief="flat")
        yasak_bit_alan.insert(0, self.ayar.get("yasak_bit", "07:00"))
        yasak_bit_alan.pack(side="left", padx=6, ipady=3)

        # ---- EBEVEYNE DÜRÜSTLÜK ----
        # Ebeveyn bu kipi ÇOCUĞU için açıyor. Neyin garanti olduğunu,
        # neyin olmadığını bilmezse korunmadığı hâlde korunduğunu sanar.
        # Elimizde ölçülmüş bir atlatma listesi var (ILERLEME.md); burada
        # onun ebeveyni ilgilendiren kısmı yazılı. Eskiden yalnızca
        # "güvenlik duvarı değildir" yazıyordu — doğruydu ama EN KOLAY
        # atlatma yolunu ve gerçek çözümü söylemiyordu.
        tk.Frame(p, bg=P["cizgi"], height=1).pack(fill="x", padx=26,
                                                  pady=(12, 8))
        tk.Label(p, text="Bu kip ne yapar, ne yapmaz",
                 font=("Segoe UI", 9, "bold"), fg=P["yazi"],
                 bg=P["kart"]).pack(padx=26, anchor="w")

        tk.Label(p, text="Denendi, atlatılamıyor: sistem saatini geri ya da "
                         "ileri almak, gece yarısını bekleyip sınırı "
                         "sıfırlatmak, ayarlara girip kipi kapatmak, molayı "
                         "kısayolla geçmek.\n"
                         "Kayıt dosyasını düzenleyip ekran süresini geri almak "
                         "da yakalanıyor: süre gün içinde geri gidemez ve "
                         "denenirse burada uyarı çıkar.",
                 font=("Segoe UI", 8), fg=P["soluk"], bg=P["kart"],
                 wraplength=400, justify="left").pack(padx=26, pady=(6, 0),
                                                      anchor="w")

        tk.Label(p, text="Atlatılabiliyor — bilmen gerekir:\n"
                         "•  Ayar dosyası silinirse kip tümüyle kalkar. Dosya "
                         "çocuğun kendi kullanıcı klasöründe duruyor; bunu "
                         "engelleyemeyiz.\n"
                         "•  Görev Yöneticisi'nden iki süreç birden "
                         "kapatılabilir.\n"
                         "•  Windows güvenli kipte açılırsa hiçbir program "
                         "başlamaz.\n"
                         "•  Tarayıcıdaki sürümde aile kipi yoktur.",
                 font=("Segoe UI", 8), fg="#ffb27a", bg=P["kart"],
                 wraplength=400, justify="left").pack(padx=26, pady=(6, 0),
                                                      anchor="w")

        tk.Label(p, text="Gerçek koruma için çocuğa yönetici hakkı olmayan "
                         "AYRI bir Windows hesabı açın. Bu uygulama onun "
                         "yerini tutmaz; amacı engellemek değil, sınırı "
                         "görünür kılmaktır.",
                 font=("Segoe UI", 8), fg=P["soluk"], bg=P["kart"],
                 wraplength=400, justify="left").pack(padx=26, pady=(6, 0),
                                                      anchor="w")

        def kip_degisti(*_):
            if kip_secim.get() == "aile" and not self.kilitli_mi():
                aile_uyari.configure(
                    text="Aile kipi için önce yukarıdan bir şifre koymalısın. "
                         "Şifresiz aile kipi kaydedilmez.")
            else:
                aile_uyari.configure(text="")

        kip_secim.trace_add("write", kip_degisti)
        kip_degisti()

        # Hatalı giriş olursa kullanıcı görsün — eskiden sessizce hiçbir şey
        # olmuyordu ve "ayar kaydedilmiyor" gibi görünüyordu.
        hata_yazi = tk.Label(alt_cerceve, text="", font=("Segoe UI", 9),
                             fg="#ff8f7a", bg=P["kart"], wraplength=380)

        def kaydet():
            SINIRLAR = (
                ("calisma_dk", "Çalışma süresi", 1, 180),
                ("mola_sn", "Mola süresi", 5, 600),
                ("uyari_sn", "Ön uyarı", 0, 60),
                ("uzun_mola_esigi_dk", "Uzun mola eşiği", 10, 600),
                ("uzun_mola_dk", "Uzun mola süresi", 1, 60),
            )
            yeni = {}
            for anahtar, ad, enaz, encok in SINIRLAR:
                ham = alanlar[anahtar].get().strip()
                deger = sayi_oku(ham)
                if deger is None:
                    hata_yazi.configure(
                        text="“%s” alanına sayı yazmalısın (%s yazılmış)." % (ad, ham or "boş"))
                    hata_yazi.pack(pady=(6, 0))
                    alanlar[anahtar].focus_set()
                    return
                if not (enaz <= deger <= encok):
                    hata_yazi.configure(
                        text="“%s” %d ile %d arasında olmalı (%g yazılmış)."
                             % (ad, enaz, encok, deger))
                    hata_yazi.pack(pady=(6, 0))
                    alanlar[anahtar].focus_set()
                    return
                yeni[anahtar] = deger if anahtar == "calisma_dk" else int(deger)

            hata_yazi.pack_forget()
            self.ayar.update(yeni)
            self.ayar["tam_ekranda_sor"] = bool(tam_ekran.get())
            self.ayar["analiz_izni"] = bool(analiz.get())
            self.ayar["ses"] = bool(sesli.get())
            self.ayar["bekci"] = bool(bekci.get())
            self.ayar["saatler_acik"] = bool(saatler.get())
            # Açılışta başlatma: kısayolu ekle/kaldır
            if bool(acilis.get()) != kl.acilista_baslar_mi():
                kl.acilista_baslat(bool(acilis.get()))
            self.ayar["acilis_izni"] = bool(acilis.get())
            # Hatalı saat SESSİZCE varsayılana dönmüyor artık: kullanıcı
            # yazdığı saatin kaydedilmediğini bilmeli.
            for alan, anahtar, ad in ((bas_alan, "bas_saat", "Başlangıç saati"),
                                      (bit_alan, "bit_saat", "Bitiş saati")):
                ham = alan.get().strip()
                deger = saat_oku(ham)
                if deger is None:
                    hata_yazi.configure(
                        text="“%s” SS:DD biçiminde olmalı, 00:00 ile 23:59 "
                             "arasında (%s yazılmış)." % (ad, ham or "boş"))
                    hata_yazi.pack(pady=(6, 0))
                    alan.focus_set()
                    return
                self.ayar[anahtar] = deger
            # --- Aile kipi ---
            istenen_kip = kip_secim.get()
            if istenen_kip == "aile" and not self.kilitli_mi():
                # Şifresiz aile kipi anlamsız; sessizce kaydetmek yerine
                # söylüyoruz. Sessiz reddetme "ayar kaydedilmiyor" gibi
                # görünüyor — bu hatayı bu dosyada bir kez yaptık.
                hata_yazi.configure(
                    text="Aile kipi için önce bir kilit şifresi koy. "
                         "Şifresiz aile kipi çocuk tarafından kapatılabilir.")
                hata_yazi.pack(pady=(6, 0))
                return
            # Aile kipinden ÇIKMAK da şifre ister — yoksa kural kural olmaz
            if self.ayar.get("kip") == "aile" and istenen_kip != "aile":
                if not self.izin_al("Aile kipini kapatmak için ebeveyn şifresi.",
                                    ust=pencere):
                    return
            self.ayar["kip"] = istenen_kip
            if istenen_kip == "aile":
                # Aile kipinde bekçi zorunlu; kullanıcı kapatmışsa geri aç
                self.ayar["bekci"] = True
            self.ayar["yasak_acik"] = bool(yasak_acik.get())
            # Okunamayan değeri SESSİZCE 0 yapmak, "sınır yok" demekti.
            # Ebeveyn sınır koyduğunu sanıp hiç koymamış oluyordu.
            # Artık okunamıyorsa söylüyoruz ve kaydetmiyoruz.
            ham_sinir = sinir_alan.get().strip()
            sinir = sayi_oku(ham_sinir, varsayilan=(0 if not ham_sinir else None))
            if sinir is None:
                hata_yazi.configure(
                    text="Günlük sınır alanına sayı yazmalısın "
                         "(%s yazılmış). Boş bırakırsan sınır olmaz." % ham_sinir)
                hata_yazi.pack(pady=(6, 0))
                sinir_alan.focus_set()
                return
            self.ayar["gunluk_sinir_dk"] = max(0, min(1440, int(sinir)))
            for alan, anahtar, ad in ((yasak_bas_alan, "yasak_bas", "Yasak başlangıcı"),
                                      (yasak_bit_alan, "yasak_bit", "Yasak bitişi")):
                ham = alan.get().strip()
                deger = saat_oku(ham)
                if deger is None:
                    hata_yazi.configure(
                        text="“%s” SS:DD biçiminde olmalı, 00:00 ile 23:59 "
                             "arasında (%s yazılmış)." % (ad, ham or "boş"))
                    hata_yazi.pack(pady=(6, 0))
                    alan.focus_set()
                    return
                self.ayar[anahtar] = deger

            ayarlari_yaz(self.ayar)
            self.hedef = time.time() + self.ayar["calisma_dk"] * 60
            self._bekciyi_kur()
            # Kip değiştiyse engel durumunu hemen gözden geçir
            try:
                self.engeli_uygula()
            except Exception:
                pass
            pencere.destroy()

        # Düğmeler kayan alanın DIŞINDA — hep görünür kalsınlar
        tk.Frame(alt_cerceve, bg=P["cizgi"], height=1).pack(fill="x")
        af = tk.Frame(alt_cerceve, bg=P["kart"])
        af.pack(pady=14)
        dugme(af, "Vazgeç", pencere.destroy).pack(side="left", padx=6)
        dugme(af, "Kaydet", kaydet, ana_mi=True).pack(side="left", padx=6)

        # ---------------------------------------------------------------
        # BOYUT: içerik ne kadar uzun olursa olsun pencere ekranı aşmasın.
        # Aşarsa Kaydet düğmesi görünmez olur ve ayar kaydedilemez.
        # ---------------------------------------------------------------
        pencere.update_idletasks()
        ekran_g = pencere.winfo_screenwidth()
        ekran_y = pencere.winfo_screenheight()

        istenen_g = p.winfo_reqwidth() + self.ol(22)      # kaydırma çubuğu payı
        istenen_y = p.winfo_reqheight() + af.winfo_reqheight() + self.ol(30)

        gen = min(istenen_g, ekran_g - self.ol(60))
        yuk = min(istenen_y, ekran_y - self.ol(90))       # görev çubuğuna pay
        pencere.geometry("%dx%d+%d+%d" % (
            gen, yuk, (ekran_g - gen) // 2, max(0, (ekran_y - yuk) // 2)))
        pencere.minsize(self.ol(360), self.ol(320))
        _govde_olcu()

    def calistir(self):
        self.kok.mainloop()


if __name__ == "__main__":
    # Bekçi kipi: "--bekci <izlenecek_pid> <klasor>" ile çağrılır.
    # Arayüz açmaz, sadece programın hayatta olup olmadığını izler.
    if len(sys.argv) >= 4 and sys.argv[1] == "--bekci":
        # 5. argüman gizli söz; eski sürümden kalan bekçiler onsuz
        # çağırabilir, o durumda eski davranış sürüyor.
        soz = sys.argv[4] if len(sys.argv) >= 5 else ""
        sys.exit(kl.bekci_calis(int(sys.argv[2]), sys.argv[3], soz))

    # Zaten açıksa ikinci kopya açma; açık olana "pencereni göster" de.
    if not kl.tek_ornek_al():
        kl.goster_iste(KAYIT_KLASOR)
        sys.exit(0)

    Uygulama().calistir()
