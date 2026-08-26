# -*- coding: utf-8 -*-
"""SIZINTI DENETİMİ — hangi sınama kullanıcının verisine dokunuyor?

NEDEN VAR
  `sinama_zaman.py` kullanıcının gerçek `ayarlar.json` dosyasına yazdı:
  `kip=aile`, sınama şifresi, 60 dakikalık günlük sınır. O günkü ekran
  süresi 339 dakikaydı; engel ekranı kalıcı açıldı ve **kullanıcının
  bilgisayarı kullanılamaz hâle geldi.**

  O sızıntıyı düzelttik. Ama düzelttiğimiz TEK sınamaydı — diğerlerinde
  de aynı sızıntı olabilir. Kodu okuyup "bu yazmıyor herhalde" demek,
  bu kazanın tam olarak nasıl olduğudur.

NASIL
  Her sınama AYRI BİR SÜREÇTE çalıştırılıyor. Öncesinde ve sonrasında
  kullanıcının gerçek klasörünün parmak izi alınıyor. Bir bayt bile
  değiştiyse o sınama SIZDIRIYOR demektir.

  Okumakla değil ölçmekle karar veriyoruz.

ÇALIŞTIRMA
  python sinama_sizinti.py
"""
import os
import subprocess
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
GERCEK = os.path.join(os.environ.get("APPDATA", ""), "GozMolasi")

# `sinama_acilis.py` BU LİSTEDE YOK ve olmayacak.
# O sınama gerçek exe'yi çalıştırıyor ve gerçek klasöre bayrak
# yazıyor — işi bu. Yalıtılamaz, çünkü yalıtılırsa neyi sınadığı
# kalmaz. Ayrıca uygulamayı AÇIYOR; kullanıcı "bulaşmasın" dediği
# sürece hiç çalıştırılmamalı. Sınırı gizlemek yerine yazıyoruz.
SINANACAKLAR = [
    "sinama_veri.py",
    "sinama_aile.py",
    "sinama_zaman.py",
    "sinama_yerlesim.py",
]


def parmak_izi(klasor):
    if not os.path.isdir(klasor):
        return {}
    iz = {}
    for ad in sorted(os.listdir(klasor)):
        y = os.path.join(klasor, ad)
        try:
            d = os.stat(y)
            iz[ad] = (d.st_size, int(d.st_mtime * 1000))
        except OSError:
            pass
    return iz


def fark(once, sonra):
    sorunlar = []
    for ad in sorted(set(once) | set(sonra)):
        if ad not in once:
            sorunlar.append("OLUŞTURDU: " + ad)
        elif ad not in sonra:
            sorunlar.append("SİLDİ: " + ad)
        elif once[ad] != sonra[ad]:
            sorunlar.append("DEĞİŞTİRDİ: " + ad)
    return sorunlar


def main():
    print("Korunan klasör:", GERCEK)
    print("Dosya sayısı  :", len(parmak_izi(GERCEK)))
    print()

    sizdiran = 0
    for dosya in SINANACAKLAR:
        yol = os.path.join(BURASI, dosya)
        if not os.path.exists(yol):
            print("  %-22s ATLANDI (dosya yok)" % dosya)
            continue

        once = parmak_izi(GERCEK)
        kod = subprocess.call([sys.executable, dosya], cwd=BURASI,
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        sonra = parmak_izi(GERCEK)

        sorunlar = fark(once, sonra)
        if sorunlar:
            sizdiran += 1
            print("  %-22s SIZDIRIYOR" % dosya)
            for s in sorunlar:
                print("      -", s)
        else:
            durum = "temiz" if kod == 0 else "temiz (sınama kaldı)"
            print("  %-22s %s" % (dosya, durum))

    print()
    print("  %-22s ÇALIŞTIRILMADI — uygulamayı açıyor ve gerçek"
          % "sinama_acilis.py")
    print("  %-22s klasöre bayrak yazıyor. İşi bu; yalıtılamaz."
          % "")

    if sizdiran:
        print("\nBAŞARISIZ — %d sınama kullanıcının verisine dokunuyor."
              % sizdiran)
        print("Çözüm: sınamanın başına `sinama_yalitim.yalit(gm)` ekle.")
        return 1
    print("\nTAMAM — hiçbir sınama kullanıcının verisine dokunmuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
