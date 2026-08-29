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

    # ---------------- DURUMLAR ----------------
    # 27.08.2026, bagimsiz denetimde bulundu: bu sinama YALNIZCA
    # "calisiyor" durumunu olcuyordu. Hayalet mola hatasinin yasadigi
    # butun durumlar (bosta / duraklatildi / saat_disi / olcuyor)
    # hic olculmemisti. Tek durumda gecen bir sinama, o durumun
    # disindaki hicbir sey icin kanit degildir.
    #
    # HATA NEYDI: donmus durumlarda `hedef` ILERLEMIYOR, yalnizca
    # cizim `dondurulmus` ile donuyor. Kopru ham `hedef - now`
    # yayinliyordu -> sayi sifira iniyor -> tarayici 25 saniyede bir
    # SAHTE MOLA veriyordu. Ogle molasinda ~50 sahte mola, hepsi
    # istatistige kalici yaziliyordu.
    class Durumlu(Sahte):
        def __init__(self, durum, dondurulmus=None, kalan=493):
            Sahte.__init__(self, {}, kalan)
            self.durum = durum
            self.dondurulmus = dondurulmus

    # (durum, dondurulmus, sayiyor_olmali, beklenen_kalan)
    DURUMLAR = [
        ("calisiyor",    None, True,  493),
        ("uyari",        None, True,  493),
        ("bosta",        630,  False, 630),
        ("duraklatildi", 300,  False, 300),
        ("saat_disi",    900,  False, 900),
        ("mola",         None, False, 493),
        ("olcuyor",      None, False, 493),
    ]
    for durum, dondurulmus, sayiyor, beklenen in DURUMLAR:
        p = Durumlu(durum, dondurulmus)._kopru_verisi()
        kontrol("durum %-13s -> sayiyor=%s" % (durum, sayiyor),
                p.get("sayiyor") is sayiyor,
                "sayiyor=%r" % p.get("sayiyor"))
        kontrol("durum %-13s -> kalan %d sn" % (durum, beklenen),
                abs(p.get("kalan_sn", -1) - beklenen) <= 1,
                "kalan_sn=%r (beklenen %d)" % (p.get("kalan_sn"), beklenen))

    # DONMUS DURUM ZAMANLA SIFIRA INMEMELI - hatanin ta kendisi buydu.
    # `hedef`i cok geriye alip donmus sayacin ETKILENMEDIGINI gosteriyoruz.
    donuk = Durumlu("bosta", 630)
    donuk.hedef = time.time() - 5000        # hedef coktan gecti
    p = donuk._kopru_verisi()
    kontrol("bosta iken hedef gecse bile kalan DUSMUYOR",
            abs(p["kalan_sn"] - 630) <= 1,
            "kalan_sn=%r -> tarayici bunu 0 gorup SAHTE MOLA verirdi"
            % p.get("kalan_sn"))
    kontrol("bosta iken sayiyor=False (tarayici dokunmaz)",
            p["sayiyor"] is False)

    # Calisirken hedef gectiyse 0 gorunmeli (dogru davranis)
    biten = Durumlu("calisiyor")
    biten.hedef = time.time() - 10
    kontrol("calisirken hedef gectiyse kalan 0",
            biten._kopru_verisi()["kalan_sn"] == 0)

    # AILE KIPI ENGEL EKRANI - hayalet molanin IKINCI KAPISI.
    # 29.08.2026 olcumu: engel acikken `durum` "calisiyor" kaliyor ve
    # `hedef` ilerlemiyordu; kopru sayiyor=true + kalan_sn=0 yolluyor,
    # tarayici surumu bunu devralip aninda mola veriyordu. Olculdu:
    # IdleDetector izni acikken 30 dakikada 71, 2 saatte 287 sahte
    # mola - hepsi cocugun istatistigine kalici yaziliyor.
    engelli = Durumlu("calisiyor", dondurulmus=612)
    engelli.engel_ekrani = object()         # ekran kapli, sayac donuk
    engelli.hedef = time.time() - 5000      # hedef coktan gecti
    pe = engelli._kopru_verisi()
    kontrol("engel ekrani acikken sayiyor=False", pe["sayiyor"] is False,
            "sayiyor=%r -> tarayici SAHTE MOLA verir" % pe.get("sayiyor"))
    kontrol("engel ekrani acikken donmus=True", pe["donmus"] is True,
            "donmus=%r" % pe.get("donmus"))
    kontrol("engel ekrani acikken kalan DUSMUYOR",
            abs(pe["kalan_sn"] - 612) <= 1,
            "kalan_sn=%r (beklenen 612)" % pe.get("kalan_sn"))

    # TERS DAL: engel YOKKEN ayni nesne hala dogru sayiyor. Duzeltme
    # fazla kirpiyor olabilir; onu da olcuyoruz.
    engelsiz = Durumlu("calisiyor", dondurulmus=612)
    engelsiz.engel_ekrani = None
    ps = engelsiz._kopru_verisi()
    kontrol("engel yokken sayiyor=True (fazla kirpmiyoruz)",
            ps["sayiyor"] is True, "sayiyor=%r" % ps.get("sayiyor"))
    kontrol("engel yokken kalan gercek sayac", abs(ps["kalan_sn"] - 493) <= 1,
            "kalan_sn=%r (beklenen 493)" % ps.get("kalan_sn"))

    # ASIMETRI SIZINTISI - 29.08.2026 bagimsiz denetiminde bulundu.
    # Yukaridaki duzeltmenin ILK hali `_tik`in engel dalinda
    # `dondurulmus`u KOSULSUZ set ediyor, `engeli_kaldir` ise yalnizca
    # donmus OLMAYAN durumlarda geri veriyordu. Asimetri yuzunden
    # `dondurulmus`, daha once None oldugu `duraklatildi`/`saat_disi`
    # durumlarina siziyordu: kopru engelden once 0, sonra 400 diyor,
    # ekranda ise calisma_dk*60 (1200) yaziyordu. Bu, tam da koprunun
    # onlemek icin yazildigi sinif - EKRANDA YAZMAYAN sayi.
    # Sayilar cakismadigi icin tarayici molaya girmezdi; hata sessizdi.
    # Sessiz oldugu icin bekcisi var.
    class SahteEngel(object):
        def kapat(self):
            pass

    class SahteKok(object):
        def after(self, ms, fn):
            pass

    class TikDurumlu(Durumlu):
        """GERCEK `_tik` cagrilabilsin diye cevresi susturulmus nesne."""

        def __init__(self, durum, kalan=400):
            Durumlu.__init__(self, durum, None, kalan)
            self.engel_ekrani = SahteEngel()
            self.mola_ekrani = None
            self.balon = None
            self.kok = SahteKok()

        def _saat_sicramasini_yakala(self, simdi):
            return 0.0

        def _gunu_tazele(self):
            return False

        def engeli_uygula(self):
            pass

    for durum in ("duraklatildi", "saat_disi"):
        t = TikDurumlu(durum)
        once = t._kopru_verisi()["kalan_sn"]
        gm.Uygulama._tik(t)                  # GERCEK _tik - engel dali
        gm.Uygulama.engeli_kaldir(t)         # GERCEK engeli_kaldir
        sonra = t._kopru_verisi()["kalan_sn"]
        kontrol("engel gelip gecince %s sayisi degismiyor" % durum,
                once == sonra,
                "engelden once %r, sonra %r -> kopru EKRANDA YAZMAYAN "
                "bir sayi soyluyor" % (once, sonra))
        kontrol("engel %s durumunda dondurulmus UYDURMUYOR" % durum,
                t.dondurulmus is None,
                "dondurulmus=%r -> o dalin kendi degeri olmaliydi"
                % (t.dondurulmus,))
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
                      "http://[::1]:8451"):
            _, _, izin = iste(kaynak=bizim)
            kontrol("izin var: %s" % bizim, izin == bizim, "izin %r" % izin)

        # 27.08.2026 KARAR DEĞİŞİKLİĞİ: yayındaki adres artık izinli
        # DEĞİL. Ölçüldü, oraya zaten ulaşılamıyor (eklenti kesiyor) ama
        # izin sayfadaki HER betiğe geçiyordu — reklam betikleri dahil.
        # Risk bugünden alınıyor, fayda hiç gelmiyordu.
        # (Bu satır eskiden "izin VAR" diye ölçüyordu. Koruma değişti,
        #  koruma sınaması da değişti — kod eskimedi, sınav eskimişti.)
        _, _, izin = iste(kaynak="https://meteotr06.github.io")
        kontrol("yayındaki adrese izin YOK (bilinçli karar)", izin is None,
                "izin %r" % izin)

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
        print("--- 7b) DNS REBINDING (Host doğrulaması) ---")
        # CORS tek başına yetmez: saldırgan kendi alan adını 127.0.0.1'e
        # çözdürürse tarayıcı için AYNI-KAYNAK olur ve CORS hiç devreye
        # girmez. Transmission ve Zoom bu yoldan düştü.
        import http.client as _hc
        for konak, beklenen in (("127.0.0.1", 200), ("localhost", 200),
                                ("kotu.example", 403),
                                ("127.0.0.1.kotu.example", 403)):
            b = _hc.HTTPConnection("127.0.0.1", k.port, timeout=4)
            b.putrequest("GET", "/durum", skip_host=True)
            b.putheader("Host", "%s:%d" % (konak, k.port))
            b.endheaders()
            kod = b.getresponse().status
            b.close()
            kontrol("Host %-24s -> %d" % (konak, beklenen), kod == beklenen,
                    "gelen %d" % kod)

        print("--- 7c) İKİNCİ KOPYA ---")
        # Windows'ta SO_REUSEADDR ikinci bind'e izin veriyor: eskiden
        # ikinci kopya hata ALMIYOR, açıldığını sanıyor, ama tek istek
        # bile ona gelmiyordu. Hatanın olmaması, çalıştığı demek değil.
        ikinci = kp.Kopru(veri, port=k.port)
        acildi = ikinci.baslat()
        kontrol("ikinci kopya açılmıyor", not acildi)
        kontrol("ikinci kopya sebebi yazıyor", bool(ikinci.hata),
                "hata=%r" % ikinci.hata)
        ikinci.durdur()

        print("--- 8) AĞA AÇIK MI (yalnız bu bilgisayar olmalı) ---")
        # Bu, ölçülmesi gereken bir sorudur; koda bakıp "127.0.0.1
        # yazmış" demek yetmez. Bir gün biri kolaylık olsun diye
        # "0.0.0.0" yazarsa aynı Wi-Fi'daki herkes ekran sürenizi
        # okuyabilir ve kimse fark etmez — hiçbir şey bozulmaz.
        kontrol("dinlenen adres 127.0.0.1",
                k.sunucu.server_address[0] == "127.0.0.1",
                str(k.sunucu.server_address[0]))

        # Yapılandırmaya değil DAVRANIŞA bak: ağ IP'sinden bağlanmayı dene.
        import socket
        yerel_ip = None
        try:
            for bilgi in socket.getaddrinfo(socket.gethostname(), None,
                                            socket.AF_INET):
                aday = bilgi[4][0]
                if not aday.startswith(("127.", "169.254.")):
                    yerel_ip = aday
                    break
        except Exception:
            pass
        if yerel_ip:
            s = socket.socket()
            s.settimeout(2)
            try:
                s.connect((yerel_ip, k.port))
                acik = True
            except Exception:
                acik = False
            finally:
                s.close()
            kontrol("ağ IP'sinden (%s) erişilemiyor" % yerel_ip, not acik,
                    "AĞA AÇIK — aynı Wi-Fi'daki herkes okuyabilir")
        else:
            # Ölçemediğimizi gizlemiyoruz.
            print("  %-52s %s" % ("ağ IP'si bulunamadı — ölçülemedi", "ATLA"))

        print("--- 9) UYGULAMANIN VERDİĞİ PAKET ---")
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
