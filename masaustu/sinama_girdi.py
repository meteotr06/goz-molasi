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

    for s in sinama_yalitim.dogrula():
        hatalar.append(s)

    if hatalar:
        print("\nBAŞARISIZ — %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("\nTAMAM — %d sayı, %d saat, 5 sınır değeri, "
          "%d süzgeç denetimi."
          % (len(SAYILAR), len(SAATLER), suz_n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
