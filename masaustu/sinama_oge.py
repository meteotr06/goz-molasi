# -*- coding: utf-8 -*-
"""SOZ VERILMIS AMA KONMAMIS OGE — SINAMA-LISTESI 413.

Bu sinif 04.09.2026'da uc kusur cikardi. En belirgini: `stil.css`
`.saatlik-eksen`i tanimliyordu, ustundeki aciklama niyeti de
soyluyordu ("telefonda 24 etiket sigmaz, yalniz 0/6/12/18 yazilir"),
ama `index.html` icinde oyle bir oge YOKTU. Kullanici 24 isimsiz
cubuga bakiyordu ve "hatalar var" dedi.

NEDEN GOZDEN KACIYOR: stil dosyasi KENDI ICINDE tutarli gorunuyor.
Kimse "peki bu sinifi kim kullaniyor?" diye sormuyor. Sinama takimi da
goremiyor - eksik oge hata vermez, yalnizca GORUNMEZ.

UC YON DENETLENIYOR
  A. stil.css'te tanimli, hicbir html/js dosyasinda gecmeyen sinif
  B. arayuz.js'te $('id') ile aranan, hicbir yerde uretilmeyen id
  C. cekirdek'in _duyur ettigi, kimsenin dinlemedigi olay

ARACIN KENDISI DE SINANIYOR (`--kendini-sina`): sahte bir sinif
eklenince BULMALI. Bulmayan bir denetci, "temiz" demekle "bakamadim"
demeyi ayirt edemez - bu depoda yasanmis bir hata.
"""
import io
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def oku(ad):
    with io.open(os.path.join(KOK, ad), encoding="utf-8") as f:
        return f.read()


def dosyalar(uzanti):
    return sorted(a for a in os.listdir(KOK) if a.endswith(uzanti))


# Dinlenmeyen olaylar burada GEREKCESIYLE duruyor. Listeye eklemek
# serbest degil: her satir "neden dinlenmiyor" sorusunu yanitlamali.
# Amac sessizligi YASAKLAMAK degil, KARARI YAZIYA DOKMEK.
OLAY_ISTISNA = {
    'basladi': "Ekran zaten `degisti` ve `tik` olaylariyla ciziliyor; "
               "`basladi` disariya acilan bir kanca olarak duruyor.",
}


def sinif_denetle():
    """A. stil.css'te tanimli ama hicbir yerde kullanilmayan sinif."""
    stil = oku("stil.css")
    metin = "\n".join(oku(a) for a in dosyalar(".html") + dosyalar(".js"))
    # Yalniz satir basindaki secicileri aliyoruz; ic ice yazilmis
    # kurallar ve bilesik seciciler zaten bu kumede geciyor.
    sinif = sorted(set(re.findall(r"(?m)^\.([A-Za-z][\w-]*)", stil)))
    return [s for s in sinif if s not in metin], len(sinif)


def id_denetle():
    """B. $('id') aranan ama hicbir yerde uretilmeyen id.

    DIKKAT: bazi ogeleri JS'in kendisi uretiyor (rehber penceresi
    `id="rehberGovde"` diye bir govde kuruyor ve sonra ariyor). Yalniz
    HTML'e bakan bir denetci onu KUSUR sanardi - araci yayina almadan
    once bu yanilgiya dustu. O yuzden JS icindeki id= metinleri de
    sayiliyor.
    """
    ay = oku("arayuz.js")
    html = "\n".join(oku(a) for a in dosyalar(".html"))
    js = "\n".join(oku(a) for a in dosyalar(".js"))
    istenen = set(re.findall(r"\$\(\s*'([A-Za-z][\w-]*)'\s*\)", ay))
    varolan = set(re.findall(r'\bid\s*=\s*"([^"]+)"', html))
    # ESITTIRIN ETRAFINDA BOSLUK OLABILIR.
    # Eski desen yalniz `id="x"` (HTML bicimi) goruyordu; JS'te oge
    # `d.id = 'x'` diye kurulur ve arac bunu GORMUYORDU -- saglam bir
    # dugmeyi "konmamis oge" diye kirmiziya dusurdu (06.09.2026).
    # Yanlis alarm veren nobetci, bir sure sonra umursanmayan nobetci.
    varolan |= set(re.findall(r"""id\s*=\s*[\\'"]+([A-Za-z][\w-]*)""", js))
    return sorted(istenen - varolan), len(istenen)


def kullanilan_sinif_denetle():
    """D. HTML/JS'te KULLANILAN ama stil.css'te TANIMLI OLMAYAN sinif.

    A denetimi ters yonu goruyordu (tanimli ama kullanilmayan). Bu yon
    daha zararli: sinif yaziliyor, gorunum HIC uygulanmiyor ve kimse
    hata gormuyor.

    OLCULDU (06.09.2026): `.kutu` ve `.kutu-baslik` -- "Neler degisti"
    bolumu, ustundeki butun bilgi kartlarinin aksine cercevesiz,
    zeminsiz duruyordu. `.saat-ikili` -- hafta sonu saat cifti
    bosluksuz ve ayiracsizdi, ayni isi yapan oteki iki cift duzgundu.
    Ucu de sessizdi.

    ISTISNA: durum siniflari (`acik`, `gizli`, `secili` gibi) ve
    tarayicinin kendi siniflari degil, YALNIZ bizim yazdigimiz
    ad-benzeri siniflar araniyor; kisa ve genel adlar gurultu uretir.
    """
    html = "\n".join(oku(a) for a in dosyalar(".html"))
    js = "\n".join(oku(a) for a in dosyalar(".js"))
    # SAYFA ICI `<style>` BLOKLARI DA SAYILIYOR. Ilk surumde yalniz
    # `stil.css`e bakiyordum ve `rehber.html` / `guide.html` kendi
    # stillerini icerde tasidigi icin `.ust-bilgi` ve `.uygulama-kutu`
    # SAHTE BULGU olarak cikti. Bagiran nobetci, susan nobetciden
    # kotudur: iki sahte bulgu, ucuncu GERCEK bulguyu gurultuye
    # cevirirdi.
    stil = oku("stil.css") + "\n" + "\n".join(
        re.findall(r"(?is)<style[^>]*>(.*?)</style>", html))
    tanimli = set(re.findall(r"\.([A-Za-z][\w-]*)", stil))
    kullanilan = set()
    for m in re.findall(r'class\s*=\s*"([^"]+)"', html):
        kullanilan.update(m.split())
    for m in re.findall(r"""className\s*=\s*['"]([^'"]+)['"]""", js):
        kullanilan.update(m.split())
    # Tireli adlar bizim yazdiklarimiz; tek kelimelik kisa adlar
    # cogunlukla durum sinifi (`acik`, `gizli`) ve CSS'te baska bir
    # secicinin parcasi olarak gecebiliyor.
    aday = sorted(s for s in kullanilan if "-" in s and s not in tanimli)
    return aday, len(kullanilan)


def degisken_denetle():
    """F. `var(--x)` ile ISTENEN ama HICBIR YERDE tanimlanmayan degisken.

    Tanimsiz bir degiskene basvuran bildirim GECERSIZ sayilir ve yedek
    deger (varsa) uygulanir; yedek yoksa oge devraldigi rengi alir.
    Ikisi de SESSIZ: ekranda hata yok, yalnizca yanlis renk.

    BU DENETIM BIR OLCUMDEN DOGDU (07.09.2026): `.sekme.secili`
    `var(--ana-yazi, #0d2b28)` yaziyordu ve `--ana-yazi` butun depoda
    baska hicbir yerde YOKTU. Her tema sessizce yedege dusuyor,
    karsitlik 2,41:1'e kadar iniyordu -- ve kontrast sinamasi bunu
    goremiyordu cunku o, ekranda olmayan baska bir cifti olcuyordu.
    Ayni sinif daha once `--soluk` icin de yasandi.

    JS'in KURDUGU degiskenler de tanim sayilir (`setProperty('--x')`).
    """
    # YORUMLAR SAYILMAZ. Ilk kosusta bu denetim kendi ACIKLAMAMI
    # kusur diye bildirdi: duzeltilen degiskenin adi yorumda geciyordu.
    # Kendi belgesini kusur sanan bir nobetci, guveni once kendi
    # yikar -- bagiran nobetci, susan nobetciden kotudur.
    css = re.sub(r"/\*.*?\*/", "", oku("stil.css"), flags=re.S)
    js = "\n".join(oku(a) for a in dosyalar(".js"))
    html = "\n".join(oku(a) for a in dosyalar(".html"))
    istenen = set(re.findall(r"var\(\s*(--[\w-]+)", css))
    # Tanim: `--x:` bir kural icinde, ya da JS'ten setProperty ile.
    varolan = set(re.findall(r"(--[\w-]+)\s*:", css))
    varolan |= set(re.findall(r"""setProperty\(\s*['"](--[\w-]+)""", js))
    varolan |= set(re.findall(r"""setProperty\(\s*['"](--[\w-]+)""", html))
    return sorted(istenen - varolan), len(istenen)


def etiket_denetle():
    """E. `<label for="X">` var ama X diye bir oge YOK.

    OLCULDU: "Cihaz etkinligini izle" etiketi `for="ayEtkinlik"`
    diyordu, oyle bir id hicbir yerde yoktu. Penceredeki oteki butun
    satirlarda etiket yazisina dokunmak denetimi degistiriyor, o
    satirda hicbir sey olmuyordu -- sessiz ve gozle gorulmez.
    """
    html = "\n".join(oku(a) for a in dosyalar(".html"))
    js = "\n".join(oku(a) for a in dosyalar(".js"))
    hedef = set(re.findall(r'<label[^>]*\sfor\s*=\s*"([^"]+)"', html))
    varolan = set(re.findall(r'\bid\s*=\s*"([^"]+)"', html))
    varolan |= set(re.findall(r"""id=[\'"]+([A-Za-z][\w-]*)""", js))
    return sorted(hedef - varolan), len(hedef)


def olay_denetle():
    """C. Cekirdegin yaydigi ama kimsenin dinlemedigi olay."""
    ce = oku("cekirdek.js")
    js = "\n".join(oku(a) for a in dosyalar(".js"))
    yayin = set(re.findall(r"_duyur\(\s*'(\w+)'", ce))
    dinle = set(re.findall(r"\.uzerine\(\s*'(\w+)'", js))
    sahipsiz = sorted(y for y in (yayin - dinle) if y not in OLAY_ISTISNA)
    # Ters yon de kusur: olmayan bir olayi dinlemek sessizce hicbir sey
    # yapmaz - "duzenek kurulmus, baglanmamis"in obur yuzu.
    bos_dinleyici = sorted(dinle - yayin)
    return sahipsiz, bos_dinleyici, len(yayin)


def kendini_sina():
    """Arac sahte bir sinifi BULUYOR mu? Bulmuyorsa 'temiz' demesi
    hicbir sey ifade etmez."""
    stilYol = os.path.join(KOK, "stil.css")
    htmlYol = os.path.join(KOK, "index.html")
    stilAsil = io.open(stilYol, encoding="utf-8").read()
    htmlAsil = io.open(htmlYol, encoding="utf-8").read()
    try:
        # A: tanimli ama kullanilmayan sinif
        io.open(stilYol, "w", encoding="utf-8", newline="\n").write(
            stilAsil + "\n.sahte-sinama-sinifi { color: red; }\n")
        a = "sahte-sinama-sinifi" in sinif_denetle()[0]

        # D ve E: HER DENETIM AYRI AYRI SINANIR.
        #
        # "Sifir bulundu" sonucu, ancak o denetimin BOZUK bir girdide
        # kusuru BULDUGU gosterildiginde bir sey ifade eder. Bu dosyada
        # bugun tam bunu yasadim: `\b` kacisi bozulmus bir desen yuzunden
        # E denetimi otuz uc etiketin OTUZ UCUNU birden "karsiliksiz"
        # gosterdi. Ters yonu -- hicbir seyi bulamayan bir denetim --
        # ayni kolaylikla olabilirdi ve "TAMAM" yazardi.
        io.open(htmlYol, "w", encoding="utf-8", newline="\n").write(
            htmlAsil.replace(
                "</body>",
                '<p class="sahte-tanimsiz-sinif">x</p>'
                '<label for="sahteOlmayanId">x</label></body>', 1))
        d = "sahte-tanimsiz-sinif" in kullanilan_sinif_denetle()[0]
        e = "sahteOlmayanId" in etiket_denetle()[0]

        # B: TERS YON — SAGLAM OLANI KUSUR SANMASIN.
        #
        # Ustteki uc denetim "kusuru buluyor mu" diye soruyor. Bu
        # dorduncusu tam tersini soruyor: JS'in KENDI urettigi bir
        # ogeyi "konmamis" saniyor mu? 06.09.2026'da tam bu oldu --
        # desen esittirin etrafindaki boslugu gormedigi icin
        # `d.id = 'durumNotuCikis'` satiri yok sayildi ve saglam bir
        # dugme kirmiziya dustu. Iki yanilgi ayri seydir ve ikisi de
        # yasandi; ikisi de sinaniyor.
        ayYol = os.path.join(KOK, "arayuz.js")
        ayAsil = io.open(ayYol, encoding="utf-8").read()
        try:
            io.open(ayYol, "w", encoding="utf-8", newline="\n").write(
                ayAsil + "\n/* kendini sinama */\n"
                "const _sn = document.createElement('b');\n"
                "_sn.id = 'sahteUretilenOge';\n"
                "$('sahteUretilenOge');\n")
            b = "sahteUretilenOge" not in id_denetle()[0]
        finally:
            io.open(ayYol, "w", encoding="utf-8", newline="\n").write(ayAsil)

        # F: tanimsiz degiskeni buluyor mu?
        io.open(stilYol, "w", encoding="utf-8", newline="\n").write(
            stilAsil + "\n.sahte-f { color: var(--sahte-tanimsiz-degisken); }\n")
        f = "--sahte-tanimsiz-degisken" in degisken_denetle()[0]

        return a and b and d and e and f
    finally:
        io.open(stilYol, "w", encoding="utf-8", newline="\n").write(stilAsil)
        io.open(htmlYol, "w", encoding="utf-8", newline="\n").write(htmlAsil)


def calistir():
    hata = []

    if not kendini_sina():
        print("  KENDINI SINAMA BASARISIZ: arac sahte sinifi bulamadi.")
        print("  Bu durumda 'temiz' sonucu HICBIR SEY ifade etmez.")
        return 1
    print("  kendini sinama: sahte sinif bulundu, arac gorebiliyor")

    kullanilmayan, toplam_sinif = sinif_denetle()
    print("  A. stil.css sinifi: %d tanimli, %d kullanilmayan"
          % (toplam_sinif, len(kullanilmayan)))
    for s in kullanilmayan:
        hata.append("stil.css '.%s' tanimli ama hicbir html/js "
                    "dosyasinda gecmiyor" % s)

    eksik_id, toplam_id = id_denetle()
    print("  B. $('id') aramasi: %d tane, %d karsiliksiz"
          % (toplam_id, len(eksik_id)))
    for i in eksik_id:
        hata.append("arayuz.js $('%s') ariyor ama boyle bir oge "
                    "hicbir yerde uretilmiyor" % i)

    sahipsiz, bos, toplam_olay = olay_denetle()
    print("  C. cekirdek olayi: %d yayin, %d sahipsiz, %d bos dinleyici"
          % (toplam_olay, len(sahipsiz), len(bos)))
    for o in sahipsiz:
        hata.append("cekirdek '%s' olayini yayiyor ama kimse dinlemiyor "
                    "(bilerekse OLAY_ISTISNA'ya gerekcesiyle yaz)" % o)
    for o in bos:
        hata.append("'%s' olayi dinleniyor ama cekirdek onu hic yaymiyor"
                    % o)

    kullanilmayanSinif, toplamKullanilan = kullanilan_sinif_denetle()
    print("  D. HTML/JS sinifi: %d kullanilan, %d tanimsiz"
          % (toplamKullanilan, len(kullanilmayanSinif)))
    for s in kullanilmayanSinif:
        hata.append("'.%s' HTML/JS'te kullaniliyor ama stil.css'te "
                    "TANIMLI DEGIL - gorunum hic uygulanmiyor" % s)

    oluEtiket, toplamEtiket = etiket_denetle()
    tanimsiz, degSayisi = degisken_denetle()
    for d in tanimsiz:
        hata.append("stil.css `%s` degiskenini kullaniyor ama onu "
                    "hicbir yer TANIMLAMIYOR — kural sessizce gecersiz "
                    "olur, oge devraldigi rengi alir" % d)
    print("  F. CSS degiskeni: %d kullanilan, %d tanimsiz"
          % (degSayisi, len(tanimsiz)))
    print("  E. <label for>: %d tane, %d karsiliksiz"
          % (toplamEtiket, len(oluEtiket)))
    for e_ in oluEtiket:
        hata.append("<label for=\"%s\"> boyle bir oge YOK - etikete "
                    "dokunmak hicbir sey yapmiyor" % e_)

    if hata:
        print("  BASARISIZ - %d konmamis/baglanmamis oge:" % len(hata))
        for h in hata:
            print("    -", h)
        return 1
    print("  TAMAM - soz verilen her oge yerinde")
    return 0


if __name__ == "__main__":
    if "--kendini-sina" in sys.argv:
        print("kendini sinama:", "GECTI" if kendini_sina() else "KALDI")
        sys.exit(0)
    sys.exit(calistir())
