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
import os
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


# Bu sınamanın denemesi gereken en az durum sayısı.
#
# NEDEN VAR: "belirti yok" ile "dal hiç çalışmadı" aynı yeşili
# gösteriyor. `dene(...)` çağrılarının yarısı silinse bu sınama yine
# "TAMAM" derdi — ve doğruladığı şey, ebeveynin çocuğuna güvenerek
# açtığı koruma. Sayı buranın altına düşerse sonuç okunmaz.
EN_AZ_DURUM = 62


class _TekOrnekAtla(Exception):
    """Tek ornek sinamasi olculemedi - kusur degil, ortam."""


def main():
    hatalar = []
    sayac = {"n": 0}
    sifre = kl.ozet_uret("2468", tur=1000)     # sınama için hızlı tur

    def dene(ad, ayar, ekran_sn, beklenen):
        sayac["n"] += 1
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

    # =================================================================
    # 8) SAAT OYUNUYLA GUN ATLATMA
    # =================================================================
    # OLCULDU (29.08.2026): sistem saatini bir gun ILERI alip geri
    # getirmek gunluk ekran suresi sinirini sifirliyordu. Yonetici hakki
    # gerekmiyor, sinirsiz tekrarlanabiliyor, ekranda hicbir iz yok.
    # `_gunu_tazele` yalnizca "gun etiketi degisti mi" diye bakiyordu;
    # degisimin YONUNU ve o gunun daha once kapanip kapanmadigini hic
    # sormuyordu.
    def gun_kontrol(ad, sart, ayrinti=""):
        sayac["n"] += 1
        if not sart:
            hatalar.append("%s%s" % (ad, (" - " + ayrinti) if ayrinti else ""))
        print("  %-54s %s" % (ad, "TAMAM" if sart else "KALDI"))

    _bugun = time.strftime("%Y-%m-%d")
    _dun = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400))
    _yarin = time.strftime("%Y-%m-%d", time.localtime(time.time() + 86400))

    def gunu_cevir(ist_gun, gecmis_veri=None):
        """Verilen gun etiketiyle `_gunu_tazele` calistirir."""
        gm.gcm.yaz(gm.KAYIT_KLASOR, gecmis_veri or {})
        u = SahteUygulama(dict(t, gunluk_sinir_dk=60), 0)
        u.ist = dict(gm.Uygulama.ist_baslangic(),
                     gun=ist_gun, ekran_sn=7200.0, tamamlanan=9)
        u._istatistik_yaz = lambda: None
        u._gunu_tazele()
        return u

    # Saat yarina alinip geri getirildi: donuste gun GERI gidiyor.
    ileri_geri = gunu_cevir(_yarin)
    gun_kontrol("saat ileri-geri alinca ekran suresi sifirlanmiyor",
                gm.sayi_oku(ileri_geri.ist.get("ekran_sn"), 0) >= 7200,
                repr(ileri_geri.ist.get("ekran_sn")))
    gun_kontrol("gun atlatilinca ekranda uyari cikiyor",
                bool(ileri_geri.ayar_uyarisi()),
                repr(ileri_geri.ayar_uyarisi()))

    # TERS DAL: normal gece yarisi gecisi HALA sifirliyor. Duzeltme
    # fazla kirparsa cocuk ertesi gun de bos yere kilitli kalirdi.
    normal = gunu_cevir(_dun)
    gun_kontrol("normal gun donusunde sayac sifirlaniyor",
                gm.sayi_oku(normal.ist.get("ekran_sn"), -1) == 0,
                repr(normal.ist.get("ekran_sn")))
    gun_kontrol("normal gun donusunde uyari CIKMIYOR",
                not normal.ayar_uyarisi(), repr(normal.ayar_uyarisi()))

    # Bugun bir kez kapanmissa (arsivde kaydi varsa) sayac ARSIVDEN
    # geri gelir - uydurma bir sayi degil, kendi yazdigimiz kayit.
    arsivli = gunu_cevir(_dun, {_bugun: {"mola": 3, "uzun": 1,
                                         "ekran_sn": 5400}})
    gun_kontrol("arsivi olan gune donunce sayac arsivden geliyor",
                gm.sayi_oku(arsivli.ist.get("ekran_sn"), 0) == 5400,
                repr(arsivli.ist.get("ekran_sn")))

    # OKUNAMAYAN ARSIV ALANI SAYACI SIFIRLAMAZ.
    # OLCULDU (30.08.2026, denetim): `_gunu_tazele` once dogrudan
    # `yeni.update(arsiv)` diyordu. Arsiv kaydinin ekran_sn'i bozuk,
    # eksik ya da sinir ustu oldugunda `_gun_sayaclari` o alani hic
    # tasimiyor, alan `ist_baslangic`ten gelen 0'da kaliyordu. Olculen
    # sonuc: sayac 7200 -> 0 ve GUNLUK SINIR ENGELI KALKIYORDU; ustelik
    # ekranda hala "sayaç sıfırlanmadı" yaziyordu. Yani yarim bozuk bir
    # arsiv, hic arsiv olmamasindan KOTUYDU.
    for _ad, _kayit in (
            ("ekran_sn bozuk",   {"mola": 3, "uzun": 1, "ekran_sn": "cok"}),
            ("ekran_sn sinir ustu", {"mola": 3, "uzun": 1, "ekran_sn": 999999}),
            ("ekran_sn eksik",   {"mola": 3, "uzun": 1})):
        _u = gunu_cevir(_yarin, {_bugun: _kayit})
        gun_kontrol("arsivde %s olsa da sayac dusmuyor" % _ad,
                    gm.sayi_oku(_u.ist.get("ekran_sn"), 0) >= 7200,
                    repr(_u.ist.get("ekran_sn")))
        gun_kontrol("arsivde %s olsa da sinir engeli ayakta" % _ad,
                    (_u.engel_sebebi() or ("YOK",))[0] == "sinir",
                    repr(_u.engel_sebebi()))

    # TERS DAL: arsiv OKUNABILIYORSA belirleyici odur - daha DUSUK bir
    # kayit bile gecerlidir. Duzeltme "her zaman buyugunu al" olsaydi
    # baska bir gun etiketi altinda birikmis sayac bugune eklenir,
    # ekrana sisirilmis bir sayi yazilirdi.
    _dusuk = gunu_cevir(_yarin, {_bugun: {"mola": 3, "uzun": 1,
                                          "ekran_sn": 100}})
    gun_kontrol("okunabilen arsiv DUSUK olsa da belirleyici",
                gm.sayi_oku(_dusuk.ist.get("ekran_sn"), -1) == 100,
                repr(_dusuk.ist.get("ekran_sn")))
    gm.gcm.yaz(gm.KAYIT_KLASOR, {})

    # =================================================================
    # 9) BEKCI
    # =================================================================
    # OLCULDU (29.08.2026):
    #   • Gizli soz bekcinin KOMUT SATIRINDA duz metin duruyordu; Gorev
    #     Yoneticisi > Ayrintilar > "Komut satiri" sutunuyla tek adimda
    #     okunuyor, sahte "temiz cikis" bayragi yazilabiliyordu.
    #   • Acilistan ~22 sn icinde oldurulen program yeniden ACILMIYORDU;
    #     art arda iki oldurme bekciyi kalici olarak kaldiriyordu.
    #   • Uygulama bekcinin oldugunu hic fark etmiyordu.
    _yakalanan = []

    class _SahtePopen(object):
        """Gercek surec acmadan komut satirini ve ortami yakalar."""

        def __init__(self, komut, **k):
            _yakalanan.append((list(komut), k.get("env") or {}))
            self.pid = 4242

    class _SahteSub(object):
        Popen = _SahtePopen

    _eski_sub = kl.subprocess
    kl.subprocess = _SahteSub
    try:
        _pid = kl.bekci_baslat(gm.KAYIT_KLASOR)
    finally:
        kl.subprocess = _eski_sub
    _komut, _ortam = (_yakalanan[0] if _yakalanan else ([], {}))
    _komut_metni = " ".join(str(x) for x in _komut)
    _soz = kl._GIZLI_SOZ

    gun_kontrol("bekci PID donduruyor (yasiyor mu olculebilsin)",
                isinstance(_pid, int) and _pid > 0, repr(_pid))
    gun_kontrol("gizli soz KOMUT SATIRINDA gecmiyor",
                bool(_soz) and _soz not in _komut_metni, _komut_metni)
    gun_kontrol("gizli soz bekciye ortamla ulasiyor",
                _ortam.get(kl.SOZ_ORTAM_ADI) == _soz)

    _once = dict(os.environ)
    os.environ[kl.SOZ_ORTAM_ADI] = "deneme-soz"
    _alinan = kl.bekci_sozu_al()
    gun_kontrol("bekci sozu ortamdan okunup SILINIYOR",
                _alinan == "deneme-soz" and kl.SOZ_ORTAM_ADI not in os.environ,
                repr(_alinan))
    os.environ.clear()
    os.environ.update(_once)

    # TERS DAL: taklit bayrak hala reddedilmeli - duzeltme korumayi
    # gevsetmesin.
    _bayrak_yolu = os.path.join(gm.KAYIT_KLASOR, kl.TEMIZ_CIKIS_DOSYA)
    io.open(_bayrak_yolu, "w", encoding="utf-8").write("uydurma")
    gun_kontrol("taklit temiz cikis bayragi hala reddediliyor",
                not kl.temiz_cikis_gecerli_mi(gm.KAYIT_KLASOR, _soz))
    try:
        os.remove(_bayrak_yolu)
    except OSError:
        pass

    # Ayaga kalkmis program erken oldurulurse HER SEFERINDE geri acilir.
    kl._erken_olum_sifirla(gm.KAYIT_KLASOR)
    gun_kontrol("ayaga kalkmis program erken oldurulunce geri aciliyor",
                all(kl.erken_olum_karari(gm.KAYIT_KLASOR, 3.0, True)[0]
                    for _ in range(6)))

    # TERS DAL: hic ayaga kalkamayan program sonsuz donguye sokmamali.
    kl._erken_olum_sifirla(gm.KAYIT_KLASOR)
    _kararlar = [kl.erken_olum_karari(gm.KAYIT_KLASOR, 3.0, False)[0]
                 for _ in range(kl.AZAMI_ERKEN_DENEME + 2)]
    gun_kontrol("acilista coken program once denenip sonra birakiliyor",
                _kararlar[0] and not _kararlar[-1], repr(_kararlar))
    gun_kontrol("bekci pes edince ekranda iz birakiyor",
                kl.bekci_notu_var_mi(gm.KAYIT_KLASOR))
    try:
        os.remove(os.path.join(gm.KAYIT_KLASOR, kl.BEKCI_NOTU))
    except OSError:
        pass
    kl._erken_olum_sifirla(gm.KAYIT_KLASOR)

    # Olen bekci fark ediliyor mu? Gercek surec acmadan olculuyor.
    _pidler = [111, 222]
    _eski_baslat, _eski_yasiyor = kl.bekci_baslat, kl.surec_yasiyor_mu
    kl.bekci_baslat = lambda klasor: _pidler.pop(0)
    kl.surec_yasiyor_mu = lambda p: False
    try:
        b = SahteUygulama(dict(t, bekci=True), 0)
        b._bekciyi_kur()
        _ilk = getattr(b, "_bekci_pid", None)
        b._bekci_denemesi = -1e9          # deneme araligini atla
        b._bekciyi_kur()
        _ikinci = getattr(b, "_bekci_pid", None)
    finally:
        kl.bekci_baslat, kl.surec_yasiyor_mu = _eski_baslat, _eski_yasiyor
    gun_kontrol("olen bekcinin yerine yenisi kuruluyor",
                _ilk == 111 and _ikinci == 222,
                "%r -> %r" % (_ilk, _ikinci))

    # TERS DAL: yasayan bekcinin yerine YENISI kurulmamali.
    _eski_yasiyor2 = kl.surec_yasiyor_mu
    kl.surec_yasiyor_mu = lambda p: True
    try:
        b._bekci_denemesi = -1e9
        b._bekciyi_kur()
        _ucuncu = getattr(b, "_bekci_pid", None)
    finally:
        kl.surec_yasiyor_mu = _eski_yasiyor2
    gun_kontrol("yasayan bekci bosuna yeniden kurulmuyor",
                _ucuncu == _ikinci, repr(_ucuncu))

    for s in sinama_yalitim.dogrula():
        hatalar.append(s)

    # ---------- Tek ornek korumasi ----------
    #
    # Ikinci kopya acilabilseydi iki surec AYNI istatistik dosyasina
    # yazardi: ekran suresi cift sayilir, gunluk sinir asilir ve aile
    # kipi korumasi delinirdi. Web tarafinda ayni sinif "iki sekme"
    # olarak cikmisti (v133/v144); masaustundeki karsiligi bu.
    #
    # IKI CAGRI DA AYRI SURECTE YAPILIR - bu sart.
    # Ilk yazimda ilk cagriyi BU surecte yapmistim; mutex'i sinamanin
    # kendisi tutuyordu ve cocuk her hâlukârda False goruyordu. Yani
    # sinama, TUTUCUYU HIC OLCMEDEN geciyordu. Kasten bozunca
    # (tutucuya baska mutex adi verdim) yine "TAMAM" demesi ele verdi.
    #
    # Bu blok `if hatalar:` denetiminden ONCE durmali; sonrasina
    # konursa icindeki hata sessizce yutulur (o da ilk yazimda oldu).
    try:
        import subprocess
        sayac["n"] += 1
        burasi = os.path.dirname(os.path.abspath(__file__))
        cagri = ("import sys;sys.path.insert(0, r'" + burasi + "');"
                 "import kilit as kl;print(kl.tek_ornek_al());")

        # A: ilk kopya - mutex'i alir ve tutar.
        #
        # SABIT BEKLEME YOK. Once `time.sleep(1.5)` vardi ve ilk
        # kopyanin o sure icinde mutex'i aldigi VARSAYILIYORDU. Makine
        # mesgulken (tarayici, derleme) yetmiyor; o zaman ikinci kopya
        # da mutex'i aliyor ve sinama "koruma yok" diye RASTGELE
        # kirmizi veriyordu. Iki kez yasandi (01.09.2026), dort kosuda
        # tekrarlamadi - yani kusur uründe degil, sinamanin zamanlama
        # varsayimindaydi.
        #
        # Artik ilk kopya sonucu yazinca O SATIR bekleniyor: varsayim
        # yerine ISARET.
        a = subprocess.Popen([sys.executable, "-c",
                              cagri + "sys.stdout.flush();"
                              "import time;time.sleep(8)"],
                             stdout=subprocess.PIPE, text=True)
        ilk = ""
        try:
            import threading
            kutu = {}

            def oku():
                kutu["s"] = (a.stdout.readline() or "").strip()

            t = threading.Thread(target=oku, daemon=True)
            t.start()
            t.join(10)                     # en cok 10 sn bekle
            ilk = kutu.get("s", "")
        except Exception:
            pass

        # ILK KOPYA MUTEX'I ALAMADIYSA asagidaki karsilastirma anlamsiz.
        # "Koruma yok" demek yerine "olculemedi" demek dogru: yanlis
        # sebeple kirmizi vermek, kirmizi vermemekten iyi degil.
        if ilk != "True":
            a.terminate()
            hatalar.append("tek ornek OLCULEMEDI: ilk kopya mutex'i "
                           "alamadi (%r) - makine mesgul olabilir" % ilk)
            print("  %-54s %s" % ("ikinci kopya acilamiyor (tek ornek)",
                                  "OLCULEMEDI"))
            raise _TekOrnekAtla()

        # B: ikinci kopya - False gormeli
        b = subprocess.run([sys.executable, "-c", cagri],
                           capture_output=True, text=True)
        ikinci = (b.stdout or "").strip()
        a.terminate()

        tamam = (ikinci == "False")
        if not tamam:
            hatalar.append(
                "tek ornek: ikinci kopya %r dondu (False bekleniyordu); "
                "ilk kopya %r" % (ikinci, ilk))
        print("  %-54s %s" % ("ikinci kopya acilamiyor (tek ornek)",
                              "TAMAM" if tamam else "KALDI"))
    except _TekOrnekAtla:
        pass
    except Exception as e:
        hatalar.append("tek ornek SINANAMADI: %s: %s" % (type(e).__name__, e))
        print("  %-54s %s" % ("ikinci kopya acilamiyor (tek ornek)",
                              "OLCULEMEDI"))

    # ---------- Kip adinin YAZIMI ----------
    #
    # Ayar dosyasi elle duzenlenebiliyor ve Turkce'nin i/I sorunu
    # yuzunden ayni kelimenin iki buyuk harf yazimi FARKLI sonuc
    # veriyordu:
    #     "AILE".lower() -> "aile"    eslesiyordu
    #     "AILE".lower() -> "ai" + birlesen nokta + "le"   ESLESMIYORDU
    # (ikincisi Turkce buyuk I ile yazilmis hali). Yani oyle yazan
    # ebeveynde aile kipi SESSIZCE uygulanmiyor, ayar ekrani ise "Aile"
    # secili gosteriyordu. En kotu hal: koruma yok ama var gorunuyor.
    #
    # Ters dal da olculuyor: aile DISI degerler aile sayilmamali. Yoksa
    # "hepsine evet diyen" bir eslestirici de bu sinamayi gecerdi.
    ESLESMELI = ("aile", "Aile", "AILE", "A\u0130LE", " Aile ", "AiLe")
    ESLESMEMELI = ("bireysel", "Bireysel", "B\u0130REYSEL", "", "aileler",
                   None, 5)

    def _kip_ayari(k):
        return {"kip": k, "kilit": "x" * 40, "kilit_tuz": "y" * 16}

    for _y in ESLESMELI:
        sayac["n"] += 1
        if not gm.aile_kipinde_mi(_kip_ayari(_y)):
            hatalar.append("kip yazimi: %r aile kipi sayilmadi "
                           "(koruma sessizce uygulanmaz)" % (_y,))
    for _y in ESLESMEMELI:
        sayac["n"] += 1
        if gm.aile_kipinde_mi(_kip_ayari(_y)):
            hatalar.append("kip yazimi: %r aile kipi SAYILDI "
                           "(olcut ayirt edici degil)" % (_y,))
    print("  %-54s %s" % ("kip adi her yazimda dogru eslesiyor",
                          "TAMAM" if not hatalar else "KALDI"))

    if hatalar:
        print("denenen durum : %d" % sayac["n"])
        print("BAŞARISIZ — %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("denenen durum : %d" % sayac["n"])
    if sayac["n"] < EN_AZ_DURUM:
        print("ÖLÇÜLEMEDİ — yalnızca %d durum denendi, en az %d bekleniyordu."
              % (sayac["n"], EN_AZ_DURUM))
        print("  Durumlar silinmiş ya da bir dal hiç çalışmamış olabilir.")
        print("  SESSİZ GEÇMİYORUZ: bu sınama aile korumasını doğruluyor.")
        return 1
    print("TAMAM — %d durum denendi; kip, süre sınırı, ek süre, saat yasağı "
          "ve şifre doğru." % sayac["n"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
