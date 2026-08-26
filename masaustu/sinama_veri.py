# -*- coding: utf-8 -*-
"""VERİ SINAMASI — masaüstü ve web sürümü aynı şeyi mi anlatıyor?

NEDEN VAR
  bilgiler.py'nin başında şu not duruyor: "Bu dosya web sürümündeki
  bilgiler.js ile aynı içeriktedir. Birini güncellersen diğerini de
  güncelle." Bunu insanın hatırlamasına bırakmak, er ya da geç iki
  sürümün farklı şeyler söylemesiyle biter. Kullanıcı Windows'ta bir
  bilgi görüp web'de göremeyince "hangisi doğru?" diye düşünür.

  Ayrıca her bilginin KAYNAĞI olmalı. Kaynaksız sağlık iddiası
  uygulamanın en büyük riski — hem güven hem AdSense açısından.

NE DENETLER
  1. Her bilginin başlığı, metni ve kaynağı dolu mu
  2. Masaüstü ve web sürümündeki bilgi/ipucu SAYILARI aynı mı
  3. Başlıklar birebir eşleşiyor mu
  4. İngilizce sürümde eksik bilgi var mı
  5. Aynı başlık iki kez geçiyor mu

ÇALIŞTIRMA
  python sinama_veri.py
"""
import io
import os
import re
import sys

import bilgiler as masaustu

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def js_basliklari(dosya, dizi_adi):
    """JS dosyasındaki bir dizinin baslik alanlarını sırayla döndürür.

    Tam bir JS ayrıştırıcısı değil — sadece `baslik: '...'` satırlarını
    okuyor. Bu iş için yeterli ve bağımlılık gerektirmiyor."""
    yol = os.path.join(KOK, dosya)
    if not os.path.exists(yol):
        return None
    s = io.open(yol, encoding="utf-8").read()
    m = re.search(re.escape(dizi_adi) + r"\s*=\s*\[", s)
    if not m:
        return None
    # Diziyi kaba biçimde sonlandır: aynı girintide kapanan ']'
    kalan = s[m.end():]
    son = kalan.find("\n];")
    if son == -1:
        son = len(kalan)
    govde = kalan[:son]
    return re.findall(r"baslik:\s*'((?:[^'\\]|\\.)*)'", govde) or \
        re.findall(r'baslik:\s*"((?:[^"\\]|\\.)*)"', govde)


def sadelestir(metin):
    """Tipografik süsleri düzleştirir.

    Masaüstünde "Türkiye'de", web'de "Türkiye’de" yazıyordu — düz
    kesme işareti ile tipografik kesme işareti. Kullanıcıya ikisi de
    aynı görünüyor, içerik farkı değil. Karşılaştırmada bunları
    eşitliyoruz ki sınama yalnızca GERÇEK içerik farkında bağırsın."""
    for eski, yeni in (("’", "'"), ("‘", "'"),
                       ("“", '"'), ("”", '"'),
                       ("–", "-"), ("—", "-"),
                       (" ", " ")):
        metin = metin.replace(eski, yeni)
    return " ".join(metin.split())


def kaynaklari_dogrula(dizi, ad, hatalar):
    gorulen = set()
    for i, oge in enumerate(dizi):
        baslik, metin, kaynak = oge[0], oge[1], oge[2]
        if not (baslik or "").strip():
            hatalar.append("%s[%d]: başlık boş" % (ad, i))
        if not (metin or "").strip():
            hatalar.append("%s[%d] (%s): metin boş" % (ad, i, baslik))
        if not (kaynak or "").strip():
            hatalar.append("%s[%d] (%s): KAYNAK YOK — kaynaksız sağlık "
                           "iddiası yayınlanamaz" % (ad, i, baslik))
        if baslik in gorulen:
            hatalar.append("%s: '%s' başlığı iki kez geçiyor" % (ad, baslik))
        gorulen.add(baslik)


def karsilastir(ad, masaustu_basliklar, web_basliklar, hatalar):
    if web_basliklar is None:
        hatalar.append("%s: web sürümünde dizi bulunamadı" % ad)
        return
    if len(masaustu_basliklar) != len(web_basliklar):
        hatalar.append(
            "%s: masaüstünde %d, web'de %d tane — iki sürüm farklı şey "
            "anlatıyor" % (ad, len(masaustu_basliklar), len(web_basliklar)))
    m = [sadelestir(b) for b in masaustu_basliklar]
    w = [sadelestir(b) for b in web_basliklar]
    eksik = [b for b in m if b not in w]
    fazla = [b for b in w if b not in m]
    for b in eksik:
        hatalar.append("%s: '%s' masaüstünde var, WEB'DE YOK" % (ad, b))
    for b in fazla:
        hatalar.append("%s: '%s' web'de var, MASAÜSTÜNDE YOK" % (ad, b))


def main():
    hatalar = []

    # 1) Kaynak ve doluluk
    kaynaklari_dogrula(masaustu.BILGILER, "BILGILER", hatalar)
    kaynaklari_dogrula(masaustu.IPUCLARI, "IPUCLARI", hatalar)

    # 2-3) Masaüstü <-> web karşılaştırması
    m_bilgi = [x[0] for x in masaustu.BILGILER]
    m_ipucu = [x[0] for x in masaustu.IPUCLARI]
    karsilastir("BILGILER", m_bilgi, js_basliklari("bilgiler.js", "BILGILER"),
                hatalar)
    karsilastir("IPUCLARI", m_ipucu,
                js_basliklari("mola_icerik.js", "IPUCLARI"), hatalar)

    # 3b) Dünya kartları — dunya.py ÜRETİLEN dosya, dunya.js kaynak.
    #     Üretimi unutmak iki sürümü sessizce ayırır; burada yakalıyoruz.
    try:
        import dunya as m_dunya
        m_dun = [x[0] for x in m_dunya.DUNYA]
    except Exception as e:
        m_dun = None
        hatalar.append("dunya.py okunamadı: %r — 'python dunya_uret.py' "
                       "çalıştırıldı mı?" % e)
    if m_dun is not None:
        w_dun = js_basliklari("dunya.js", "DUNYA")
        karsilastir("DUNYA", m_dun, w_dun, hatalar)
        kaynaklari_dogrula(m_dunya.DUNYA, "DUNYA", hatalar)

    # 4) İngilizce sürümde sayı tutuyor mu
    en_bilgi = js_basliklari("bilgiler_en.js", "BILGILER_EN")
    if en_bilgi is None:
        hatalar.append("bilgiler_en.js: BILGILER_EN bulunamadı")
    elif len(en_bilgi) != len(m_bilgi):
        hatalar.append("İngilizce sürümde %d bilgi var, Türkçede %d — "
                       "İngilizce kullanıcı eksik bilgi görüyor"
                       % (len(en_bilgi), len(m_bilgi)))

    print("Bilgi: %d masaüstü · ipucu: %d · mola cümlesi: %d"
          % (len(masaustu.BILGILER), len(masaustu.IPUCLARI),
             len(masaustu.MOLA_CUMLELERI)))
    if hatalar:
        print("\nBAŞARISIZ — %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("TAMAM — her bilginin kaynağı var, iki sürüm aynı şeyi anlatıyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
