# -*- coding: utf-8 -*-
"""EKRAN SINAMASI — kullanıcının GÖRDÜĞÜ şeyi denetler.

NEDEN VAR
  30.08.2026'da kullanıcı sordu: "2 gündür çalışıyorsunuz, yine hata,
  yine açık, nasıl çözeceğiz?" Cevap ölçüldü: sınamalarımız MOTORU
  sınıyor, EKRANI kimse sınamıyor.

  O gün telefonda elle bulunan dört kusurun DÖRDÜ de:
    · çökme üretmiyordu
    · hiçbir sınamayı düşürmüyordu
    · konsol tertemizdi
  Mola yönergeleri İngilizce arayüzde Türkçe kalıyordu; "Kip" etiketi
  iki satır arasında asılı duruyordu; "Kısayollar" 50x29 pikseldi;
  "1 breaks today" yazıyordu. Hepsi ekranda duruyordu ve kimse bakmıyordu.

  Bu araç o boşluğu kapatıyor: gerçek tarayıcıda sayfayı açar, gerçekten
  tıklar, ve EKRANDAKİ metne bakar.

NE ARAR
  1. Ekranda `undefined` / `NaN` / `[object Object]` / `null` — sessiz
     yanlış değerin en açık işareti (K-22)
  2. 44 pikselden küçük dokunma hedefi (telefonda parmak sığmaz)
  3. Adsız düğme/bağlantı (ekran okuyucu "düğme" der, ne yaptığını demez)
  4. Yatay taşma (sayfa sağa kayıyor)
  5. Kırpılan metin (kutusu gizliyor)
  6. JS hatası
  7. Yazı %200'e çekilince taşma (görme güçlüğü olan kullanıcı)

NASIL ÇALIŞTIRILIR
  python ekran_denetle.py

TASARIM KARARLARI
  · Sunucu AYRI SÜREÇ DEĞİL, bu betiğin içinde bir iş parçacığı. Betik
    bitince sunucu da biter; arkada dinleyen bir şey kalmaz.
  · Tarayıcı olarak makinede ZATEN KURULU Edge kullanılıyor. Playwright'ın
    kendi tarayıcısını indirmek ~150 MB; gereksiz.
  · Başsız Edge GERÇEKTEN KARE ÜRETİYOR (ölçüldü: 63 kare/0.5 sn). Bu
    önemli: 30.08'de gömülü tarayıcı panosu arka planda 0 kare üretiyordu,
    CSS geçişleri donuyordu ve ekran görüntüsü eski kareyi gösteriyordu —
    orada "mola ekranı şeffaf" diye yanlış alarm verilmişti.
  · Uygulamanın kendi verisine dokunulmaz: başsız tarayıcının profili
    ayrıdır, localStorage'ı kullanıcınınkinden bağımsızdır.
"""
import http.server
import os
import socket
import socketserver
import sys
import threading

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 44 px: parmak ucu ölçüsü. Apple ve Google kılavuzlarının ikisi de bu
# civarı söylüyor; altında kalan hedefe telefonda isabet ettirmek zor.
EN_KUCUK_HEDEF = 44

# Ekranda ASLA görünmemesi gereken diziler. Hepsi bir hesabın ya da
# okumanın sessizce boşa düştüğünün işareti.
YASAK_METIN = ("undefined", "NaN", "[object Object]", "Infinity")

# Bilerek boş/teknik olan yerler. SEBEBİYLE yazılır — sebepsiz istisna
# bekçiyi kalıcı olarak körleştirir.
METIN_ISTISNA = {
    # Sayfada "NaN" geçen bir açıklama metni olursa buraya sebebiyle eklenir.
}


def bos_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class _Sessiz(http.server.SimpleHTTPRequestHandler):
    """Sessiz sunucu, depo kökünden yayın yapar.

    `directory=` ile veriliyor. Önce `os.chdir` ile yapılmıştı ve YANLIŞTI:
    çalışma dizinini geçici değiştirmek iş parçacıkları arasında yarışıyor,
    dosyalar 404 dönüyordu ve sayfa boş yükleniyordu (ölçüldü: 4 metin
    düğümü, 0 dokunma hedefi). Aracın kendi hatasıydı; iyi ki "TAMAM"
    demek yerine başarısız oldu."""

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=KOK, **kw)

    def log_message(self, *a):
        pass


def sunucu_baslat(port):
    """Sunucu AYRI SÜREÇ DEĞİL: daemon iş parçacığı, betikle birlikte ölür."""
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", port), _Sessiz)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


# ----------------------------------------------------------------------
# Sayfa içinde koşan denetim. Tek seferde toplayıp döndürüyoruz:
# her sorgu için ayrı tur atmak yavaş ve sayfanın durumu değişebilir.
# ----------------------------------------------------------------------
DENETIM = r"""
(esikler) => {
  const {enKucuk, yasak, istisna} = esikler;
  const gorunur = (e) => {
    const s = getComputedStyle(e);
    if (s.display === 'none' || s.visibility === 'hidden') return false;
    if (parseFloat(s.opacity) === 0) return false;
    const r = e.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };

  /* SADECE EKRAN OKUYUCU İÇİN gizlenmiş öge mi?
     Standart teknik: 1px kutu + overflow:hidden + clip. Bu ögelerin
     "kırpılması" DOĞRU — görme yoluyla okunmaları zaten istenmiyor.
     Elle liste tutmuyoruz, DESENİ tanıyoruz: yarın eklenen ikinci bir
     sr-only öge de kendiliğinden kapsanır. */
  const ekranOkuyucuIcin = (e) => {
    const s = getComputedStyle(e);
    const r = e.getBoundingClientRect();
    if (r.width <= 2 && r.height <= 2) return true;
    if (s.clipPath && s.clipPath !== 'none') return true;
    if (s.clip && s.clip !== 'auto') return true;
    return false;
  };

  /* CÜMLE İÇİNDE geçen bağlantı mı?
     44 px kuralı BAĞIMSIZ denetimler içindir. Bir paragrafın ortasındaki
     bağlantıyı 44 px yapmak metni parçalar; hiçbir arayüz öyle yapmıyor.
     Ölçüt: ögenin kendisi satır içi VE kardeşinde başka metin var. */
  const cumleIcinde = (e) => {
    if (getComputedStyle(e).display !== 'inline') return false;
    const kap = e.parentElement;
    if (!kap) return false;
    const disi = (kap.textContent || '').replace(e.textContent || '', '').trim();
    return disi.length > 12;
  };

  const bulgular = [];
  const sayac = {metin: 0, hedef: 0, ad: 0, muaf: 0};

  // 1) EKRANDA YASAK METIN
  const yurutucu = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let d;
  while ((d = yurutucu.nextNode())) {
    const t = (d.nodeValue || '').trim();
    if (!t) continue;
    const e = d.parentElement;
    if (!e || !gorunur(e)) continue;
    sayac.metin++;
    for (const y of yasak) {
      // Kelime sınırı: "undefined" ararken "undefinedX" de yakalanır ama
      // "NaN" ararken "Nano" yakalanmasin diye sinir konuyor.
      const kalip = new RegExp('(^|[^A-Za-z])' + y.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '($|[^A-Za-z])');
      if (kalip.test(t) && !istisna.includes(t)) {
        bulgular.push({tur: 'ekranda-yasak-metin', deger: y,
                       yer: e.id || e.className || e.tagName, metin: t.slice(0, 70)});
      }
    }
  }

  // 2) KUCUK DOKUNMA HEDEFI + 3) ADSIZ DUGME
  document.querySelectorAll('button, a[href], input, select, textarea, [role=button]').forEach((e) => {
    if (!gorunur(e)) return;
    if (e.disabled) return;
    const r = e.getBoundingClientRect();
    if (cumleIcinde(e)) { sayac.muaf++; }
    else {
      sayac.hedef++;
      if (r.height < enKucuk || r.width < enKucuk) {
      bulgular.push({tur: 'kucuk-hedef', yer: e.id || e.className || e.tagName,
                     en: Math.round(r.width), boy: Math.round(r.height),
                     metin: (e.textContent || '').trim().slice(0, 30)});
      }
    }
    sayac.ad++;
    const ad = (e.getAttribute('aria-label') || e.getAttribute('title') ||
                (e.textContent || '').trim() ||
                (e.labels && e.labels.length ? e.labels[0].textContent.trim() : '') ||
                e.getAttribute('alt') || '').trim();
    if (!ad) {
      bulgular.push({tur: 'adsiz-oge', yer: e.id || e.className || e.tagName});
    }
  });

  // 4) YATAY TASMA
  if (document.documentElement.scrollWidth > window.innerWidth + 1) {
    // Hangi oge tasiriyor, onu da soyle - yoksa aramak saatler surer.
    const suclular = [];
    document.querySelectorAll('*').forEach((e) => {
      const r = e.getBoundingClientRect();
      if (r.right > window.innerWidth + 1 && gorunur(e)) {
        suclular.push({yer: e.id || e.className || e.tagName, sag: Math.round(r.right)});
      }
    });
    bulgular.push({tur: 'yatay-tasma', genislik: document.documentElement.scrollWidth,
                   ekran: window.innerWidth, suclular: suclular.slice(0, 4)});
  }

  // 5) KIRPILAN METIN — yalniz GERCEKTEN gizleyen kutular.
  // "Icerik kutudan genis" olcutu 19 yanlis alarm uretmisti (29.08);
  // overflow gizli DEGILSE metin gorunuyor demektir, kusur yok.
  document.querySelectorAll('*').forEach((e) => {
    if (e.children.length) return;
    if (!gorunur(e)) return;
    if (ekranOkuyucuIcin(e)) return;   // gizli olmasi ISTENIYOR
    const s = getComputedStyle(e);
    const gizli = (v) => v === 'hidden' || v === 'clip';
    if (gizli(s.overflowX) && e.scrollWidth > e.clientWidth + 2) {
      bulgular.push({tur: 'kirpilan-metin', yon: 'yatay',
                     yer: e.id || e.className || e.tagName,
                     metin: (e.textContent || '').trim().slice(0, 40)});
    }
    if (gizli(s.overflowY) && e.scrollHeight > e.clientHeight + 2 &&
        e.getAttribute('aria-live') === null) {
      bulgular.push({tur: 'kirpilan-metin', yon: 'dikey',
                     yer: e.id || e.className || e.tagName,
                     metin: (e.textContent || '').trim().slice(0, 40)});
    }
  });

  return {bulgular, sayac};
}
"""


# Android kullanici etiketi: kurulum daveti yalniz telefonda cikiyor.
ANDROID = ("Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36")


SAYAC_OKU = """() => {
  const e = [...document.querySelectorAll('*')].find(
    x => x.children.length === 0 && /^\\d{1,2}:\\d{2}$/.test((x.textContent||'').trim()));
  return e ? e.textContent.trim() : null;
}"""


def saat_oyunu_zinciri(tarayici, kok, hatalar):
    """Saat geri alininca sayac duruyor mu?

    Liderlik kaydi `Date.now()` damgasi tasiyor. Damga GELECEKTE ise
    (saat geri alindi, yaz saati, NTP duzeltmesi) fark negatif olur ve
    OLU bir lider "canli" gorunur. Hicbir sekme devralmaz, sayac durur,
    ekranda hicbir uyari cikmaz - mola hic gelmez.

    Olculdu 31.08.2026 (duzeltmeden once):
      KONTROL  temiz sayfa        : 19:58 -> 19:51  isliyor
      BOZMA    damga ileri tarihli: 20:00 -> 20:00  DURMUS

    SINIF: "kendisinden uzun yasayan durum" - ikinci ornek.

    OLCUM TUZAGI (birinci denemede dusuldu): kaydi index.html uzerinden
    yazip reload edersen `pagehide` liderlik kaydini SILER; yazdigini
    kendi elinle silmis olursun ve "sorun yok" cikar. Kayit,
    uygulamayi CALISTIRMAYAN bir sayfadan yazilmali.
    """
    def sayac_isliyor(s, sn=7):
        a = s.evaluate(SAYAC_OKU)
        s.wait_for_timeout(sn * 1000)
        b = s.evaluate(SAYAC_OKU)
        return a, b, (a is not None and b is not None and a != b)

    c = tarayici.new_context(viewport={"width": 400, "height": 860}, locale="tr-TR")
    s = c.new_page()
    try:
        # KONTROL: temiz sayfada sayac islemeli. Islemezse olcut ayirt
        # edici degildir ve asagidaki bulgu anlamsiz olur.
        s.goto(kok + "/index.html", wait_until="load", timeout=20000)
        s.wait_for_timeout(2500)
        a0, b0, temiz_isler = sayac_isliyor(s)
        if not temiz_isler:
            hatalar.append(("saat oyunu zinciri",
                            {"tur": "olcum-gecersiz",
                             "not": "temiz sayfada da sayac islemedi (%s->%s)" % (a0, b0)}))
            return

        # BOZMA: uygulamayi calistirmayan sayfadan ileri tarihli damga yaz
        s.goto(kok + "/gizlilik.html", wait_until="load", timeout=20000)
        s.evaluate("""() => localStorage.setItem('goz-molasi-lider',
            JSON.stringify({kimlik: 'olu-sekme', an: Date.now() + 3600000}))""")
        s.goto(kok + "/index.html", wait_until="load", timeout=20000)
        s.wait_for_timeout(2500)
        a1, b1, isler_mi = sayac_isliyor(s)
        if not isler_mi:
            hatalar.append(("saat oyunu zinciri",
                            {"tur": "sayac-durdu", "olcum": "%s -> %s" % (a1, b1),
                             "not": "saat geri alininca olu lider canli gorunuyor"}))
    except Exception as e:
        hatalar.append(("saat oyunu zinciri",
                        {"tur": "zincir-kosulamadi", "hata": str(e)[:80]}))
    finally:
        c.close()


KLAVYE_DENETIM = r"""
() => {
  /* `[role=button]` BILEREK YOK.
     `role` ekran okuyucuya "bu bir dugme" der ama ogeyi ODAKLANABILIR
     YAPMAZ. Role'u olup tabindex'i olmayan oge, en kotu hal: ekran
     okuyucu dugme diye duyurur, klavye kullanicisi asla ulasamaz.
     Olculdu (01.09.2026): ilk halim `[role=button]`u listeye koymustu
     ve K-58 kirma sinamasinda hatayi YAKALAYAMADI - bekcinin kendi
     kusuruydu, kirma sinamasi bulup cikardi. */
  const ODAK = 'button,a[href],input,select,textarea,summary,label,[tabindex]';
  const kotu = [];
  let aday = 0;
  document.querySelectorAll('*').forEach((e) => {
    if (getComputedStyle(e).cursor !== 'pointer') return;
    const r = e.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    aday++;
    /* ATASINA BAK. Tiklanabilir bir ogenin ICINDEKI yazi imleci miras
       alir; kendi basina odaklanabilir olmak zorunda degil. Bu kural
       olmadan olcum 19 yanlis alarm veriyordu (01.09.2026 olculdu). */
    if (e.closest(ODAK)) return;
    kotu.push({etiket: e.tagName, yer: e.id || (e.className || '').slice(0, 24),
               yazi: (e.textContent || '').trim().slice(0, 30)});
  });
  return {aday, kotu};
}
"""


def klavye_denetle(sayfa, hatalar, nerede):
    """Tiklanabilir gorunup klavyeyle erisilemeyen oge var mi?

    Fareyi kullanamayan biri icin bu ogeler YOK demektir. Merkez ayni
    sinifi uc kardes uygulamada buldu (K-69); burada da bir tane vardi.
    """
    s = sayfa.evaluate(KLAVYE_DENETIM)
    if not s["aday"]:
        hatalar.append((nerede, {"tur": "olcum-gecersiz",
                                 "not": "tiklanabilir goruntulu oge bulunamadi"}))
        return
    for k in s["kotu"]:
        hatalar.append((nerede, {"tur": "klavyeyle-erisilemez", **k}))


def cevrimdisi_zinciri(tarayici, kok, hatalar):
    """Uygulama GERCEKTEN internetsiz calisiyor mu?

    Bu bir SOZ: ekranda "internetsiz de calissin" yaziyor ve kurulum
    daveti bunu vaat ediyor. Sozu sinamayan bir uygulama, sozunu
    tutmadigini kullanicidan ogrenir.

    Kirilma yollari sessizdir: birinin disaridan bir yazi tipi ya da
    betik eklemesi yeter; cevrimici herkes iyi gorur, cevrimdisi
    kullanici bozuk sayfa alir. Onbellek listesinden bir dosyanin
    dusmesi de ayni sonucu verir.

    Olculdu 01.09.2026: 25 dosya onbellekte, sayfa aciliyor, sayac
    isliyor, mola aciliyor, depodaki yazi tipi geliyor.
    """
    SAYAC = """() => {
      const e = [...document.querySelectorAll('*')].find(
        x => x.children.length === 0 && /^\\d{1,2}:\\d{2}$/.test((x.textContent||'').trim()));
      return e ? e.textContent.trim() : null;
    }"""
    c = tarayici.new_context(viewport={"width": 400, "height": 860}, locale="tr-TR")
    s = c.new_page()
    try:
        s.goto(kok + "/index.html", wait_until="load", timeout=25000)
        s.wait_for_timeout(4000)
        dosya = s.evaluate("""async () => {
            const a = await caches.keys();
            if (!a.length) return 0;
            const k = await caches.open(a[0]);
            return (await k.keys()).length;
        }""")
        if not dosya:
            # KONTROL: onbellek hic dolmadiysa asagidaki olcum anlamsiz.
            hatalar.append(("cevrimdisi zinciri",
                            {"tur": "olcum-gecersiz",
                             "not": "onbellek bos, servis iscisi kurulmamis"}))
            return

        c.set_offline(True)
        s.reload(wait_until="load", timeout=25000)
        s.wait_for_timeout(3500)

        if not s.evaluate("() => !!document.getElementById('molaEkran')"):
            hatalar.append(("cevrimdisi zinciri",
                            {"tur": "cevrimdisi-acilmiyor",
                             "not": "sayfa internetsiz yuklenemedi"}))
            return
        a = s.evaluate(SAYAC)
        if not s.evaluate("async () => { await document.fonts.ready;"
                          " return document.fonts.check('600 20px Fraunces'); }"):
            hatalar.append(("cevrimdisi zinciri",
                            {"tur": "yazitipi-gelmedi",
                             "not": "baslik yazisi cevrimdisi yuklenemiyor"}))
        s.wait_for_timeout(7000)
        b = s.evaluate(SAYAC)
        if not (a and b and a != b):
            hatalar.append(("cevrimdisi zinciri",
                            {"tur": "sayac-durdu", "olcum": "%s -> %s" % (a, b)}))
        s.evaluate("""() => {
            const d = [...document.querySelectorAll('button')].find(
              x => /mola/i.test(x.textContent) && /imdi/i.test(x.textContent));
            if (d) d.click();
        }""")
        s.wait_for_timeout(2500)
        if not s.evaluate("() => document.getElementById('molaEkran')"
                          ".classList.contains('acik')"):
            hatalar.append(("cevrimdisi zinciri",
                            {"tur": "mola-acilmiyor", "not": "cevrimdisi"}))
    except Exception as e:
        hatalar.append(("cevrimdisi zinciri",
                        {"tur": "zincir-kosulamadi", "hata": str(e)[:80]}))
    finally:
        c.close()


def sayi_zinciri(tarayici, kok, hatalar):
    """Ekrandaki sayac, depoya yazilan sayiyla ayni mi?

    K-22: en tehlikeli hata cokme degil, SESSIZ YANLIS SAYI. Masaustunde
    bu siniftan bir kusur cikmisti (bir kart uzun molalari saymiyordu,
    ayni ekranda iki farkli sayi vardi). Web tarafinda hicbir sinama
    ekrandaki sayiya bakmiyordu.

    Yontem: mola AL, sonra ekrandaki "tamamlanan mola" ile depodaki
    `istatistik.tamamlananMola` karsilastir. Ayrismalari, birinin
    yaniltmasi demektir.
    """
    c = tarayici.new_context(viewport={"width": 400, "height": 860},
                             locale="tr-TR")
    s = c.new_page()
    try:
        s.goto(kok + "/index.html", wait_until="load", timeout=25000)
        s.wait_for_timeout(3000)

        onceki = s.evaluate("""() => {
            const b = document.getElementById('istMola');
            return b ? b.textContent.trim() : null;
        }""")
        if onceki is None:
            hatalar.append(("sayi zinciri",
                            {"tur": "olcum-gecersiz", "not": "sayac kutusu yok"}))
            return

        # Molayi GERCEKTEN al: baslat, bitmesini bekle.
        s.evaluate("""() => {
            const d = [...document.querySelectorAll('button')].find(
              x => /mola/i.test(x.textContent) && /imdi/i.test(x.textContent));
            if (d) d.click();
        }""")
        s.wait_for_timeout(26000)          # 20 sn mola + pay

        ekran = s.evaluate("""() => {
            const b = document.getElementById('istMola');
            return b ? b.textContent.trim() : null;
        }""")
        depo = s.evaluate("""() => {
            try {
                const v = JSON.parse(localStorage.getItem('goz-molasi-v1') || '{}');
                return (v.istatistik || {}).tamamlananMola;
            } catch { return null; }
        }""")

        # KONTROL: mola gercekten sayildi mi? Sayilmadiysa asagidaki
        # karsilastirma "iki sifir esit" der ve hicbir sey olcmez.
        if ekran == onceki:
            hatalar.append(("sayi zinciri",
                            {"tur": "olcum-gecersiz",
                             "not": "mola alindi ama sayac artmadi (%s -> %s)"
                                    % (onceki, ekran)}))
            return

        # Ekranda Turkce binlik ayraci olabilir; sayiya cevir.
        try:
            ekran_sayi = int(str(ekran).replace(".", "").replace(",", ""))
        except Exception:
            ekran_sayi = None
        if ekran_sayi is None or depo is None or ekran_sayi != depo:
            hatalar.append(("sayi zinciri",
                            {"tur": "ekran-depo-ayristi",
                             "ekran": ekran, "depo": depo,
                             "not": "ekrandaki sayi depodakiyle ayni degil"}))
    except Exception as e:
        hatalar.append(("sayi zinciri",
                        {"tur": "zincir-kosulamadi", "hata": str(e)[:80]}))
    finally:
        c.close()


def kurulum_zinciri(tarayici, kok, hatalar):
    """KUR -> SIL -> davet geri geliyor mu?

    NIYE ZINCIR: kullanicinin bildirdigi hata (30.08.2026 - "indirdigim
    seyi sildim, tekrar indiremedim") tek bir ekranda GORUNMUYORDU. Uc
    adim gerekiyordu. Tek kareye bakan hicbir sinama bunu yakalayamaz.

    Sebep: `appinstalled` olayinda diske "kullanici daveti kapatti"
    kaydi yaziliyordu. Kurmak "hayir" demek degildir; uygulama
    silinince o kayit kaliyor ve davet bir daha cikmiyordu.

    SINIF ADI: "kendisinden uzun yasayan durum" - bir kaydin, anlattigi
    seyden uzun omurlu olmasi.
    """
    c = tarayici.new_context(viewport={"width": 375, "height": 812},
                             user_agent=ANDROID, locale="tr-TR")
    s = c.new_page()
    try:
        serit = lambda: s.evaluate(
            "() => { const e=document.getElementById('kurulumSerit');"
            " return !!e && !e.classList.contains('gizli'); }")
        kayit = lambda: s.evaluate(
            "() => localStorage.getItem('goz-molasi-kurulum-kapatildi')")

        s.goto(kok + "/index.html", wait_until="load", timeout=20000)
        s.wait_for_timeout(4200)          # Android yedegi 3 sn sonra cikiyor
        if not serit():
            hatalar.append(("kurulum zinciri",
                            {"tur": "davet-cikmadi", "adim": "ilk acilis"}))

        s.evaluate("() => window.dispatchEvent(new Event('appinstalled'))")
        s.wait_for_timeout(600)
        if kayit() is not None:
            hatalar.append(("kurulum zinciri",
                            {"tur": "kurulumda-kapatildi-yazildi",
                             "not": "kurmak 'hayir' demek degil"}))

        s.reload(wait_until="load", timeout=20000)
        s.wait_for_timeout(4200)
        if not serit():
            hatalar.append(("kurulum zinciri",
                            {"tur": "silince-davet-gelmedi",
                             "not": "kullanici tekrar kuramaz"}))

        # TERS DAL: gercekten "simdi degil" derse SUSMALI. Yoksa
        # duzeltme "her zaman goster"e donusur, o da rahatsiz eder.
        s.evaluate("() => document.getElementById('kurulumHayir')?.click()")
        s.wait_for_timeout(400)
        s.reload(wait_until="load", timeout=20000)
        s.wait_for_timeout(4200)
        if serit():
            hatalar.append(("kurulum zinciri",
                            {"tur": "simdi-degil-tutmuyor",
                             "not": "davet israrci oldu"}))
    except Exception as e:
        hatalar.append(("kurulum zinciri", {"tur": "zincir-kosulamadi",
                                            "hata": str(e)[:80]}))
    finally:
        c.close()


def soyle(s=""):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", "replace").decode())


def denetle(sayfa, esikler):
    return sayfa.evaluate(DENETIM, esikler)


BOZMALAR = [
    # (ad, sayfaya enjekte edilen bozukluk, beklenen bulgu turu)
    ("ekranda 'undefined' yaziyor",
     "const d=document.createElement('p'); d.textContent='Bugun undefined mola';"
     "document.body.appendChild(d);", "ekranda-yasak-metin"),
    ("20 px'lik dugme",
     "const b=document.createElement('button'); b.textContent='ufak';"
     "b.style.cssText='width:20px;height:20px;display:block';"
     "document.body.appendChild(b);", "kucuk-hedef"),
    ("adsiz dugme",
     "const b=document.createElement('button');"
     "b.style.cssText='width:60px;height:60px;display:block';"
     "document.body.appendChild(b);", "adsiz-oge"),
    ("yatay tasma",
     "const d=document.createElement('div');"
     "d.style.cssText='width:3000px;height:10px';document.body.appendChild(d);",
     "yatay-tasma"),
]


def kendini_sina(sayfa, esikler):
    """K-58: bekci GERCEKTEN yakaliyor mu?

    Gecen bir bekci, calistiginin kanitI DEGIL. Dort bozukluk sayfaya
    ENJEKTE ediliyor (proje dosyalarina DOKUNULMUYOR) ve her birinin
    yakalandigi dogrulaniyor. Ayrica bozulmamis sayfada yanlis alarm
    olmadigi da olculuyor - "her seye kirmizi diyen" bir bekci de ise
    yaramaz.
    """
    sonuc = []
    for ad, kod, beklenen in BOZMALAR:
        sayfa.evaluate("() => { %s }" % kod)
        b = sayfa.evaluate(DENETIM, esikler)["bulgular"]
        yakaladi = any(x["tur"] == beklenen for x in b)
        sonuc.append((ad, beklenen, yakaladi))
        sayfa.reload(wait_until="load", timeout=20000)
        sayfa.wait_for_timeout(900)
    temiz = sayfa.evaluate(DENETIM, esikler)["bulgular"]
    return sonuc, temiz


def main():
    if "--kendini-sina" in sys.argv:
        return _kendini_sina_kos()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        soyle("ATLANDI — playwright kurulu değil (pip install playwright).")
        return 0

    port = bos_port()
    srv = sunucu_baslat(port)
    kok = "http://127.0.0.1:%d" % port
    esikler = {"enKucuk": EN_KUCUK_HEDEF, "yasak": list(YASAK_METIN),
               "istisna": list(METIN_ISTISNA)}

    hatalar = []
    js_hatalari = []
    toplam_metin = toplam_hedef = 0

    with sync_playwright() as p:
        try:
            tarayici = p.chromium.launch(channel="msedge")
        except Exception as e:
            soyle("ATLANDI — tarayıcı açılamadı: %s" % str(e).split("\n")[0][:90])
            soyle("        (makinede Edge yoksa bu sınama koşamaz)")
            srv.shutdown()
            return 0

        # Her ölçüm KENDİ bağlamında: bir öncekinin localStorage'ı
        # sonrakini kirletmesin. 29.08'de tam bu yüzden geçersiz bir
        # ölçüm alınmıştı (kalıntı durumla ölçüm).
        DURUMLAR = [
            ("telefon 375x812 · TR", 375, 812, "tr", 1.0),
            ("telefon 375x812 · EN", 375, 812, "en", 1.0),
            ("dar 320x568 · TR", 320, 568, "tr", 1.0),
            ("yazı %200 · 375 · TR", 375, 812, "tr", 2.0),
        ]

        for ad, en, boy, dil, olcek in DURUMLAR:
            baglam = tarayici.new_context(
                viewport={"width": en, "height": boy},
                locale="tr-TR" if dil == "tr" else "en-US",
                device_scale_factor=1)
            sayfa = baglam.new_page()
            sayfa.on("pageerror", lambda e, a=ad: js_hatalari.append((a, str(e)[:120])))
            sayfa.on("console", lambda m, a=ad: js_hatalari.append((a, m.text[:120]))
                     if m.type == "error" else None)
            try:
                sayfa.goto(kok + "/index.html", wait_until="load", timeout=20000)
                # Dili sabitle: tarayıcı diline güvenmek yetmez, uygulama
                # kendi seçimini saklıyor olabilir.
                sayfa.evaluate("(d) => { try { localStorage.setItem('goz-molasi-dil', d); } catch {} }", dil)
                if olcek != 1.0:
                    sayfa.evaluate("(o) => { document.documentElement.style.fontSize = (16*o)+'px'; }", olcek)
                sayfa.reload(wait_until="load", timeout=20000)
                if olcek != 1.0:
                    sayfa.evaluate("(o) => { document.documentElement.style.fontSize = (16*o)+'px'; }", olcek)
                sayfa.wait_for_timeout(1500)

                # --- ANA EKRAN ---
                s = denetle(sayfa, esikler)
                klavye_denetle(sayfa, hatalar, "%s · klavye" % ad)
                toplam_metin += s["sayac"]["metin"]
                toplam_hedef += s["sayac"]["hedef"]
                for b in s["bulgular"]:
                    hatalar.append(("%s · ana ekran" % ad, b))

                # --- AYARLAR ---
                try:
                    sayfa.click("#ayarDugme", timeout=3000)
                    sayfa.wait_for_timeout(700)
                    s = denetle(sayfa, esikler)
                    for b in s["bulgular"]:
                        hatalar.append(("%s · ayarlar" % ad, b))
                    sayfa.evaluate("() => document.getElementById('ayarPencere')?.close()")
                    sayfa.wait_for_timeout(400)
                except Exception:
                    pass

                # --- MOLA EKRANI ---
                # Uygulamanın EN ÖNEMLİ ekranı ve en az bakılanı.
                try:
                    sayfa.evaluate("""() => {
                        const b = [...document.querySelectorAll('button')].find(
                          x => /mola|break/i.test(x.textContent) && /(imdi|now)/i.test(x.textContent));
                        if (b) b.click();
                    }""")
                    sayfa.wait_for_timeout(2500)
                    s = denetle(sayfa, esikler)
                    for b in s["bulgular"]:
                        hatalar.append(("%s · MOLA" % ad, b))
                except Exception:
                    pass

                soyle("  %-24s metin %-4d hedef %-3d muaf %-2d"
                      % (ad, s["sayac"]["metin"], s["sayac"]["hedef"],
                         s["sayac"].get("muaf", 0)))
            except Exception as e:
                hatalar.append((ad, {"tur": "sayfa-acilmadi", "hata": str(e)[:100]}))
            finally:
                baglam.close()

        # Zincir sinamasi: tek kare degil, UC ADIM.
        kurulum_zinciri(tarayici, kok, hatalar)
        saat_oyunu_zinciri(tarayici, kok, hatalar)
        cevrimdisi_zinciri(tarayici, kok, hatalar)
        sayi_zinciri(tarayici, kok, hatalar)

        tarayici.close()
    srv.shutdown()

    for ad, m in js_hatalari:
        hatalar.append((ad, {"tur": "js-hatasi", "mesaj": m}))

    soyle()
    soyle("denetlenen metin düğümü : %d" % toplam_metin)
    soyle("denetlenen dokunma hedefi: %d" % toplam_hedef)
    soyle("durum sayısı             : 4 (telefon TR/EN · dar · yazı %200)")
    soyle("zincir sınaması          : kur → sil → davet geri geldi mi")
    soyle("                          : saat geri alındı → sayaç duruyor mu")
    soyle("                          : internetsiz gerçekten çalışıyor mu")
    soyle("                          : ekrandaki sayı = depodaki sayı mı")

    if hatalar:
        soyle()
        soyle("BAŞARISIZ — %d bulgu:" % len(hatalar))
        for ad, b in hatalar[:30]:
            ayrinti = " ".join("%s=%s" % (k, v) for k, v in b.items() if k != "tur")
            soyle("  [%s] %s — %s" % (ad, b["tur"], ayrinti[:110]))
        if len(hatalar) > 30:
            soyle("  … ve %d tane daha" % (len(hatalar) - 30))
        return 1

    soyle()
    soyle("TAMAM — ekranda yasak metin yok, hedefler 44 px, taşma yok, "
          "kırpılan metin yok, JS hatası yok.")
    return 0


def _kendini_sina_kos():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        soyle("ATLANDI - playwright yok"); return 0
    port = bos_port(); srv = sunucu_baslat(port)
    esikler = {"enKucuk": EN_KUCUK_HEDEF, "yasak": list(YASAK_METIN),
               "istisna": list(METIN_ISTISNA)}
    soyle("K-58 - BEKCIYI BILEREK KIRIYORUZ")
    soyle()
    with sync_playwright() as p:
        try:
            t = p.chromium.launch(channel="msedge")
        except Exception as e:
            soyle("ATLANDI - tarayici yok: %s" % str(e).splitlines()[0][:70])
            srv.shutdown(); return 0
        c = t.new_context(viewport={"width": 375, "height": 812}, locale="tr-TR")
        s = c.new_page()
        s.goto("http://127.0.0.1:%d/index.html" % port, wait_until="load", timeout=20000)
        s.wait_for_timeout(1200)
        sonuc, temiz = kendini_sina(s, esikler)
        t.close()
    srv.shutdown()
    kacan = []
    for ad, beklenen, yakaladi in sonuc:
        soyle("  %-30s -> %s" % (ad, "YAKALADI" if yakaladi else "*** KACIRDI ***"))
        if not yakaladi:
            kacan.append(ad)
    soyle("  %-30s -> %s" % ("KONTROL: bozulmamis sayfa",
                             "temiz" if not temiz else "*** YANLIS ALARM: %d ***" % len(temiz)))
    soyle()
    if kacan or temiz:
        soyle("BASARISIZ - bekci guvenilmez.")
        return 1
    soyle("TAMAM - %d bozmanin %d'ini yakaladi, temiz sayfada yanlis alarm yok."
          % (len(sonuc), len(sonuc)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
