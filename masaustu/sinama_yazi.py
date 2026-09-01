# -*- coding: utf-8 -*-
"""BÜYÜK HARF TÜRKÇE'Yİ BOZMASIN — mola kartı başlıkları ve panel yazıları.

NİYE VAR
  Ölçüldü (01.09.2026): mola ekranında gösterilen 39 kart başlığından
  29'u YANLIŞ büyük harfle yazılıyordu. Sebep, Python'un `.upper()`
  işlevinin İngilizce kurallarına göre çalışması:

      "Yakın iş ve miyopi".upper()  ->  "YAKIN IŞ VE MIYOPI"   (yanlış)
      doğrusu                       ->  "YAKIN İŞ VE MİYOPİ"

  Noktalı i büyüyünce noktasız I oluyor; Türkçe'de bu AYRI BİR HARF.
  Uygulama çökmüyor, sayı da yanlış değil — ama kullanıcının her mola
  ekranında gördüğü ilk satır bozuk yazılmış oluyor.

  Küçültme yönü daha sinsi: `"İ".lower()` -> "i" + U+0307 (birleşen
  nokta) verir. Harf gözle "i" görünür ama karşılaştırmada EŞLEŞMEZ;
  arama sessizce boş döner.

NE ÖLÇÜLÜYOR
  1. `gorunum.buyut()` / `gorunum.kucult()` gerçekten Türkçe kurallı mı
     (bilinen tuzak harflerle tek tek).
  2. Kart kaynaklarındaki (BILGILER, IPUCLARI, DUNYA) HER başlık,
     ekranda gösterilen yoldan geçince doğru yazılıyor mu.
  3. Ekrana büyük harf basan yerlerde `.upper()` geri gelmiş mi
     (`goz_molasi.py` içinde çıplak `.upper()` araması).

NE ÖLÇÜLMÜYOR
  Ekranın pikselleri. Bu, metnin kendisini ölçer; yazı tipinin harfi
  çizip çizmediğini değil.

ÇALIŞTIR
  python sinama_yazi.py
"""
import io
import os
import re
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BURASI)

import gorunum as gor
from bilgiler import BILGILER, IPUCLARI
from dunya import DUNYA

h = []


def bak(kosul, mesaj):
    if not kosul:
        h.append(mesaj)


# ---------------------------------------------------------------
# ÖLÇÜT — sınamanın kendi bağımsız doğrusu.
# Bilerek `gorunum.buyut()` ÇAĞRILMIYOR: sınanan işlevi ölçüt olarak
# kullanmak hiçbir şey ölçmez, ikisi de aynı şekilde bozulur.
# ---------------------------------------------------------------
def _dogru_buyuk(s):
    return s.replace(u"i", u"İ").replace(u"ı", u"I").upper()


def _dogru_kucuk(s):
    return s.replace(u"İ", u"i").replace(u"I", u"ı").lower()


# 1) Tuzak harfler tek tek
for kucuk, buyuk in [(u"i", u"İ"), (u"ı", u"I"),
                     (u"is", u"İS"), (u"miyopi", u"MİYOPİ"),
                     (u"ışık", u"IŞIK")]:
    bak(gor.buyut(kucuk) == buyuk,
        u"gorunum.buyut(%r) -> %r, doğrusu %r" % (kucuk, gor.buyut(kucuk), buyuk))

for buyuk, kucuk in [(u"İ", u"i"), (u"I", u"ı"),
                     (u"IŞIK", u"ışık"),
                     (u"İŞ", u"iş")]:
    bak(gor.kucult(buyuk) == kucuk,
        u"gorunum.kucult(%r) -> %r, doğrusu %r" % (buyuk, gor.kucult(buyuk), kucuk))

# Türkçe'ye özgü OLMAYAN harfler bozulmasın (düzeltme fazla ileri gitmesin)
bak(gor.buyut(u"çğöşü") == u"ÇĞÖŞÜ",
    u"gorunum.buyut: ç/ğ/ö/ş/ü bozuldu")
bak(gor.buyut(u"abc") == u"ABC", u"gorunum.buyut: düz ASCII bozuldu")
bak(gor.buyut(u"") == u"", u"gorunum.buyut: boş dizge çökertti")
bak(gor.buyut(None) is None, u"gorunum.buyut(None) çökertti")

# 2) HER kart başlığı — asıl bulgu buydu
yanlis = []
toplam = 0
for kaynak_adi, liste in (("BILGILER", BILGILER), ("IPUCLARI", IPUCLARI),
                          ("DUNYA", DUNYA)):
    for kart in liste:
        baslik = kart[0]
        toplam += 1
        if gor.buyut(baslik) != _dogru_buyuk(baslik):
            yanlis.append(u"[%s] %r -> %r (doğrusu %r)"
                          % (kaynak_adi, baslik, gor.buyut(baslik),
                             _dogru_buyuk(baslik)))

bak(toplam > 0, u"kart kaynakları BOŞ okundu — sınama hiçbir şey ölçmedi")
if yanlis:
    h.append(u"%d/%d kart başlığı yanlış büyütülüyor:" % (len(yanlis), toplam))
    for x in yanlis:
        h.append(u"    " + x)

# 3) Ekrana basan yerlerde çıplak `.upper()` geri gelmiş mi
#
# NEDEN METİN ARAMASI: düzeltme bir işlev çağrısı; birisi ileride
# `gor.buyut(...)` yerine yine `.upper()` yazarsa hiçbir sınama
# düşmez, sadece ekran bozulur. `create_text`/`itemconfigure` ile
# aynı satırda geçen `.upper()` ekrana giden yazıdır.
gm = io.open(os.path.join(BURASI, "goz_molasi.py"), encoding="utf-8").read()
for no, satir in enumerate(gm.splitlines(), 1):
    if ".upper()" not in satir:
        continue
    # `isupper()` bir denetimdir, büyütme değil.
    if re.search(r"\.upper\(\)", satir) and "text=" in satir:
        h.append(u"goz_molasi.py:%d ekrana giden yazıda çıplak `.upper()` "
                 u"— `gor.buyut()` kullanılmalı: %s" % (no, satir.strip()))

if h:
    print("HATA:")
    for x in h:
        print("  -", x)
    sys.exit(1)
print("TAMAM — %d kart başlığının hepsi Türkçe kurallarıyla büyüyor." % toplam)
print("buyut()/kucult() tuzak harflerde (i/İ · ı/I) doğru,")
print("ç/ğ/ö/ş/ü ve ASCII bozulmuyor, ekranda çıplak `.upper()` yok.")
print("NOT: metni ölçer, ekranın piksellerini ÖLÇMEZ.")
