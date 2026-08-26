# -*- coding: utf-8 -*-
"""HTML'deki yerel dosya bağlantılarına sürüm etiketi ekler.

NEDEN: tarayıcı, önbellek başlığı olmayan dosyaları kendi kafasına göre
saklıyor. Sonuç: güncelleme yayınladıktan sonra kullanıcı bir süre ESKİ
kodu çalıştırıyor. Ölçtüm — servis işçisi kaldırılıp önbellek silindiği
hâlde sayfa eski cekirdek.js'i yüklüyordu.

Çözüm: dosya adının sonuna ?s=<sürüm> eklemek. Sürüm değişince adres de
değişiyor, tarayıcının elindeki kopya geçersiz oluyor.

Sürüm, sw.js içindeki SURUM sabitinden okunuyor; tek yerden yönetiliyor.

Çalıştır:  python surum_ekle.py
"""
import io
import os
import re

KOK = r"D:\Projeler\05 Ekran koruması"
SAYFALAR = ["index.html", "rehber.html", "guide.html", "gizlilik.html"]

# Sürümü sw.js'ten oku
sw = io.open(os.path.join(KOK, "sw.js"), encoding="utf-8").read()
m = re.search(r"SURUM\s*=\s*'goz-molasi-(v\d+)'", sw)
if not m:
    raise SystemExit("sw.js icinde SURUM bulunamadi")
SURUM = m.group(1)
print("surum:", SURUM)

# Sürümlenecek yerel dosyalar (ikonlar hariç — onlar nadiren degisiyor
# ve manifest'ten de referans veriliyor)
HEDEF = re.compile(
    r'(src|href)="(\./)?((?:stil|cekirdek|dil|bilgiler|bilgiler_en|'
    r'mola_icerik|arayuz|egzersiz|reklam|dunya)\.(?:js|css))(\?s=v\d+)?"'
)

for ad in SAYFALAR:
    yol = os.path.join(KOK, ad)
    if not os.path.exists(yol):
        continue
    s = io.open(yol, encoding="utf-8").read()
    yeni, n = HEDEF.subn(
        lambda x: '%s="%s%s?s=%s"' % (x.group(1), x.group(2) or "", x.group(3), SURUM),
        s)
    if n:
        io.open(yol, "w", encoding="utf-8", newline="\n").write(yeni)
    print("  %-14s %d bağlantı" % (ad, n))
