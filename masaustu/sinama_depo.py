# -*- coding: utf-8 -*-
"""Depo erişimi uygulamayı öldürebilir mi? (statik denetim)

NİYE VAR
  Gizli sekmede, site verileri engelliyken ya da kota dolduğunda
  `localStorage` **istisna atar**. Bu istisna açılış sırasında
  yakalanmazsa bütün betik düşer ve uygulama **hiç açılmaz** —
  kullanıcı boş ekran görür. Çökmenin en ağır türü budur: hata
  mesajı bile yok.

  Ölçüldü (28.08.2026): `canlilikOku()` açılışta en üst düzeyde
  çağrılıyordu ve `getItem` çıplaktı. Hemen altındaki `setItem`
  ise `try` ile sarılıydı — yani yazma korunmuş, okuma unutulmuştu.
  Aynı satırın iki yarısı farklı korunuyorsa bu gözden kaçmadır.

NE ÖLÇÜLMÜYOR
  Uygulamanın depo gerçekten bozukken açıldığı. Denendi: çerçevede
  `Storage.prototype` yamalanıyor ama navigasyon yeni bir realm
  yarattığı için yama siliniyor. Yani bu sınama "koruma yazılmış"
  der, "gizli sekmede açılıyor" DEMEZ. Gerçek ölçüm tarayıcının
  gizli kipinde yapılmalı.

ÇALIŞTIR
  python sinama_depo.py
"""
import io
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSYALAR = ["arayuz.js", "cekirdek.js", "dil.js"]
# Yalnızca gerçek erişimler; `localStorage` kelimesinin yorumda geçmesi değil.
ERISIM = re.compile(r"localStorage\s*\.\s*(getItem|setItem|removeItem|clear|key)\b")


def yorum_mu(satir):
    s = satir.strip()
    return s.startswith("//") or s.startswith("*") or s.startswith("/*")


def main():
    korumasiz = []
    toplam = 0
    for ad in DOSYALAR:
        yol = os.path.join(KOK, ad)
        if not os.path.exists(yol):
            continue
        satirlar = io.open(yol, encoding="utf-8").read().split("\n")
        for i, satir in enumerate(satirlar):
            if yorum_mu(satir) or not ERISIM.search(satir):
                continue
            toplam += 1
            # `try` aynı satırda ya da yakın üstte olmalı. Dört satırlık
            # pencere: bu bir metin taraması, JS ayrıştırmıyoruz.
            pencere = "\n".join(satirlar[max(0, i - 4):i + 1])
            if "try" not in pencere:
                korumasiz.append("%s:%d  %s" % (ad, i + 1, satir.strip()[:80]))

    if not toplam:
        print("HİÇ ERİŞİM BULUNAMADI — desen değişmiş olabilir.")
        print("Sıfır sonuç 'temiz' değildir.")
        return 1

    if korumasiz:
        print("KORUMASIZ DEPO ERİŞİMİ: %d / %d" % (len(korumasiz), toplam))
        for x in korumasiz:
            print("  -", x)
        print()
        print("Gizli sekmede bunlar istisna atar. Açılış yolundaysa")
        print("uygulama HİÇ açılmaz.")
        return 1

    print("TAMAM — %d depo erişiminin hepsi try ile korunuyor." % toplam)
    print("NOT: bu statik bir denetim. 'Gizli sekmede açılıyor' DEMEZ;")
    print("onu tarayıcının gizli kipinde ölçmek gerekir.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
