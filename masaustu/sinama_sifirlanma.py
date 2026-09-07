# -*- coding: utf-8 -*-
"""SIFIRLANMA NÖBETÇİSİ — kullanıcının aylardır bildirdiği tek sınıf.

KULLANICININ SÖZLERİ (aynen, farklı günlerde):
  "ya bu göz uygulaması gerçekten kendini sıfırlayıp duruyot"
  "knk ama molayı hiç göremeden sıfırlıyr"
  "düzeltmen lazım hala sıfırlanıp duruyor"
  "bu sıfırlanma ve süre sayma olayına bişey bulmalıyız"

DÖRT AYRI SEBEBİ ÇIKTI ve dördü de ayrı ayrı düzeltildi. Bu dosya
onların GERİ GELMEDİĞİNİ ölçüyor. Neden ayrı bir nöbetçi:

  Bu depoda kural, düzeltilen her hata sınıfının kalıcı bir ölçümle
  kapatılması (K-28: yeni sınıf eskiyi geçersiz kılar). Sıfırlanma
  sınıfının ölçümleri bugüne kadar geçici bir klasörde duruyordu —
  yani bir sonraki oturumda YOK olacaklardı ve aynı hata sessizce
  geri gelebilirdi.

DÖRT SEBEP
  1. Sayfa gizlenirken diske YAZILMIYORDU. Mola kaydı bayat kalıyor,
     sonraki açılışta sayaç başa alınıyordu.
  2. Sıfırlanma notunda ÇIKIŞ yoktu: kullanıcı sebebini okuyor ama
     bir daha olmasını engelleyemiyordu.
  3. Devralan sekme, diskteki ayarı KENDİ bayat değeriyle eziyordu —
     kapatılmış "uzak kalınca sıfırla" ayarı geri açılıyordu.
  4. (En temeli) Günlük sayılar İKİ AYRI ANAHTARDA yaşıyor. Anlık
     kayıt kaybolunca bugün sıfıra düşüyordu — oysa arşivde duruyordu.

HER ÖLÇÜMÜN KARŞI KONTROLÜ VAR. "Sayı yerinde kaldı" tek başına kanıt
değildir: ölçümün o yoldan gerçekten geçtiğini de göstermek gerekir.
Bu dosyada iki yönlü sınama özellikle önemli — veriyi KORUYAN bir
düzeltme, kolayca veri UYDURAN bir düzeltmeye dönüşebilir.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BURASI = os.path.dirname(os.path.abspath(__file__))
if BURASI not in sys.path:
    sys.path.insert(0, BURASI)

import ekran_denetle as ED

sonuc = []

# KAC OLCUM KOSMALI. Bu sayi olmadan "TAMAM — 19 olcum" ile
# "TAMAM — 24 olcum" ayni gorunur: sessizce KOSMAYAN bir kontrol,
# GECEN bir kontrol gibi okunur. Merkez bugun ayni acigi kendi
# aracinda buldu (K-89) ve haber verdi; burada da vardi.
#
# Yeni olcum ekleyince bu sayiyi da buyut -- bilerek zahmetli:
# sayiyi guncellemek, kontrolun kostugunu ONAYLAMAK demek.
BEKLENEN_OLCUM = 24


def kontrol(ad, gecti, ayrinti=""):
    sonuc.append((gecti, ad, ayrinti))
    print(("  + " if gecti else "  X ") + ad + ("  — " + ayrinti if ayrinti else ""))


BUGUN_JS = """
  const g = new Date();
  const bugun = g.getFullYear() + '-'
    + String(g.getMonth() + 1).padStart(2, '0') + '-'
    + String(g.getDate()).padStart(2, '0');
"""


def yeni_olcum_baglami(t, port, arka_plan_acik):
    """Arka plan ayarı belli bir değere KURULMUŞ taze oturum."""
    bg = t.new_context(viewport={"width": 390, "height": 844}, locale="tr-TR")
    # OLCULEMEYEN SURE DEPODAN GELIYOR, sayfa acildiktan sonra
    # motora elle yazilarak DEGIL: cizim kendi ic degiskeninden okuyor
    # ve disaridan yazilan dizi hic gorunmuyordu -- ilk yazimda tam bu
    # oldu ve olcum "cumle yok" dedi, oysa senaryo hic kurulmamisti.
    bg.add_init_script("""
      try {
        const g = new Date();
        const s = g.getHours();
        const kova = new Array(24).fill(0);
        const olcusuz = new Array(24).fill(0);
        kova[s] = 600;          // 10 dk olculdu
        olcusuz[s] = 1800;      // 30 dk olculemedi
        const gun = g.getFullYear() + '-'
          + String(g.getMonth() + 1).padStart(2, '0') + '-'
          + String(g.getDate()).padStart(2, '0');
        localStorage.setItem('goz-molasi-v1', JSON.stringify({
          arkaPlanAcik: %s,
          istatistik: { gun: gun, ekranSuresi: 600,
                        saatlik: kova, olculemeyen: olcusuz },
        }));
      } catch (e) {}
    """ % ("true" if arka_plan_acik else "false"))
    s = bg.new_page()
    hata = []
    s.on("pageerror", lambda e: hata.append(str(e)[:120]))
    s.goto("http://127.0.0.1:%d/index.html" % port, wait_until="load", timeout=30000)
    s.wait_for_timeout(2000)
    return bg, s, hata


def olc(t, port):
    """Bütün ölçümler AYRI oturumlarda: biri ötekinin deposunu görmesin."""

    def yeni(tohum=""):
        bg = t.new_context(viewport={"width": 390, "height": 844}, locale="tr-TR")
        if tohum:
            # TOHUM `add_init_script` ILE EKILIYOR, sayfa acildiktan
            # sonra DEGIL. Sayfanin kendi `kaydet()`i (pagehide /
            # visibilitychange) yenileme sirasinda tohumu EZIYOR;
            # 06.09.2026'da tam bu yuzden calisan bir duzeltme
            # "calismiyor" gorundu. Olcumun kendisi yanlis olabilir.
            bg.add_init_script(tohum)
        s = bg.new_page()
        hata = []
        s.on("pageerror", lambda e: hata.append(str(e)[:120]))
        s.goto("http://127.0.0.1:%d/index.html" % port,
               wait_until="load", timeout=30000)
        s.wait_for_timeout(2000)
        return bg, s, hata

    def yaz(s, kimlik):
        return s.eval_on_selector("#" + kimlik, "e => e.textContent.trim()")

    # ---------------------------------------------------------------
    # 1. ANLIK KAYIT GİTTİ, ARŞİV DURUYOR -> BUGÜN GERİ GELİYOR
    # ---------------------------------------------------------------
    bg, s, hata = yeni("""
      try {
        %s
        const kova = new Array(24).fill(0);
        kova[9] = 1800;
        localStorage.setItem('goz-molasi-gecmis', JSON.stringify({
          [bugun]: { mola: 6, atlanan: 2, ekran: 5400, saatlik: kova },
        }));
        localStorage.removeItem('goz-molasi-v1');
      } catch (e) {}
    """ % BUGUN_JS)
    kontrol("anlık kayıt yokken bugün ARŞİVDEN geri geliyor (6 mola)",
            yaz(s, "istMola").startswith("6"), "ekranda: " + yaz(s, "istMola"))
    kontrol("ekran süresi de geri geliyor (90 dk)",
            yaz(s, "istSure").startswith("90"), "ekranda: " + yaz(s, "istSure"))
    kontrol("atlanan mola da geri geliyor (2)",
            yaz(s, "istAtlanan").startswith("2"), "ekranda: " + yaz(s, "istAtlanan"))
    kontrol("KONTROL — geri yüklemede sayfa hatası yok",
            not hata, "; ".join(hata[:1]) or "0 hata")
    bg.close()

    # ---------------------------------------------------------------
    # 2. KARŞI KONTROL: ARŞİV DE YOKSA SIFIR — VERİ UYDURULMAZ
    #
    #    Bu ölçüm olmadan birincisi hiçbir şey ifade etmez: her zaman
    #    "6" yazan bir ekran da o sınamayı geçerdi.
    # ---------------------------------------------------------------
    bg, s, hata = yeni("""
      try {
        localStorage.removeItem('goz-molasi-gecmis');
        localStorage.removeItem('goz-molasi-v1');
      } catch (e) {}
    """)
    kontrol("KONTROL — arşiv de yoksa sıfır (veri uydurulmuyor)",
            yaz(s, "istMola").startswith("0"), "ekranda: " + yaz(s, "istMola"))
    bg.close()

    # ---------------------------------------------------------------
    # 3. ARŞİV SAYIYI DÜŞÜREMEZ — YALNIZ YUKARI
    #
    #    Bugünün canlı sayısı arşivdekinden BÜYÜKSE arşiv onu geri
    #    çekmemeli. Aksi hâlde "sıfırlanmayı önleyen" düzeltmenin
    #    kendisi sayıyı geri alan bir hataya dönerdi.
    # ---------------------------------------------------------------
    bg, s, hata = yeni("""
      try {
        %s
        localStorage.setItem('goz-molasi-gecmis', JSON.stringify({
          [bugun]: { mola: 1, atlanan: 0, ekran: 60 },
        }));
        localStorage.setItem('goz-molasi-v1', JSON.stringify({
          istatistik: { gun: bugun, tamamlananMola: 9, atlananMola: 0,
                        ekranSuresi: 3600, kesintisizSure: 0 },
        }));
      } catch (e) {}
    """ % BUGUN_JS)
    kontrol("arşiv KÜÇÜKSE canlı sayı düşmüyor (9 kaldı)",
            yaz(s, "istMola").startswith("9"), "ekranda: " + yaz(s, "istMola"))
    bg.close()

    # ---------------------------------------------------------------
    # 3b. TAVAN HER OKUMA YOLUNDA (K-102)
    #
    #     `istatistikSuz` günlük sayılara tavan koyuyor — ama YALNIZ
    #     diskten okuma yolunda. Kalıcı arşive yazan yol ondan
    #     geçmiyordu: bozuk tek bir kayıt ("ekran: 1e9") arşive girip
    #     her okuyanda öyle görünürdü. Korumayı yazmak yetmez, her
    #     kullanım yerine taşımak gerekir.
    # ---------------------------------------------------------------
    bg, s, hata = yeni("""
      try {
        %s
        localStorage.setItem('goz-molasi-gecmis', JSON.stringify({
          [bugun]: { mola: 999999, atlanan: 0, ekran: 1e9 },
        }));
        localStorage.removeItem('goz-molasi-v1');
      } catch (e) {}
    """ % BUGUN_JS)
    mola_yazi = yaz(s, "istMola")
    sure_yazi = yaz(s, "istSure")
    kontrol("arşivdeki TAVAN ÜSTÜ mola sayısı ekrana çıkmıyor",
            not mola_yazi.startswith("999"), "ekranda: " + mola_yazi)
    kontrol("arşivdeki tavan üstü ekran süresi ekrana çıkmıyor",
            "1000000" not in sure_yazi.replace(".", "").replace(",", ""),
            "ekranda: " + sure_yazi)
    bg.close()

    # ---------------------------------------------------------------
    # 3c. "NEDEN SAYMIYOR" SORUSUNUN CEVABI EKRANDA MI?
    #
    #     Kullanıcı (07.09.2026): "neden saymayı bırakıyor uygulama ya".
    #     Sayfa "ölçemedik" diyordu ama bunu DÜZELTEN ayarı
    #     söylemiyordu. Sebebi yazmak, çareyi yazmadan yarım kalıyor.
    #
    #     Ayar AÇIKSA cümle çıkmamalı: zaten yapmış birine "şunu yap"
    #     demek okunmayan bir uyarı üretir.
    # ---------------------------------------------------------------
    for acik, beklenen in ((False, True), (True, False)):
        bg, s, hata = yeni_olcum_baglami(t, port, acik)
        s.eval_on_selector_all(".saatlik-sutun",
                               "els => { const s = new Date().getHours();"
                               " els[s] && els[s].click(); }")
        s.wait_for_timeout(400)
        yazi = s.eval_on_selector("#saatlikAyrinti", "e => e.textContent")
        var = "Arka planda çalışmaya devam edersem" in yazi
        kontrol("arka plan ayarı %s iken çare cümlesi %s"
                % ("KAPALI" if not acik else "AÇIK",
                   "yazıyor" if beklenen else "yazmıyor"),
                var is beklenen, yazi.strip()[-80:] or "boş")

        # DUGME: care sorunun YANINDA mi, ayarlar penceresinde mi?
        dugme = s.evaluate("() => { const b = document.getElementById"
                           "('arkaPlanAc');"
                           " return !!b && !b.classList.contains('gizli'); }")
        kontrol("arka plan ayarı %s iken tek dokunuşluk düğme %s"
                % ("KAPALI" if not acik else "AÇIK",
                   "görünüyor" if beklenen else "görünmüyor"),
                dugme is beklenen, "düğme görünür: %s" % dugme)

        if beklenen:
            # BASINCA GERCEKTEN ACIYOR MU? Ayni yolu ayarlar
            # penceresindeki anahtar da kullaniyor.
            s.eval_on_selector("#arkaPlanAc", "e => e.click()")
            s.wait_for_timeout(500)
            durum = s.evaluate("""() => {
              const h = JSON.parse(localStorage.getItem('goz-molasi-v1') || '{}');
              const b = document.getElementById('arkaPlanAc');
              const k = document.getElementById('ayArkaPlan');
              return { diskte: h.arkaPlanAcik === true,
                       dugmeGizli: !!b && b.classList.contains('gizli'),
                       anahtar: !!k && k.checked };
            }""")
            kontrol("düğmeye basınca ayar DİSKE yazılıyor",
                    durum["diskte"] is True, "diskte: %s" % durum["diskte"])
            kontrol("ayarlar penceresindeki anahtar da işaretleniyor",
                    durum["anahtar"] is True, "anahtar: %s" % durum["anahtar"])
            kontrol("iş bitince düğme kayboluyor (tekrar sormuyor)",
                    durum["dugmeGizli"] is True)
        bg.close()

    # ---------------------------------------------------------------
    # 4. DEVRALAN SEKME DİSKTEKİ AYARLARI EZMİYOR
    #
    #    Sıfırlanmanın üçüncü sebebi: ikinci sekme devralınca kendi
    #    bayat değerini diske yazıyor, kapatılmış "uzak kalınca
    #    sıfırla" ayarı geri açılıyordu.
    # ---------------------------------------------------------------
    bg, s, hata = yeni("""
      try {
        const ham = JSON.parse(localStorage.getItem('goz-molasi-v1') || '{}');
        ham.puan = 240;
        ham.arkaPlanAcik = true;
        ham.uzakSifirla = false;
        ham.uzakSifirlaSecildi = true;
        ham.ayarlar = Object.assign({}, ham.ayarlar,
          { uzakKalincaSifirla: false });
        localStorage.setItem('goz-molasi-v1', JSON.stringify(ham));
        // BASKA bir sekme lider ve TAZE: devralmak zorunda kalsin.
        localStorage.setItem('goz-molasi-lider', JSON.stringify(
          { kimlik: 'baska-sekme-olcum', an: Date.now() }));
      } catch (e) {}
    """)
    ortu = s.evaluate("() => { const e = document.getElementById('ikinciSekme');"
                      " return !!e && !e.hidden; }")
    kontrol("KONTROL — başka lider varken 'ikinci sekme' örtüsü çıkıyor",
            ortu is True, "çıkmazsa devralma yolu hiç ölçülmemiş olur")
    s.eval_on_selector("#buradaDevamDugme", "e => e.click()")
    s.wait_for_timeout(1500)
    d = s.evaluate("""() => {
      const h = JSON.parse(localStorage.getItem('goz-molasi-v1') || '{}');
      return { puan: h.puan, arkaPlan: h.arkaPlanAcik,
               uzak: h.ayarlar && h.ayarlar.uzakKalincaSifirla };
    }""")
    kontrol("devralan sekme `puan`ı ezmiyor", d["puan"] == 240,
            "diskte: %s" % d["puan"])
    kontrol("devralan sekme `arkaPlanAcik` ayarını ezmiyor",
            d["arkaPlan"] is True, "diskte: %s" % d["arkaPlan"])
    kontrol("devralan sekme `uzakKalincaSifirla`yı ezmiyor",
            d["uzak"] is False, "diskte: %s" % d["uzak"])
    bg.close()

    # ---------------------------------------------------------------
    # 5. GİZLENİRKEN DİSKE YAZILIYOR
    #
    #    Sıfırlanmanın birinci sebebi: kayıt yalnız `pagehide` ve 15
    #    saniyelik zamanlayıcıya bağlıydı. Telefonda `pagehide`
    #    garanti değil; uygulama öldürülünce son dakikalar kayboluyor
    #    ve sonraki açılış sayacı başa alıyordu.
    # ---------------------------------------------------------------
    bg, s, hata = yeni("""
      try { localStorage.removeItem('goz-molasi-v1'); } catch (e) {}
    """)
    s.evaluate("() => { try { localStorage.removeItem('goz-molasi-v1'); }"
               " catch (e) {} }")
    yoktu = s.evaluate("() => !localStorage.getItem('goz-molasi-v1')")
    # `document.hidden` DE TAKLIT EDILIYOR -- ikisi ayri ozellik.
    # Ilk yazimda yalniz `visibilityState` degistirilmisti; kodun
    # okudugu ise `document.hidden`. Olcum "kayit yazilmiyor" dedi,
    # oysa yazan yol hic calistirilmamisti. Bu depoda bilinen tuzak:
    # once olcumun kendisinden suphelen.
    s.evaluate("""() => {
      Object.defineProperty(document, 'hidden',
        { get: () => true, configurable: true });
      Object.defineProperty(document, 'visibilityState',
        { get: () => 'hidden', configurable: true });
      document.dispatchEvent(new Event('visibilitychange'));
    }""")
    s.wait_for_timeout(600)
    yazildi = s.evaluate("() => !!localStorage.getItem('goz-molasi-v1')")
    kontrol("KONTROL — kayıt önce gerçekten yoktu", yoktu is True)
    kontrol("sayfa gizlenince kayıt diske YAZILIYOR", yazildi is True,
            "yazılmazsa son dakikalar kaybolur ve sayaç başa döner")
    bg.close()

    # ---------------------------------------------------------------
    # 6. DAMGAYI BIRAKAN SEKME KENDİNİ LİDER SANMIYOR
    #
    #    `pagehide` damgayı siliyordu ama bayrak true kalıyordu:
    #    bfcache'ten dönen sekme gerçek liderin sayacını bayat
    #    değeriyle diske yazıp eziyordu.
    # ---------------------------------------------------------------
    bg, s, hata = yeni()
    liderdi = s.evaluate("() => !!localStorage.getItem('goz-molasi-lider')")
    s.evaluate("() => window.dispatchEvent("
               "new PageTransitionEvent('pagehide', { persisted: true }))")
    s.wait_for_timeout(300)
    gitti = s.evaluate("() => !localStorage.getItem('goz-molasi-lider')")
    s.evaluate("""() => {
      localStorage.setItem('goz-molasi-lider', JSON.stringify(
        { kimlik: 'baska-sekme-olcum', an: Date.now() }));
      window.dispatchEvent(new PageTransitionEvent('pageshow',
        { persisted: true }));
    }""")
    s.wait_for_timeout(3500)
    ortu2 = s.evaluate("() => { const e = document.getElementById('ikinciSekme');"
                       " return !!e && !e.hidden; }")
    kontrol("KONTROL — sekme önce gerçekten liderdi", liderdi is True)
    kontrol("`pagehide` lider damgasını bırakıyor", gitti is True)
    kontrol("damgayı bırakan sekme kendini LİDER SANMIYOR", ortu2 is True,
            "sanırsa gerçek liderin sayacını bayat değerle ezer")
    bg.close()


def calistir():
    from playwright.sync_api import sync_playwright
    port = ED.bos_port()
    # SUNUCUNUN KENDİ ÖLÜM SAATİ VAR: bir ölçüm çökse bile arkada
    # dinleyen bir sunucu kalmasın (06.09.2026'da unutulan sunucular
    # kullanıcının oyununu böldü).
    srv = ED.sunucu_baslat(port, 300)
    try:
        with sync_playwright() as p:
            t = p.chromium.launch(channel="msedge")
            try:
                olc(t, port)
            finally:
                t.close()
    finally:
        try:
            srv.shutdown()
        except Exception:
            pass

    kotu = [a for g, a, _ in sonuc if not g]
    print()
    if len(sonuc) < BEKLENEN_OLCUM:
        print("BASARISIZ — %d olcum kosmasi gerekirken %d kostu."
              % (BEKLENEN_OLCUM, len(sonuc)))
        print("  Eksik kontrol SESSIZCE atlandi. Bir oge adi degismis ya da")
        print("  bir dal hic girilmemis olabilir; 'gecti' diyen satirlar bu")
        print("  yuzden hicbir sey ifade etmiyor.")
        return False
    if kotu:
        print("BAŞARISIZ — %d ölçüm tutmadı:" % len(kotu))
        for a in kotu:
            print("  -", a)
        return False
    print("TAMAM — %d ölçüm; sıfırlanmanın dört sebebi de kapalı." % len(sonuc))
    return True


if __name__ == "__main__":
    sys.exit(0 if calistir() else 1)
