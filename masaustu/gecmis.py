# -*- coding: utf-8 -*-
"""
GEÇMİŞ — Gün gün kayıt ve seri (streak) hesabı.

Bugünkü sayaçlar `istatistik.json`'da tutuluyor; gün değişince sıfırlanıyor.
Burada ise her günün özeti kalıcı olarak saklanıyor, böylece "son 7 gün"
grafiği ve "kaç gündür üst üste hedefi tutturdum" sayısı çıkarılabiliyor.

Dosya küçük kalsın diye sadece son 120 gün saklanır.
"""

import json
import os
from datetime import date, timedelta

SAKLANAN_GUN = 120
GUNLUK_HEDEF = 8          # günde bu kadar mola = "hedef tuttu"

GUN_ADLARI = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]


def _yol(klasor):
    return os.path.join(klasor, "gecmis.json")


def oku(klasor):
    try:
        with open(_yol(klasor), "r", encoding="utf-8-sig") as f:
            veri = json.load(f)
        return veri if isinstance(veri, dict) else {}
    except Exception:
        return {}


def yaz(klasor, veri):
    try:
        os.makedirs(klasor, exist_ok=True)
        # Eskiyenleri at
        sinir = (date.today() - timedelta(days=SAKLANAN_GUN)).isoformat()
        veri = {g: d for g, d in veri.items() if g >= sinir}
        with open(_yol(klasor), "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=1, sort_keys=True)
    except Exception:
        pass


def gunu_isle(klasor, gun, istatistik):
    """Bir günün özetini geçmişe yaz (üstüne yazar, toplamaz)."""
    veri = oku(klasor)
    veri[gun] = {
        "mola": int(istatistik.get("tamamlanan", 0)),
        "uzun": int(istatistik.get("uzun_mola", 0)),
        "ekran_sn": int(istatistik.get("ekran_sn", 0)),
    }
    yaz(klasor, veri)
    return veri


def son_gunler(klasor, adet=7, bugun_istatistik=None):
    """Son N günü [(gun_adi, mola_sayisi, bugun_mu), ...] olarak döndürür.

    Bugünün verisi henüz geçmişe yazılmamış olabilir; o yüzden anlık
    istatistiği dışarıdan alıp üstüne biniyoruz.
    """
    veri = oku(klasor)
    bugun = date.today()
    sonuc = []
    for i in range(adet - 1, -1, -1):
        g = bugun - timedelta(days=i)
        anahtar = g.isoformat()
        if i == 0 and bugun_istatistik is not None:
            sayi = int(bugun_istatistik.get("tamamlanan", 0)) + \
                   int(bugun_istatistik.get("uzun_mola", 0))
        else:
            d = veri.get(anahtar) or {}
            sayi = int(d.get("mola", 0)) + int(d.get("uzun", 0))
        sonuc.append((GUN_ADLARI[g.weekday()], sayi, i == 0))
    return sonuc


def seri(klasor, bugun_istatistik=None, hedef=GUNLUK_HEDEF):
    """Kaç gündür üst üste günlük hedefi tutturuyor?

    Bugün henüz hedefe ulaşmadıysa seri bozulmuş sayılmaz — dün'den
    geriye doğru sayılır. Sabahın köründe "serin bitti" demek haksızlık.
    """
    veri = oku(klasor)
    bugun = date.today()

    def gunun_sayisi(g):
        if g == bugun and bugun_istatistik is not None:
            return int(bugun_istatistik.get("tamamlanan", 0)) + \
                   int(bugun_istatistik.get("uzun_mola", 0))
        d = veri.get(g.isoformat()) or {}
        return int(d.get("mola", 0)) + int(d.get("uzun", 0))

    sayac = 0
    # Bugün hedefi tutturduysa bugünden, tutturmadıysa dünden başla
    baslangic = 0 if gunun_sayisi(bugun) >= hedef else 1
    i = baslangic
    while i < SAKLANAN_GUN:
        if gunun_sayisi(bugun - timedelta(days=i)) >= hedef:
            sayac += 1
            i += 1
        else:
            break
    return sayac
