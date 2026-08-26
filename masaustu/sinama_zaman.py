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


def main():
    hatalar = []

    def kontrol(ad, sart, ayrinti=""):
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

    if hatalar:
        print("\nBASARISIZ - %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("\nTAMAM - sayac dogru, saat oyunuyla atlatilamiyor.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        gm.time = gercek_zaman
