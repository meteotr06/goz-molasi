# -*- coding: utf-8 -*-
"""EXE TAZELİĞİ — kullanıcının çalıştırdığı program güncel mi?

NEDEN VAR
  28.08.2026 gecesi ölçüldü: web sürümü v93 yayındaydı ve gecenin
  bütün işlerine sahipti. Ama kullanıcının çift tıkladığı `.exe`
  26.08 21:53'ten kalmaydı — arada **sekiz commit** masaüstü işi
  vardı ve hiçbiri çalışan programda yoktu:

    köprü · hayalet mola düzeltmesi · aile kipinde yedi sessiz
    atlatma · ebeveyne dürüstlük metni · uyarı genişliği

  Yani ebeveyn kontrolü için yapılan her şey kaynakta duruyordu,
  ebeveynin bilgisayarında durmuyordu.

  > Kaynakta düzeltmek, kullanıcıya ulaştırmak değildir.

  Yayın nöbetçisi bu sınıfı göremez: o `sw.js` damgasını canlıyla
  karşılaştırır, yani YALNIZCA web'i ölçer. Derlenmiş dosya hiç
  sorulmaz. Masaüstü uygulaması olan her projede aynı kör nokta var.

NİYE SINAMA TAKIMINDA DEĞİL
  `sinama.py` derlemeden ÖNCE koşuyor. Bu denetim orada olsaydı her
  derlemeden önce düşerdi — yani kendisini düzeltecek derlemeyi
  engellerdi. Bu ayrı bir soru: "elimdeki exe güncel mi?" Derleme
  akışının değil, kullanma ve yayma akışının sorusu.

ÇALIŞTIRMA
  python exe_tazelik.py          -> insan için rapor
  Çıkış kodu 0 = güncel, 1 = eski. Nöbetçi bunu çağırabilir.
"""
import io
import os
import subprocess
import sys
import time

BURASI = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(BURASI)

# Bunlar derlenip exe'nin içine giriyor. Değişirlerse exe eskir.
IZLENEN_UZANTI = (".py", ".ico", ".png", ".wav")
# Sınama ve araç dosyaları exe'ye girmiyor; onların değişmesi exe'yi
# eskitmez. Yanlış alarm veren denetim, bir süre sonra bakılmayandır.
HARIC_ONEK = ("sinama", "damga_denetle", "surum_ekle", "dunya_uret",
              "ikon_uret", "onizleme_uret", "exe_tazelik")


def exe_bul():
    for ad in sorted(os.listdir(KOK)):
        if ad.lower().endswith(".exe"):
            return os.path.join(KOK, ad)
    return None


def kaynak_dosyalar():
    for ad in sorted(os.listdir(BURASI)):
        if not ad.lower().endswith(IZLENEN_UZANTI):
            continue
        if ad.startswith(HARIC_ONEK):
            continue
        yield os.path.join(BURASI, ad)


def commit_sayisi(andan_beri):
    """exe derlendiğinden beri masaustu/ içinde kaç commit var?"""
    try:
        tarih = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(andan_beri))
        c = subprocess.run(
            ["git", "log", "--oneline", "--since=" + tarih, "--", "masaustu/"],
            cwd=KOK, capture_output=True, text=True, timeout=15)
        satirlar = [s for s in c.stdout.splitlines() if s.strip()]
        return satirlar
    except Exception:
        return None


def main():
    exe = exe_bul()
    if not exe:
        # Ölçemediğimizi gizlemiyoruz.
        print("ÖLÇÜLEMEDİ — kök klasörde .exe yok.")
        print("Derleme yapılmamış olabilir; bu bir hata değil ama")
        print("kullanıcıya verilecek bir program da yok.")
        return 0

    exe_an = os.path.getmtime(exe)
    yeniler = []
    for yol in kaynak_dosyalar():
        an = os.path.getmtime(yol)
        if an > exe_an:
            yeniler.append((os.path.basename(yol), an))

    bicim = lambda a: time.strftime("%d.%m %H:%M", time.localtime(a))
    print("exe    : %s  (%s)" % (os.path.basename(exe), bicim(exe_an)))

    if not yeniler:
        print("SONUÇ  : GÜNCEL — exe'den yeni kaynak dosyası yok.")
        return 0

    yeniler.sort(key=lambda x: -x[1])
    print("SONUÇ  : ESKİ — %d kaynak dosyası exe'den yeni:" % len(yeniler))
    for ad, an in yeniler[:8]:
        print("         %-24s %s" % (ad, bicim(an)))
    if len(yeniler) > 8:
        print("         ... ve %d dosya daha" % (len(yeniler) - 8))

    commitler = commit_sayisi(exe_an)
    if commitler:
        print()
        print("exe derlendiğinden beri masaüstü tarafında %d commit:"
              % len(commitler))
        for s in commitler[:6]:
            print("   ", s)
        if len(commitler) > 6:
            print("    ... ve %d commit daha" % (len(commitler) - 6))

    print()
    print("Kullanıcının çift tıkladığı program bu değişikliklerin")
    print("HİÇBİRİNİ içermiyor. Kaynakta düzeltmek, kullanıcıya")
    print("ulaştırmak değildir.")
    print()
    print("Yapılacak: DERLE.bat")
    print("UYARI: DERLE.bat sonunda uygulamayı AÇAR. Kullanıcının")
    print("       kendi kararı olmadan çalıştırılmaz.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
