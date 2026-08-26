# -*- coding: utf-8 -*-
"""SINAMA YALITIMI — sınamalar kullanıcının verisine DOKUNAMAZ.

NEDEN VAR — bu dosya bir kaza sonucu doğdu
  `sinama_zaman.py` içindeki `_gunu_tazele()`, modül düzeyindeki
  `ayarlari_yaz()` fonksiyonunu çağırıyor. Sahte uygulama nesnesi
  yalnızca METOTLARI eziyordu; modül fonksiyonu ezilmemişti. Sonuç:
  sınamanın sahte ayarları — `kip: aile`, sınama şifresi, 60 dakikalık
  günlük sınır — kullanıcının GERÇEK ayar dosyasına yazıldı.

  Kullanıcının o günkü ekran süresi 339 dakikaydı. 60 dakikalık sınırla
  birlikte engel ekranı kalıcı olarak açıldı ve **bilgisayar
  kullanılamaz hâle geldi.**

  Sınamanın görevi hata bulmaktır, hata yaratmak değil. Kullanıcının
  makinesine zarar verebilen bir sınama, hiç sınama olmamasından
  kötüdür.

NASIL KULLANILIR
  Sınama dosyasının EN BAŞINDA, goz_molasi içe aktarıldıktan hemen
  sonra:

      import goz_molasi as gm
      import sinama_yalitim
      sinama_yalitim.yalit(gm)

  Bundan sonra bütün yazmalar geçici bir klasöre gider. Sınama bitince
  `dogrula()` gerçek dosyaya dokunulmadığını KANITLAR — güvenmek
  yetmez, ölçmek gerekir.
"""
import atexit
import os
import shutil
import tempfile

# Korunacak gerçek yol
GERCEK_KLASOR = os.path.join(os.environ.get("APPDATA", ""), "GozMolasi")

_gecici = None
_parmak_izi = None


def _klasor_parmak_izi(klasor):
    """Klasördeki dosyaların (ad, boyut, değişim anı) listesi."""
    if not os.path.isdir(klasor):
        return []
    izler = []
    for ad in sorted(os.listdir(klasor)):
        y = os.path.join(klasor, ad)
        try:
            d = os.stat(y)
            izler.append((ad, d.st_size, int(d.st_mtime)))
        except OSError:
            pass
    return izler


def yalit(gm):
    """Modülün bütün yazma yollarını geçici klasöre çevirir.

    Yalnızca yolları değiştirmek YETMİYOR: `ayarlari_yaz` gibi modül
    fonksiyonları yolu içeriden okuyor olabilir. O yüzden hem yollar
    değiştiriliyor hem de yazan fonksiyonlar susturuluyor. İkisi
    birden, çünkü tek başına biri unutulabilir.
    """
    global _gecici, _parmak_izi
    _parmak_izi = _klasor_parmak_izi(GERCEK_KLASOR)

    _gecici = tempfile.mkdtemp(prefix="goz-molasi-sinama-")
    atexit.register(_temizle)

    gm.KAYIT_KLASOR = _gecici
    for ad, dosya in (("AYAR_DOSYA", "ayarlar.json"),
                      ("IST_DOSYA", "istatistik.json"),
                      ("DURUM_DOSYA", "durum.json")):
        if hasattr(gm, ad):
            setattr(gm, ad, os.path.join(_gecici, dosya))

    # Kemer ve askı: yazan fonksiyonları da sustur
    gm.ayarlari_yaz = lambda *a, **k: None
    if hasattr(gm, "gcm"):
        gm.gcm.gunu_isle = lambda *a, **k: None

    return _gecici


def dogrula():
    """Gerçek klasöre dokunuldu mu? Dokunulduysa sınama BAŞARISIZDIR.

    Bu denetim olmadan yalıtımın işlediğine güvenmiş oluruz. Güvenmek
    ölçmek değildir — zaten bu dosya tam da bu yüzden var.
    """
    if _parmak_izi is None:
        return []
    yeni = _klasor_parmak_izi(GERCEK_KLASOR)
    if yeni == _parmak_izi:
        return []
    eski_d = {a: (b, c) for a, b, c in _parmak_izi}
    yeni_d = {a: (b, c) for a, b, c in yeni}
    sorunlar = []
    for ad in sorted(set(eski_d) | set(yeni_d)):
        if ad not in eski_d:
            sorunlar.append("SINAMA DOSYA OLUŞTURDU: %s" % ad)
        elif ad not in yeni_d:
            sorunlar.append("SINAMA DOSYA SİLDİ: %s" % ad)
        elif eski_d[ad] != yeni_d[ad]:
            sorunlar.append("SINAMA DOSYAYI DEĞİŞTİRDİ: %s" % ad)
    return sorunlar


def _temizle():
    if _gecici and os.path.isdir(_gecici):
        shutil.rmtree(_gecici, ignore_errors=True)


if __name__ == "__main__":
    print("Gerçek klasör:", GERCEK_KLASOR)
    print("İçerik:")
    for ad, boyut, _ in _klasor_parmak_izi(GERCEK_KLASOR):
        print("  %-28s %d bayt" % (ad, boyut))
