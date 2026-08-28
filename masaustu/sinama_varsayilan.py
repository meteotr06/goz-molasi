# -*- coding: utf-8 -*-
"""Telefon varsayılanı geri masaüstü varsayımına dönmesin.

NİYE VAR
  Kullanıcı aynı hatayı **iki kez** bildirdi: "mobilde sürekli
  sıfırlanıyor". İlkinde eşiği düzelttik (60 sn → 5 dk) ve yetmedi,
  çünkü düzelttiğimiz şey eşikti — **varsayım** değil.

  Varsayım şuydu: "uzun süre uzaklaşmak = gözler dinlendi".
  Bilgisayarda doğru: sekme açık kalır, uzaklaşmak ekrandan kalkmaktır.
  TELEFONDA YANLIŞ: başka uygulamaya geçmek normal kullanımdır ve kişi
  hâlâ ekrana bakıyordur. Kullanıcı 10 dakika mesajlaşıp dönüyor ve
  sayacı sıfırlanmış buluyordu.

  Bu yüzden varsayılan artık cihaza göre: dokunmatikte sıfırlama YOK.

NE ÖLÇÜLÜYOR
  Yalnızca kararın kodda durduğu ve DOĞRU ÖLÇÜTLE verildiği.
  `pointer: coarse` dokunmatik cihazı gösterir; ekran genişliği
  göstermez — dar bir masaüstü penceresi telefon değildir. Genişliğe
  dönülürse bu sınama düşer.

NE ÖLÇÜLMÜYOR
  Gerçek telefonda davranış. Bu statik bir denetim.

ÇALIŞTIR
  python sinama_varsayilan.py
"""
import io
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = []


def bak(kosul, mesaj):
    if not kosul:
        h.append(mesaj)


arayuz = io.open(os.path.join(KOK, "arayuz.js"), encoding="utf-8").read()

# 1) Karar var mı ve doğru ölçütle mi veriliyor
bak("pointer: coarse" in arayuz,
    "arayuz.js: dokunmatik ölçütü (`pointer: coarse`) yok")
bak(re.search(r"uzakSifirla\s*=\s*\(kayit\.uzakSifirla === undefined\)", arayuz),
    "arayuz.js: `uzakSifirla` varsayılanı 'kayıtta yoksa' dalına bağlı değil")
bak("? !dokunmatik" in arayuz,
    "arayuz.js: dokunmatikte varsayılan TERS çevrilmiyor")

# 2) Genişliğe dönülmüş mü — dar masaüstü penceresi telefon değildir
kesit = arayuz[max(0, arayuz.find("const dokunmatik") - 200):
               arayuz.find("const dokunmatik") + 400]
bak("innerWidth" not in kesit and "max-width" not in kesit,
    "arayuz.js: dokunmatik kararı ekran GENİŞLİĞİNE bakıyor — "
    "dar bir masaüstü penceresi telefon değildir")

# 3) Kullanıcının kendi seçimi korunuyor mu
bak("kayit.uzakSifirla !== false" in arayuz,
    "arayuz.js: kullanıcının elle seçimi okunmuyor — "
    "ayarı değiştiren kişi her açılışta varsayılana dönerdi")

# 4) Değişiklik kaydında anlatılıyor mu (sessiz davranış değişikliği olmasın)
js = io.open(os.path.join(KOK, "degisiklikler.js"), encoding="utf-8").read()
bak("Telefonda kapalı" in js or "Telefonda <b>kapalı</b>" in js,
    "degisiklikler.js: telefon varsayılanı anlatılmıyor — "
    "davranış sessizce değişmiş olur")

if h:
    print("HATA:")
    for x in h:
        print("  -", x)
    sys.exit(1)
print("TAMAM — telefon varsayılanı yerinde, ölçüt `pointer: coarse`,")
print("kullanıcının seçimi korunuyor, değişiklik kaydında anlatılıyor.")
print("NOT: statik denetim; gerçek telefonda davranışı ÖLÇMEZ.")
