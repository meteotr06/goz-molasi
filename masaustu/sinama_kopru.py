# -*- coding: utf-8 -*-
"""KÖPRÜ SINAMASI — Windows ↔ tarayıcı bağlantısı doğru VE dar mı?

NEDEN VAR
  Köprü bir ağ ucu açıyor. Bu sınıf hatalar sessizdir: uç fazla açık
  olursa hiçbir şey bozulmaz, hiçbir uyarı çıkmaz, yalnızca veri
  sızar. "Çalışıyor" burada yeterli bir cevap değil; "ne kadarı
  açık" diye sorulmalı.

NE DENETLER
  1. Sayaç okunuyor mu (asıl iş)
  2. Veri TAZE mi — her istekte yeniden üretiliyor mu
  3. Yazma ucu YOK mu (POST/PUT reddedilmeli)
  4. Yabancı siteye CORS izni VERİLMİYOR mu
  5. Uygulamanın kendi sayfalarına izin VERİLİYOR mu
  6. Bilinmeyen yol 404 mü
  7. Veri üreteci çökerse sunucu ayakta kalıyor mu

NÖBETÇİLİK ÖLÇÜMÜ
  Sonda korumalar bilerek kaldırılıp sınamanın DÜŞTÜĞÜ gösteriliyor.
  Düşmeyen sınama süstür.

ÇALIŞTIRMA
  python sinama_kopru.py
"""
import json
import sys
import urllib.error
import urllib.request

import kopru as kp

PORT = 0             # 0 = boş portu işletim sistemi seçsin.
#
# 27.08.2026: burada 8462 yazıyordu ve sınama BİR KEZ KARARSIZ ÇIKTI —
# aynı kod, arka arkaya iki koşuda iki farklı sonuç. Sebep kod değildi,
# bir önceki koşudan henüz boşalmamış porttu. Kararsız sınama, düpedüz
# başarısız sınamadan kötüdür: insan bir süre sonra onu ciddiye almaz.
# Ürünün portunu (8452) de kullanmıyoruz — kullanıcının çalışan
# uygulaması varsa onu bozardık.


def iste(yol="/durum", kaynak=None, yontem="GET"):
    """(kod, govde, izin_verilen_kaynak) döndürür."""
    q = urllib.request.Request("http://127.0.0.1:%d%s" % (PORT, yol),
                               method=yontem)
    if kaynak:
        q.add_header("Origin", kaynak)
    try:
        with urllib.request.urlopen(q, timeout=4) as y:
            return y.status, y.read().decode("utf-8"), \
                y.headers.get("Access-Control-Allow-Origin")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8"), \
            e.headers.get("Access-Control-Allow-Origin")


def uygulama_tarafi(kontrol):
    """Uygulamanın köprüye VERDİĞİ paketi denetler — GUI açmadan.

    Köprünün kendisi sağlam olsa bile yanlış paket gönderilirse
    tarayıcıda sessiz yanlış sayı olur. Ayrıca burada bir GİZLİLİK
    sınırı var: pakete şifre özeti ya da program listesi karışırsa
    kimse fark etmez, çünkü hiçbir şey bozulmaz.
    """
    import time
    import sinama_yalitim
    import goz_molasi as gm
    sinama_yalitim.yalit(gm)

    class Sahte(gm.Uygulama):
        def __init__(self, ist, kalan=493):
            self.ayar = dict(gm.VARSAYILAN)
            self.ist = ist
            self.durum = "calisiyor"
            self.hedef = time.time() + kalan

    d = Sahte({"tamamlanan": 3, "ekran_sn": 7420.7})._kopru_verisi()
    kontrol("paket: kaynak windows", d.get("kaynak") == "windows")
    kontrol("paket: kalan süre doğru", 490 <= d.get("kalan_sn", 0) <= 494,
            repr(d.get("kalan_sn")))

    # GİZLİLİK — köprü sayacı anlatır, uygulamayı açmaz.
    for gizli in ("kilit", "tuz", "ozet", "sifre", "programlar",
                  "yasak_bas", "acilis_izni", "analiz_izni"):
        kontrol("gizli alan sızmıyor: %s" % gizli, gizli not in d)

    # BOZUK DEĞER — nan JSON'a girerse tarayıcı tarafı çöker ya da
    # sessizce yanlış sayı gösterir. Bu sınıfı bu projede yaşadık.
    nan, inf = float("nan"), float("inf")
    for etiket, ist in (("nan", {"tamamlanan": nan, "ekran_sn": nan}),
                        ("inf", {"tamamlanan": inf, "ekran_sn": inf}),
                        ("metin", {"tamamlanan": "abc", "ekran_sn": None}),
                        ("boş", {})):
        try:
            m = json.dumps(Sahte(ist)._kopru_verisi())
            kontrol("bozuk değer (%s) JSON'a sızmıyor" % etiket,
                    "NaN" not in m and "Infinity" not in m)
        except Exception as e:
            kontrol("bozuk değer (%s) çökertmiyor" % etiket, False,
                    "%s: %s" % (type(e).__name__, e))

    # Kullanıcı istemiyorsa bilgisayarında ağ ucu açık kalmamalı.
    u = Sahte({})
    u.ayar["kopru"] = False
    u._kopruyu_kur()
    kontrol("ayar kapalıyken köprü açılmıyor", u.kopru is None)

    for s in sinama_yalitim.dogrula():
        kontrol("yalıtım: %s" % s, False)


def main():
    hatalar = []

    def kontrol(ad, sart, ayrinti=""):
        if not sart:
            hatalar.append("%s%s" % (ad, (" - " + ayrinti) if ayrinti else ""))
        print("  %-52s %s" % (ad, "TAMAM" if sart else "KALDI"))

    sayac = {"n": 0}

    def veri():
        sayac["n"] += 1
        return {"kalan_sn": 100 + sayac["n"], "durum": "calisiyor"}

    k = kp.Kopru(veri, port=PORT)
    if not k.baslat():
        print("KÖPRÜ AÇILAMADI: %s" % k.hata)
        return 1
    globals()["PORT"] = k.port      # işletim sisteminin verdiği gerçek port

    try:
        print("--- 1) SAYAÇ OKUNUYOR MU ---")
        kod, govde, _ = iste()
        kontrol("durum okunuyor", kod == 200, "kod %s" % kod)
        try:
            d = json.loads(govde)
        except Exception:
            d = {}
            hatalar.append("cevap JSON degil: %r" % govde[:60])
        kontrol("kalan süre geliyor", "kalan_sn" in d, repr(govde[:60]))

        print("--- 2) VERİ TAZE Mİ ---")
        # Bayat cevap bu uygulamada "süre başa sardı" demektir.
        _, g2, _ = iste()
        kontrol("her istekte yeniden üretiliyor",
                json.loads(g2).get("kalan_sn") != d.get("kalan_sn"),
                "iki istek aynı sayıyı döndü — önbellek/dondurma var")

        print("--- 3) YAZMA UCU OLMAMALI ---")
        for yontem in ("POST", "PUT", "DELETE"):
            kod, _, _ = iste(yontem=yontem)
            kontrol("%s reddediliyor" % yontem, kod >= 400, "kod %s" % kod)

        print("--- 4) YABANCI SİTEYE İZİN YOK ---")
        for yabanci in ("https://kotusite.example", "http://reklam.test",
                        "https://meteotr06.github.io.kotu.example",
                        "null"):
            _, _, izin = iste(kaynak=yabanci)
            kontrol("izin yok: %s" % yabanci[:34], izin is None,
                    "CORS izni verildi: %r" % izin)

        print("--- 5) KENDİ SAYFAMIZA İZİN VAR ---")
        for bizim in ("http://localhost:8451", "http://127.0.0.1:8455",
                      "https://meteotr06.github.io"):
            _, _, izin = iste(kaynak=bizim)
            kontrol("izin var: %s" % bizim, izin == bizim, "izin %r" % izin)

        print("--- 6) BİLİNMEYEN YOL ---")
        kod, _, _ = iste("/ayarlar")
        kontrol("/ayarlar 404", kod == 404, "kod %s" % kod)

        print("--- 7) VERİ ÜRETECİ ÇÖKERSE ---")
        # Uygulama içinde bir hata olsa bile köprü sunucusu ölmemeli;
        # ölürse sonraki istekler bağlanamaz ve sebebi hiç anlaşılmaz.
        eski = k.veri_uret
        k.veri_uret = lambda: 1 / 0
        kod, _, _ = iste()
        kontrol("çökme 500 olarak dönüyor", kod == 500, "kod %s" % kod)
        k.veri_uret = eski
        kod, _, _ = iste()
        kontrol("çökmeden sonra sunucu ayakta", kod == 200, "kod %s" % kod)

        # ---------------------------------------------------------------
        print("--- NÖBETÇİLİK: koruma kaldırılınca sınama düşüyor mu ---")
        # Bu bölüm sınamanın kendisini sınıyor. Geçen bir sınama, hiçbir
        # şeyi tutmuyor olabilir.
        gercek = kp._izinli_mi
        kp._izinli_mi = lambda kaynak: True          # kapıyı ardına kadar aç
        _, _, izin = iste(kaynak="https://kotusite.example")
        kontrol("koruma kalkınca 4. madde DÜŞÜYOR", izin is not None,
                "koruma kaldırıldı ama sınama hâlâ geçiyor — SÜS")
        kp._izinli_mi = gercek
        _, _, izin = iste(kaynak="https://kotusite.example")
        kontrol("koruma geri gelince yine kapalı", izin is None)
        print("--- 8) UYGULAMANIN VERDİĞİ PAKET ---")
        uygulama_tarafi(kontrol)
    finally:
        k.durdur()

    kontrol("durdurulunca kapanıyor", not k.acik_mi())

    if hatalar:
        print("\nBAŞARISIZ — %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("\nTAMAM — köprü okuyor, yazmıyor, yalnız kendi sayfalarına açık.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
