# -*- coding: utf-8 -*-
"""SINAMA KOŞUCUSU — bütün masaüstü sınamalarını sırayla çalıştırır.

NEDEN VAR
  Bulunan hataların hepsi gözle bulundu: şerit sayaç kartının içine
  düşmüştü, öneri şeridi kapat düğmesine biniyordu, pencere görev
  çubuğunun altına kaçıyordu, bir derleme hiç açılmıyordu. Hiçbiri
  kullanıcıya ulaşmamalıydı.

  Buradaki fikir basit: DERLE.bat bu koşucuyu çağırır ve sınamalar
  geçmezse uygulamayı AÇMAZ. Bozuk derleme yayına çıkamaz.

SIRALAMA — ucuzdan pahalıya. Veri hatası varsa exe'yi hiç açmaya
gerek yok.
  1. veri     — bilgilerin kaynağı var mı, iki sürüm aynı mı
  2. yerlesim — panelde çakışma / taşma var mı (16 tema x 3 ölçek)
  3. acilis   — derlenen exe gerçekten açılıyor mu

ÇALIŞTIRMA
  python sinama.py            → hepsi
  python sinama.py hizli      → exe açılış sınaması hariç (hızlı)
"""
import os
import subprocess
import sys
import time

BURASI = os.path.dirname(os.path.abspath(__file__))

SINAMALAR = [
    ("sizinti", "sinama_sizinti.py", "Sınamalar kullanıcı verisine dokunuyor mu"),
    ("veri", "sinama_veri.py", "Bilgilerin kaynağı ve sürümler arası tutarlılık"),
    ("degisiklik", "sinama_degisiklik.py", "\"Neler değişti\" bildirimi sessizce kaybolmuş mu"),
    ("damga", "damga_denetle.py", "Dosya değişti mi, sürüm damgası arttı mı"),
    ("girdi", "sinama_girdi.py", "Sayı ve saat okuma (Türkçe yazım dahil)"),
    ("aile", "sinama_aile.py", "Ebeveyn kontrolü: kip, sınır, yasak, şifre"),
    ("kopru", "sinama_kopru.py", "Tarayıcı köprüsü: okuyor mu, fazla açık mı"),
    ("zaman", "sinama_zaman.py", "Sayaç doğruluğu ve saat oyunları"),
    ("yerlesim", "sinama_yerlesim.py", "Panelde çakışma ve taşma"),
    ("acilis", "sinama_acilis.py", "Derlenen exe açılıyor mu"),
]

# Bunlar exe gerektirir; "hizli" kipinde atlanır
EXE_GEREKENLER = {"acilis"}


def main():
    hizli = len(sys.argv) > 1 and sys.argv[1].lower() in ("hizli", "hızlı", "-h")

    print("=" * 62)
    print("GÖZ MOLASI — SINAMA" + (" (hızlı kip)" if hizli else ""))
    print("=" * 62)

    sonuclar = []
    for ad, dosya, aciklama in SINAMALAR:
        if hizli and ad in EXE_GEREKENLER:
            sonuclar.append((ad, "atlandi", 0.0))
            print("\n[%s] ATLANDI — %s" % (ad, aciklama))
            continue

        print("\n[%s] %s" % (ad, aciklama))
        print("-" * 62)
        basladi = time.time()
        kod = subprocess.call([sys.executable, dosya], cwd=BURASI)
        gecen = time.time() - basladi
        sonuclar.append((ad, "TAMAM" if kod == 0 else "BASARISIZ", gecen))

    print("\n" + "=" * 62)
    print("ÖZET")
    print("=" * 62)
    kalan_hata = 0
    for ad, durum, gecen in sonuclar:
        isaret = {"TAMAM": "TAMAM   ", "BASARISIZ": "BASARISIZ",
                  "atlandi": "atlandi "}[durum]
        print("  %-10s %s  %5.1f sn" % (ad, isaret, gecen))
        if durum == "BASARISIZ":
            kalan_hata += 1

    if kalan_hata:
        print("\n%d SINAMA BASARISIZ — bu derleme yayina cikmamali." % kalan_hata)
        return 1
    print("\nHEPSI GECTI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
