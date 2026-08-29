# -*- coding: utf-8 -*-
"""ZAMAN SINAMASI — sayaç doğru mu, saat oyunuyla atlatılabiliyor mu?

NEDEN VAR
  Bu uygulamanın bütün riski iki şeyde: **yanlış süre** ve **yanlış
  güven**. Şifre gücü tahmininin 1000 kat şiştiğini gözle yakaladık;
  aynı sınıftan başka hatalar sessizce durabilir. Süre hataları
  görünmez — sayaç yanlış saysa kimse fark etmez, yalnızca molalar
  gelmez ve kimse "gelmeyen mola"yı aramaz.

  Aile kipi ayrıca bir güvenlik özelliği. "Çalışıyor" yetmez,
  **atlatılabiliyor mu** diye sorulmalı.

BULUNAN ÜÇ HATA (hepsi bu sınamayla yakalandı)
  1. Gece yarısı gün değişmiyordu → günlük sınır sıfırlanmıyor, ekran
     süresi dünkü kovaya yazılıyordu.
  2. Saat yasağı sistem saati değiştirilerek atlatılabiliyordu.
  3. Saat geri alınınca mola erteleniyordu (yaz/kış saati ve NTP
     eşitlemesi de aynı etkiyi yapıyor).

NASIL
  Modülün `time`'ı sahte bir saatle değiştiriliyor. Duvar saati ile
  monotonik saat AYRI kontrol ediliyor — gerçek hayatta da ayrılar,
  sıçrama tespiti tam bu farka dayanıyor.

ÇALIŞTIRMA
  python sinama_zaman.py
"""
import io
import os
import sys
import time as gercek_zaman

import goz_molasi as gm
import kilit as kl
import sinama_yalitim

# EN BASTA YALIT. Bu satir olmadan sinama, kullanicinin gercek ayar
# dosyasina yazabiliyor - bir kez yazdi ve bilgisayari kilitledi.
sinama_yalitim.yalit(gm)


class SahteSaat:
    """time modülünün yerine geçer.

    `an`  : duvar saati — elle ileri/geri alınabilir (kullanıcı gibi)
    `mono`: monotonik saat — yalnızca ilerler, saat oyunundan etkilenmez
    """

    def __init__(self, an):
        self.an = float(an)
        self.mono = 1000.0

    def time(self):
        return self.an

    def monotonic(self):
        return self.mono

    def localtime(self, an=None):
        return gercek_zaman.localtime(self.an if an is None else an)

    def strftime(self, kalip, t=None):
        return gercek_zaman.strftime(kalip, t or self.localtime())

    def sleep(self, sn):
        pass

    def struct_time(self, *a, **k):
        return gercek_zaman.struct_time(*a, **k)

    # --- yardımcılar ---
    def ilerle(self, sn):
        """Normal akış: ikisi birlikte ilerler."""
        self.an += sn
        self.mono += sn

    def saati_kaydir(self, sn):
        """Kullanıcı saati değiştirdi: yalnızca duvar saati oynar."""
        self.an += sn


def an(yil, ay, gun, saat, dakika=0):
    return gercek_zaman.mktime((yil, ay, gun, saat, dakika, 0, 0, 0, -1))


class SahteUygulama(gm.Uygulama):
    """Uygulama.__init__ atlanır; yalnızca zaman mantığı sınanır."""

    def __init__(self, saat, ayar=None, ekran_sn=0.0):
        self.saat = saat
        self.ayar = dict(gm.VARSAYILAN)
        if ayar:
            self.ayar.update(ayar)
        self.ist = {
            "gun": saat.strftime("%Y-%m-%d"),
            "tamamlanan": 0, "ertelenen": 0, "uzun_mola": 0,
            "ekran_sn": float(ekran_sn), "kesintisiz_sn": 0.0,
            "programlar": {},
        }
        self.durum = "calisiyor"
        self.hedef = saat.time() + self.ayar["calisma_dk"] * 60
        self.engel_ekrani = None
        self.mola_ekrani = None
        self.kok = None
        self.telafi_sayisi = 0
        self.telafi_suresi = None
        self.duraklama_bitis = 0
        # İlk tik: sıçrama ölçümü için başlangıç noktası
        self._saat_sicramasini_yakala(saat.time())

    def tik(self):
        """Gerçek _tik'in zamanla ilgili kısmı."""
        self._saat_sicramasini_yakala(self.saat.time())
        self._gunu_tazele()

    # Diske yazma yok
    def _sayaci_kaydet(self):
        pass

    def _istatistik_yaz(self):
        pass


class SahteSoru(object):
    """Soru penceresinin yerine gecer: sorulan metni saklar, "hayir" der."""

    son = {}

    def __init__(self, kok, baslik, metin, **k):
        SahteSoru.son = {"baslik": baslik, "metin": metin}

    def bekle(self):
        return False


class TuvalDurdu(Exception):
    """Cizime girmeden once durmak icin."""


class DurTuval(object):
    """delete() cagrisinda duran sahte tuval.

    `_oneri_ciz` metni URETTIKTEN sonra tuvale ciziyor. Metni okumak
    icin Tk penceresi acmak gerekmesin diye cizimin ilk adiminda
    duruyoruz; uretilen metin `oneri_imza` alaninda kaliyor.
    """

    def delete(self, *a, **k):
        raise TuvalDurdu()


def oneri_metni(u):
    """`_oneri_ciz`in ekrana yazacagi metni dondurur (cizim yapmadan)."""
    u.oneri_imza = None
    try:
        u._oneri_ciz()
    except TuvalDurdu:
        pass
    return u.oneri_imza


# Bu sinamanin yapmasi gereken en az kontrol sayisi.
#
# NEDEN VAR: "belirti yok" ile "dal hic calismadi" ayni yesili
# gosteriyor. Kontrollerin yarisi silinse bu sinama yine "TAMAM"
# derdi - ve dogruladigi sey, ekranda gordugun SAYININ dogrulugu.
# 25 -> 48: asagidaki "EKRANDAKI RAKAM" bolumu 23 kontrol ekliyor.
# Taban yukseltilmezse bu bolumun tamami silinse bile sinama 25'i
# gecip "TAMAM" derdi - dosyanin bu tabani koymasinin sebebi tam da
# buydu ("belirti yok" ile "dal hic kosmadi" ayni yesili gosteriyor).
# 48 -> 74: asagidaki "EKRANDAKI SURE YAZISI" bolumu 26 kontrol
# daha ekliyor (ayardan turemeyen sabit sure/esik metinleri).
EN_AZ_KONTROL = 74


def sayim_dogrulugu(kontrol):
    """EKRANDAKI RAKAM dogru mu? (bulgu 5, 6, 17 - 29.08.2026)

    Bu ucu de "uygulama calisir, sayi yanlistir" sinifindan; hicbiri
    cokme uretmiyor, hepsini kullanici HER GUN goruyor.

      * `sure_okunakli` 24 saati gecen her sureye "0 sn" diyordu.
      * Sayac her tikte sabit 0,25 sn ekliyordu, oysa dongu 250 ms
        istiyor ve 258-260 ms'de donuyor: %3,2-3,8 eksik, 8 saatte
        ~16 dakika, hep ayni yonde.
      * "Senin durumun" karti uzun molalari hic saymiyor, dinlenme
        dakikasini 5,6 kat dusuk yaziyordu.

    TERS DAL da olculuyor: duzeltme fazla kirpiyor olabilir.
    """
    def sure(deger):
        """Cokmeyi de bir SONUC sayar, sinamayi durduran kaza degil.

        Olculdu (29.08.2026): `sure_okunakli(float('inf'))`
        OverflowError atiyordu; sinama tam orada duruyor ve geri kalan
        kontroller hic kosmuyordu."""
        try:
            return gm.sure_okunakli(deger)
        except Exception as e:
            return "COKTU(%s)" % type(e).__name__

    # ---- 5) SURE YAZIMI ----
    for saniye, beklenen, ad in (
            (0, "0 sn", "sifir"),
            (45, "45 sn", "saniye"),
            (60, "1 dk", "tam dakika"),
            (3599, "59 dk", "bir saatin bir eksigi"),
            (3600, "1 sa 0 dk", "tam saat"),
            (86399, "23 sa 59 dk", "bir gunun bir eksigi"),
            (86400, "1 gün 0 sa", "tam gun"),
            (90000, "1 gün 1 sa", "25 saat - eskiden '0 sn'"),
            (3 * 86400 + 4 * 3600, "3 gün 4 sa", "uc gunluk calisma suresi"),
            (-5, "0 sn", "negatif - sifirlanir"),
            ("cok", "0 sn", "metin - sifirlanir"),
            (None, "0 sn", "None - sifirlanir"),
            (float("inf"), "0 sn", "sonsuz - sifirlanir"),
            (400 * 86400, "0 sn", "400 gun - bozuk kayit, sifirlanir")):
        cikan = sure(saniye)
        kontrol("sure_okunakli(%s) = %s [%s]" % (saniye, beklenen, ad),
                cikan == beklenen, cikan)

    # ---- 6) SAYAC GERCEK SUREYI SAYIYOR MU ----
    saat = SahteSaat(an(2026, 8, 26, 14, 0))
    gm.time = saat
    if not hasattr(gm.Uygulama, "_sayim_araligi"):
        # Islev silinmisse geri kalan kontroller cokerdi; "olculemedi"
        # demek, sessizce yesil gostermekten iyidir.
        kontrol("Uygulama._sayim_araligi tanimli", False,
                "islev yok - sayac yine sabit deger ekliyor olabilir")
        return
    u = SahteUygulama(saat)
    u._sayim_yapildi = False
    toplam = 0.0
    # Ilk sayim anma degeri (0,25) doner; sonrakiler gercek arayi olcer.
    toplam += u._sayim_araligi(False)
    for _ in range(3600):                 # 15 dakikalik dongu
        saat.ilerle(0.26)                 # Tkinter'in gercek araligi
        toplam += u._sayim_araligi(True)
    beklenen = 3600 * 0.26 + 0.25
    kontrol("sayac gercek gecen sureyi sayiyor (0,26 sn'lik tik)",
            abs(toplam - beklenen) < 0.5,
            "%.1f sn sayildi, %.1f olmaliydi" % (toplam, beklenen))
    kontrol("sabit 0,25 sn'lik eski sayim geri gelmemis",
            toplam > 3600 * 0.25 + 1,
            "%.1f sn - eski hesap %.1f verirdi" % (toplam, 3600 * 0.25))

    # Uyku / askiya alma: dev aralik ekran suresine YAZILMAZ,
    # "olculemeyen" hanesine gider.
    u2 = SahteUygulama(saat)
    u2._sayim_araligi(False)
    saat.ilerle(2 * 3600)
    uyku = u2._sayim_araligi(True)
    kontrol("2 saatlik uyku ekran suresine eklenmiyor", uyku == 0.0,
            "%.1f sn eklendi" % uyku)
    kontrol("uyku suresi 'olculemeyen' hanesine yaziliyor",
            abs(getattr(u2, "olculemeyen_sn", 0.0) - 2 * 3600) < 2,
            "%.0f sn" % getattr(u2, "olculemeyen_sn", 0.0))

    # TERS DAL: arada mola/bosta vardiysa o bosluk ekran suresi degil.
    u3 = SahteUygulama(saat)
    u3._sayim_araligi(False)
    saat.ilerle(20)                       # 20 saniyelik mola
    ara = u3._sayim_araligi(False)
    kontrol("mola arasi ekran suresi sayilmiyor (bayrak False)",
            ara == 0.25, "%.2f sn" % ara)

    # ---- 17) "SENIN DURUMUN" KARTI ----
    kart_u = SahteUygulama(saat, {"mola_sn": 20, "uzun_mola_dk": 5})
    kart_u.ist["tamamlanan"] = 4
    kart_u.ist["uzun_mola"] = 2
    kart = gm.Uygulama._durum_karti(kart_u)
    metin = kart[1] if kart else ""
    # DIKKAT: yalnizca "6 mola" aramak yetmez - bozuk surum de
    # "Son yedi gunde toplam 6 mola" yaziyordu. Olculen cumle BUGUNKU
    # sayiyi soyleyen cumle.
    kontrol("kart uzun molalari da sayiyor (4 kisa + 2 uzun = 6)",
            "Bugün 6 mola" in metin, metin)
    # 4*20 + 2*300 = 680 sn = 11,3 dakika. Eskiden 6*20/60 = 2 dakika.
    kontrol("dinlenme dakikasi mola TURUNE gore hesaplaniyor",
            "11 dakikalık" in metin, metin)

    # TERS DAL: yalniz kisa molalik gun bozulmamali (8 x 20 sn = 3 dk)
    kisa_u = SahteUygulama(saat, {"mola_sn": 20, "uzun_mola_dk": 5})
    kisa_u.ist["tamamlanan"] = 8
    kisa_metin = (gm.Uygulama._durum_karti(kisa_u) or ("", "", ""))[1]
    kontrol("yalniz kisa molalik gun hala dogru (8 mola, 3 dakika)",
            "Bugün 8 mola" in kisa_metin and "3 dakikalık" in kisa_metin,
            kisa_metin)

    # TERS DAL: hic mola yoksa kart gosterilmez ("bugun 0 mola" demiyoruz)
    bos_u = SahteUygulama(saat)
    kontrol("hic mola yokken kart gosterilmiyor",
            gm.Uygulama._durum_karti(bos_u) is None)


def main():
    hatalar = []
    sayac = {"n": 0}

    def kontrol(ad, sart, ayrinti=""):
        sayac["n"] += 1
        if not sart:
            hatalar.append("%s%s" % (ad, (" - " + ayrinti) if ayrinti else ""))
        print("  %-54s %s" % (ad, "TAMAM" if sart else "KALDI"))

    sifre = kl.ozet_uret("2468", tur=1000)
    AILE = {"kip": "aile", "kilit": sifre}

    # =================================================================
    print("--- 1) GECE YARISI ---")
    # =================================================================
    saat = SahteSaat(an(2026, 8, 26, 23, 50))
    gm.time = saat
    u = SahteUygulama(saat, dict(AILE, gunluk_sinir_dk=60), ekran_sn=3700)
    kontrol("gece yarısından önce sınır dolu -> engel",
            (u.engel_sebebi() or ("", ))[0] == "sinir")

    saat.ilerle(20 * 60)                       # 00:10, normal akış
    u.tik()
    kontrol("gün etiketi yeni güne geçti",
            u.ist["gun"] == "2026-08-27", u.ist["gun"])
    kontrol("günlük sayaçlar sıfırlandı",
            u.ist["ekran_sn"] == 0, "%d sn" % u.ist["ekran_sn"])
    kontrol("gece yarısından sonra engel kalktı",
            u.engel_sebebi() is None)

    u2 = SahteUygulama(saat, dict(AILE, gunluk_sinir_dk=60), ekran_sn=100)
    u2.ayar["ek_sure_bitis"] = saat.time() + 3600
    saat.ilerle(24 * 3600)                     # ertesi gün
    u2.tik()
    kontrol("dünkü ek süre yeni güne devretmiyor",
            not u2.ayar.get("ek_sure_bitis"))

    # =================================================================
    print("--- 2) SAAT GERİ ALINIRSA ---")
    # =================================================================
    saat = SahteSaat(an(2026, 8, 26, 14, 0))
    gm.time = saat
    u = SahteUygulama(saat, dict(AILE, gunluk_sinir_dk=60), ekran_sn=3700)
    saat.saati_kaydir(-4 * 3600)
    u.tik()
    kontrol("saat geri alınınca günlük sınır HÂLÂ dolu",
            u.engel_sebebi() is not None,
            "birikimli saniye tutuluyor, duvar saatine bağlı değil")

    # Yasak saati
    saat = SahteSaat(an(2026, 8, 26, 22, 0))
    gm.time = saat
    y = SahteUygulama(saat, dict(AILE, yasak_acik=True,
                                 yasak_bas="21:00", yasak_bit="07:00"))
    y.tik()
    kontrol("22:00'de yasak var", (y.engel_sebebi() or ("", ))[0] == "yasak")

    saat.saati_kaydir(-9 * 3600)               # saat 13:00 yapıldı
    y.tik()
    sebep = y.engel_sebebi()
    kontrol("saat değiştirerek yasak ATLATILAMIYOR",
            sebep is not None, "engel kalktı - atlatıldı")
    kontrol("sebep olarak saat oyunu bildiriliyor",
            sebep is not None and sebep[0] == "saat",
            (sebep or ("yok",))[0])

    saat.saati_kaydir(9 * 3600)                # saat düzeltildi
    y.tik()
    kontrol("saat düzeltilince suçlu sayılmıyor",
            (y.engel_sebebi() or ("", ))[0] != "saat")

    # =================================================================
    print("--- 3) SAYACIN KENDİSİ ---")
    # =================================================================
    saat = SahteSaat(an(2026, 8, 26, 14, 0))
    gm.time = saat
    u = SahteUygulama(saat)
    u.hedef = saat.time() + 20 * 60
    saat.ilerle(5 * 60)
    u.tik()
    kontrol("5 dk sonra kalan 15 dk",
            abs((u.hedef - saat.time()) - 15 * 60) < 1,
            "%.0f sn" % (u.hedef - saat.time()))

    saat.saati_kaydir(-60 * 60)                # saat 1 saat geri
    u.tik()
    kalan = u.hedef - saat.time()
    kontrol("saat geri alınınca mola ERTELENMİYOR",
            abs(kalan - 15 * 60) < 3,
            "kalan %.1f dk (15 olmalı)" % (kalan / 60))

    saat.saati_kaydir(3 * 3600)                # saat 3 saat ileri
    u.tik()
    kalan = u.hedef - saat.time()
    kontrol("saat ileri alınınca mola aniden gelmiyor",
            abs(kalan - 15 * 60) < 3,
            "kalan %.1f dk (15 olmalı)" % (kalan / 60))

    # =================================================================
    print("--- 4) TELAFİ VE EK SÜRE ---")
    # =================================================================
    saat = SahteSaat(an(2026, 8, 26, 14, 0))
    gm.time = saat
    u = SahteUygulama(saat, {"mola_sn": 20})
    for beklenen in (10, 8, 8):
        u._molayi_atladi()
        kontrol("atlamada telafi süresi %d sn" % beklenen,
                u.telafi_suresi == beklenen, str(u.telafi_suresi))
    kontrol("telafi molası %d dk sonraya konuyor" % gm.Uygulama.TELAFI_DK,
            abs((u.hedef - saat.time()) - gm.Uygulama.TELAFI_DK * 60) < 2,
            "%.1f dk" % ((u.hedef - saat.time()) / 60))

    u3 = SahteUygulama(saat, dict(AILE, gunluk_sinir_dk=60), ekran_sn=3700)
    u3.ayar["ek_sure_bitis"] = saat.time() + 15 * 60
    kontrol("ek süre verilince engel kalkıyor", u3.engel_sebebi() is None)
    saat.ilerle(15 * 60 + 1)
    u3.tik()
    kontrol("ek süre bitince engel geri geliyor",
            u3.engel_sebebi() is not None)

    # =================================================================
    print("--- 5) UZUN OTURUM VE YAZI/KIŞ SAATİ ---")
    # =================================================================
    saat = SahteSaat(an(2026, 8, 26, 8, 0))
    gm.time = saat
    u = SahteUygulama(saat, dict(AILE, gunluk_sinir_dk=120))
    u.ist["ekran_sn"] = 26 * 3600
    metin = u.engel_kalan_metni()
    kontrol("26 saatlik süre okunaklı yazılıyor",
            "sa" in metin or "dk" in metin, metin)

    # Yaz/kış saati: duvar saati 1 saat oynar, monotonik oynamaz
    saat = SahteSaat(an(2026, 10, 25, 3, 30))
    gm.time = saat
    u = SahteUygulama(saat)
    u.hedef = saat.time() + 10 * 60
    saat.saati_kaydir(-3600)                   # kış saatine geçiş
    u.tik()
    kontrol("kış saatine geçişte sayaç bozulmuyor",
            abs((u.hedef - saat.time()) - 10 * 60) < 3,
            "kalan %.1f dk" % ((u.hedef - saat.time()) / 60))

    # Gercek klasore dokunuldu mu? Guvenmek yetmez, olculur.
    for s in sinama_yalitim.dogrula():
        hatalar.append(s)

    # =================================================================
    print("--- 6) UYKU / UYANMA ---")
    # =================================================================
    # Windows'ta bilgisayar uyurken monotonik saat ilerlemez ama duvar
    # saati ilerler. Bizim sicrama yakalayicimiz tam bu farka bakiyor.
    # Beklenen davranis: KALAN SURE korunur. Kisi uyurken ekrana
    # bakmiyordu; molasini hak etmis sayilmaz, ama molasi da
    # kaybolmamali.
    saat = SahteSaat(an(2026, 8, 26, 14, 0))
    gm.time = saat
    u = SahteUygulama(saat)
    u.hedef = saat.time() + 12 * 60
    saat.saati_kaydir(2 * 3600)      # 2 saat uyku: duvar ilerledi, mono durdu
    u.tik()
    kalan = u.hedef - saat.time()
    kontrol("2 saatlik uykudan sonra kalan süre korunuyor",
            abs(kalan - 12 * 60) < 3,
            "kalan %.1f dk (12 olmalı)" % (kalan / 60))

    saat.ilerle(60)                  # uyandi, normal akis
    u.tik()
    kalan = u.hedef - saat.time()
    kontrol("uyandıktan sonra sayaç normal işliyor",
            abs(kalan - 11 * 60) < 3,
            "kalan %.1f dk (11 olmalı)" % (kalan / 60))

    # =================================================================
    print("--- 7) İLK AÇILIŞ / VERİ SİLİNMİŞ ---")
    # =================================================================
    # Yalıtım sayesinde geçici klasör BOŞ; gerçek ilk açılış durumu.
    saat = SahteSaat(an(2026, 8, 26, 10, 0))
    gm.time = saat
    try:
        hedef = gm.Uygulama._sayaci_geri_yukle(
            SahteUygulama(saat))
        temiz = abs((hedef - saat.time()) - 20 * 60) < 2
    except Exception as e:
        hedef, temiz = None, False
        hatalar.append("veri yokken sayaç geri yükleme çöktü: %r" % e)
    kontrol("durum dosyası yokken temiz 20 dk başlıyor", temiz,
            "%.1f dk" % ((hedef - saat.time()) / 60) if hedef else "çöktü")

    # Bozuk JSON
    bozuk = os.path.join(os.path.dirname(gm.DURUM_DOSYA), "durum.json")
    try:
        io.open(bozuk, "w", encoding="utf-8").write("{bozuk json")
        u2 = SahteUygulama(saat)
        hedef2 = gm.Uygulama._sayaci_geri_yukle(u2)
        saglam = abs((hedef2 - saat.time()) - 20 * 60) < 2
    except Exception as e:
        saglam = False
        hatalar.append("bozuk durum dosyasında çöktü: %r" % e)
    kontrol("bozuk durum dosyası çökertmiyor", saglam)

    # =================================================================
    print("--- 8) EKRANDAKİ RAKAM ---")
    # =================================================================
    sayim_dogrulugu(kontrol)

    # =================================================================
    print("--- 9) EKRANDAKİ SÜRE YAZISI AYARDAN TÜRÜYOR MU? ---")
    # =================================================================
    # NEDEN VAR (29.08.2026): bu sinifin bes ornegi ayni gun olculdu.
    # Hicbiri cokme uretmiyor; hepsi ekrana YANLIS SAYI yaziyordu.
    #   • yasak_saatinde_mi kendi saat cozumleyicisini tasiyordu ve
    #     okuyamadigi degere 0 donuyordu -> yasak sessizce 00:00'a
    #     kayiyor, ebeveyn 21:00 yazdigini saniyordu.
    #   • engel ekrani "saat oyunu" sebebinde "gece yarisi sifirlanir"
    #     diyordu; engel gerceklikte saat duzeltilince kalkiyor.
    #   • "2 saate yaklasiyorsun" sabitti, esik 10-600 dk arasi.
    #   • "20 saniyelik molalar" sabitti, mola_sn 5-600 sn arasi.
    #   • panel ipucu atlanan moladan sonra hâlâ mola_sn yaziyordu.
    #
    # KAYNAK TARAMASI DEGIL OLCUM: "kaynakta 20 saniye ara" demek,
    # mesru yerleri (hazir ayar etiketleri, Amerikan Optometri Birligi
    # alintisi) ELLE listelemeyi gerektirirdi; elle liste bu projede
    # bir kez zaten yanildi. Bunun yerine metni gercekten uretip
    # icindeki HER SAYIYI "ayardan turetilebilir mi" diye soruyoruz.
    import re

    saat = SahteSaat(an(2026, 8, 26, 14, 0))
    gm.time = saat

    # --- a) uzun mola sorusu kisa molanin suresini dogru soyluyor mu?
    gercek_soru = gm.Soru
    gm.Soru = SahteSoru
    try:
        for mola_sn in (20, 60):
            u = SahteUygulama(saat, {"mola_sn": mola_sn, "uzun_mola_dk": 7})
            u.ist["kesintisiz_sn"] = 3 * 3600
            u._uzun_mola_sor()
            metin = SahteSoru.son.get("metin", "")
            kontrol("uzun mola sorusu %d sn'lik molayı söylüyor" % mola_sn,
                    "%d saniyelik" % mola_sn in metin,
                    metin.replace("\n", " ")[-58:])
    finally:
        gm.Soru = gercek_soru

    # --- b) kesintisiz calisma uyarisi esigi ayardan aliyor mu?
    # KURAL: uretilen metindeki her sayi, ayardan turetilen iki
    # sayidan (gecen sure, kalan sure) birine ait olmali. Sabit
    # yazilmis bir sayi bu kurala takilir; elle liste gerekmez.
    for esik_dk, gecen_dk in ((120, 108), (600, 540)):
        u = SahteUygulama(saat, {"uzun_mola_esigi_dk": esik_dk})
        u.ist["kesintisiz_sn"] = gecen_dk * 60
        u.t = DurTuval()
        metin = oneri_metni(u)
        izinli = set(re.findall(r"\d+", gm.sure_okunakli(gecen_dk * 60)))
        izinli |= set(re.findall(
            r"\d+", gm.sure_okunakli((esik_dk - gecen_dk) * 60)))
        gorulen = set(re.findall(r"\d+", metin or ""))
        kontrol("kesintisiz uyarısında ayardan türemeyen sayı yok (%d dk)"
                % esik_dk,
                bool(metin) and gorulen <= izinli,
                "%r -> fazla sayı %s" % (metin, sorted(gorulen - izinli)))

    # --- c) engel ekraninin alt satiri: saat oyunu kolu
    saat = SahteSaat(an(2026, 8, 26, 22, 0))
    gm.time = saat
    y = SahteUygulama(saat, dict(AILE, yasak_acik=True,
                                 yasak_bas="21:00", yasak_bit="07:00"))
    y.tik()
    dogru = y.engel_kalan_metni()
    kontrol("TERS DAL: normal yasakta geri sayım hâlâ doğru",
            "07:00" in dogru and "9 sa 0 dk" in dogru, dogru)
    saat.saati_kaydir(-9 * 3600)               # saat 13:00 yapildi
    y.tik()
    sebep = (y.engel_sebebi() or ("", ))[0]
    metin = y.engel_kalan_metni()
    kontrol("saat oyununda sebep 'saat'", sebep == "saat", sebep)
    kontrol("saat oyununda 'gece yarısı' yalanı yazılmıyor",
            "gece yarısı" not in metin, metin)
    kontrol("saat oyununda ekran ne yapılacağını söylüyor",
            "düzelt" in metin, metin)

    # --- d) bozuk yasak saati: sessizce 00:00'a kaymiyor, ekranda cikiyor
    gece_2 = gercek_zaman.struct_time((2026, 8, 26, 2, 0, 0, 2, 238, -1))
    for ham in ("9 pm", "25:00", "", "abc"):
        bozuk = {"yasak_acik": True, "yasak_bas": ham, "yasak_bit": "07:00"}
        kontrol("bozuk yasak başlangıcı %r 00:00'a kaymıyor" % (ham,),
                not gm.yasak_saatinde_mi(bozuk, gece_2))
        u = SahteUygulama(saat, dict(AILE, **bozuk))
        kontrol("bozuk yasak saati ekranda söyleniyor %r" % (ham,),
                bool(u.ayar_uyarisi()), repr(u.ayar_uyarisi()))

    # --- e) TERS DAL: gecerli saatler hâlâ dogru calisiyor
    saglam_yasak = {"yasak_acik": True,
                    "yasak_bas": "21:00", "yasak_bit": "07:00"}
    for s, beklenen in ((20, False), (21, True), (2, True), (7, False)):
        st = gercek_zaman.struct_time((2026, 8, 26, s, 0, 0, 2, 238, -1))
        kontrol("TERS DAL: geçerli yasak %02d:00 -> %s" % (s, beklenen),
                gm.yasak_saatinde_mi(saglam_yasak, st) == beklenen)
    kontrol("nokta ile yazılmış saat (21.00) artık okunuyor",
            gm.yasak_saatinde_mi(
                dict(saglam_yasak, yasak_bas="21.00"),
                gercek_zaman.struct_time((2026, 8, 26, 22, 0, 0, 2, 238, -1))))
    kontrol("TERS DAL: sağlam yasak ayarı uyarı üretmiyor",
            not SahteUygulama(saat, dict(AILE, **saglam_yasak)).ayar_uyarisi())

    # --- f) vaat edilen mola suresi = baslatilan mola suresi
    saat = SahteSaat(an(2026, 8, 26, 14, 0))
    gm.time = saat
    u = SahteUygulama(saat, {"mola_sn": 20, "tam_ekranda_sor": False})

    def vaat(uyg):
        """Vaat edilen sure. Yontem YOKSA cokme degil KALDI uretir.

        NIYE (29.08.2026, denetim): burada dogrudan
        `u.sonraki_mola_sn()` cagriliyordu. Duzeltme geri alinirsa bu
        satir AttributeError ile COKUYOR; asagidaki kontroller hic
        kosmuyor ve dosyanin sonundaki EN_AZ_KONTROL denetimi de
        atlaniyor. Yani bekci "neyi kaybettim" diyemiyor. Olculdu:
        yamasiz kaynakta 14 kontrol KALDI diyor ama cikti bir yigin
        izi ile bitiyordu.
        """
        islev = getattr(uyg, "sonraki_mola_sn", None)
        return islev() if islev else None

    kontrol("TERS DAL: mola atlanmadan vaat edilen süre = ayar",
            vaat(u) == 20, repr(vaat(u)))
    u._molayi_atladi()
    kontrol("mola atlandıktan sonra vaat = telafi süresi",
            vaat(u) == u.telafi_suresi == 10,
            "vaat %r / gerçek %r" % (vaat(u), u.telafi_suresi))
    baslatilan = []
    u._molayi_baslat = lambda sn: baslatilan.append(sn)
    u._mola_zamani()
    # BAGIMSIZ beklenen deger: `sonraki_mola_sn()` ile karsilastirmak
    # dairesel olurdu - ikisi ayni sekilde bozulursa sinama yine yesil
    # yanar. Telafi suresi (10 sn) ayri bir yoldan uretiliyor.
    kontrol("başlatılan mola, vaat edilen süreyle aynı",
            baslatilan == [u.telafi_suresi], str(baslatilan))

    # --- g) panel ipucu Tk olmadan cagrilamiyor; capasi kaynakta olculur
    kaynak_gm = io.open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "goz_molasi.py"), encoding="utf-8").read()
    kontrol("panel ipucu süreyi sonraki_mola_sn'den alıyor",
            re.search(r'saniye sürecek"\s*%\s*self\.sonraki_mola_sn\(\)',
                      kaynak_gm) is not None)

    if hatalar:
        print("\nyapilan kontrol : %d" % sayac["n"])
        print("BASARISIZ - %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1

    print("\nyapilan kontrol : %d" % sayac["n"])
    if sayac["n"] < EN_AZ_KONTROL:
        print("OLCULEMEDI - yalnizca %d kontrol yapildi, en az %d "
              "bekleniyordu." % (sayac["n"], EN_AZ_KONTROL))
        print("  Kontroller silinmis ya da bir dal hic kosmamis olabilir.")
        print("  SESSIZ GECMIYORUZ: bu sinama sayacin dogrulugunu")
        print("  ve saat oyunuyla atlatilamadigini dogruluyor.")
        return 1
    print("TAMAM - %d kontrol yapildi; sayac dogru, saat oyunuyla "
          "atlatilamiyor." % sayac["n"])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        gm.time = gercek_zaman
