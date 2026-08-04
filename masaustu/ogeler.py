# -*- coding: utf-8 -*-
"""
ÖĞELER — Tuvale çizilen arayüz parçaları.

Tkinter'ın hazır düğme/çerçeveleri 1995'ten kalma görünüyor: köşeler
keskin, gölge yok, gradyan yok. Bu yüzden hepsini Canvas'a kendimiz
çiziyoruz. Kartlar yuvarlak, düğmelerin üstüne gelince rengi değişiyor,
kartların altında yumuşak gölge var.
"""

import tkinter as tk
from tkinter import font as tkfont

import gorunum as gor


def yazi_tipi_sec(kok):
    """Sistemde olan en iyi yazı tipini seç."""
    mevcut = set(tkfont.families(kok))
    for ad in ("Segoe UI Variable Display", "Segoe UI", "Calibri", "Arial"):
        if ad in mevcut:
            return ad
    return "TkDefaultFont"


def yuvarlak(tuval, x1, y1, x2, y2, r=14, **kw):
    """Yuvarlak köşeli dikdörtgen.

    Tkinter'da böyle bir şekil yok; köşe noktalarını iki kez verip
    smooth=True diyerek eğri elde ediyoruz.
    """
    r = min(r, abs(x2 - x1) / 2, abs(y2 - y1) / 2)
    noktalar = [
        x1 + r, y1,  x2 - r, y1,  x2, y1,  x2, y1 + r,
        x2, y2 - r,  x2, y2,  x2 - r, y2,  x1 + r, y2,
        x1, y2,  x1, y2 - r,  x1, y1 + r,  x1, y1,
    ]
    return tuval.create_polygon(noktalar, smooth=True, **kw)


def kart(tuval, x1, y1, x2, y2, zemin, renk, r=18, golge=3, etiket=None):
    """Altında yumuşak gölgesi olan yuvarlak kart.

    Gerçek gölge (bulanıklık) tkinter'da yok; kartın altına gitgide
    zemine karışan birkaç kopya koyarak taklit ediyoruz.
    """
    etiketler = (etiket,) if etiket else ()
    for i in range(golge, 0, -1):
        c = gor.karistir(zemin, "#000000", 0.05 * (golge - i + 1))
        yuvarlak(tuval, x1 + i * 0.6, y1 + i * 1.4, x2 - i * 0.6, y2 + i * 1.4,
                 r=r, fill=c, outline="", tags=etiketler)
    return yuvarlak(tuval, x1, y1, x2, y2, r=r, fill=renk,
                    outline=gor.karistir(renk, "#ffffff", 0.06), tags=etiketler)


class Dugme:
    """Tuvale çizilen düğme. Üstüne gelince ve basınca rengi değişir."""

    def __init__(self, tuval, x, y, genislik, yukseklik, yazi, komut,
                 zemin, renk, yazi_rengi, yazi_tipi, kalin=False, r=None):
        self.t = tuval
        self.komut = komut
        self.renk = renk
        self.uzerinde = gor.karistir(renk, "#ffffff", 0.14)
        self.basili = gor.karistir(renk, "#000000", 0.12)
        self.etiket = "dugme_%d" % id(self)

        r = r if r is not None else yukseklik / 2
        self.sekil = yuvarlak(tuval, x, y, x + genislik, y + yukseklik, r=r,
                              fill=renk, outline="", tags=(self.etiket,))
        self.isik = yuvarlak(
            tuval, x + 1, y + 1, x + genislik - 1, y + yukseklik * 0.5,
            r=r * 0.8, fill=gor.karistir(renk, "#ffffff", 0.09),
            outline="", tags=(self.etiket,))
        self.yazi = tuval.create_text(
            x + genislik / 2, y + yukseklik / 2, text=yazi, fill=yazi_rengi,
            font=(yazi_tipi, 10, "bold" if kalin else "normal"),
            tags=(self.etiket,))

        tuval.tag_bind(self.etiket, "<Enter>", self._gir)
        tuval.tag_bind(self.etiket, "<Leave>", self._cik)
        tuval.tag_bind(self.etiket, "<Button-1>", self._bas)
        tuval.tag_bind(self.etiket, "<ButtonRelease-1>", self._birak)

    def _boya(self, renk):
        self.t.itemconfigure(self.sekil, fill=renk)
        self.t.itemconfigure(self.isik, fill=gor.karistir(renk, "#ffffff", 0.09))

    def _gir(self, e=None):
        self._boya(self.uzerinde)
        self.t.configure(cursor="hand2")

    def _cik(self, e=None):
        self._boya(self.renk)
        self.t.configure(cursor="")

    def _bas(self, e=None):
        self._boya(self.basili)

    def _birak(self, e=None):
        self._boya(self.uzerinde)
        if callable(self.komut):
            self.komut()


def halka(tuval, x, y, yaricap, kalinlik, iz_renk, etiket_iz="halka_iz"):
    """Geri sayım halkasının boş izini çizer, dolu yayı çağıran ekler."""
    tuval.create_oval(x - yaricap, y - yaricap, x + yaricap, y + yaricap,
                      outline=iz_renk, width=kalinlik, tags=(etiket_iz,))


def parlaklik(tuval, x1, y1, x2, y2, r, renk, etiket=None):
    """Düğmenin üst yarısına ince bir ışık — düz renk yassı duruyordu."""
    etiketler = (etiket,) if etiket else ()
    yuvarlak(tuval, x1 + 1, y1 + 1, x2 - 1, y1 + (y2 - y1) * 0.55,
             r=r * 0.8, fill=gor.karistir(renk, "#ffffff", 0.10),
             outline="", tags=etiketler)


def goz_simgesi(tuval, x, y, boy, disi, ici, etiket=None):
    """Uygulamanın göz simgesi — başlıkta durur."""
    etiketler = (etiket,) if etiket else ()
    g = boy / 2
    tuval.create_oval(x - g, y - g, x + g, y + g, fill=gor.karistir(disi, "#000000", 0.35),
                      outline="", tags=etiketler)
    # badem şekli: üstü ve altı eğri iki yay
    tuval.create_arc(x - g * 0.92, y - g * 0.78, x + g * 0.92, y + g * 1.05,
                     start=0, extent=180, style="chord", fill=disi, outline="",
                     tags=etiketler)
    tuval.create_arc(x - g * 0.92, y - g * 1.05, x + g * 0.92, y + g * 0.78,
                     start=180, extent=180, style="chord", fill=disi, outline="",
                     tags=etiketler)
    p = g * 0.42
    tuval.create_oval(x - p, y - p, x + p, y + p, fill=ici, outline="", tags=etiketler)


def nokta_seridi(tuval, x, y, adet, dolu, cap, ara, dolu_renk, bos_renk, etiket=None):
    """Bugün tamamlanan molaları nokta nokta gösterir."""
    etiketler = (etiket,) if etiket else ()
    for i in range(adet):
        cx = x + i * (cap + ara)
        renk = dolu_renk if i < dolu else bos_renk
        tuval.create_oval(cx, y, cx + cap, y + cap, fill=renk, outline="",
                          tags=etiketler)


def cubuk(tuval, x, y, genislik, yukseklik, oran, zemin_renk, renk, r=None,
          etiket=None):
    """Grafikteki yuvarlak uçlu çubuk (arka plan + dolu kısım).

    etiket ŞART: etiketsiz çizilen parçalar canvas.delete(etiket) ile
    silinemiyor ve sekme değiştirince eski grafik altta kalıyordu.
    """
    etiketler = (etiket,) if etiket else ()
    r = r if r is not None else yukseklik / 2
    yuvarlak(tuval, x, y, x + genislik, y + yukseklik, r=r,
             fill=zemin_renk, outline="", tags=etiketler)
    dolu = max(yukseklik, genislik * max(0.0, min(1.0, oran)))
    yuvarlak(tuval, x, y, x + dolu, y + yukseklik, r=r, fill=renk, outline="",
             tags=etiketler)
    # Üst yarıya ince ışık — düz renk çubuklar yassı duruyordu
    if dolu > yukseklik * 1.2:
        yuvarlak(tuval, x + 1, y + 1, x + dolu - 1, y + yukseklik * 0.5,
                 r=r * 0.75, fill=gor.karistir(renk, "#ffffff", 0.16),
                 outline="", tags=etiketler)


def dikey_cubuk(tuval, x, taban, genislik, yukseklik, renk, r=None, etiket=None):
    """7 gün grafiğindeki dikey çubuk — üstü yuvarlak, üstünde ışık."""
    etiketler = (etiket,) if etiket else ()
    r = r if r is not None else genislik * 0.28
    tepe = taban - max(yukseklik, r * 1.2)
    yuvarlak(tuval, x, tepe, x + genislik, taban, r=r, fill=renk,
             outline="", tags=etiketler)
    if yukseklik > genislik * 0.6:
        yuvarlak(tuval, x + 1, tepe + 1, x + genislik - 1,
                 tepe + (taban - tepe) * 0.42, r=r * 0.8,
                 fill=gor.karistir(renk, "#ffffff", 0.18), outline="",
                 tags=etiketler)
