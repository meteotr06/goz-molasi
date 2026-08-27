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
# 27.08.2026: burada ELLE YAZILMIS bir dosya listesi vardi
# (stil|cekirdek|dil|...). Yeni eklenen `kopru.js` listede olmadigi icin
# arac onu HIC damgalamadi: surum v84'e cikti, kopru.js v83'te kaldi.
# Sessiz hataydi - arac "10 baglanti damgalandi" deyip basariyla bitti.
# Yakalayan sey damga_denetle.py'nin yeni tutarlilik denetimi oldu.
#
# Liste yerine DESEN: yereldeki her .js/.css damgalanir. Boylece yeni
# dosya eklerken ikinci bir yeri guncellemeyi unutmak IMKANSIZ.
# Adres icinde egik cizgi olmadigi icin dis baglantilar (https://...)
# eslesmiyor; ikonlar zaten .png.
HEDEF = re.compile(
    r'(src|href)="(\./)?([A-Za-z0-9_-]+\.(?:js|css))(\?s=v\d+)?"'
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

# Damga kaydını bırak: damga_denetle.py bir dosya değişip SURUM aynı
# kaldıysa bunu görüp derlemeyi durduruyor.
try:
    import damga_denetle
    damga_denetle.kaydet()
    print("  damga kaydı güncellendi")
except Exception as e:
    print("  damga kaydı yazılamadı:", e)
