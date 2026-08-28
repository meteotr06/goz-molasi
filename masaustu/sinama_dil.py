# -*- coding: utf-8 -*-
"""Ekrana yazılan Türkçe metin çeviriden GEÇİYOR mu?

NİYE VAR — SÖZLÜK BEKÇİSİNİN GÖREMEDİĞİ YER
  `sinama_sozluk.py` şunu soruyor: "`C()` ile çevrilen her metin
  sözlükte var mı?" Ama bir metin **hiç `C()`'ye uğramıyorsa** o
  soru hiç sorulmuyor. Yani:

      og.durum.textContent = 'Açık — sekme arka plandayken…';

  satırı sözlük denetiminden **görünmez** geçer ve İngilizce
  arayüzde olduğu gibi Türkçe çıkar.

  Ölçüldü (28.08.2026): tam dört tane vardı — tanıtımdaki örnek
  mola yazısı ve cihaz etkinliği izninin üç durumu (desteklenmiyor
  / açık / kapalı). Dördü de kullanıcıya görünen yazılardı.

  `sayfayiCevir()` de bunları kurtarmıyor: o, sayfa kurulurken bir
  kez geziyor. Bu yazılar ÇALIŞMA ANINDA yazılıyor.

NE ÖLÇÜYOR
  `arayuz.js` içinde `.textContent = '…'` gibi doğrudan atamalarda
  Türkçe'ye özgü harf geçiyor mu — ve o metin `C()` / `CS()`
  içinden mi geliyor.

NE ÖLÇMÜYOR
  İngilizce karşılığın DOĞRU olduğunu. Yalnızca çeviri yolundan
  geçtiğini ölçer.

  Ayrıca Türkçe'ye özgü harf içermeyen bir Türkçe cümleyi
  (ör. "Tamam") göremez. Bu sınır bilerek kabul edildi: alternatifi
  her dizgeyi elle işaretlemekti.

SIFIR ÖLÇÜM = ÖLÇÜLEMEDİ
  Bakılan atama sayısı yazdırılıyor. Sayı beklenmedik biçimde
  düşerse (biçim değişmiş, kalıp tutmuyor) sınama "TAMAM" demez,
  "ÖLÇÜLEMEDİ" der — sessizce geçmek, kaçırılan hatadan kötüdür.

ÇALIŞTIR
  python sinama_dil.py
"""
import io
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Turkce'ye ozgu harfler
TR_HARF = re.compile(u"[çğıöşü"
                     u"ÇĞİÖŞÜ]")

# Ciplak dizge atamasi: `.textContent = 'metin'`
KALIP = re.compile(
    r"\.(textContent|innerHTML|placeholder|title|ariaLabel|value)"
    r"\s*=\s*(['\"])((?:(?!\2).){4,})\2")

# Ekrana yazan HER atama - PAYDA bu.
TUM_KALIP = re.compile(
    r"\.(textContent|innerHTML|placeholder|title|ariaLabel)\s*=")

# PAYDA DOGRU SECILMELI.
#
# Ilk yazdigimda paydayi "ciplak dizge atamasi" yapmistim - yani tam da
# OLMAMASI gereken sey. Dordunu duzeltince sayi 2'ye dustu ve sinama
# "olculemedi" dedi: kendi basarim, olcumu bozdu. Payda, BOL olmasi
# beklenen seye baglanmali - ekrana yazan butun atamalar.
EN_AZ_ATAMA = 20


def soyle(s=""):
    try:
        print(s)
    except UnicodeEncodeError:
        kod = getattr(sys.stdout, "encoding", None) or "ascii"
        print(s.encode(kod, "replace").decode(kod, "replace"))


def main():
    yol = os.path.join(KOK, "arayuz.js")
    try:
        k = io.open(yol, encoding="utf-8").read()
    except Exception as e:
        soyle("OLCULEMEDI - arayuz.js okunamadi: %s" % e)
        return 1

    tumu = TUM_KALIP.findall(k)
    if len(tumu) < EN_AZ_ATAMA:
        soyle("OLCULEMEDI - ekrana yazan yalnizca %d atama goruldu "
              "(en az %d bekleniyordu). Kalip artik tutmuyor olabilir; "
              "SESSIZ GECMIYORUZ." % (len(tumu), EN_AZ_ATAMA))
        return 1

    atamalar = list(KALIP.finditer(k))

    ciplak = []
    for m in atamalar:
        metin = m.group(3)
        if not TR_HARF.search(metin):
            continue
        satir = k[:m.start()].count("\n") + 1
        ciplak.append((satir, m.group(1), metin))

    soyle("ekrana yazan atama : %d" % len(tumu))
    soyle("ciplak dizge       : %d" % len(atamalar))
    soyle("Turkce harf iceren : %d" % len(ciplak))

    if ciplak:
        soyle()
        soyle("BASARISIZ - %d metin ceviriden GECMEDEN ekrana yaziliyor "
              "(Ingilizce arayuzde Turkce cikar):" % len(ciplak))
        for satir, alan, metin in ciplak[:20]:
            soyle("  - arayuz.js:%d  .%s = %s" % (satir, alan, metin[:70]))
        soyle()
        soyle("Yapilacak: metni `CS('tr', 'en')` ile sar (calisma aninda")
        soyle("           yazilan metinler icin) ya da `C()` + sozluk.")
        return 1

    soyle()
    soyle("TAMAM - ekrana dogrudan yazilan Turkce metin yok.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
