# -*- coding: utf-8 -*-
"""
SES — Yumuşak uyarı sesleri.

winsound.Beep sert ve kulak tırmalayıcı. Onun yerine sesi kendimiz
üretiyoruz: sinüs dalgası + yavaş açılıp kapanan ses zarfı (fade in/out).
Böylece "ding" değil, yumuşak bir çan sesi çıkıyor.

Dosyaya yazmıyoruz; WAV verisini bellekte oluşturup oradan çalıyoruz.
Ek kurulum gerekmez, sadece Python'un kendi modülleri.
"""

import io
import math
import struct
import threading
import wave

try:
    import winsound
except ImportError:            # Windows dışında sessizce çalışmaz
    winsound = None

ORNEKLEME = 22050


def _dalga(frekanslar, sure, ses_seviyesi=0.35):
    """Birkaç frekansı üst üste bindirip yumuşak bir ton üretir."""
    n = int(ORNEKLEME * sure)
    kareler = []
    for i in range(n):
        t = i / ORNEKLEME
        # Ses zarfı: hızlı açılır (%1), yavaş söner — çan gibi
        acilis = min(1.0, t / (sure * 0.02))
        sonus = (1.0 - t / sure) ** 2.2
        zarf = acilis * sonus
        deger = 0.0
        for k, (frekans, agirlik) in enumerate(frekanslar):
            deger += agirlik * math.sin(2 * math.pi * frekans * t)
        deger = deger / sum(a for _, a in frekanslar)
        kareler.append(int(max(-1.0, min(1.0, deger * zarf * ses_seviyesi)) * 32767))
    return struct.pack("<%dh" % n, *kareler)


def _wav(veri):
    tampon = io.BytesIO()
    with wave.open(tampon, "wb") as d:
        d.setnchannels(1)
        d.setsampwidth(2)
        d.setframerate(ORNEKLEME)
        d.writeframes(veri)
    return tampon.getvalue()


# Sesleri bir kez üretip saklıyoruz — her seferinde hesaplamak gereksiz
_onbellek = {}


def _uret(ad):
    if ad in _onbellek:
        return _onbellek[ad]
    if ad == "mola_basi":
        # Alçaktan yükselen iki nota — "dur, dinlen"
        veri = _dalga([(392, 1.0), (784, 0.35), (1176, 0.12)], 1.1)
    elif ad == "mola_sonu":
        # Yükselen üçlü — "devam edebilirsin"
        veri = _dalga([(523, 1.0), (1046, 0.30), (1568, 0.10)], 0.9)
    else:  # uyari
        veri = _dalga([(880, 1.0), (1320, 0.20)], 0.35, ses_seviyesi=0.22)
    _onbellek[ad] = _wav(veri)
    return _onbellek[ad]


def cal(ad, acik=True):
    """Sesi arka planda çal — program bu sırada donmasın."""
    if not acik or winsound is None:
        return

    def calistir():
        try:
            winsound.PlaySound(_uret(ad), winsound.SND_MEMORY | winsound.SND_ASYNC)
        except Exception:
            pass

    threading.Thread(target=calistir, daemon=True).start()


def onceden_hazirla():
    """Sesleri önceden üret ki ilk çalışta gecikme olmasın."""
    def hazirla():
        for ad in ("mola_basi", "mola_sonu", "uyari"):
            try:
                _uret(ad)
            except Exception:
                pass
    threading.Thread(target=hazirla, daemon=True).start()
