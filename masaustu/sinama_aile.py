# -*- coding: utf-8 -*-
"""AİLE KİPİ SINAMASI — ebeveyn kontrolü doğru çalışıyor mu?

NEDEN VAR
  Aile kipi sessizce bozulabilecek bir özellik: kural uygulanmazsa
  hiçbir şey görünmez, ebeveyn kuralın işlediğini sanar. Bir mola
  ekranının açılmadığı hemen fark edilir; uygulanmayan bir saat yasağı
  fark edilmez. O yüzden makineye sınatıyoruz.

NE DENETLER
  1. Bireysel kipte hiçbir engel çıkmıyor
  2. Şifresiz aile kipi geçersiz sayılıyor (çocuk kapatabilirdi)
  3. Günlük süre sınırı doğru anda devreye giriyor
  4. Ebeveynin verdiği ek süre engeli kaldırıyor, bitince geri geliyor
  5. Saat yasağı gece yarısını doğru aşıyor
  6. Yasak, süre sınırından önce geliyor
  7. Şifre doğrulama ve yükseltme çalışıyor

ÇALIŞTIRMA
  python sinama_aile.py
"""
import io
import sys
import time

import goz_molasi as gm
import kilit as kl
import sinama_yalitim

# Bu sinama da gercek ayar dosyasina yazabilir; ayni yalitim.
sinama_yalitim.yalit(gm)


class SahteUygulama(gm.Uygulama):
    """Uygulama.__init__ atlanır; yalnızca engel mantığı sınanır."""

    def __init__(self, ayar, ekran_sn=0):
        self.ayar = dict(gm.VARSAYILAN)
        self.ayar.update(ayar)
        self.ist = {"ekran_sn": ekran_sn}
        self.engel_ekrani = None
        self.mola_ekrani = None
        self.kok = None


def main():
    hatalar = []
    sifre = kl.ozet_uret("2468", tur=1000)     # sınama için hızlı tur

    def dene(ad, ayar, ekran_sn, beklenen):
        u = SahteUygulama(ayar, ekran_sn)
        try:
            sonuc = u.engel_sebebi()
        except Exception as e:
            # Cokme = hicbir engel uygulanmaz (saat yasagi dahil) ve kimse
            # haberdar olmaz. Sessiz gecilmemeli.
            hatalar.append("%s -> COKME %s: %s" % (ad, type(e).__name__, e))
            return
        tur = sonuc[0] if sonuc else None
        if tur != beklenen:
            hatalar.append("%s -> '%s' (beklenen '%s')" % (ad, tur, beklenen))

    # 1-4) Kip ve süre sınırı
    dene("bireysel kipte engel yok",
         {"kip": "bireysel", "kilit": sifre, "gunluk_sinir_dk": 1}, 99999, None)
    dene("şifresiz aile kipi geçersiz",
         {"kip": "aile", "kilit": None, "gunluk_sinir_dk": 1}, 99999, None)
    dene("sınır dolunca engel",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60}, 3700, "sinir")
    dene("sınır dolmadan engel yok",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60}, 3500, None)
    dene("sınır 0 = sınırsız",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 0}, 99999, None)
    dene("ek süre engeli kaldırır",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60,
          "ek_sure_bitis": time.time() + 600}, 99999, None)
    dene("ek süre bitince engel geri gelir",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60,
          "ek_sure_bitis": time.time() - 10}, 99999, "sinir")

    # 4b) BOZUK AYAR — 26.08.2026'da olculdu: bu satirlar yokken
    #     gunluk_sinir_dk=nan/inf/"abc" uygulamayi COKERTIYORDU; cokunce
    #     saat yasagi dahil hicbir koruma uygulanmiyordu.
    nan, inf = float("nan"), float("inf")
    for etiket, deger in (("nan", nan), ("inf", inf), ("metin", "abc"),
                          ("bos", None), ("liste", [1])):
        dene("bozuk sinir (%s) cokertmemeli" % etiket,
             {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": deger}, 99999, None)
    dene("bozuk sayac (nan) cokertmemeli",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60}, nan, None)
    # Metin olarak yazilmis gecerli sayi calismaya devam etmeli
    dene("metin sinir '60' calisir",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": "60"}, 3700, "sinir")
    dene("virgullu sinir '60,5' calisir",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": "60,5"}, 3700, "sinir")

    # KULLANICI KARARI (27.08.2026): bozuk ayarda ENGELLEME, ama UYAR.
    # Bozuk ek sure de cokertmemeli; `float("abc")` burada da cokuyordu.
    for etiket, deger in (("nan", nan), ("inf", inf), ("metin", "abc"),
                          ("liste", [1])):
        dene("bozuk ek sure (%s) cokertmemeli" % etiket,
             {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60,
              "ek_sure_bitis": deger}, 99999, None)
    dene("gecerli ek sure engeli kaldirir",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60,
          "ek_sure_bitis": time.time() + 600}, 99999, None)

    # UYARI — karar "engelleme ama uyar" oldugu icin uyarinin CIKMASI sart.
    # Engellememek tek basina yeterli olsaydi bu sessiz yanlis olurdu.
    def uyari_dene(ad, ayar, ekran_sn, beklenen_var):
        u = SahteUygulama(ayar, ekran_sn)
        try:
            uyari = u.ayar_uyarisi()
        except Exception as e:
            hatalar.append("%s -> COKME %s: %s" % (ad, type(e).__name__, e))
            return
        if bool(uyari) != beklenen_var:
            hatalar.append("%s -> uyari %r (beklenen %s)"
                           % (ad, uyari, "var" if beklenen_var else "yok"))

    t = {"kip": "aile", "kilit": sifre}
    uyari_dene("bozuk sinir uyarmali", dict(t, gunluk_sinir_dk="abc"), 0, True)
    uyari_dene("bozuk sinir (nan) uyarmali", dict(t, gunluk_sinir_dk=nan), 0, True)
    uyari_dene("bozuk sayac uyarmali", dict(t, gunluk_sinir_dk=60), nan, True)
    uyari_dene("bozuk ek sure uyarmali",
               dict(t, gunluk_sinir_dk=60, ek_sure_bitis=inf), 100, True)
    uyari_dene("saglam ayar uyarmamali", dict(t, gunluk_sinir_dk=60), 100, False)
    uyari_dene("sinir 0 (sinirsiz) bozukluk degil",
               dict(t, gunluk_sinir_dk=0), 100, False)
    uyari_dene("bos sinir bozukluk degil",
               dict(t, gunluk_sinir_dk=""), 100, False)
    uyari_dene("bireysel kipte uyari yok",
               {"kip": "bireysel", "gunluk_sinir_dk": "abc"}, 0, False)

    # Uyari CIKARKEN engel HALA cikmamali — karar buydu.
    dene("uyari varken engel yok (engelleme, uyar)",
         dict(t, gunluk_sinir_dk="abc"), 99999, None)

    # 4b-2) GECERLI GORUNEN AMA KORUMAYI KALDIRAN DEGERLER
    #
    # OLCULDU (27.08.2026): "bozuk ayar" denetimleri yalnizca
    # OKUNAMAYAN degerleri yakaliyordu. Oysa en tehlikelileri gayet
    # GECERLI sayilar/metinler - o yuzden hicbir denetim gormuyordu:
    #
    #   kip = "aile "  (sonda bosluk)  -> esitlik tutmaz, kip YOK SAYILIR
    #   kip = "AILE"                   -> ayni
    #   ek_sure_bitis = simdi + 10 yil -> sinir KALICI kalkar
    #   gunluk_sinir_dk = 10**30       -> "sinir var" gorunur, yoktur
    #   gunluk_sinir_dk = -60          -> sessizce yok sayilir
    #   kilit = {}                     -> kip uygulanmaz ama ayar
    #                                     ekraninda "Aile" SECILI gorunur
    #
    # Hepsi ayni sinif: ebeveyn korundugunu sanir. Aile kipinde ayar
    # dosyasi cocugun kendi klasorunde duruyor.
    dene("kip 'aile ' (bosluk) korumayi kaldirmiyor",
         {"kip": "aile ", "kilit": sifre, "gunluk_sinir_dk": 60}, 3700, "sinir")
    dene("kip 'AILE' (buyuk harf) korumayi kaldirmiyor",
         {"kip": "AILE", "kilit": sifre, "gunluk_sinir_dk": 60}, 3700, "sinir")
    dene("10 yillik ek sure gecerli sayilmiyor",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60,
          "ek_sure_bitis": time.time() + 315360000}, 3700, "sinir")
    dene("mesru ek sure (30 dk) HALA calisiyor",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60,
          "ek_sure_bitis": time.time() + 1800}, 3700, None)
    dene("sinirdaki ek sure (3 saat) kabul ediliyor",
         {"kip": "aile", "kilit": sifre, "gunluk_sinir_dk": 60,
          "ek_sure_bitis": time.time() + 3 * 3600}, 3700, None)

    uyari_dene("10 yillik ek sure uyariyor",
               dict(t, gunluk_sinir_dk=60,
                    ek_sure_bitis=time.time() + 315360000), 3700, True)
    uyari_dene("mesru ek sure uyarmiyor",
               dict(t, gunluk_sinir_dk=60,
                    ek_sure_bitis=time.time() + 1800), 3700, False)
    uyari_dene("bir gunden uzun sinir uyariyor",
               dict(t, gunluk_sinir_dk=10 ** 30), 100, True)
    uyari_dene("1440 dk (tam bir gun) uyarmiyor",
               dict(t, gunluk_sinir_dk=1440), 100, False)
    uyari_dene("negatif sinir uyariyor",
               dict(t, gunluk_sinir_dk=-60), 100, True)
    uyari_dene("sifresiz aile kipi uyariyor",
               {"kip": "aile", "kilit": {}, "gunluk_sinir_dk": 60}, 100, True)
    uyari_dene("sifresiz BIREYSEL kip uyarmiyor",
               {"kip": "bireysel", "kilit": None}, 100, False)

    # durum.json'a metin yazilinca UYGULAMA ACILMIYORDU. Acilmayan
    # uygulamada aile kipi de dahil hicbir koruma yok - cokme, en
    # sessiz atlatmadir.
    class SayacUyg(SahteUygulama):
        def __init__(self):
            SahteUygulama.__init__(self, {"kip": "aile", "kilit": sifre}, 0)
            self.olculemeyen_sn = 0.0

    import json as _json
    import os as _os
    for etiket, icerik in (("metin hedef", '{"hedef": "cok sonra", '
                            '"kayit_ani": 0, "durum": "calisiyor"}'),
                           ("cop", "{bozuk"),
                           ("bos", "")):
        io.open(gm.DURUM_DOSYA, "w", encoding="utf-8").write(icerik)
        try:
            SayacUyg()._sayaci_geri_yukle()
        except Exception as e:
            hatalar.append("durum.json %s -> COKME %s: %s"
                           % (etiket, type(e).__name__, e))
    try:
        _os.remove(gm.DURUM_DOSYA)
    except OSError:
        pass

    # 4c) KAYIT DOSYASI KURCALANMASI
    #
    # OLCULDU (27.08.2026): aile kipinde %APPDATA%\GozMolasi COCUGUN
    # KENDI klasoru. `_istatistik_oku` dosyadaki JSON'u korlemesine
    # `self.ist.update(veri)` ile birlestiriyordu. Cocuk `ekran_sn`
    # degerini 0 yapinca gunluk sinir TAMAMEN kalkiyordu.
    #
    # BELGELENMIS ATLATMALARDAN FARKI: onlar IZ BIRAKIR.
    #   ayarlar.json'i sil      -> aile kipi kapanir, ebeveyn GORUR
    #   istatistik.json'i duzenle -> kip acik, sifre yerinde, sinir
    #                                yazili, uyari yok. Ebeveyn her
    #                                seyin calistigini SANIR.
    # Sessiz atlatma, gurultulu atlatmadan tehlikelidir.
    #
    # ONLENMIYOR (dosya cocugun klasorunde), GORUNUR KILINIYOR:
    # ekran suresi gun icinde geri gidemez.
    bugun = time.strftime("%Y-%m-%d")
    isaretli = dict(t, gunluk_sinir_dk=60,
                    ekran_isareti={"gun": bugun, "sn": 3700.0})

    def kurcala(ad, dosyadaki, engel_beklenen, uyari_beklenen):
        u = SahteUygulama(isaretli, 0)
        u.ist = {"gun": bugun, "ekran_sn": dosyadaki}
        try:
            u._sayac_isaretini_dogrula()
            tur = (u.engel_sebebi() or ("YOK",))[0]
            uyari = bool(u.ayar_uyarisi())
        except Exception as e:
            hatalar.append("%s -> COKME %s: %s" % (ad, type(e).__name__, e))
            return
        if tur != engel_beklenen:
            hatalar.append("%s -> engel '%s' (beklenen '%s')"
                           % (ad, tur, engel_beklenen))
        if uyari != uyari_beklenen:
            hatalar.append("%s -> uyari %s (beklenen %s)"
                           % (ad, uyari, uyari_beklenen))

    kurcala("sayaci sifirlama yakalaniyor", 0, "sinir", True)
    kurcala("negatif deger yakalaniyor", -999999, "sinir", True)
    kurcala("kucuk deger yakalaniyor", 1, "sinir", True)
    kurcala("metin '0' yakalaniyor", "0", "sinir", True)
    # Tolerans: isaret ve istatistik AYRI anlarda yaziliyor; kucuk bir
    # fark mesrudur ve YANLIS ALARM vermemeli.
    kurcala("tolerans ici dusus yanlis alarm vermiyor", 3670, "sinir", False)
    kurcala("normal ilerleme uyarmiyor", 3800, "sinir", False)

    # BIREYSEL KIPTE CALISMAMALI: kullanici kendi verisinin sahibidir,
    # sifirlamak mesrudur. Koruma, korumasi gerekmeyen yerde davranis
    # degistirmemeli.
    bir = SahteUygulama({"kip": "bireysel", "gunluk_sinir_dk": 60,
                         "ekran_isareti": {"gun": bugun, "sn": 3700.0}}, 0)
    bir.ist = {"gun": bugun, "ekran_sn": 0}
    bir._sayac_isaretini_dogrula()
    if bir.ist["ekran_sn"] != 0:
        hatalar.append("bireysel kipte kertme calisti (%r) - calismamali"
                       % bir.ist["ekran_sn"])
    if bir.ayar_uyarisi():
        hatalar.append("bireysel kipte kurcalama uyarisi cikti")

    # Gun degisince isaret devretmemeli - dunun isareti bugunu engellemez.
    dun = SahteUygulama(dict(t, gunluk_sinir_dk=60,
                             ekran_isareti={"gun": "2020-01-01", "sn": 9999}), 0)
    dun.ist = {"gun": bugun, "ekran_sn": 10}
    dun._sayac_isaretini_dogrula()
    if dun.ist["ekran_sn"] != 10:
        hatalar.append("dunun isareti bugune devretti (%r)" % dun.ist["ekran_sn"])

    # 5) Saat yasağı — gece yarısını aşan aralık
    a = {"yasak_acik": True, "yasak_bas": "21:00", "yasak_bit": "07:00"}
    for saat, beklenen in ((20, False), (21, True), (23, True), (2, True),
                           (6, True), (7, False), (13, False)):
        st = time.struct_time((2026, 8, 26, saat, 0, 0, 2, 238, -1))
        if gm.yasak_saatinde_mi(a, st) != beklenen:
            hatalar.append("saat yasağı %02d:00 -> %s (beklenen %s)"
                           % (saat, not beklenen, beklenen))
    if gm.yasak_saatinde_mi({"yasak_acik": False},
                            time.struct_time((2026, 8, 26, 23, 0, 0, 2, 238, -1))):
        hatalar.append("yasak kapalıyken engel çıktı")

    # 6) Şifre doğrulama ve yükseltme
    dogru, yukselt = kl.dogrula("2468", sifre)
    if not dogru:
        hatalar.append("doğru şifre reddedildi")
    if not yukselt:
        hatalar.append("düşük turlu kayıt yükseltmeye işaretlenmedi")
    if kl.dogrula("9999", sifre)[0]:
        hatalar.append("yanlış şifre kabul edildi")

    # 7) Aile kipi tanımı
    if gm.aile_kipinde_mi({"kip": "aile"}):
        hatalar.append("şifresiz aile kipi geçerli sayıldı")
    if not gm.aile_kipinde_mi({"kip": "aile", "kilit": sifre}):
        hatalar.append("şifreli aile kipi geçersiz sayıldı")

    for s in sinama_yalitim.dogrula():
        hatalar.append(s)

    if hatalar:
        print("BAŞARISIZ — %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("TAMAM — kip, süre sınırı, ek süre, saat yasağı ve şifre doğru.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
