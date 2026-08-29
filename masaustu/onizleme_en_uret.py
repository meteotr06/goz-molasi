# -*- coding: utf-8 -*-
"""INGILIZCE paylasim gorselini (onizleme-en.png) uretir.

NIYE AYRI DOSYA
  `onizleme_uret.py` TURKCE karti uretiyor ve simgeyi `ikon_uret`ten
  aliyor. Bu betik merkez oturumunun yazdigi ayri bir cizim; ikisi
  BIRBIRININ YERINE GECMEZ.

  29.08.2026: bu betik bir ara `onizleme_uret.py` adiyla kaydedildi ve
  ASIL URETICININ USTUNE YAZDI. Sebep, benim yanlis bir bulgumdu:
  "onizleme.png'nin ureticisi yok" demistim - oysa vardi, ben aramayi
  `head -4` ile kirptigim icin gormemistim. Git farki "eklendi" degil
  "degistirildi" dedigi icin fark edildi ve geri alindi.

  DERS: bir dosyayi tasimadan once o yolda ne oldugunu SOR.

TURKCE KART ELLE CIZILEN KALIYOR
  Ikisi karsilastirildi (29.08.2026): elle cizilende iris halkali ve
  goz yayin ICINDE oturuyor; uretilende iris duz. Yayindaki
  `onizleme.png` degistirilmedi.
"""
import io, os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

KOK = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630
C = 2                                   # ic olcek (kenar yumusatma icin)

ZEMIN_UST = (18, 46, 55)
ZEMIN_ALT = (34, 81, 89)
IKON_ZEMIN = (13, 29, 33)
NANE = (143, 216, 200)
BEYAZ = (255, 255, 255)
SOLUK = (206, 224, 226)

YAZI = "C:/Windows/Fonts/"
def yt(ad, boy):
    for aday in (ad, "segoeui.ttf", "arial.ttf"):
        try: return ImageFont.truetype(YAZI + aday, boy)
        except Exception: continue
    return ImageFont.load_default()


def gecis(w, h, ust, alt):
    """Kosegen gecis: sol ust koyu, sag alt acik."""
    g = Image.new("RGB", (w, h))
    p = g.load()
    for y in range(h):
        for x in range(0, w, 4):
            t = (x / w * 0.45 + y / h * 0.55)
            r = int(ust[0] + (alt[0] - ust[0]) * t)
            gg = int(ust[1] + (alt[1] - ust[1]) * t)
            b = int(ust[2] + (alt[2] - ust[2]) * t)
            for dx in range(4):
                if x + dx < w:
                    p[x + dx, y] = (r, gg, b)
    return g


def ikon(im, x0, y0, boy):
    """ONAYLANAN ikonu yapistirir (ikon-512.png).

    29.08.2026'da olculdu: bu dosyanin KENDI cizimi vardi, yani
    logo ucuncu bir yerde daha uretiliyordu (ikon_uret.py ve
    onizleme_uret.py'nin yanina). Kullanicinin onayladigi logo
    diskte durdugu icin cizmenin anlami kalmadi; cizmek, paylasim
    gorselinin uygulamanin ikonundan sapmasi demek.
    """
    yol = os.path.join(os.path.dirname(KOK), "ikon-512.png")
    simge = Image.open(yol).convert("RGBA").resize((boy, boy),
                                                   Image.LANCZOS)
    # `paste` + maske: taban gorsel RGBA olmak zorunda degil.
    # Olculdu: alpha_composite burada "image has wrong mode" veriyordu.
    im.paste(simge, (x0, y0), simge)


def _eski_ikon_cizimi(d, x0, y0, boy):
    """ARTIK KULLANILMIYOR - eski logonun cizimi, kayit olsun diye durur."""
    r = int(boy * 0.235)
    d.rounded_rectangle([x0, y0, x0 + boy, y0 + boy], radius=r,
                        fill=IKON_ZEMIN, outline=(48, 84, 90), width=max(1, boy // 260))

    cx, cy = x0 + boy / 2, y0 + boy / 2
    # HALKA: sagdan acik C
    hr = boy * 0.335
    kal = int(boy * 0.072)
    d.arc([cx - hr, cy - hr, cx + hr, cy + hr], start=305, end=205, fill=NANE, width=kal)

    # GOZ: badem + iris
    gw, gh = boy * 0.255, boy * 0.115
    d.polygon([(cx - gw, cy)] +
              [(cx - gw + 2 * gw * i / 40.0,
                cy - gh * math.sin(math.pi * i / 40.0)) for i in range(41)] +
              [(cx + gw, cy)] +
              [(cx + gw - 2 * gw * i / 40.0,
                cy + gh * math.sin(math.pi * i / 40.0)) for i in range(41)],
              fill=(214, 226, 224))
    ir = boy * 0.088
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=(58, 138, 128))
    d.ellipse([cx - ir * 0.55, cy - ir * 0.55, cx + ir * 0.55, cy + ir * 0.55],
              fill=(22, 62, 62))
    d.ellipse([cx - ir * 0.42, cy - ir * 0.62, cx - ir * 0.10, cy - ir * 0.30],
              fill=(240, 250, 250))


def cip(d, x, y, metin, font):
    """Yuvarlak etiket kutusu; genisligini metne gore alir."""
    sag, alt = d.textbbox((0, 0), metin, font=font)[2:]
    p = int(font.size * 0.62)
    yuk = alt + p
    d.rounded_rectangle([x, y, x + sag + p * 2, y + yuk], radius=yuk // 2,
                        fill=(52, 92, 98), outline=(76, 122, 126), width=2)
    d.text((x + p, y + p // 2 - 1), metin, font=font, fill=BEYAZ)
    return x + sag + p * 2


def ciz(yol, baslik, altbaslik, satirlar, cipler, adres):
    im = gecis(W * C, H * C, ZEMIN_UST, ZEMIN_ALT)
    d = ImageDraw.Draw(im)

    ikon(im, int(95 * C), int(118 * C), int(395 * C))

    x = int(545 * C)
    fB = yt("segoeuib.ttf", int(66 * C))
    fA = yt("segoeuib.ttf", int(27 * C))
    fM = yt("segoeui.ttf",  int(30 * C))
    fC = yt("segoeui.ttf",  int(21 * C))
    fU = yt("segoeui.ttf",  int(22 * C))

    d.text((x, int(168 * C)), baslik, font=fB, fill=BEYAZ)
    d.text((x, int(250 * C)), altbaslik, font=fA, fill=NANE)
    y = int(305 * C)
    for s in satirlar:
        d.text((x, y), s, font=fM, fill=SOLUK)
        y += int(40 * C)

    cx = x
    for c in cipler:
        cx = cip(d, cx, int(418 * C), c, fC) + int(18 * C)

    d.text((x, int(538 * C)), adres, font=fU, fill=(150, 178, 182))

    im.resize((W, H), Image.LANCZOS).save(yol)
    return yol


def main():
    # TURKCE KARTI UZERINE YAZMIYORUZ.
    # Yayindaki `onizleme.png` ELLE yapilmis ve iris detayi bu betigin
    # urettiginden zengin. Calisan ve daha iyi bir gorseli, yalnizca
    # "uretilebilir olsun" diye daha sadesiyle degistirmek gerileme
    # olurdu. Betik Turkce'yi AYRI ada yazar; karsilastirip karar
    # vermek projeyi yuruten oturumun isi.
    # Sayfalar bu gorselleri DEPO KOKUNDEN okuyor (index.html og:image).
    # Olculdu 29.08.2026: burasi masaustu\ altina yaziyordu - uretilen
    # gorsel hicbir sayfaya ulasmiyordu.
    _KOK = os.path.dirname(KOK)
    # TR kartI KARSILASTIRMA icin uretiliyor; sayfalarin kullandigi TR
    # gorseli `onizleme_uret.py` uretiyor (onizleme.png). Bu yuzden
    # masaustu\ altinda kaliyor - koke yazilsa yayina cikar ve hicbir
    # sayfanin kullanmadigi ikinci bir TR kart olurdu.
    tr = ciz(os.path.join(KOK, "onizleme-tr-uretilmis.png"),
             "Göz Molası", "20 DAKİKA · 20 SANİYE · 6 METRE",
             ["Her 20 dakikada bir ekranı kapatır,",
              "gözünü ne yapman gerektiğini gösterir."],
             ["Ücretsiz", "Kurulum yok", "Çevrimdışı çalışır"],
             "meteotr06.github.io/goz-molasi")
    en = ciz(os.path.join(_KOK, "onizleme-en.png"),
             "Eye Break", "20 MINUTES · 20 SECONDS · 6 METRES",
             ["Every 20 minutes it dims the screen and",
              "shows your eyes exactly what to do."],
             ["Free", "No install", "Works offline"],
             "meteotr06.github.io/goz-molasi/guide")
    for y in (tr, en):
        print("  %-28s %d bayt" % (os.path.basename(y), os.path.getsize(y)))
    print("TAMAM")
    return 0


if __name__ == "__main__":
    sys.exit(main())
