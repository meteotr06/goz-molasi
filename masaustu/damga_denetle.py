# -*- coding: utf-8 -*-
"""DAMGA DENETİMİ — dosya değişti ama sürüm damgası aynı mı kaldı?

NEDEN VAR
  `surum_ekle.py`, HTML'deki betik adlarına `?s=v79` gibi bir damga
  basıyor. Damga `sw.js` içindeki SURUM'dan geliyor. Bir dosyayı
  değiştirip SURUM'u artırmayı unutursan damga aynı kalır.

  KİMİ ETKİLER — ölçüldü:
    • Servis işçisi KURULU kullanıcı: etkilenmez. Bizim işçi "önce ağ"
      + `cache: 'no-cache'` çalışıyor, damga aynı olsa da güncel
      dosyayı alıyor. Bunu deneyerek ölçtüm: damgayı artırmadan
      dunya.js'e kayıt ekledim, sayfa yeni kodu okudu.
    • Servis işçisi HENÜZ KURULMAMIŞ kullanıcı (ilk ziyaret, önbellek
      temizlenmiş, işçi kaydı silinmiş): **etkilenir.** Onun için
      tarayıcı önbelleğini kıran tek şey damga.

  Yani bu denetim "her şey bozulur" diye değil, ölçülmüş dar bir
  kitleyi korumak için var. Korkunun büyüklüğünü ölçmeden düzeltmeye
  kalkmıyoruz.

NASIL
  `surum_ekle.py` her çalıştığında damgalanan dosyaların özetini
  `.damga_kayit.json` içine yazar. Bu betik özetleri yeniden hesaplar:
  bir dosya değişmiş ama SURUM aynıysa hata verir.

ÇALIŞTIRMA
  python damga_denetle.py
"""
import hashlib
import io
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYIT = os.path.join(KOK, ".damga_kayit.json")

# surum_ekle.py'nin damgaladığı dosyalar
DAMGALANAN = [
    "stil.css", "cekirdek.js", "dil.js", "bilgiler.js", "bilgiler_en.js",
    "mola_icerik.js", "arayuz.js", "egzersiz.js", "reklam.js", "dunya.js",
]


def surum_oku():
    sw = io.open(os.path.join(KOK, "sw.js"), encoding="utf-8").read()
    m = re.search(r"SURUM\s*=\s*'goz-molasi-(v\d+)'", sw)
    return m.group(1) if m else None


def ozetler():
    d = {}
    for ad in DAMGALANAN:
        y = os.path.join(KOK, ad)
        if not os.path.exists(y):
            continue
        h = hashlib.sha256(open(y, "rb").read()).hexdigest()[:16]
        d[ad] = h
    return d


def kaydet():
    """surum_ekle.py bunu çağırır."""
    io.open(KAYIT, "w", encoding="utf-8").write(json.dumps(
        {"surum": surum_oku(), "ozetler": ozetler()},
        ensure_ascii=False, indent=1) + "\n")


def main():
    surum = surum_oku()
    if not surum:
        print("BAŞARISIZ — sw.js içinde SURUM bulunamadı")
        return 1

    if not os.path.exists(KAYIT):
        kaydet()
        print("İlk kayıt oluşturuldu (%s). Bundan sonra denetlenecek." % surum)
        return 0

    eski = json.load(io.open(KAYIT, encoding="utf-8-sig"))
    simdi = ozetler()

    degisen = [a for a in simdi
               if eski.get("ozetler", {}).get(a) != simdi[a]]

    if not degisen:
        print("TAMAM — damgalanan dosyaların hiçbiri değişmemiş (%s)." % surum)
        return 0

    if eski.get("surum") == surum:
        print("BAŞARISIZ — %d dosya değişti ama SURUM hâlâ %s:"
              % (len(degisen), surum))
        for a in degisen:
            print("  -", a)
        print()
        print("Servis işçisi kurulu olmayan kullanıcı ESKİ kodu görür.")
        print("Yapılacak: sw.js içindeki SURUM'u artır, sonra")
        print("           python masaustu/surum_ekle.py")
        return 1

    kaydet()
    print("TAMAM — %d dosya değişti, SURUM %s -> %s."
          % (len(degisen), eski.get("surum"), surum))
    return 0


if __name__ == "__main__":
    sys.exit(main())
