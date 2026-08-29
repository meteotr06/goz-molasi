# -*- coding: utf-8 -*-
"""Çevrilmesi gereken her metin sözlükte var mı? — İKİ YOL BİRDEN

NİYE VAR
  Çeviri üç yoldan yapılıyor:
    • `CS(tr, en)` — iki dil YAN YANA yazılır, unutulması imkânsız.
    • `C(metin)`   — sözlükten arar; **sözlükte yoksa Türkçesini
      olduğu gibi döndürür.** Sessizce. Hata yok, uyarı yok.
    • `sayfayiCevir()` — HTML'deki metin DÜĞÜMLERİNİ gezer ve aynı
      sözlükten çevirir; **sözlükte yoksa Türkçesini olduğu gibi
      bırakır.** Yine sessizce.

  Yani hem `C()` ile yazılmış tek bir eksik anahtar, hem de HTML'e
  elle yazılmış tek bir Türkçe cümle, İngilizce arayüzde Türkçe bir
  yazı demek — ve kimse fark etmez, çünkü o metin yalnızca belirli
  bir DURUMDA ya da belirli bir yüzeyde ekrana gelir.

  Ölçüldü (28.08.2026): ekranda o an duran metinleri taramak
  yetmiyor. `DURUM_ADI` tablosundaki "Boşta — sayaç durdu" gibi
  yazılar yalnızca o duruma girilince çıkıyor; tarama sırasında
  ekranda olmadıkları için hiç denetlenmemişlerdi. (Denetlendi,
  yedisi de sözlükteydi — ama bunu ŞANS belirlememeli.)

  Bu, "ad listesiyle korunan her yer delinir" maddesinin çeviri
  hâli: tek tek bakmak yerine KURAL yazıyoruz.

  29.08.2026 — İKİNCİ YARISI EKLENDİ. Bu bekçi yalnızca `C()`
  çağrılarına bakıyordu ve "TAMAM" diyordu. Ama `sayfayiCevir()`
  aynı sözlüğü HTML metin düğümleri için de kullanıyor; o taraf
  hiç denetlenmiyordu. `index.html` 252 metin düğümü taşıyor —
  bekçinin gördüğü sayı SIFIRDI. Ölçüm yapılmayan yer, ölçülmüş
  görünüyordu.

HTML TARAFI NASIL ÖLÇÜLÜYOR
  Kapsam kuraldan: `dil.js`i YÜKLEYEN her HTML sayfası (bugün
  yalnızca `index.html`; `rehber.html`/`gizlilik.html` çeviriyi
  ayrı dosyayla yapıyor, `sayfayiCevir()` oralarda hiç koşmuyor).

  Her metin düğümü sırayla şu elekten geçiyor — hepsi SAYILIYOR,
  hiçbiri sessizce düşmüyor:
    1. Sözlükte var           → geçti
    2. İki dilli blok içinde  → istisna (KURAL)
    3. Türkçe'ye özgü harf yok→ kapsam dışı (aşağıdaki sınır)
    4. JS'te dizge olarak var → çalışma anında yazılıyor (KURAL)
    5. Elle istisna listesi   → sebebi yanında yazılı
    6. Kalan                  → BAŞARISIZ

  KARŞILAŞTIRMADAN ÖNCE İKİ TARAF DA DÜZLENİYOR. HTML ile JS aynı
  cümleyi farklı yazıyor: `&ldquo;`, satır kırığı, tipografik
  tırnak (’ “ ”), uzun tire, `…`. Ham karşılaştırma bunların
  hepsinde "eksik" diye bağırırdı. Düzleme: HTML varlıklarını çöz,
  JS kaçışlarını çöz, tırnak/tire çeşitlerini düzle, boşlukları tek
  boşluğa indir, küçük harfe çevir.

NİYE JS HAVUZU DAR (yalnızca arayuz.js, mola_icerik.js, reklam.js)
  Havuzu genişletmek bu kuralda TEHLİKELİ: `degisiklikler.js` 36 KB
  Türkçe değişiklik kaydı taşıyor. O da havuza girse, HTML'deki
  gerçek bir kaçak "JS'te geçiyor" diye AFFEDİLİRDİ. Dar havuz en
  fazla yanlış alarm verir; geniş havuz SESSİZLİK verir. Ekrana
  yazan dosyalar bunlar; taranan dosyalar çıktıya yazılıyor.

NE ÖLÇÜLMÜYOR
  • Çok satıra bölünmüş `C('...' + '...')` çağrıları. Bunlar ayrıca
    SAYILIP yazılıyor — sessizce atlanmıyorlar. Payda görünür olsun.
  • Türkçe'ye özgü harf içermeyen bir Türkçe metin (ör. "Tamam",
    "Sayac"). Bu sınır bilerek kabul edildi — `sinama_dil.py`
    aynı sınırı taşıyor; alternatifi her metni elle işaretlemekti.
  • HTML NİTELİKLERİ (`placeholder`, `title`, `aria-label`, `alt`).
    `sayfayiCevir()` onları da çeviriyor; burada ölçülmüyorlar.
    Bilinen açık.

ÇALIŞTIR
  python sinama_sozluk.py
"""
import html as htmlmod
import io
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

# KONSOL BULGUYU YUTMASIN. Windows konsolu cp1254; bulunan metinde
# `⊕` gibi bir karakter varsa `print` UnicodeEncodeError atiyor
# ve GERCEK BULGU ekrana hic gelmiyor - sinama "coktu" gorunuyor,
# "6 eksik metin var" demiyor. Olculdu: ilk kosuda tam bu oldu.
def soyle(s=""):
    try:
        print(s)
    except UnicodeEncodeError:
        kod = getattr(sys.stdout, "encoding", None) or "ascii"
        print(s.encode(kod, "replace").decode(kod, "replace"))

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ekrana yazan betikler. Bu liste NIYE dar - dosya basindaki
# "NIYE JS HAVUZU DAR" bolumune bak.
YAZAN_JS = ["arayuz.js", "mola_icerik.js", "reklam.js"]

# ELLE ISTISNALAR - her birinin SEBEBI yaninda.
#
# Kural: buraya yalnizca "cevrilmemesi DOGRU olan" metin girer.
# Bir madde artik hicbir metinle eslesmiyorsa sinama BASARISIZ der
# (asagida "kullanilmayan istisna"): olu istisna, olculmus gibi
# gorunen olculmemis alandir.
ELLE_ISTISNA = [
    (u"Hesap Araçları",
     u"baska uygulamanin MARKA adi (../hesap/ baglantisi) - cevrilmez"),
    (u"Kur Pusulası",
     u"baska uygulamanin MARKA adi (../kur/ baglantisi) - cevrilmez"),
    (u"Türkçe",
     u"dil seciciden dilin KENDI adi - Ingilizce arayuzde de 'Turkce' yazar"),
    (u"Başlat’a bas. 20 dakika sonra ekran 20 saniyeliğine kapanacak, "
     u"bu sırada gözünü 6 metre uzağa çevir.",
     u"#aciklama'nin VARSAYILANI; acilista arayuz.js `aciklamaMetni()` "
     u"(CS ile iki dilli) uzerine yaziyor. JS'teki cumle bilerek FARKLI "
     u"kuruldugu icin (sayi iceriyor) dizge kurali yakalayamiyor"),
]

# PAYDA ALT SINIRLARI - "sifir olcum = olculemedi".
# Bir kalip bozulursa sayilar cakilir; sinama sessizce TAMAM
# dememeli, OLCULEMEDI demeli.
EN_AZ_ANAHTAR = 50
EN_AZ_METIN = 100
EN_AZ_JS_DIZGE = 300


def oku(*yol):
    with io.open(os.path.join(KOK, *yol), encoding="utf-8") as d:
        return d.read()


def kok_dosyalari(desen):
    """Yayina giden kok dosyalari - elle listeden degil, depodan."""
    try:
        c = subprocess.run(["git", "ls-files", desen], cwd=KOK,
                           capture_output=True, text=True, encoding="utf-8")
        adlar = [y.strip() for y in c.stdout.splitlines() if y.strip()]
    except Exception as e:
        soyle("OLCULEMEDI - `git ls-files` calismadi: %s" % e)
        return []
    return [a for a in adlar
            if "/" not in a.replace("\\", "/")
            and not a.rsplit("/", 1)[-1].startswith("sinama")
            and not a.rsplit("/", 1)[-1].startswith("test-")]


def cevirenler():
    """`C()` çağırabilecek dosyalar KURALDAN türüyor.

    Bu bekçi önce yalnızca `arayuz.js`e bakıyordu ve bugün için
    DOĞRUYDU — ölçüldü (29.08.2026): `C()` çağrısı yalnızca orada var.
    Ama bu doğruluk KURALDAN değil ŞANSTAN geliyordu: yarın
    `mola_icerik.js`e bir `C('…')` eklenirse bekçi onu hiç görmez ve
    yine "TAMAM" der.

    Kapsam artık yayına giden bütün kök `.js` dosyaları; hangilerinin
    tarandığı çıktıya yazılıyor — payda görünmeden sonuç okunmaz.
    """
    return kok_dosyalari("*.js")


def cevrilen_sayfalar():
    """`sayfayiCevir()` HANGİ sayfalarda koşuyor? Kuraldan bul.

    Ölçüt: sayfa `dil.js`i yüklüyor mu. Bugün yalnızca `index.html`
    yüklüyor. Yarın `rehber.html` de yüklerse kapsama KENDİLİĞİNDEN
    girer — ad listesine eklenmeyi beklemez.
    """
    ci = []
    for ad in kok_dosyalari("*.html"):
        try:
            govde = oku(ad)
        except Exception:
            continue
        if re.search(r"""<script[^>]+src=['"][^'"]*dil\.js""", govde):
            ci.append((ad, govde))
    return ci


# ---------------------------------------------------------------
# DUZLEME - karsilastirmadan once iki tarafi da ayni bicime sok
# ---------------------------------------------------------------
TEK_TIRNAK = u"‘’‚‛′´"
CIFT_TIRNAK = u"“”„‟″«»"
TIRE = u"‐‑‒–—―−"

# Turkce'ye ozgu harfler (buyuk/kucuk). Kucultmeden ONCE bakilir:
# Python `'İ'.lower()` -> 'i' + U+0307 uretiyor, harf kayboluyor.
TR_OZGU = re.compile(u"[çğıöşü"
                     u"ÇĞİÖŞÜ]")


def duzle(s):
    """HTML varligi coz, tirnak/tire cesitlerini duzle, bosluklari tek
    bosluga indir, kucult. HTML ve JS ayni cumleyi farkli yaziyor."""
    s = htmlmod.unescape(s)
    for c in TEK_TIRNAK:
        s = s.replace(c, "'")
    for c in CIFT_TIRNAK:
        s = s.replace(c, '"')
    for c in TIRE:
        s = s.replace(c, "-")
    s = s.replace(u" ", " ").replace(u"…", "...")
    return re.sub(r"\s+", " ", s).strip().lower()


JS_KACIS = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f",
            "'": "'", '"': '"', "`": "`", "\\": "\\", "/": "/", "0": "\0"}


def js_coz(s):
    """JS dizge kacislarini coz: \\n, \\', \\u00e7 ..."""
    ci, i, n = [], 0, len(s)
    while i < n:
        if s[i] == "\\" and i + 1 < n:
            k = s[i + 1]
            if k == "u" and i + 5 < n:
                try:
                    ci.append(chr(int(s[i + 2:i + 6], 16)))
                    i += 6
                    continue
                except ValueError:
                    pass
            ci.append(JS_KACIS.get(k, k))
            i += 2
            continue
        ci.append(s[i])
        i += 1
    return "".join(ci)


# Duzenli ifade degismezi bu karakterlerden SONRA baslayabilir.
# (Bolme isareti ile ayirmak icin; `/['\"]/` gibi bir desen dizge
# cikaricisini kandirmasin diye.)
ONCE_REGEX = set("(,=:[!&|?{};+-*%<>~^\n")


def js_dizgeler(kaynak):
    """JS kaynagindan dizge degismezlerini cikar.

    YORUMLARI ATLIYOR. Bu onemli: bu dosyalarin yorumlari Turkce ve
    BOL. Yorum metni havuza girseydi HTML'deki gercek bir kacak
    "JS'te geciyor" diye affedilirdi - yani bekcinin sustugu yer
    tam da en cok Turkce metin bulunan yer olurdu.
    """
    ci = []
    i, n = 0, len(kaynak)
    onceki = "\n"
    while i < n:
        c = kaynak[i]
        if c == "/" and i + 1 < n and kaynak[i + 1] == "/":
            j = kaynak.find("\n", i)
            i = n if j < 0 else j + 1
            continue
        if c == "/" and i + 1 < n and kaynak[i + 1] == "*":
            j = kaynak.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if c == "/" and onceki in ONCE_REGEX:
            j, koseli, tamam = i + 1, False, False
            while j < n:
                if kaynak[j] == "\\":
                    j += 2
                    continue
                if kaynak[j] == "[":
                    koseli = True
                elif kaynak[j] == "]":
                    koseli = False
                elif kaynak[j] == "/" and not koseli:
                    tamam = True
                    break
                elif kaynak[j] == "\n":
                    break
                j += 1
            if tamam:
                i = j + 1
                onceki = "/"
                continue
        if c in ("'", '"', "`"):
            j, parca = i + 1, []
            while j < n:
                if kaynak[j] == "\\":
                    parca.append(kaynak[j:j + 2])
                    j += 2
                    continue
                if kaynak[j] == c:
                    break
                if c != "`" and kaynak[j] == "\n":
                    break
                parca.append(kaynak[j])
                j += 1
            ci.append("".join(parca))
            i = j + 1
            onceki = c
            continue
        if not c.isspace() or c == "\n":
            onceki = c
        i += 1
    return ci


# ---------------------------------------------------------------
# HTML metin dugumleri
# ---------------------------------------------------------------
BOS_ETIKET = {"br", "hr", "img", "input", "meta", "link", "source",
              "area", "base", "col", "embed", "param", "track", "wbr"}


class MetinToplayici(HTMLParser):
    """Metin düğümlerini ve "iki dilli blok" işaretini toplar.

    İKİ DİLLİ BLOK NEDİR — `#baslamadiUyari` kutusu betikler hiç
    gelmediğinde çıkıyor, yani `dil.js` de yokken. O yüzden metni
    HTML'de iki dilde SABİT yazılı (`<p lang="en">` yan yana duruyor).
    Sözlükte olmaması DOĞRU. Kural: bir öğenin DOĞRUDAN çocuğunda
    `lang="en"` varsa, o öğenin altı bilerek iki dillidir.
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.yigin = []          # [(etiket, kimlik)]
        self.sayac = 0
        self.metinler = []       # (metin, [kimlik...], etiket, satir)
        self.ikidilli = set()    # atlanacak oge kimlikleri

    def _isaretle(self, nitelikler):
        d = dict(nitelikler)
        if (d.get("lang") or "").lower().startswith("en"):
            if self.yigin:
                self.ikidilli.add(self.yigin[-1][1])
            return True
        return False

    def handle_starttag(self, etiket, nit):
        if etiket in BOS_ETIKET:
            self._isaretle(nit)
            return
        ingilizce = self._isaretle(nit)
        self.sayac += 1
        if ingilizce:
            self.ikidilli.add(self.sayac)
        self.yigin.append((etiket, self.sayac))

    def handle_startendtag(self, etiket, nit):
        self._isaretle(nit)

    def handle_endtag(self, etiket):
        for i in range(len(self.yigin) - 1, -1, -1):
            if self.yigin[i][0] == etiket:
                del self.yigin[i:]
                return

    def handle_data(self, veri):
        if not veri.strip():
            return
        etiketler = [e for e, _ in self.yigin]
        if "script" in etiketler or "style" in etiketler:
            return
        self.metinler.append((veri, [k for _, k in self.yigin],
                              etiketler[-1] if etiketler else "?",
                              self.getpos()[0]))


def sozluk_anahtarlari(dil):
    """`const SOZLUK = { ... };` bloğundaki anahtarlar.

    İKİ TIRNAK DA SAYILIR. Önceki hâli yalnızca tek tırnaklı
    anahtarları görüyordu; `dil.js` içinde kesme işareti taşıyan
    metinler çift tırnakla yazılmış (`"Dokunulmazsa sayaç durur;
    5 dk'dan…"`). Bekçi onları YOK sayıyordu — HTML denetimi
    eklendiğinde ilk verdiği alarmlar tam da bunlardı, yani
    sözlükte olan metinler "eksik" görünüyordu.

    Blokla sınırlı: dosyanın geri kalanındaki başka bir nesnenin
    anahtarı sözlükmüş gibi sayılmasın.
    """
    bas = dil.find("const SOZLUK = {")
    if bas < 0:
        return None
    son = dil.find("\n};", bas)
    if son < 0:
        return None
    govde = dil[bas:son]
    ci = re.findall(r"^[ \t]*(?:'((?:[^'\\]|\\.)*)'"
                    r"|\"((?:[^\"\\]|\\.)*)\")[ \t]*:", govde, re.M)
    return [a or b for a, b in ci]


def html_denetle(anahtar_duz):
    """HTML metin düğümleri sözlükten geçiyor mu? (0 = tamam)"""
    sayfalar = cevrilen_sayfalar()
    soyle()
    soyle("--- HTML metin dugumleri (sayfayiCevir) ---")
    if not sayfalar:
        soyle("OLCULEMEDI - `dil.js` yukleyen HTML sayfasi bulunamadi; "
              "kalip degismis olabilir. SESSIZ GECMIYORUZ.")
        return 1
    soyle("taranan sayfa       : %d (%s)"
          % (len(sayfalar), ", ".join(a for a, _ in sayfalar)))

    # Calisma aninda yazilan metinler icin JS dizge havuzu.
    havuz = []
    for ad in YAZAN_JS:
        try:
            havuz += [duzle(js_coz(x)) for x in js_dizgeler(oku(ad))]
        except Exception as e:
            soyle("OLCULEMEDI - %s okunamadi: %s" % (ad, e))
            return 1
    havuz = set(h for h in havuz if h)
    soyle("JS dizge havuzu     : %d (%s)"
          % (len(havuz), ", ".join(YAZAN_JS)))
    if len(havuz) < EN_AZ_JS_DIZGE:
        soyle("OLCULEMEDI - JS dizge havuzu beklenenden kucuk (%d < %d); "
              "cikarici bozulmus olabilir." % (len(havuz), EN_AZ_JS_DIZGE))
        return 1

    istisna_duz = [(duzle(m), m, sebep) for m, sebep in ELLE_ISTISNA]
    kullanilan = set()

    say = {"sozluk": 0, "ikidilli": 0, "trdegil": 0, "js": 0, "elle": 0}
    toplam = 0
    eksik = []

    for ad, govde in sayfalar:
        t = MetinToplayici()
        t.feed(govde)
        toplam += len(t.metinler)
        for metin, kimlikler, etiket, satir in t.metinler:
            d = duzle(metin)
            if d in anahtar_duz:
                say["sozluk"] += 1
                continue
            if any(k in t.ikidilli for k in kimlikler):
                say["ikidilli"] += 1
                continue
            if not TR_OZGU.search(metin):
                say["trdegil"] += 1
                continue
            if any(d in h for h in havuz):
                say["js"] += 1
                continue
            bulundu = False
            for i, (idz, _, _) in enumerate(istisna_duz):
                if d == idz:
                    kullanilan.add(i)
                    say["elle"] += 1
                    bulundu = True
                    break
            if bulundu:
                continue
            eksik.append((ad, satir, etiket, duzle(metin)))

    soyle("metin dugumu        : %d" % toplam)
    soyle("  sozlukte var      : %d" % say["sozluk"])
    soyle("  iki dilli blok    : %d  (kural: lang=\"en\" kardesi var)"
          % say["ikidilli"])
    soyle("  Turkce harf yok   : %d  (kapsam disi)" % say["trdegil"])
    soyle("  JS'te dizge       : %d  (kural: calisma aninda yaziliyor)"
          % say["js"])
    soyle("  elle istisna      : %d  (liste: %d madde)"
          % (say["elle"], len(ELLE_ISTISNA)))
    soyle("  KALAN             : %d" % len(eksik))

    if toplam < EN_AZ_METIN:
        soyle("OLCULEMEDI - yalnizca %d metin dugumu goruldu (en az %d "
              "bekleniyordu). Ayristirici bozulmus olabilir; SESSIZ "
              "GECMIYORUZ." % (toplam, EN_AZ_METIN))
        return 1

    hata = 0

    olu = [i for i in range(len(ELLE_ISTISNA)) if i not in kullanilan]
    if olu:
        soyle()
        soyle("BASARISIZ - %d elle istisna artik hicbir metinle "
              "eslesmiyor (olu istisna, olculmus gibi gorunur):" % len(olu))
        for i in olu:
            soyle("  - %s" % ELLE_ISTISNA[i][0][:80])
        soyle("  Yapilacak: metin degistiyse istisnayi guncelle, "
              "silindiyse istisnayi da sil.")
        hata = 1

    if eksik:
        soyle()
        soyle("BASARISIZ - sozlukte OLMAYAN %d HTML metni "
              "(Ingilizce arayuzde Turkce cikar):" % len(eksik))
        for ad, satir, etiket, d in eksik[:25]:
            soyle("  - %s:%d <%s> %s" % (ad, satir, etiket, d[:80]))
        if len(eksik) > 25:
            soyle("  ... ve %d tane daha" % (len(eksik) - 25))
        soyle()
        soyle("Yapilacak: metni `dil.js` sozlugune ekle. Cevrilmemesi")
        soyle("           DOGRUYSA ELLE_ISTISNA'ya SEBEBIYLE yaz.")
        hata = 1

    if not hata:
        soyle()
        soyle("TAMAM - HTML'deki her Turkce metin sozlukten geciyor.")
    return hata


def main():
    dosyalar = cevirenler()
    if not dosyalar:
        soyle("OLCULEMEDI - taranacak dosya listesi bos.")
        return 1
    soyle("taranan dosya : %d (%s)"
          % (len(dosyalar), ", ".join(sorted(dosyalar))))
    try:
        arayuz = "\n".join(oku(a) for a in dosyalar if a != "dil.js")
        dil = oku("dil.js")
    except Exception as e:
        soyle("OLCULEMEDI - dosya okunamadi: %s" % e)
        return 1

    ham = sozluk_anahtarlari(dil)
    if ham is None:
        soyle("OLCULEMEDI - `const SOZLUK = {` blogu bulunamadi; "
              "bicim degismis olabilir.")
        return 1
    anahtarlar = set(ham)
    if len(anahtarlar) < EN_AZ_ANAHTAR:
        soyle("OLCULEMEDI - sozluk beklenenden kucuk (%d anahtar); "
              "bicim degismis olabilir" % len(anahtarlar))
        return 1
    anahtar_duz = set(duzle(js_coz(a)) for a in anahtarlar)

    # `C('...')` — ama `CS(` degil. Onunden harf/alt tire gelmemeli.
    tekil = re.findall(r"(?<![A-Za-z_$])C\(\s*'((?:[^'\\]|\\.)*)'\s*\)", arayuz)

    # Kapanmayan (cok satirli / birlestirilmis) cagrilar: sayilsin,
    # sessizce dusmesin.
    coksatir = len(re.findall(r"(?<![A-Za-z_$])C\(\s*'(?:[^'\\]|\\.)*'\s*\+", arayuz))

    eksik = []
    for m in tekil:
        d = m.replace("\\'", "'").strip()
        if not d:
            continue
        if d not in anahtarlar and re.sub(r"\s+", " ", d) not in anahtarlar:
            eksik.append(d)

    # Tekrarlari at, sirayi koru.
    gorulen = set()
    benzersiz = []
    for d in eksik:
        if d not in gorulen:
            gorulen.add(d)
            benzersiz.append(d)

    soyle("sozluk anahtari      : %d" % len(anahtarlar))
    soyle("denetlenen C() metni : %d" % len(tekil))
    soyle("denetlenmeyen (cok satirli C()): %d" % coksatir)

    hata = 0
    if benzersiz:
        soyle()
        soyle("BASARISIZ - sozlukte OLMAYAN %d metin "
              "(Ingilizce arayuzde Turkce cikar):" % len(benzersiz))
        for d in benzersiz[:25]:
            soyle("  - %s" % d[:90])
        if len(benzersiz) > 25:
            soyle("  ... ve %d tane daha" % (len(benzersiz) - 25))
        hata = 1
    else:
        soyle()
        soyle("TAMAM - C() ile cevrilen her metin sozlukte var.")

    if html_denetle(anahtar_duz):
        hata = 1
    return hata


if __name__ == "__main__":
    sys.exit(main())
