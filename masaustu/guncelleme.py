# -*- coding: utf-8 -*-
"""GÜNCELLEME DENETİMİ — yeni sürüm çıktı mı?

NEDEN VAR
  Web sürümü kendini güncelliyor; Windows sürümü güncellemiyor.
  Kullanıcı exe'yi bir kez indiriyor ve aylarca o sürümde kalıyor.
  Düzelttiğimiz hatayı görmeye devam ediyor, eklediğimiz özelliği
  hiç görmüyor ve bundan haberi bile olmuyor.

  Bu modül GitHub Releases'e bakıp yeni sürüm var mı diye soruyor.
  Varsa uygulama küçük bir kart gösteriyor: "yeni sürüm çıktı, indir".

KURALLAR
  • İnternete GÜNDE EN FAZLA BİR KEZ çıkılır. Sürüm denetimi için
    sürekli ağ trafiği üretmek saygısızlık.
  • Hiçbir kişisel veri gönderilmez. Sadece herkese açık bir
    adresten JSON okunuyor.
  • İnternet yoksa ya da GitHub cevap vermezse SESSİZCE geçilir.
    Sürüm denetimi başarısız diye kullanıcıyı rahatsız etmeyiz.
  • Kullanıcı bir sürümü "görmezden gel" derse o sürüm bir daha
    sorulmaz.
  • İndirme OTOMATİK YAPILMAZ. Karar kullanıcının; biz sadece
    tarayıcıda indirme sayfasını açıyoruz.
"""
import json
import re
import time
import urllib.request

DEPO = "meteotr06/goz-molasi"
API = "https://api.github.com/repos/%s/releases/latest" % DEPO
INDIRME_SAYFASI = "https://github.com/%s/releases/latest" % DEPO

ZAMAN_ASIMI = 6            # saniye — takılırsa açılışı bekletmesin
GUNDE_BIR = 24 * 3600


def _sayilar(surum):
    """'v1.2.3' -> (1, 2, 3). Karşılaştırma için."""
    return tuple(int(x) for x in re.findall(r"\d+", surum or "")) or (0,)


def yeni_mi(uzak, yerel):
    """Uzaktaki sürüm yereldekinden yeni mi?"""
    u, y = _sayilar(uzak), _sayilar(yerel)
    # Farklı uzunlukta olabilir: (1,1) ile (1,1,2) — kısasını sıfırla
    boy = max(len(u), len(y))
    u = u + (0,) * (boy - len(u))
    y = y + (0,) * (boy - len(y))
    return u > y


def son_surumu_sor():
    """GitHub'daki son sürümü döndürür: (etiket, adres) ya da (None, None)."""
    try:
        istek = urllib.request.Request(
            API, headers={"Accept": "application/vnd.github+json",
                          "User-Agent": "GozMolasi"})
        with urllib.request.urlopen(istek, timeout=ZAMAN_ASIMI) as cevap:
            veri = json.loads(cevap.read().decode("utf-8"))
        return veri.get("tag_name"), veri.get("html_url") or INDIRME_SAYFASI
    except Exception:
        # İnternet yok, GitHub kapalı, kota dolu... hepsi aynı: sessizce geç
        return None, None


def denetle(ayar, yerel_surum):
    """Günde bir kez denetler.

    Döner: (etiket, adres) yeni sürüm varsa, yoksa (None, None).
    `ayar` sözlüğünü günceller — çağıran tarafın kaydetmesi gerekir.
    """
    simdi = time.time()
    if simdi - float(ayar.get("surum_denetim_ani", 0) or 0) < GUNDE_BIR:
        return None, None
    ayar["surum_denetim_ani"] = simdi

    etiket, adres = son_surumu_sor()
    if not etiket:
        return None, None
    if not yeni_mi(etiket, yerel_surum):
        return None, None
    # Kullanıcı bu sürümü zaten geçtiyse bir daha sorma
    if ayar.get("gormezden_gelinen_surum") == etiket:
        return None, None
    return etiket, adres


if __name__ == "__main__":
    # Elle deneme: python guncelleme.py
    print("son surum:", son_surumu_sor())
    for u, y in (("v1.1", "1.0"), ("v1.0", "1.0"), ("v1.0.2", "1.1"),
                 ("v2.0", "1.9.9")):
        print("  %-8s > %-6s ? %s" % (u, y, yeni_mi(u, y)))
