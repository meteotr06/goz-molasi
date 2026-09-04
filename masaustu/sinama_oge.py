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
    varolan |= set(re.findall(r"""id=[\\'"]+([A-Za-z][\w-]*)""", js))
    return sorted(istenen - varolan), len(istenen)


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
    yol = os.path.join(KOK, "stil.css")
    asil = io.open(yol, encoding="utf-8").read()
    try:
        io.open(yol, "w", encoding="utf-8", newline="\n").write(
            asil + "\n.sahte-sinama-sinifi { color: red; }\n")
        bulunan, _ = sinif_denetle()
        return "sahte-sinama-sinifi" in bulunan
    finally:
        io.open(yol, "w", encoding="utf-8", newline="\n").write(asil)


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
