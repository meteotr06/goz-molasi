# -*- coding: utf-8 -*-
"""Yayınlanan dosya kümesi ile sayfanın istediği küme aynı mı?

NİYE VAR
  Merkez 29.08.2026'da Arsa Rehberi'nde şu sınıfı buldu: elle tutulan
  yayın listesi **bayatlamıştı** — dört dosya geriden geliyordu ve
  listenin "gitmeyecek" dediği bir dosya canlıdaydı. Liste harfiyen
  izlenip temiz bir hedefe yayın yapılsaydı sayfa **yine açılırdı**
  ama iki özellik **sessizce yok olurdu**. Açılan bir sayfa, doğru
  yayınlandığının kanıtı değildir.

  Göz Molası'nda liste yok — çalışma ağacının kendisi yayınlanıyor
  (`meteotr06/goz-molasi` ayrı depo). O yüzden soru başka biçim alıyor:

    1. Sayfanın İSTEDİĞİ her dosya depoda VAR mı?
       (yoksa: canlıda 404, özellik sessizce ölür)
    2. Depoda olup KİMSENİN istemediği dosya var mı?
       (varsa: ya ölü ağırlık, ya da sızıntı)

NE ÖLÇÜYOR
  Referansları KAYNAKTAN çıkarıyor: HTML'lerdeki `src`/`href`,
  `sw.js` ön önbellek listesi, manifest'teki ikonlar, ve JS içinde
  geçen `'...js'` / `'...png'` gibi dosya adları.

NE ÖLÇMÜYOR
  Çalışma anında üretilen adresleri (`'ikon-' + boy + '.png'` gibi).
  Bu sınır bilerek kabul edildi; tarayıcıda ölçülen istek listesiyle
  birlikte okunmalı. Ölçüldü (29.08.2026, tarayıcı): sayfa 12 betik +
  `stil.css` + `ikon-192.png` istiyor, hepsi 200.

SIFIR ÖLÇÜM = ÖLÇÜLEMEDİ
  Referans sayısı beklenenin altına düşerse "TAMAM" demiyor.

ÇALIŞTIR
  python sinama_kume.py
"""
import io
import os
import re
import subprocess
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Yayına giden sayfalar
SAYFALAR = ["index.html", "rehber.html", "guide.html", "gizlilik.html"]

# Bu klasörler yayına gitmiyor (Jekyll alt tireyi yayınlamaz; masaustu
# ayrı bir uygulama; docs/ ve md dosyaları belge).
YAYIN_DISI = ("_sinama/", "masaustu/", ".claude/", ".github/")
YAYIN_DISI_UZANTI = (".md", ".py", ".bat", ".exe", ".spec")

# Referans çıkarma kalıpları
KALIP_NITELIK = re.compile(r"""(?:src|href)\s*=\s*["']([^"'#?]+)""")
KALIP_DIZGE = re.compile(r"""["']([A-Za-z0-9_\-./]+\.(?:js|css|png|json|html|svg|ico|txt))["']""")

EN_AZ_REFERANS = 12


def soyle(s=""):
    try:
        print(s)
    except UnicodeEncodeError:
        kod = getattr(sys.stdout, "encoding", None) or "ascii"
        print(s.encode(kod, "replace").decode(kod, "replace"))


def izlenen_dosyalar():
    try:
        c = subprocess.run(["git", "ls-files"], cwd=KOK, capture_output=True,
                           text=True, encoding="utf-8")
        return [y.strip() for y in c.stdout.splitlines() if y.strip()]
    except Exception:
        return []


def yayina_gider(yol):
    y = yol.replace("\\", "/")
    if any(y.startswith(k) for k in YAYIN_DISI):
        return False
    if y.lower().endswith(YAYIN_DISI_UZANTI):
        return False
    if "/" in y:            # alt klasörler (varsa) elle değerlendirilir
        return True
    return True


def _sadelestir(yol):
    """Bastaki `./` ONEKINI atar - `../` KORUNUR.

    `lstrip("./")` KULLANILMAZ: o bir onek degil, KARAKTER KUMESI
    siliyor. `../hesap/` verildiginde bastaki iki nokta ve boluyu de
    yiyip `hesap/` donduruyordu; boylece depo disi komsu baglanti,
    "depoda olmayan dosya" gibi gorunuyordu. Yanlis alarm buradan
    geliyordu (29.08.2026'da olculdu ve duzeltildi).
    """
    y = yol.strip()
    while y.startswith("./"):
        y = y[2:]
    return y


def oku(yol):
    try:
        return io.open(os.path.join(KOK, yol), encoding="utf-8").read()
    except Exception:
        return ""


def main():
    izlenen = izlenen_dosyalar()
    if not izlenen:
        soyle("OLCULEMEDI - `git ls-files` bos dondu (depo yok olabilir).")
        return 1

    yayindakiler = set(y for y in izlenen if yayina_gider(y))

    # ---- Referanslari topla ----
    referans = set()
    kaynaklar = list(SAYFALAR) + ["sw.js", "manifest.json", "manifest.webmanifest"]
    kaynaklar += [y for y in yayindakiler if y.endswith(".js")]
    okunan = 0
    for k in kaynaklar:
        metin = oku(k)
        if not metin:
            continue
        okunan += 1
        for m in KALIP_NITELIK.finditer(metin):
            referans.add(_sadelestir(m.group(1)))
        for m in KALIP_DIZGE.finditer(metin):
            referans.add(_sadelestir(m.group(1)))

    # Dis adresler ve veri adresleri elensin
    referans = set(r for r in referans
                   if not r.startswith(("http", "data:", "blob:", "//")))

    soyle("izlenen dosya   : %d" % len(izlenen))
    soyle("yayina giden    : %d" % len(yayindakiler))
    soyle("okunan kaynak   : %d" % okunan)
    soyle("bulunan referans: %d" % len(referans))
    soyle()

    if len(referans) < EN_AZ_REFERANS:
        soyle("OLCULEMEDI - yalnizca %d referans bulundu, en az %d "
              "bekleniyordu." % (len(referans), EN_AZ_REFERANS))
        soyle("  Kalip artik tutmuyor olabilir; SESSIZ GECMIYORUZ.")
        return 1

    # ---- 1) Istenen ama depoda YOK ----
    #
    # `../` ile baslayanlar DEPO DISINI gosteriyor: alt bilgideki
    # kardes uygulama baglantilari (`../hesap/`, `../planlayici/`...).
    # Bunlar `meteotr06.github.io` altinda AYRI depolarda duruyor;
    # burada olmamalari dogru. Ama unutulmasinlar diye ayri yaziliyor.
    # Olculdu (29.08.2026, canli): alti da 200.
    komsu = sorted(r for r in referans if r.startswith("../"))
    eksik = []          # ne diskte ne depoda
    izlenmeyen = []     # diskte VAR ama depoda YOK -> yayina GITMEZ
    for r in sorted(referans):
        if r.startswith("../"):
            continue
        if r in yayindakiler:
            continue
        if os.path.exists(os.path.join(KOK, r)):
            # DIKKAT: burada "geç" DEMEK YANLIS OLURDU.
            #
            # Bu projede yayin git uzerinden yapiliyor (calisma agaci =
            # yayinlanan kaynak). Diskte duran ama IZLENMEYEN bir dosya
            # yayina HIC GITMEZ: yerelde her sey calisir, canlida 404
            # olur ve ozellik sessizce olur. Tam da Arsa'da yasanan sinif.
            #
            # Ilk yazimda burada `continue` vardi; kasten bozma sinamasi
            # bunu yakaladi - `cekirdek.js`'i depodan dusurdum ve sinama
            # yine "TAMAM" dedi.
            izlenmeyen.append(r)
            continue
        eksik.append(r)

    # ---- 2) Depoda var ama KIMSE istemiyor ----
    istenmeyen = []
    for y in sorted(yayindakiler):
        if y in referans:
            continue
        if y in SAYFALAR:
            continue                      # sayfalar dogrudan aciliyor
        if y in ("sw.js", "manifest.json", "manifest.webmanifest",
                 "robots.txt", "sitemap.xml", "ads.txt", "favicon.ico",
                 ".damga_kayit.json", ".gitignore"):
            continue                      # kok dosyalari: tarayici/arama
        if y.startswith("google") and y.endswith(".html"):
            # Search Console dogrulama dosyasi. Hicbir yerden BAGLANMAZ;
            # Google dogrudan ister. Olculdu (29.08.2026): icerigi tek
            # satirlik dogrulama belirteci, canlida 200.
            continue
        istenmeyen.append(y)

    if eksik or izlenmeyen:
        if eksik:
            soyle("BASARISIZ - sayfanin istedigi %d dosya HIC YOK:" % len(eksik))
            for e in eksik:
                soyle("  - %s" % e)
        if izlenmeyen:
            soyle("BASARISIZ - %d dosya diskte VAR ama depoda IZLENMIYOR:"
                  % len(izlenmeyen))
            for i in izlenmeyen:
                soyle("  - %s" % i)
            soyle("  Yerelde calisir, YAYINA GITMEZ.")
        soyle("  Canlida 404 olur; ozellik SESSIZCE olur.")
        return 1

    soyle("TAMAM - sayfanin istedigi butun dosyalar depoda.")
    if komsu:
        soyle()
        soyle("Depo disi komsu baglanti (%d) - ayri depolarda, canli"
              % len(komsu))
        soyle("olduklari ELLE dogrulanmali (son olcum 29.08.2026: hepsi 200):")
        for k2 in komsu:
            soyle("  - %s" % k2)
    if istenmeyen:
        soyle()
        soyle("NOT - depoda olup hicbir kaynakta ADI GECMEYEN %d dosya:"
              % len(istenmeyen))
        for i in istenmeyen:
            soyle("  - %s" % i)
        soyle("  Bu bir HATA DEGIL: bazilari calisma aninda uretilen")
        soyle("  adreslerle isteniyor olabilir (ornegin ikon boyutlari).")
        soyle("  Ama gozden gecirilmeli: olu agirlik ya da sizinti olabilir.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
