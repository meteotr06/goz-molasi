# -*- coding: utf-8 -*-
"""Paylaşım görselini (onizleme.png) üretir.

Bu görsel, birisi uygulamanın bağlantısını WhatsApp'ta, Twitter'da ya
da bir forumda paylaştığında görünen şey. Yani uygulamanın yüzü.

Eskisi mor zemin + kehribar halka + düz bir gözdü; simge deniz yeşiline
dönünce ortada kaldı. Simgeyi ikon_uret'ten alıyoruz ki ikisi bir daha
ayrışmasın.

Ölçü 1200x630 — Open Graph ve Twitter'ın istediği oran.

Çalıştır:  python onizleme_uret.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

import ikon_uret as ik

GEN, YUK = 1200, 630
KAT = 2                       # 2 katında çiz, küçültürken yumuşasın

YAZI = (232, 242, 239)        # #e8f2ef
SOLUK = (159, 191, 186)       # #9fbfba
VURGU = (143, 216, 200)       # #8fd8c8
ROZET_ZEMIN = (30, 70, 78)
ROZET_YAZI = (200, 224, 218)

YAZI_TIPI = "C:/Windows/Fonts/segoeui.ttf"
YAZI_TIPI_KALIN = "C:/Windows/Fonts/segoeuib.ttf"
YAZI_TIPI_YARI = "C:/Windows/Fonts/seguisb.ttf"


def _tip(yol, boy):
    try:
        return ImageFont.truetype(yol, boy)
    except Exception:
        return ImageFont.load_default()


def _zemin(gen, yuk):
    """Köşegen çamurcun gradyanı + iki yumuşak ışık lekesi."""
    im = Image.new("RGB", (gen, yuk))
    p = im.load()
    ust, alt = ik.ZEMIN_UST, ik.ZEMIN_ALT
    for y in range(yuk):
        for x in range(gen):
            t = (x / gen * 0.45 + y / yuk * 0.55)
            p[x, y] = tuple(round(ust[k] + (alt[k] - ust[k]) * t) for k in range(3))
    im = im.convert("RGBA")
    # Sağ altta ve sol üstte hafif ışıma — düz gradyan cansız duruyor
    im = ik._parilti(im, gen * 0.86, yuk * 0.80, gen * 0.42, VURGU, guc=0.10)
    im = ik._parilti(im, gen * 0.10, yuk * 0.16, gen * 0.30, VURGU, guc=0.06)
    return im


def uret():
    G, Y = GEN * KAT, YUK * KAT
    im = _zemin(G, Y)
    ciz = ImageDraw.Draw(im)

    # ---- Simge: ikon_uret'ten, aynı çizim ----
    simge_boy = int(Y * 0.62)
    simge = ik.yuvarlat(ik.simge_ciz(simge_boy, pay_orani=0.10), 0.22)
    sx, sy = int(G * 0.075), (Y - simge_boy) // 2
    im.alpha_composite(simge, (sx, sy))

    # ---- Yazılar ----
    x = sx + simge_boy + int(G * 0.055)
    baslik = _tip(YAZI_TIPI_KALIN, int(Y * 0.135))
    ustyazi = _tip(YAZI_TIPI_YARI, int(Y * 0.046))
    govde = _tip(YAZI_TIPI, int(Y * 0.052))
    rozet_tipi = _tip(YAZI_TIPI_YARI, int(Y * 0.036))

    y = int(Y * 0.235)
    ciz.text((x, y), "Göz Molası", font=baslik, fill=YAZI + (255,))
    y += int(Y * 0.155)

    ciz.text((x, y), "20 DAKİKA · 20 SANİYE · 6 METRE",
             font=ustyazi, fill=VURGU + (255,))
    y += int(Y * 0.095)

    for satir in ("Her 20 dakikada bir ekranı kapatır,",
                  "gözünü ne yapman gerektiğini gösterir."):
        ciz.text((x, y), satir, font=govde, fill=SOLUK + (255,))
        y += int(Y * 0.068)

    # ---- Rozetler ----
    y += int(Y * 0.035)
    rx = x
    for metin in ("Ücretsiz", "Kurulum yok", "Çevrimdışı çalışır"):
        kutu = ciz.textbbox((0, 0), metin, font=rozet_tipi)
        gen_m, yuk_m = kutu[2] - kutu[0], kutu[3] - kutu[1]
        yatay, dikey = int(Y * 0.028), int(Y * 0.022)
        w, h = gen_m + yatay * 2, yuk_m + dikey * 2
        ciz.rounded_rectangle([rx, y, rx + w, y + h], radius=h // 2,
                              fill=ROZET_ZEMIN + (255,))
        ciz.text((rx + yatay, y + dikey - kutu[1]), metin,
                 font=rozet_tipi, fill=ROZET_YAZI + (255,))
        rx += w + int(Y * 0.024)

    # ---- Adres ----
    adres = _tip(YAZI_TIPI, int(Y * 0.040))
    ciz.text((x, int(Y * 0.855)), "meteotr06.github.io/goz-molasi",
             font=adres, fill=SOLUK + (200,))

    return im.convert("RGB").resize((GEN, YUK), Image.LANCZOS)


if __name__ == "__main__":
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yol = os.path.join(kok, "onizleme.png")
    uret().save(yol, optimize=True)
    print(yol)
