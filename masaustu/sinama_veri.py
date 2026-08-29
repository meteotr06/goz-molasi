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


def gecmis_dayanikli_mi(hatalar):
    """gecmis.json bozulunca ne oluyor? (K-22: sessiz yanlış sayı)

    NEDEN VAR — 29.08.2026'da ölçülen üç hata:
      • Tek bir bozuk gün kaydı `son_gunler`/`seri` çağrılarını
        çökertiyordu. Çökme `_ciz` içinde olduğu için çeyrek saniyelik
        `_tik` döngüsü YENİDEN KURULMADAN kesiliyor: pencere açık,
        sayaç kalıcı donmuş, mola hiç gelmiyor. Kullanıcı fark etmiyor.
      • `yaz()` doğrudan `open(..., "w")` yapıyordu; yarım kalan tek bir
        yazma 120 günlük geçmişi geri dönülmez biçimde siliyordu
        (120 gün / seri=120 -> 1 gün / seri=0).
      • `gunu_isle` üstüne yazıyordu; istatistik.json yarım kalınca
        günün 9 molası KALICI olarak 0'a düşüyordu — oysa tam o anda
        gecmis.json'da doğru değer duruyordu.

    Her denetimin TERS DALI da ölçülüyor: sağlam veri hâlâ doğru sonucu
    veriyor mu? Düzeltme fazla kırpıyorsa burada görünür.

    Bu denetim kullanıcının gerçek verisine DOKUNMAZ: her şey
    tempfile.mkdtemp içinde geçer (bkz. sinama_yalitim.py).
    """
    import ast
    import json
    import shutil
    import tempfile
    from datetime import date, timedelta

    import gecmis as gcm

    burasi = os.path.dirname(os.path.abspath(__file__))
    klasor = tempfile.mkdtemp(prefix="goz-molasi-gecmis-")
    gecmis_json = os.path.join(klasor, "gecmis.json")
    bugun = date.today()
    dun = (bugun - timedelta(days=1)).isoformat()
    saglam = {(bugun - timedelta(days=i)).isoformat():
              {"mola": 9, "uzun": 0, "ekran_sn": 3600} for i in range(1, 8)}
    bugun_ist = {"tamamlanan": 4, "uzun_mola": 0}

    try:
        # 1) KONTROL (ters dal): sağlam veri doğru sonucu veriyor mu?
        gcm.yaz(klasor, dict(saglam))
        gunler = [s for _, s, _ in gcm.son_gunler(klasor, 7, bugun_ist)]
        if gunler != [9] * 6 + [4]:
            hatalar.append("geçmiş: SAĞLAM veride 7 gün grafiği yanlış: %r "
                           "(beklenen [9,9,9,9,9,9,4]) — düzeltme fazla "
                           "kırpıyor olabilir" % (gunler,))
        if gcm.seri(klasor, bugun_ist) != 7:
            hatalar.append("geçmiş: SAĞLAM veride seri %r, beklenen 7"
                           % gcm.seri(klasor, bugun_ist))

        # 2) Bozuk gün kaydı çökertmemeli; değer KIRPILMAZ, SIFIRLANIR
        denemeler = [
            ("gün kaydının kendisi metin", "bozuk"),
            ("gün kaydı liste", [1, 2]),
            ("mola metin", {"mola": "sekiz", "uzun": 0, "ekran_sn": 0}),
            ("mola null", {"mola": None, "uzun": 0, "ekran_sn": 0}),
            ("mola sonsuz", {"mola": float("inf"), "uzun": 0, "ekran_sn": 0}),
            ("mola NaN", {"mola": float("nan"), "uzun": 0, "ekran_sn": 0}),
            ("mola devasa", {"mola": 10 ** 9, "uzun": 0, "ekran_sn": 0}),
            ("mola negatif", {"mola": -50, "uzun": 0, "ekran_sn": 0}),
        ]
        for ad, deger in denemeler:
            veri = dict(saglam)
            veri[dun] = deger
            gcm.yaz(klasor, veri)
            try:
                g = [s for _, s, _ in gcm.son_gunler(klasor, 7, bugun_ist)]
                gcm.seri(klasor, bugun_ist)
            except Exception as e:
                hatalar.append(
                    "geçmiş: '%s' kaydı çizim yolunu ÇÖKERTİYOR (%s) — çökme "
                    "_ciz içinde olursa mola sayacı KALICI donar"
                    % (ad, e.__class__.__name__))
                continue
            if g[-2] != 0:
                hatalar.append(
                    "geçmiş: '%s' bozuk değeri ekrana %r olarak çıkıyor — "
                    "bozuk sayı kırpılmaz, SIFIRLANIR" % (ad, g[-2]))

        # 3) Yazma yarıda kesilirse ESKİ dosya bozulmamalı (atomik yazma)
        gcm.yaz(klasor, dict(saglam))
        once = len(gcm.oku(klasor))
        gercek_dump = json.dump

        def yarida_kes(veri, f, **k):
            f.write('{"yarim": ')
            raise IOError("disk doldu (sınama)")

        json.dump = yarida_kes
        try:
            gcm.yaz(klasor, dict(saglam))
        except Exception:
            pass
        finally:
            json.dump = gercek_dump
        sonra = len(gcm.oku(klasor))
        if sonra != once:
            hatalar.append(
                "geçmiş: yarım kalan TEK bir yazma %d günlük geçmişi %d güne "
                "düşürdü — atomik yazma yok (geçici dosya + os.replace)"
                % (once, sonra))
        artik = [a for a in os.listdir(klasor) if a.endswith(".yeni")]
        if artik:
            hatalar.append("geçmiş: yarım geçici dosya temizlenmedi: %r" % artik)

        # 4) Bozuk dosya SİLİNMEZ, kenara alınır ve bir kez söylenir
        gcm.yaz(klasor, dict(saglam))
        with io.open(gecmis_json, "w", encoding="utf-8") as f:
            f.write('{"yarim": ')
        gcm.son_bozulma = None
        gcm.oku(klasor)
        if not os.path.exists(gecmis_json + ".bozuk"):
            hatalar.append("geçmiş: bozuk gecmis.json kenara alınmadı — "
                           "sonraki yazma 120 günü geri dönülmez siliyor")
        if not getattr(gcm, "son_bozulma", None):
            hatalar.append("geçmiş: bozulma kullanıcıya bildirilmiyor "
                           "(gecmis.son_bozulma boş) — sessizce düzeltme yok")
        gcm.son_bozulma = None

        # 4b) İKİNCİ bozulma, BİRİNCİ bozulmanın yedeğini EZMEMELİ.
        #     Ölçüldü (29.08.2026): 120 günlük yedek, bir gün sonraki
        #     ikinci bozulmada 1 günlük dosyayla değiştiriliyordu
        #     (8528 bayt -> 77 bayt) ve kurtarılacak veri kalmıyordu.
        def yedek_boyu():
            y = gecmis_json + ".bozuk"
            return os.path.getsize(y) if os.path.exists(y) else 0

        ilk_yedek = yedek_boyu()
        gcm.gunu_isle(klasor, bugun.isoformat(),
                      {"tamamlanan": 1, "uzun_mola": 0, "ekran_sn": 60})
        with io.open(gecmis_json, "a", encoding="utf-8") as f:
            f.write("BOZUK")
        gcm.oku(klasor)
        if ilk_yedek and yedek_boyu() != ilk_yedek:
            hatalar.append("geçmiş: ikinci bozulma, birincinin .bozuk "
                           "yedeğini EZDİ — geri alınacak veri kalmıyor")
        gcm.son_bozulma = None

        # 4c) GEÇİCİ okuma hatası (antivirüs/yedekleme dosyayı bir an
        #     kilitler) SAĞLAM dosyayı kenara almamalı ve üstüne tek
        #     günlük veri yazılmamalı. Bu yol saniyede dört kez
        #     geçiliyor; ölçüldü: tek bir PermissionError 120 günü 1
        #     güne düşürüyordu.
        for a in os.listdir(klasor):
            if ".bozuk" in a:
                os.remove(os.path.join(klasor, a))
        gcm.yaz(klasor, dict(saglam))
        gercek_load = json.load

        def kilitli(f, **k):
            raise PermissionError(13, "dosya kilitli (sınama)")

        tasindi = False
        json.load = kilitli
        try:
            gcm.oku(klasor)
            tasindi = not os.path.exists(gecmis_json)
            gcm.gunu_isle(klasor, bugun.isoformat(),
                          {"tamamlanan": 1, "uzun_mola": 0, "ekran_sn": 60})
        finally:
            json.load = gercek_load
        if tasindi:
            hatalar.append("geçmiş: GEÇİCİ okuma hatasında sağlam dosya "
                           ".bozuk'a taşındı — içerik bozuk değil, dosya "
                           "yalnız bir an açılamadı")
        kalan = len(gcm.oku(klasor))
        if kalan != len(saglam):
            hatalar.append("geçmiş: okunamayan dosyanın ÜSTÜNE yazıldı — "
                           "%d gün kaldı (beklenen %d)"
                           % (kalan, len(saglam)))
        gcm.son_bozulma = None

        # 5) Günün toplamı GERİYE gitmemeli
        gcm.yaz(klasor, {bugun.isoformat():
                         {"mola": 9, "uzun": 2, "ekran_sn": 21600}})
        gcm.gunu_isle(klasor, bugun.isoformat(),
                      {"tamamlanan": 0, "uzun_mola": 0, "ekran_sn": 0})
        k = gcm.oku(klasor).get(bugun.isoformat(), {})
        if (k.get("mola"), k.get("uzun")) != (9, 2):
            hatalar.append("geçmiş: sıfırlanmış istatistik günün 9 molasını "
                           "%r ile ezdi — gün içi sayaç geriye gitmez" % (k,))
        # ters dal: gerçekten ARTAN sayı yazılmalı
        gcm.gunu_isle(klasor, bugun.isoformat(),
                      {"tamamlanan": 11, "uzun_mola": 3, "ekran_sn": 30000})
        k = gcm.oku(klasor).get(bugun.isoformat(), {})
        if (k.get("mola"), k.get("uzun")) != (11, 3):
            hatalar.append("geçmiş: artan mola sayısı geçmişe YAZILMIYOR: %r "
                           "— koruma fazla kırpıyor" % (k,))
    finally:
        shutil.rmtree(klasor, ignore_errors=True)

    # 6) Çizim yollarında koruma var mı? Buradaki bir istisna
    #    kok.after(250, ...) satırına hiç gelinmemesi demek.
    kaynak = io.open(os.path.join(burasi, "goz_molasi.py"),
                     encoding="utf-8").read()
    agac = ast.parse(kaynak)
    for islev_adi, cagri in (("_ciz", "seri"), ("_hafta_ciz", "son_gunler")):
        for d in ast.walk(agac):
            if not (isinstance(d, ast.FunctionDef) and d.name == islev_adi):
                continue
            hepsi = [c for c in ast.walk(d)
                     if isinstance(c, ast.Attribute) and c.attr == cagri]
            korunan = [c for t in ast.walk(d) if isinstance(t, ast.Try)
                       for govde in t.body for c in ast.walk(govde)
                       if isinstance(c, ast.Attribute) and c.attr == cagri]
            if hepsi and not korunan:
                hatalar.append(
                    "%s içindeki gcm.%s çağrısı try ile korunmuyor — buradaki "
                    "bir istisna _tik döngüsünü yeniden kurulmadan keser, "
                    "sayaç KALICI donar" % (islev_adi, cagri))

    # 7) Geçmiş uyarısı: iki dalda da AYNI metin olmalı. sinama_yerlesim
    #    yalnız düz metin dönüşlerini ölçebiliyor, o yüzden değişkene
    #    alınamıyor — kopyaların ayrışmadığını burada denetliyoruz.
    uyarilar = re.findall(r'return "([^"]*Geçmiş dosyası[^"]*)"', kaynak)
    if len(uyarilar) < 2:
        hatalar.append("geçmiş bozulunca ekranda uyarı yok (ayar_uyarisi "
                       "içinde %d dönüş) — sessizce düzeltmek hata sayılıyor"
                       % len(uyarilar))
    elif len(set(uyarilar)) > 1:
        hatalar.append("geçmiş uyarısı %d yerde FARKLI yazılmış — kullanıcı "
                       "aynı olayı iki ayrı cümleyle görüyor" % len(set(uyarilar)))

    print("Geçmiş dayanıklılığı: %d bozuk değer sınıfı, atomik yazma, "
          "yedeğin ezilmemesi, geçici okuma hatası, geriye gitmeyen gün, "
          "iki çizim yolu denetlendi" % 8)


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

    # 5) Geçmiş dosyası bozulunca veri kaybı / donma oluyor mu?
    gecmis_dayanikli_mi(hatalar)

    print("Bilgi: %d masaüstü · ipucu: %d · mola cümlesi: %d"
          % (len(masaustu.BILGILER), len(masaustu.IPUCLARI),
             len(masaustu.MOLA_CUMLELERI)))
    if hatalar:
        print("\nBAŞARISIZ — %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("TAMAM — her bilginin kaynağı var, iki sürüm aynı şeyi anlatıyor, "
          "bozuk geçmiş ne sayacı donduruyor ne veri siliyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
