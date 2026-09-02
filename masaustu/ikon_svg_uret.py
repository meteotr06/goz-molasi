# -*- coding: utf-8 -*-
"""SİMGENİN TEK KAYNAĞI — buradan üretilir, elle çizilmez.

NEDEN BU DOSYA VAR
  01.09.2026'da yayınlanan simgenin kaynağı GEÇİCİ bir klasördeydi.
  Yani yayında duran esere karşılık gelen çizim depoda yoktu: kimse
  yeniden üretemez, bir rengi değiştiremez, küçük bir düzeltme
  yapamazdı. Bu, "üreteç ile eser sessizce ayrışıyor" sınıfının en
  ağır hâli — üreteç hiç yok.

  Aynı sınıfın hafif hâli bu depoda zaten yaşandı: `ikon_uret.py`
  ESKİ tasarımı çiziyordu, yayındaki simge yeniydi. O betik artık
  bayrak istiyor (kazara çalıştırılıp üstüne yazmasın diye).

TASARIM
  Şekil SVG'de, bezier eğrileriyle. Python'un çizim aracıyla yapılan
  üç tur "el yapımı" durdu; eğri, gradyan ve gölge tarayıcıda gerçek.
  İşleme BAŞSIZ EDGE ile: makinede zaten kurulu, indirme gerekmiyor.

  Maskelenebilir sürüm KARE ve içerik %78'e çekilmiş: Android kendi
  maskesini uyguluyor, kenara yakın şekil kırpılır.

ÇALIŞTIRMA
  python ikon_svg_uret.py          → üretir ve YAZAR
  python ikon_svg_uret.py --olc    → üretir, yazmaz, mevcutla KARŞILAŞTIRIR

  `--olc` kipi "üreteç ile eser ayrışmış mı" sorusunun cevabıdır.
"""
import io
import os
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(BURASI)

# --- ÇİZİM ------------------------------------------------------------
# Badem göz: iki kübik bezier. Eğriler elle değil, simetrik.
BADEM = ("M 118 256 C 176 156, 336 156, 394 256 "
         "C 336 356, 176 356, 118 256 Z")

# Koyu zemin + açık göz + nane iris. Kullanıcı beş turdan sonra seçti.
ZEMIN = ('<linearGradient id="zem" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="#1B4A5C"/>'
         '<stop offset="1" stop-color="#0A2430"/></linearGradient>')

GOZ = """
  <g filter="url(#yumusak)">
    <path d="%s" fill="#F6FBF8"/>
    <circle cx="256" cy="256" r="62" fill="#12312C"/>
    <circle cx="256" cy="256" r="27" fill="#54E0AC"/>
    <circle cx="236" cy="236" r="12" fill="#FFFFFF" opacity="0.85"/>
  </g>""" % BADEM


def svg(kose, olcek=1.0):
    """kose: köşe yarıçapı (0 = kare, maskelenebilir sürüm)."""
    kaydir = (1 - olcek) * 256
    return """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"
     viewBox="0 0 512 512">
  <defs>
    %s
    <filter id="yumusak" x="-30%%" y="-30%%" width="160%%" height="160%%">
      <feDropShadow dx="0" dy="10" stdDeviation="14"
                    flood-color="#04241d" flood-opacity="0.30"/>
    </filter>
    <clipPath id="kirp"><rect width="512" height="512" rx="%d" ry="%d"/></clipPath>
  </defs>
  <g clip-path="url(#kirp)">
    <rect width="512" height="512" fill="url(#zem)"/>
    <g transform="translate(%s,%s) scale(%s)">%s</g>
  </g>
</svg>""" % (ZEMIN, kose, kose, kaydir, kaydir, olcek, GOZ)


def uret(gecici):
    """SVG'leri PNG'ye işler. Döner: (buyuk_yol, maskeli_yol) ya da None."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, "playwright kurulu değil"
    try:
        with sync_playwright() as p:
            t = p.chromium.launch(channel="msedge")
            s = t.new_page(viewport={"width": 512, "height": 512})

            def cek(kod, yol):
                s.set_content('<body style="margin:0">%s</body>' % kod)
                s.wait_for_timeout(220)
                s.screenshot(path=yol, omit_background=True)

            buyuk = os.path.join(gecici, "ikon-buyuk.png")
            maskeli = os.path.join(gecici, "ikon-maskeli-ham.png")
            cek(svg(118), buyuk)
            cek(svg(0, 0.78), maskeli)      # KARE + içerik %78
            t.close()
        return (buyuk, maskeli), None
    except Exception as e:
        return None, "tarayıcı açılamadı: %s" % str(e).splitlines()[0][:70]


def main():
    olc = "--olc" in sys.argv
    import tempfile
    gecici = tempfile.mkdtemp()
    sonuc, hata = uret(gecici)
    if hata:
        print("ATLANDI — %s" % hata)
        return 0
    buyuk, maskeli = sonuc

    from PIL import Image
    kaynak = Image.open(buyuk).convert("RGBA")
    hedefler = [
        (os.path.join(KOK, "ikon-192.png"), kaynak.resize((192, 192), Image.LANCZOS)),
        (os.path.join(KOK, "ikon-512.png"), kaynak.resize((512, 512), Image.LANCZOS)),
        (os.path.join(KOK, "ikon-maskeli.png"), Image.open(maskeli).convert("RGBA")),
    ]

    farkli = []
    for yol, im in hedefler:
        yeni = os.path.join(gecici, os.path.basename(yol))
        im.save(yeni)
        eski_var = os.path.exists(yol)
        ayni = False
        if eski_var:
            ayni = (io.open(yol, "rb").read() == io.open(yeni, "rb").read())
        if olc:
            print("  %-18s %s" % (os.path.basename(yol),
                                  "AYNI" if ayni else
                                  ("FARKLI" if eski_var else "YOK")))
            if not ayni:
                farkli.append(os.path.basename(yol))
        else:
            im.save(yol)
            print("  %-18s yazildi (%d bayt)"
                  % (os.path.basename(yol), os.path.getsize(yol)))

    ico = os.path.join(BURASI, "ikon.ico")
    if not olc:
        kaynak.resize((256, 256), Image.LANCZOS).save(
            ico, format="ICO",
            sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64),
                   (128, 128), (256, 256)])
        print("  %-18s yazildi (%d bayt)" % ("ikon.ico", os.path.getsize(ico)))

    if olc:
        print()
        if farkli:
            print("URETEC ILE ESER AYRISMIS — %d dosya: %s"
                  % (len(farkli), ", ".join(farkli)))
            print("Yayindaki simge bu betikten uretilmemis demektir.")
            return 1
        print("TAMAM — yayindaki simgeler bu betikten uretiliyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
