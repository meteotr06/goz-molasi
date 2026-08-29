# -*- coding: utf-8 -*-
"""SÜRÜM ZİNCİRİ — kaynak, kayıt ve yayın birbirini yalanlıyor mu?

NİYE VAR (K-55)
  28.08.2026'da ölçüldü: aynı uygulamanın sürümü **üç yerde üç
  ayrı şey** diyordu.

      kod (goz_molasi.py)        1.1
      değişiklik kaydı           1.3
      yayınlanan sürüm (GitHub)  v1.0   (26 Ağustos)

  Sonuç: kullanıcının çalıştırdığı kopya 26 commit geride, ama
  uygulama **hiçbir şey söylemiyor** — çünkü güncelleme denetimi
  yalnızca GitHub Releases'e bakıyor ve orada kendisinden ESKİ bir
  sürüm duruyor. Mekanizma çalışıyor; gösterecek bir şey yok.

  > Eski kopya, yanlış davranan kopyadır. Sessiz kalmak yasak.

NE ÖLÇÜYOR
  1) Koddaki sürüm ile değişiklik kaydındaki en yeni masaüstü
     sürümü AYNI MI. Ayrışıyorsa bu bir hatadır: kayıt, olmayan
     bir sürümü varmış gibi anlatıyor demektir.
  2) Yayınlanan son sürüm koddan geride mi. Bu bir KOD hatası
     değil, bir YAYIN kararı — o yüzden sınamayı düşürmez, ama
     ekrana yazılır. Sessiz kalmaz.

NE ÖLÇMÜYOR
  Kullanıcının diskindeki `.exe`nin taze olup olmadığını —
  onu `exe_tazelik.py` ölçüyor. Bu ikisi farklı sorulardır:
    exe_tazelik : derlenmiş dosya kaynaktan geride mi
    sinama_surum: kaynak, kayıt ve yayın birbirini tutuyor mu

AĞ YOKSA
  Yayın sorgusu başarısız olursa "ölçülemedi" yazılır ve sınama
  DÜŞMEZ. Yanlış alarm, kaçırılan hatadan daha çok zarar veriyor
  (bugün üç kez yaşandı).

ÇALIŞTIR
  python sinama_surum.py
"""
import io
import json
import os
import re
import sys
import urllib.request

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.github.com/repos/meteotr06/goz-molasi/releases/latest"
ZAMAN_ASIMI = 8


def soyle(s=""):
    try:
        print(s)
    except UnicodeEncodeError:
        kod = getattr(sys.stdout, "encoding", None) or "ascii"
        print(s.encode(kod, "replace").decode(kod, "replace"))


def _oku(*yol):
    with io.open(os.path.join(KOK, *yol), encoding="utf-8") as d:
        return d.read()


def koddaki_surum():
    k = _oku("masaustu", "goz_molasi.py")
    m = re.search(r"^SURUM\s*=\s*[\"']([^\"']+)[\"']", k, re.M)
    return m.group(1) if m else None


def kayittaki_surum():
    """Değişiklik kaydındaki EN YENİ masaüstü sürümü."""
    k = _oku("masaustu", "degisiklikler.py")
    m = re.search(r"'masaustu_surum'\s*:\s*'([^']+)'", k)
    return m.group(1) if m else None


def yayindaki_surum():
    try:
        istek = urllib.request.Request(
            API, headers={"Accept": "application/vnd.github+json",
                          "User-Agent": "GozMolasi-sinama"})
        with urllib.request.urlopen(istek, timeout=ZAMAN_ASIMI) as cevap:
            veri = json.loads(cevap.read().decode("utf-8"))
        return veri.get("tag_name"), veri.get("published_at")
    except Exception as e:
        return None, "olculemedi: %s" % e


def _sayilar(s):
    return tuple(int(x) for x in re.findall(r"\d+", s or "")) or (0,)


def guncelleme_dallari():
    """Yeni surum kartI hangi durumda cikiyor? AG KULLANILMIYOR.

    `son_surumu_sor` sahte cevap veriyor; boylece her dal KESIN
    olculuyor ve sinama internete ya da GitHub'in o anki durumuna
    bagli kalmiyor.

    NIYE VAR: bu dosya "mekanizma calisiyor, gosterecek sey yok"
    diyebiliyordu ama mekanizmanin calistigini VARSAYIYORDU.
    "Mekanizma var" ile "mekanizma otuyor" ayri seyler; ikincisi
    olculmezse yayin gununde ogrenilir.

    Doner: hata listesi.
    """
    import time

    try:
        import guncelleme as gnc
    except Exception as e:
        return ["guncelleme.py okunamadi: %s" % e]

    hatalar = []

    def dal(baslik, uzak, yerel, ayar, bekle_kart):
        asil = gnc.son_surumu_sor
        gnc.son_surumu_sor = (lambda: (uzak, "https://ornek/%s" % uzak)) \
            if uzak else (lambda: (None, None))
        try:
            etiket, _ = gnc.denetle(ayar, yerel)
        except Exception as e:
            hatalar.append("%s: denetle COKTU (%s)" % (baslik, e))
            return
        finally:
            gnc.son_surumu_sor = asil
        cikti = bool(etiket)
        if cikti != bekle_kart:
            hatalar.append("%s: kart %s, %s bekleniyordu"
                           % (baslik, "CIKTI" if cikti else "cikmadi",
                              "cikmali" if bekle_kart else "cikmamali"))

    # Surum karsilastirmasi. v1.10 > v1.9 ozellikle onemli: metin
    # karsilastirmasi olsaydi "1.10" < "1.9" cikardi ve 10. yama
    # surumunden sonra kimse guncelleme bildirimi ALMAZDI.
    for uzak, yerel, bekle in (("v1.3", "1.3", False), ("v1.4", "1.3", True),
                               ("v1.10", "1.9", True), ("v1.3", "1.4", False),
                               ("v2.0", "1.9.9", True), ("v1.3.1", "1.3", True),
                               ("v1.3", "1.3.0", False)):
        if gnc.yeni_mi(uzak, yerel) != bekle:
            hatalar.append("yeni_mi(%r, %r) = %s, %s bekleniyordu"
                           % (uzak, yerel, not bekle, bekle))

    dal("yeni surum var", "v1.4", "1.3", {}, True)
    dal("guncel", "v1.3", "1.3", {}, False)
    dal("internet yok", None, "1.3", {}, False)
    dal("gormezden gelinen surum", "v1.4", "1.3",
        {"gormezden_gelinen_surum": "v1.4"}, False)

    # Gunde bir kurali VE ters dali: 24 saat sonra yine sormali.
    # Ters dal olmadan "hic sormuyor" hatasi fark edilmez.
    ayar = {}
    dal("gunde bir: ilk cagri", "v1.4", "1.3", ayar, True)
    dal("gunde bir: ayni gun ikinci", "v1.4", "1.3", ayar, False)
    if not ayar.get("surum_denetim_ani"):
        hatalar.append("denetle, ayar['surum_denetim_ani'] yazmiyor - "
                       "gunde bir kurali kalici degil, her acilista sorar")
    ayar["surum_denetim_ani"] = time.time() - (25 * 3600)
    dal("gunde bir: 24 saat sonra (ters dal)", "v1.4", "1.3", ayar, True)

    return hatalar


def main():
    kod = koddaki_surum()
    kayit = kayittaki_surum()

    if not kod or not kayit:
        soyle("OLCULEMEDI - surum bilgisi okunamadi (kod=%s, kayit=%s)"
              % (kod, kayit))
        return 1

    soyle("kod (goz_molasi.py)   : %s" % kod)
    soyle("degisiklik kaydi      : %s" % kayit)

    yayin, tarih = yayindaki_surum()
    if yayin:
        soyle("yayinlanan (GitHub)   : %s  (%s)" % (yayin, tarih))
    else:
        soyle("yayinlanan (GitHub)   : %s" % tarih)

    dusuk = 0

    # ---------- 0) Bildirim mekanizmasi GERCEKTEN otuyor mu? ----------
    gnc_hatalar = guncelleme_dallari()
    soyle("guncelleme dallari    : %s"
          % ("9 dal + 7 karsilastirma TAMAM" if not gnc_hatalar
             else "%d SORUN" % len(gnc_hatalar)))
    if gnc_hatalar:
        soyle()
        soyle("BASARISIZ - guncelleme bildirimi beklendigi gibi calismiyor:")
        for h in gnc_hatalar:
            soyle("  - %s" % h)
        soyle("  Bu sessiz bir hata: kullanici yeni surumden HABERSIZ kalir")
        soyle("  ve duzelttigimiz hatayi yasamaya devam eder.")
        dusuk = 1

    # ---------- 1) Kod ile kayit ayrisiyor mu? (HATA) ----------
    if kod != kayit:
        soyle()
        soyle("BASARISIZ - kod ile degisiklik kaydi ayrisiyor.")
        soyle("  Kod '%s' diyor, kayit en yeni masaustu surumunu '%s'"
              % (kod, kayit))
        soyle("  gosteriyor. Kayit, OLMAYAN bir surumu varmis gibi")
        soyle("  anlatiyor - kullanici o surumu hicbir yerde bulamaz.")
        soyle("  Yapilacak: ikisini esitle (hangisi dogruysa).")
        dusuk = 1

    # ---------- 2) Yayin geride mi? (KARAR, hata degil) ----------
    if yayin:
        if _sayilar(yayin) < _sayilar(kod):
            soyle()
            soyle("DIKKAT (sinamayi dusurmez) - yayin koddan GERIDE.")
            soyle("  Yayinda %s var, kaynak %s. Guncelleme denetimi"
                  % (yayin, kod))
            soyle("  GitHub Releases'e bakiyor; orada kullanicinin")
            soyle("  kopyasindan ESKI bir surum durdugu icin uygulama")
            soyle("  hicbir sey soylemiyor. Mekanizma calisiyor,")
            soyle("  gosterecek sey yok.")
            soyle("  Yapilacak: yeni surum derlenip yayinlanmali.")
            soyle("  BU BIR KULLANICI KARARI - kendiliginden yapilmaz.")
    else:
        soyle()
        soyle("Yayin sorgusu olculemedi (ag yok olabilir) - sinama")
        soyle("dusurulmuyor. Yanlis alarm vermiyoruz.")

    soyle()
    if dusuk:
        return 1
    soyle("TAMAM - kod ile degisiklik kaydi ayni surumu soyluyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
