# -*- coding: utf-8 -*-
"""GİRDİ SINAMASI — kullanıcının yazdığı sayı ve saat doğru okunuyor mu?

NEDEN VAR
  Bu sınıf hataların hepsi SESSİZ. Çökme gürültü çıkarır, yanlış sayı
  çıkarmaz. Ekranda hata görünmez, sadece yanlış davranış olur.

  Bu projede iki kez yaşandı:
    • Günlük sınır alanı `int(float(metin))` ile okunuyordu. "90,5"
      yazınca ValueError düşüyor, sessizce 0 oluyordu — 0 = SINIR YOK.
      Ebeveyn sınır koyduğunu sanıp hiç koymamış oluyordu.
    • `1,500.50` (İngilizce yazım) 1,5005 okunuyordu. Kuralım "nokta
      hep binliktir" diyordu; bu yalnızca Türkçe yazımda doğru.
      1000 kat hata, hem de sessiz.

  Saat alanları da aynı sınıftaydı: hatalı yazımda sessizce varsayılana
  dönüyor ve "25:00" kabul ediliyordu.

KURAL
  Okunamayan girdi SESSİZCE düzeltilmez. Sessizce düzeltilen girdi,
  kullanıcıya yalan söylemektir.

ÇALIŞTIRMA
  python sinama_girdi.py
"""
import sys

import goz_molasi as gm
import gorunum as gor
import sinama_yalitim

sinama_yalitim.yalit(gm)

# SINAMA-LISTESI.md'deki dokuz yazım + kendi uç durumlarımız
SAYILAR = [
    # (girdi, beklenen, açıklama)
    ("1500",      1500.0,   "düz"),
    ("1500.50",   1500.5,   "İngilizce ondalık"),
    ("1500,50",   1500.5,   "Türkçe ondalık"),
    ("1.500",     1500.0,   "Türkçe binlik"),
    ("1.500,50",  1500.5,   "Türkçe tam"),
    ("1,500.50",  1500.5,   "İngilizce tam — bir kez 1,5005 okundu"),
    ("1 500",     1500.0,   "boşluklu"),
    ("1500 TL",   None,     "birim ekli — reddedilmeli"),
    (" 1500 ",    1500.0,   "kenarda boşluk"),
    ("1.234.567", 1234567.0, "çok basamaklı binlik"),
    ("0",         0.0,      "sıfır"),
    ("-5",        -5.0,     "negatif"),
    ("90,5",      90.5,     "ondalık dakika"),
    ("abc",       None,     "harf — reddedilmeli"),
    ("",          None,     "boş — reddedilmeli"),
    ("...",       None,     "yalnız ayraç — reddedilmeli"),
    # float()/parseFloat() tuzagi — hepsi SESSIZCE sayiya donuyordu
    ("nan",       None,     "NaN — her karsilastirma False, sinir hic uygulanmaz"),
    ("NaN",       None,     "NaN buyuk harf"),
    ("inf",       None,     "sonsuz"),
    ("-inf",      None,     "eksi sonsuz"),
    ("Infinity",  None,     "sonsuz, uzun yazim"),
    ("1e3",       None,     "bilimsel gosterim — kullanici kastetmez"),
    ("1E5",       None,     "bilimsel gosterim buyuk harf"),
    ("1_000",     None,     "alt cizgili — Python kabul ediyordu"),
    ("1,2,3",     None,     "tutarsiz gruplama"),
    ("1.500.5",   None,     "son grup uc hane degil"),
    ("+5",        5.0,      "arti isareti"),
    ("0,30",      0.3,      "sifirla baslayan ondalik"),
    ("1.234.567,89", 1234567.89, "cok gruplu binlik"),
    (",5",        0.5,      "bastaki sifir atlanmis"),
    ("1.",        1.0,      "sondaki ayrac"),
    ("  ",        None,     "yalniz bosluk"),
]

SAATLER = [
    ("21:00", "21:00", "normal"),
    ("9:5",   "09:05", "tek haneli"),
    ("22.30", "22:30", "nokta ile yazılmış"),
    (" 7:00 ", "07:00", "kenarda boşluk"),
    ("00:00", "00:00", "gece yarısı"),
    ("23:59", "23:59", "gün sonu"),
    ("25:00", None,    "geçersiz saat — reddedilmeli"),
    ("12:75", None,    "geçersiz dakika — reddedilmeli"),
    ("10 pm", None,    "İngilizce yazım — reddedilmeli"),
    ("",      None,    "boş — reddedilmeli"),
    ("7",     None,    "yalnız saat — reddedilmeli"),
]


def suzgec_kapsami(hatalar):
    """Istatistik suzgeci UYGULAMANIN KENDI sayac alanlarini koruyor mu?

    Kapsam ELLE YAZILMIYOR: `ist_baslangic()` neyi sayi olarak
    baslatiyorsa suzgec de onu korumak ZORUNDA. Boylece yarin yeni bir
    sayac eklendiginde bu sinama kendiliginden onu da ister.

    NIYE VAR: 29.08.2026'da suzgec elle yazilmis, adlar web surumunden
    cevrilirken kaymisti ("mola"/"atlanan" - uygulamada boyle alan
    yok). Suzgec CALISIYOR gorunuyordu ama iki ana sayaci hic
    gormuyordu; bozuk deger dogrudan panele cikiyordu ("cok", "-5",
    "None"). Sinamanin kendisi elle yazilsaydi ayni kaymayi tekrar
    ederdi - o yuzden kaynak uygulamanin kendi alanlari.

    Doner: yapilan denetim sayisi.
    """
    varsayilan = gm.Uygulama.ist_baslangic()
    sayisal = [a for a, d in varsayilan.items()
               if isinstance(d, (int, float)) and not isinstance(d, bool)]
    if not sayisal:
        hatalar.append("suzgec kapsami: sayisal alan bulunamadi - sinama "
                       "kendi paydasini olcemiyor")
        return 0

    BOZUK = ("cok", None, -5, [1], {}, 10 ** 9)
    n = 0
    for ad in sayisal:
        for deger in BOZUK:
            n += 1
            cikan = gm.Uygulama.istatistik_suz({"gun": varsayilan["gun"],
                                                ad: deger}).get(ad)
            if cikan != 0:
                hatalar.append(
                    "suzgec: '%s' alani bozuk deger %r'yi HAM geciriyor "
                    "(cikan %r, 0 bekleniyordu)" % (ad, deger, cikan))

    # TERS DAL - olcut ayirt edici mi? Gecerli deger BOZULMAMALI.
    n += 1
    saglam = gm.Uygulama.istatistik_suz({"gun": varsayilan["gun"],
                                         sayisal[0]: 7})
    if saglam.get(sayisal[0]) != 7:
        hatalar.append("suzgec: gecerli deger 7 bozuldu (%r) - suzgec "
                       "fazla kirpiyor, olcut ayirt edici degil"
                       % saglam.get(sayisal[0]))

    # Sayac ekranda `str(...)` ile basiliyor: "7" gorunmeli, "7.0" degil.
    n += 1
    if str(saglam.get(sayisal[0])) != "7":
        hatalar.append("suzgec: sayac ekranda '%s' gorunur, '7' "
                       "bekleniyordu" % saglam.get(sayisal[0]))

    print("  %-2d alan x %d bozuk deger + 2 ters dal  %s"
          % (len(sayisal), len(BOZUK), "TAMAM" if not hatalar else "KALDI"))
    return n


def ayar_suzgeci_kapsami(hatalar):
    """Ayar dosyasindaki yanlis TUR uygulamayi acilmadan olduruyor mu?

    NIYE VAR: 29.08.2026'da olculdu - `ayarlari_oku`nun korumasi YALNIZ
    ayristirma hatasina bakiyordu. Gecerli JSON icindeki yanlis tur
    (calisma_dk="20", canlilik=null, tema=[1]) `__init__`in ilk uc
    satirinda cokuyordu ve UYGULAMA HIC ACILMIYORDU. Acilmayan
    uygulamada aile kipi dahil hicbir koruma yok; cokme, en sessiz
    atlatmadir.

    Kapsam ELLE YAZILMIYOR: `gm.VARSAYILAN` neyi sayi/metin olarak
    baslatiyorsa suzgec de onu korumak ZORUNDA. Boylece yarin yeni bir
    ayar eklendiginde bu sinama kendiliginden onu da ister. Ayni gun
    istatistik suzgecinde tam tersi olmustu: kapsam elle yazilmis,
    adlar kaymis, suzgec calisiyor gorunup iki ana sayaci gormemisti.

    Doner: yapilan denetim sayisi.
    """
    if not hasattr(gm, "ayarlari_suz"):
        hatalar.append("ayar suzgeci: `ayarlari_suz` YOK - ayar dosyasindaki "
                       "yanlis tur uygulamayi acilmadan olduruyor")
        return 0

    sayisal = [a for a, d in gm.VARSAYILAN.items()
               if isinstance(d, (int, float)) and not isinstance(d, bool)]
    metinsel = [a for a, d in gm.VARSAYILAN.items() if isinstance(d, str)]
    dogruluk = [a for a, d in gm.VARSAYILAN.items() if isinstance(d, bool)]
    if not sayisal or not metinsel:
        hatalar.append("ayar suzgeci: alan bulunamadi - sinama kendi "
                       "paydasini olcemiyor")
        return 0

    BOZUK_SAYI = ("cok", None, [1], {}, True, float("nan"), float("inf"))
    BOZUK_METIN = (5, None, [1], {}, 1.5)
    n = 0
    for adlar, bozuklar in ((sayisal, BOZUK_SAYI), (metinsel, BOZUK_METIN)):
        for ad in adlar:
            for deger in bozuklar:
                n += 1
                cikan = gm.ayarlari_suz({ad: deger})
                if ad in cikan:
                    hatalar.append(
                        "ayar suzgeci: '%s' alani bozuk deger %r'yi HAM "
                        "geciriyor (cikan %r)" % (ad, deger, cikan[ad]))

    # TERS DAL 1 - olcut ayirt edici mi? Gecerli deger BOZULMAMALI.
    # Fazla kirpan bir suzgec, ayarlari sessizce silen bir suzgectir.
    for ad in sayisal + metinsel:
        n += 1
        beklenen = gm.VARSAYILAN[ad]
        cikan = gm.ayarlari_suz({ad: beklenen})
        if cikan.get(ad, "YOK") != beklenen:
            hatalar.append("ayar suzgeci: gecerli '%s' degeri %r bozuldu (%r)"
                           % (ad, beklenen, cikan.get(ad, "YOK")))

    # TERS DAL 2 - metin yazilmis GECERLI sayi OKUNMALI.
    # Reddetmek gunluk siniri KALDIRIRDI: koruma tarafina dusulur.
    for ad in sayisal:
        n += 1
        beklenen = gm.VARSAYILAN[ad]
        cikan = gm.ayarlari_suz({ad: str(beklenen)})
        if cikan.get(ad, "YOK") != beklenen:
            hatalar.append("ayar suzgeci: metin yazilmis gecerli sayi "
                           "'%s' (%s) okunmadi -> %r"
                           % (beklenen, ad, cikan.get(ad, "YOK")))

    # TERS DAL 3 - DOGRULUK alanlarina dokunulmamali. Bugun hepsi
    # yalnizca dogruluk degeri olarak okunuyor; 1 yazilmis bir dosyada
    # yasagi dusurmek KORUMAYI KALDIRIRDI.
    for ad in dogruluk:
        n += 1
        if gm.ayarlari_suz({ad: 1}).get(ad) != 1:
            hatalar.append("ayar suzgeci: dogruluk alani '%s' 1 degerini "
                           "dusurdu - koruma kaldiran taraf" % ad)

    print("  %-54s %s" % ("ayar suzgeci: %d sayi + %d metin + %d dogruluk alani"
                          % (len(sayisal), len(metinsel), len(dogruluk)),
                          "TAMAM" if not hatalar else "KALDI"))
    return n


def acilis_dayanikligi(hatalar):
    """Bozuk kayit dosyasi UYGULAMAYI ACILMADAN olduruyor mu?

    Uc bulgunun kalici bekcisi (29.08.2026):
      • durum.json / ayarlar.json'daki yanlis tur -> acilis cokuyordu
      • bozuk ya da silinmis ayar dosyasi -> aile kipi SESSIZCE kapaniyordu
      • ayarlari_yaz dogrudan ustune yaziyordu ve hatayi yutuyordu

    Uygulama CALISTIRILMIYOR: yollar `sinama_yalitim` ile gecici
    klasore cevrili, `Uygulama.__init__` atlaniyor.

    Doner: yapilan denetim sayisi.
    """
    import io as _io
    import json as _json
    import os as _os
    import time as _time

    class SahteUyg(gm.Uygulama):
        """__init__ atlanir; yalnizca acilis yollari sinanir."""

        def __init__(self, ayar):
            self.ayar = ayar
            self.ist = {"gun": _time.strftime("%Y-%m-%d"), "ekran_sn": 0}
            self.olculemeyen_sn = 0.0
            self.sayac_oynanmis = False

    def yaz_durum(icerik):
        _io.open(gm.DURUM_DOSYA, "w", encoding="utf-8").write(icerik)

    def yaz_ayar(icerik):
        _io.open(gm.AYAR_DOSYA, "w", encoding="utf-8").write(icerik)

    def temizle():
        for y in (gm.AYAR_DOSYA, gm.DURUM_DOSYA, gm.AYAR_DOSYA + ".bozuk"):
            try:
                _os.remove(y)
            except OSError:
                pass
        durum = getattr(gm, "AYAR_DURUMU", None)
        if isinstance(durum, dict):
            durum.update({"dosya_bozuk": False, "dosya_kayip": False,
                          "bozuk_alanlar": [], "yazilamadi": False})

    n = 0
    temizle()

    # 1) durum.json — yanlis tur acilisi olduruyor mu?
    simdi = _time.time()
    DURUMLAR = (
        ("kayit_ani metin", '{"hedef": %f, "kayit_ani": "dun aksam"}' % (simdi + 300)),
        ("kayit_ani null", '{"hedef": %f, "kayit_ani": null}' % (simdi + 300)),
        ("kayit_ani liste", '{"hedef": %f, "kayit_ani": [1]}' % (simdi + 300)),
        ("ust duzey liste", "[1, 2, 3]"),
        ("ust duzey sayi", "5"),
        ("ust duzey metin", '"metin"'),
        ("hedef metin", '{"hedef": "cok", "kayit_ani": %f}' % simdi),
        ("bozuk JSON", "{yarim"),
        ("bos dosya", ""),
    )
    for etiket, icerik in DURUMLAR:
        n += 1
        yaz_durum(icerik)
        try:
            sonuc = SahteUyg(dict(gm.VARSAYILAN))._sayaci_geri_yukle()
            if not isinstance(sonuc, (int, float)):
                hatalar.append("durum.json %s -> hedef sayi degil (%r)"
                               % (etiket, sonuc))
        except Exception as e:
            hatalar.append("durum.json %s -> ACILIS COKMESI %s: %s"
                           % (etiket, type(e).__name__, e))

    # TERS DAL: saglam durum.json sayaci GERCEKTEN geri yuklemeli.
    n += 1
    yaz_durum(_json.dumps({"hedef": simdi + 300, "kayit_ani": simdi,
                           "durum": "calisiyor"}))
    sonuc = SahteUyg(dict(gm.VARSAYILAN))._sayaci_geri_yukle()
    if not (simdi + 295 <= sonuc <= simdi + 305):
        hatalar.append("saglam durum.json geri yuklenmedi: hedef simdi%+.0f "
                       "sn (beklenen +300) - duzeltme fazla kirpiyor"
                       % (sonuc - simdi))

    # 2) ayarlar.json — yanlis tur acilisi olduruyor mu?
    #    Acilis sirasi: ayarlari_oku -> tema_uygula -> _sayaci_geri_yukle
    sayisal = [a for a, d in gm.VARSAYILAN.items()
               if isinstance(d, (int, float)) and not isinstance(d, bool)]
    metinsel = [a for a, d in gm.VARSAYILAN.items() if isinstance(d, str)]
    for ad in sayisal + metinsel:
        for deger in ("cok", None, [1]):
            n += 1
            yaz_ayar(_json.dumps({ad: deger}))
            try:
                ayar = gm.ayarlari_oku()
                gor.tema_uygula(ayar.get("tema"), ayar.get("canlilik", 1.0))
                SahteUyg(ayar)._sayaci_geri_yukle()
            except Exception as e:
                hatalar.append("ayarlar.json %s=%r -> ACILIS COKMESI %s: %s"
                               % (ad, deger, type(e).__name__, e))
    for etiket, icerik in (("ust duzey liste", "[1,2]"),
                           ("ust duzey sayi", "5"),
                           ("bozuk JSON", "{yarim")):
        n += 1
        yaz_ayar(icerik)
        try:
            ayar = gm.ayarlari_oku()
            gor.tema_uygula(ayar.get("tema"), ayar.get("canlilik", 1.0))
            SahteUyg(ayar)._sayaci_geri_yukle()
        except Exception as e:
            hatalar.append("ayarlar.json %s -> ACILIS COKMESI %s: %s"
                           % (etiket, type(e).__name__, e))

    # 3) BULGU 11 — bozuk/silinmis ayar dosyasi SESSIZ kalmamali.
    #    Aile kipi kaybolurken ekranda iz kalmali; ebeveyn korumanin
    #    surdugunu sanmamali.
    temizle()
    n += 1
    yaz_ayar("{yarim")
    ayar = gm.ayarlari_oku()
    if not SahteUyg(ayar).ayar_uyarisi():
        hatalar.append("bozuk ayar dosyasi SESSIZ gecti - aile kipi "
                       "kayboluyor ama ekranda uyari yok")
    temizle()

    n += 1
    yaz_durum("{}")                       # klasorde baska kayit var
    ayar = gm.ayarlari_oku()              # ayarlar.json YOK
    if not SahteUyg(ayar).ayar_uyarisi():
        hatalar.append("silinmis ayar dosyasi SESSIZ gecti - aile kipi "
                       "kayboluyor ama ekranda uyari yok")
    temizle()

    # TERS DAL: saglam dosya uyarmamali. Yanlis alarm, uyariyi
    # okunmaz hâle getirir.
    n += 1
    yaz_ayar(_json.dumps({"kip": "bireysel", "calisma_dk": 20}))
    ayar = gm.ayarlari_oku()
    uyari = SahteUyg(ayar).ayar_uyarisi()
    if uyari:
        hatalar.append("saglam ayar dosyasi uyari cikardi: %r" % uyari)

    # TERS DAL — YENI UYARI ESKISINI EZMESIN.
    # Ekranda tek satir var, yani sira dogrudan ONCELIKTIR. Olculdu
    # (29.08.2026, denetim): dort dosya uyarisi da en uste konunca
    # `canlilik: "cok"` gibi KOZMETIK bir bozukluk, `kip: aile` +
    # `kilit: null` dosyasinda "Aile kipi sifresiz" uyarisini
    # susturuyordu. Korumanin hic uygulanmadigini soyleyen tek satiri
    # renk ayari yuzunden kaybetmek, duzeltmenin kendi urettigi
    # sessizlesme olurdu.
    temizle()
    n += 1
    yaz_ayar(_json.dumps({"kip": "aile", "kilit": None,
                          "canlilik": "cok", "gunluk_sinir_dk": 60}))
    uyari = SahteUyg(gm.ayarlari_oku()).ayar_uyarisi() or ""
    if "sifresiz" not in uyari.replace("ş", "s").lower():
        hatalar.append("kozmetik bozuk alan SIFRESIZ AILE uyarisini "
                       "eziyor (cikan: %r)" % (uyari,))
    temizle()

    # 4) BULGU 13/15 — atomik yazma ve yutulan yazma hatasi.
    yaz = getattr(gm, "ASIL_AYARLARI_YAZ", None)
    if yaz is None:
        hatalar.append("atomik yazma OLCULEMEDI: sinama_yalitim gercek "
                       "`ayarlari_yaz` islevini saklamiyor")
    else:
        temizle()
        saglam = {"kip": "aile", "gunluk_sinir_dk": 60,
                  "kilit": {"tuz": "t", "ozet": "o"}}
        n += 1
        if yaz(saglam) is not True:
            hatalar.append("saglam ayar yazilamadi (True bekleniyordu)")
        onceki = _io.open(gm.AYAR_DOSYA, encoding="utf-8-sig").read()

        # YARIDA KESILEN YAZMA. Elektrik kesintisini taklit etmek yerine
        # JSON'a cevrilemeyen bir deger koyuyoruz: `json.dump` dosyanin
        # yarisina kadar yazip patlar. Dogrudan ustune yazan bir islev
        # burada ayar dosyasini YARIM birakir - yarim dosya okunamaz,
        # .bozuk'a tasinir, aile kipi ve ebeveyn sifresi birlikte gider.
        n += 1
        sonuc = yaz({"kip": "aile", "gunluk_sinir_dk": 60,
                     "kilit": {"tuz": "t", "ozet": "o"},
                     "cevrilemez": set([1, 2])})
        simdiki = _io.open(gm.AYAR_DOSYA, encoding="utf-8-sig").read()
        if simdiki != onceki:
            hatalar.append("yazma YARIDA kesilince ayar dosyasi bozuldu "
                           "(%d bayt -> %d bayt) - aile kipi ve sifre gider"
                           % (len(onceki), len(simdiki)))
        if sonuc is not False:
            hatalar.append("basarisiz yazma %r dondu (False bekleniyordu) - "
                           "hata yutuluyor" % (sonuc,))
        n += 1
        if not SahteUyg(gm.ayarlari_oku()).ayar_uyarisi():
            hatalar.append("yazma hatasi SESSIZ gecti - ekranda 'kaydedildi' "
                           "gorunurken diskte hicbir sey degismemis olur")
        temizle()

    print("  %-54s %s" % ("acilis dayanikligi: %d durum" % n,
                          "TAMAM" if not hatalar else "KALDI"))
    return n


def main():
    hatalar = []

    print("--- SAYI OKUMA ---")
    # TASMA — 27.08.2026'da olculdu: bicim dogrulamasi "inf" metnini eliyor
    # ama cok uzun rakam dizisi float()'ta tasip inf oluyordu. inf ile yapilan
    # her karsilastirma False doner => sinir SESSIZCE kalkar.
    for uzunluk in (400, 1000):
        girdi = "9" * uzunluk
        if gm.sayi_oku(girdi) is not None:
            hatalar.append("sayi_oku(%d haneli 9) -> %r (beklenen None) [tasma]"
                           % (uzunluk, gm.sayi_oku(girdi)))

    for girdi, beklenen, aciklama in SAYILAR:
        sonuc = gm.sayi_oku(girdi)
        ok = sonuc == beklenen
        if not ok:
            hatalar.append("sayi_oku(%r) -> %r (beklenen %r) [%s]"
                           % (girdi, sonuc, beklenen, aciklama))
        print("  %-12r %-11s %s" % (girdi, sonuc, "TAMAM" if ok else "KALDI"))

    print("--- SAAT OKUMA ---")
    for girdi, beklenen, aciklama in SAATLER:
        sonuc = gm.saat_oku(girdi)
        ok = sonuc == beklenen
        if not ok:
            hatalar.append("saat_oku(%r) -> %r (beklenen %r) [%s]"
                           % (girdi, sonuc, beklenen, aciklama))
        print("  %-12r %-11s %s" % (girdi, sonuc, "TAMAM" if ok else "KALDI"))

    # Sınır değerleri: ±1 birim sonucu sıçratıyor mu?
    print("--- SINIR DEĞERLERİ ---")
    for girdi, beklenen in (("0", 0.0), ("1", 1.0), ("1439", 1439.0),
                            ("1440", 1440.0), ("1441", 1441.0)):
        sonuc = gm.sayi_oku(girdi)
        ok = sonuc == beklenen
        if not ok:
            hatalar.append("sınır %r -> %r" % (girdi, sonuc))
        print("  %-12r %-11s %s" % (girdi, sonuc, "TAMAM" if ok else "KALDI"))

    print("--- ISTATISTIK SUZGECI ---")
    suz_n = suzgec_kapsami(hatalar)

    print("--- AYAR SUZGECI VE ACILIS DAYANIKLIGI ---")
    ayar_n = ayar_suzgeci_kapsami(hatalar)
    ayar_n += acilis_dayanikligi(hatalar)

    for s in sinama_yalitim.dogrula():
        hatalar.append(s)

    if hatalar:
        print("\nBAŞARISIZ — %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("\nTAMAM — %d sayı, %d saat, 5 sınır değeri, "
          "%d süzgeç denetimi, %d açılış denetimi."
          % (len(SAYILAR), len(SAATLER), suz_n, ayar_n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
