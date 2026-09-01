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
    ("depo", "sinama_depo.py", "Gizli sekmede depo istisnası uygulamayı öldürür mü"),
    ("surum", "sinama_surum.py",
     "Kod, degisiklik kaydi ve yayin ayni surumu mu soyluyor"),
    ("kume", "sinama_kume.py",
     "Yayindaki dosya kumesi sayfanin istedigiyle ayni mi"),
    ("dil", "sinama_dil.py",
     "Ekrana yazilan Turkce metin ceviriden geciyor mu"),
    ("sozluk", "sinama_sozluk.py",
     "C() ile cevrilen her metin sozlukte var mi"),
    ("yazi", "sinama_yazi.py",
     "Buyuk harf Turkce'yi bozuyor mu (i/İ · ı/I)"),
    ("yayin", "sinama_yayin.py", "İç sınama sayfası depoda izleniyor mu (yayına sızar)"),
    ("varsayilan", "sinama_varsayilan.py", "Telefon varsayılanı masaüstü varsayımına dönmüş mü"),
    ("damga", "damga_denetle.py", "Dosya değişti mi, sürüm damgası arttı mı"),
    ("girdi", "sinama_girdi.py", "Sayı ve saat okuma (Türkçe yazım dahil)"),
    ("aile", "sinama_aile.py", "Ebeveyn kontrolü: kip, sınır, yasak, şifre"),
    ("kopru", "sinama_kopru.py", "Tarayıcı köprüsü: okuyor mu, fazla açık mı"),
    ("zaman", "sinama_zaman.py", "Sayaç doğruluğu ve saat oyunları"),
    ("yerlesim", "sinama_yerlesim.py", "Panelde çakışma ve taşma"),
    ("acilis", "sinama_acilis.py", "Derlenen exe açılıyor mu"),
    ("ekran", "ekran_denetle.py",
     "Kullanıcının GÖRDÜĞÜ ekran: yasak metin, 44 px, taşma, JS hatası"),
]

# Bunlar exe gerektirir; "hizli" kipinde atlanır
EXE_GEREKENLER = {"acilis"}

# Tarayıcı açar, ~2 dk sürer; "hizli" kipinde atlanır.
# TAM koşuda zorunlu: 30.08.2026'da telefonda bulunan dört kusurun
# DÖRDÜ de motor sınamalarını geçmişti, yalnızca ekranda görülüyordu.
YAVASLAR = {"ekran"}


def main():
    hizli = len(sys.argv) > 1 and sys.argv[1].lower() in ("hizli", "hızlı", "-h")

    print("=" * 62)
    print("GÖZ MOLASI — SINAMA" + (" (hızlı kip)" if hizli else ""))
    print("=" * 62)

    sonuclar = []
    for ad, dosya, aciklama in SINAMALAR:
        if hizli and (ad in EXE_GEREKENLER or ad in YAVASLAR):
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
        # ADI DA YAZ. Olculdu (30.08.2026): son satir yalniz sayi
        # soyluyordu ve ozet listesi yukarida kaldigi icin ciktinin
        # sonuna bakan hangi sinamanin dustugunu goremiyordu -
        # DERLE.bat'i izleyen kullanici dahil. Adi bulmak uc kosu aldi,
        # o arada hata bir daha cikmadi. Son satir tek basina okunabilir
        # olmali.
        dusenler = [a for a, d, _ in sonuclar if d == "BASARISIZ"]
        print("\n%d SINAMA BASARISIZ (%s) — bu derleme yayina cikmamali."
              % (kalan_hata, ", ".join(dusenler)))
        # Dosya adini SINAMALAR'dan al, uydurma: "damga" sinamasinin
        # dosyasi damga_denetle.py, sinama_damga.py degil. Yanlis komut
        # veren bir mesaj, mesaj olmamasindan daha kotu.
        dosyalar = {a: d for a, d, _ in SINAMALAR}
        for a in dusenler:
            print("  ayrintisi: python masaustu/%s" % dosyalar.get(a, "sinama.py"))
        return 1
    print("\nHEPSI GECTI.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
