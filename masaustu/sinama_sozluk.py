# -*- coding: utf-8 -*-
"""`C()` ile çevrilen her metin sözlükte var mı?

NİYE VAR
  Çeviri iki yoldan yapılıyor:
    • `CS(tr, en)` — iki dil YAN YANA yazılır, unutulması imkânsız.
    • `C(metin)`   — sözlükten arar; **sözlükte yoksa Türkçesini
      olduğu gibi döndürür.** Sessizce. Hata yok, uyarı yok.

  Yani `C()` ile yazılmış tek bir eksik anahtar, İngilizce arayüzde
  Türkçe bir cümle demek — ve kimse fark etmez, çünkü o metin
  yalnızca belirli bir DURUMDA ekrana gelir.

  Ölçüldü (28.08.2026): ekranda o an duran metinleri taramak
  yetmiyor. `DURUM_ADI` tablosundaki "Boşta — sayaç durdu" gibi
  yazılar yalnızca o duruma girilince çıkıyor; tarama sırasında
  ekranda olmadıkları için hiç denetlenmemişlerdi. (Denetlendi,
  yedisi de sözlükteydi — ama bunu ŞANS belirlememeli.)

  Bu, "ad listesiyle korunan her yer delinir" maddesinin çeviri
  hâli: tek tek bakmak yerine KURAL yazıyoruz.

NE ÖLÇÜLMÜYOR
  Çok satıra bölünmüş `C('...' + '...')` çağrıları. Bunlar ayrıca
  SAYILIP yazılıyor — sessizce atlanmıyorlar. Payda görünür olsun.

ÇALIŞTIR
  python sinama_sozluk.py
"""
import io
import os
import re
import subprocess
import sys

# KONSOL BULGUYU YUTMASIN. Windows konsolu cp1254; bulunan metinde
# `⊕` gibi bir karakter varsa `print` UnicodeEncodeError atiyor
# ve GERCEK BULGU ekrana hic gelmiyor - sinama "coktu" gorunuyor,
# "6 eksik metin var" demiyor. Olculdu: ilk kosuda tam bu oldu.
def soyle(s=""):
    try:
        print(s)
    except UnicodeEncodeError:
        kod = getattr(sys.stdout, "encoding", None) or "ascii"
        print(s.encode(kod, "replace").decode(kod, "replace"))

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def oku(*yol):
    with io.open(os.path.join(KOK, *yol), encoding="utf-8") as d:
        return d.read()


def cevirenler():
    """`C()` çağırabilecek dosyalar KURALDAN türüyor.

    Bu bekçi önce yalnızca `arayuz.js`e bakıyordu ve bugün için
    DOĞRUYDU — ölçüldü (29.08.2026): `C()` çağrısı yalnızca orada var.
    Ama bu doğruluk KURALDAN değil ŞANSTAN geliyordu: yarın
    `mola_icerik.js`e bir `C('…')` eklenirse bekçi onu hiç görmez ve
    yine "TAMAM" der.

    Kapsam artık yayına giden bütün kök `.js` dosyaları; hangilerinin
    tarandığı çıktıya yazılıyor — payda görünmeden sonuç okunmaz.
    """
    try:
        c = subprocess.run(["git", "ls-files", "*.js"], cwd=KOK,
                           capture_output=True, text=True, encoding="utf-8")
        adlar = [y.strip() for y in c.stdout.splitlines() if y.strip()]
    except Exception as e:
        soyle("OLCULEMEDI - `git ls-files` calismadi: %s" % e)
        return []
    return [a for a in adlar
            if "/" not in a.replace("\\", "/")
            and not a.rsplit("/", 1)[-1].startswith("sinama")]


def main():
    dosyalar = cevirenler()
    if not dosyalar:
        soyle("OLCULEMEDI - taranacak dosya listesi bos.")
        return 1
    soyle("taranan dosya : %d (%s)"
          % (len(dosyalar), ", ".join(sorted(dosyalar))))
    try:
        arayuz = "\n".join(oku(a) for a in dosyalar if a != "dil.js")
        dil = oku("dil.js")
    except Exception as e:
        soyle("OLCULEMEDI - dosya okunamadi: %s" % e)
        return 1

    # Sozluk anahtarlari: satir basinda '  'anahtar': ...' bicimi.
    anahtarlar = set(re.findall(r"^\s*'((?:[^'\\]|\\.)*)'\s*:", dil, re.M))
    if len(anahtarlar) < 50:
        soyle("OLCULEMEDI - sozluk beklenenden kucuk (%d anahtar); "
              "bicim degismis olabilir" % len(anahtarlar))
        return 1

    # `C('...')` — ama `CS(` degil. Onunden harf/alt tire gelmemeli.
    tekil = re.findall(r"(?<![A-Za-z_$])C\(\s*'((?:[^'\\]|\\.)*)'\s*\)", arayuz)

    # Kapanmayan (cok satirli / birlestirilmis) cagrilar: sayilsin,
    # sessizce dusmesin.
    coksatir = len(re.findall(r"(?<![A-Za-z_$])C\(\s*'(?:[^'\\]|\\.)*'\s*\+", arayuz))

    eksik = []
    for m in tekil:
        d = m.replace("\\'", "'").strip()
        if not d:
            continue
        if d not in anahtarlar and re.sub(r"\s+", " ", d) not in anahtarlar:
            eksik.append(d)

    # Tekrarlari at, sirayi koru.
    gorulen = set()
    benzersiz = []
    for d in eksik:
        if d not in gorulen:
            gorulen.add(d)
            benzersiz.append(d)

    soyle("sozluk anahtari      : %d" % len(anahtarlar))
    soyle("denetlenen C() metni : %d" % len(tekil))
    soyle("denetlenmeyen (cok satirli C()): %d" % coksatir)

    if benzersiz:
        soyle()
        soyle("BASARISIZ - sozlukte OLMAYAN %d metin "
              "(Ingilizce arayuzde Turkce cikar):" % len(benzersiz))
        for d in benzersiz[:25]:
            soyle("  - %s" % d[:90])
        if len(benzersiz) > 25:
            soyle("  ... ve %d tane daha" % (len(benzersiz) - 25))
        return 1

    soyle()
    soyle("TAMAM - C() ile cevrilen her metin sozlukte var.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
