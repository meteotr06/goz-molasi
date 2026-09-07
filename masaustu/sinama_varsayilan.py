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

# 5) AYAR SINIRLARI IKI YERDE YAZILI — AYRISMASINLAR (K-102)
#
#    Motor `SURE_SINIRLARI` ile sinir koyuyor; ayarlar penceresi ise
#    KENDI min/max degerlerini tasiyor. Ikisi ayri yerde yazili ve
#    biri degisince oteki geride kalabilir.
#
#    AYRISMANIN SONUCU SESSIZDIR: form motorun kabul etmedigi bir
#    degeri kabul ederse, o deger o oturum boyunca CANLI calisir ve
#    sonraki acilista `ayarlariSuz` onu -- en yakin sinira degil --
#    VARSAYILANA cevirir. Kullanici ayari kurdugunu sanir, sessizce
#    geri doner. Bu depoda ayni sinif `bostaEsigi` icin bir kez
#    yasandi ve kodda "ayar yalan soyluyordu" diye yaziyor.
#
#    ALAN -> (motor ayari, formun birimi kac saniye)
import re

SINIR_ESLESME = {
    "ayCalisma":  ("calismaSuresi", 60),
    "ayMola":     ("molaSuresi", 1),
    "ayUyari":    ("uyariSuresi", 1),
    "ayUzunSure": ("uzunMolaSuresi", 60),
}

cek = io.open(os.path.join(KOK, "cekirdek.js"), encoding="utf-8").read()
html = io.open(os.path.join(KOK, "index.html"), encoding="utf-8").read()

blok = re.search(r"const SURE_SINIRLARI = \{(.*?)\};", cek, re.S)
bak(blok is not None, "cekirdek.js: SURE_SINIRLARI blogu bulunamadi — "
                      "sinir denetimi HIC kosmadi")
motor_sinir = {}
if blok:
    for ad, az, cok in re.findall(
            r"(\w+):\s*\[\s*([0-9*\s]+),\s*([0-9*\s]+)\]", blok.group(1)):
        motor_sinir[ad] = (eval(az), eval(cok))   # "4 * 3600" gibi

bulunan = 0
for alan, (ayar, carpan) in SINIR_ESLESME.items():
    kutu = re.search(r'<input[^>]*id="%s"[^>]*>' % alan, html)
    if not kutu:
        bak(False, "index.html: `%s` kutusu bulunamadi — "
                   "denetim o alan icin hic kosmadi" % alan)
        continue
    metin = kutu.group(0)
    en_az = re.search(r'min="([-\d.]+)"', metin)
    en_cok = re.search(r'max="([-\d.]+)"', metin)
    if not (en_az and en_cok) or ayar not in motor_sinir:
        continue
    bulunan += 1
    f_az = float(en_az.group(1)) * carpan
    f_cok = float(en_cok.group(1)) * carpan
    m_az, m_cok = motor_sinir[ayar]
    bak(f_az >= m_az and f_cok <= m_cok,
        "index.html/%s formu [%g, %g] sn kabul ediyor, motor `%s` icin "
        "[%g, %g] — form MOTORUN DISINA cikiyor. O deger bir oturum "
        "boyunca canli calisir, sonraki acilista varsayilana doner ve "
        "kullanici ayari kurdugunu sanir."
        % (alan, f_az, f_cok, ayar, m_az, m_cok))

# KENDINI SINAMA: hicbir alan eslesmezse ustteki dongu sessizce
# "temiz" der. Bos bir denetim, temiz bir denetim degildir.
bak(bulunan >= 3,
    "sinir denetimi yalnizca %d alan buldu — kutu adlari degismis "
    "olabilir; denetim gercekte hicbir sey olcmuyor" % bulunan)

if h:
    print("HATA:")
    for x in h:
        print("  -", x)
    sys.exit(1)
print("TAMAM — telefon varsayılanı yerinde, ölçüt `pointer: coarse`,")
print("kullanıcının seçimi korunuyor, değişiklik kaydında anlatılıyor.")
print("Ayar sınırları: form aralıkları motorun kabul ettiği aralığın içinde.")
print("NOT: statik denetim; gerçek telefonda davranışı ÖLÇMEZ.")
