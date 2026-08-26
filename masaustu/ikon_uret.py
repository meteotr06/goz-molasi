# -*- coding: utf-8 -*-
"""Göz Molası simgelerini üretir.

Neden betikle? Simgeler dört ayrı yerde, beş ayrı ölçüde lazım
(web manifesti, maskelenebilir Android simgesi, Windows .ico,
tarayıcı sekmesi). Elle çizilince biri güncellenip diğeri unutuluyor.

TASARIM
  Zemin   : uygulamanın gece moru gradyanı (#141130 -> #2c2659)
  Yay     : nane yeşili, saat 12'den saat yönünde — "kalan süre"
  Göz     : badem biçimi, nane konturlu
  Bebek   : kehribar, hafif sağa kaçık — "uzağa bak"

Eski simgenin ölçülen kusurları:
  • Halka sağa/aşağı kaymıştı, göz soldaydı — kompozisyon dengesiz.
  • Yayın boşluğu saat 8 civarındaydı; ilerleme yayı değil kırık
    daire gibi duruyordu.
  • Kenar payı yoktu; maskelenen platformlarda yay kırpılıyordu.

Çalıştır:  python ikon_uret.py
"""

import math
import os

from PIL import Image, ImageDraw

# Her şeyi 4 katında çizip küçültüyoruz — PIL'in kenar yumuşatması yok,
# küçültme sırasında Lanczos bunu bizim yerimize yapıyor.
KAT = 4

# PALET — dinlendirici olması esas.
# Önceki palet (gece moru zemin + kehribar iris) uyarıcı duruyordu;
# turuncu dikkat çeken bir renk, oysa bu uygulama gözü dinlendirmek
# için var. Yeni palet alacakaranlıkta su rengi: derin çamurcun zemin,
# deniz yeşili iris. Doygunluk bilerek düşük tutuldu.
ZEMIN_UST = (18, 45, 54)        # #122d36 — derin çamurcun
ZEMIN_ALT = (33, 80, 88)        # #215058
YAY = (143, 216, 200)           # #8fd8c8 — yumuşak nane

AK = (206, 219, 216)            # #cedbd8 — göz akı; kar beyazı değil,
                                # zemine göre fazla parlamasın
IRIS_LIMBAL = (38, 82, 80)      # #265250 — irisin dış halkası
IRIS_GOVDE = (78, 155, 143)     # #4e9b8f — iris gövdesi
IRIS_LIF_ACIK = (140, 205, 188) # #8ccdbc — radyal lifler, açık
IRIS_LIF_KOYU = (52, 112, 106)  # #34706a — radyal lifler, koyu
KOLLARET = (108, 183, 168)      # #6cb7a8 — bebeğin çevresindeki halka
BEBEK = (14, 30, 33)            # #0e1e21 — göz bebeği
GOZ_ICI = (18, 45, 54)          # badem içi (ak çizilmeyen küçük boyda)

# Eski adlar bazı yerlerde geçiyor olabilir
NANE = YAY
KEHRIBAR = IRIS_GOVDE
IRIS_DIS = IRIS_LIMBAL


def _gradyan(boy):
    """Köşegen gece moru gradyanı."""
    g = Image.new("RGB", (boy, boy))
    p = g.load()
    for y in range(boy):
        for x in range(boy):
            # 155 derecelik köşegen: sol üst açık değil, sağ alt açık
            t = (x * 0.35 + y * 0.65) / boy
            t = max(0.0, min(1.0, t))
            p[x, y] = tuple(
                round(ZEMIN_UST[k] + (ZEMIN_ALT[k] - ZEMIN_UST[k]) * t)
                for k in range(3)
            )
    return g


def _badem(cx, cy, yari_g, yari_y, adim=180):
    """Badem (göz) biçimini nokta listesi olarak üret.

    Badem = üstte ve altta birer daire yayının birleşimi. Üç noktadan
    (-a,0), (0,b), (a,0) geçen dairenin merkezi y ekseninde:
        k = (b^2 - a^2) / 2b,  R = |b - k|
    """
    a, b = float(yari_g), float(yari_y)
    k = (b * b - a * a) / (2 * b)
    R = abs(b - k)

    aci_bas = math.atan2(0 - k, -a)
    aci_son = math.atan2(0 - k, a)

    ust = []
    for i in range(adim + 1):
        t = aci_bas + (aci_son - aci_bas) * i / adim
        ust.append((cx + R * math.cos(t), cy - (k + R * math.sin(t))))

    alt = [(x, 2 * cy - y) for (x, y) in reversed(ust)]
    return ust + alt


def _parilti(im, cx, cy, r, renk, guc=0.20, katman=26):
    """Yumuşak radyal ışıma. PIL'de radyal gradyan yok; içten dışa
    alfası azalan halkalar üst üste bindirilerek yapılıyor."""
    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ciz = ImageDraw.Draw(kat)
    for i in range(katman, 0, -1):
        t = i / katman
        yr = r * t
        alfa = int(255 * guc * (1 - t) ** 1.6 / katman * 6)
        if alfa <= 0:
            continue
        ciz.ellipse([cx - yr, cy - yr, cx + yr, cy + yr], fill=renk + (alfa,))
    return Image.alpha_composite(im, kat)


def _ust_isik(im, yaricap):
    """Rozetin üst kenarına ince bir ışık şeridi. Simgeye 'yapılmış'
    hissini veren şey bu — düz zemin plastik duruyor."""
    B = im.size[0]
    kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ciz = ImageDraw.Draw(kat)
    kalinlik = max(1, int(B * 0.008))
    ciz.rounded_rectangle([kalinlik, kalinlik, B - 1 - kalinlik, B - 1 - kalinlik],
                          radius=yaricap, outline=(255, 255, 255, 255),
                          width=kalinlik)

    # Işık yukarıdan aşağı sönerek bitmeli. Alt yarıyı düz kesince
    # solda ve sağda gözle görülür bir çizgi kalıyordu — hata gibi
    # duruyordu. Dikey alfa geçişiyle yumuşatıyoruz.
    gecis = Image.new("L", (1, B))
    gp = gecis.load()
    for y in range(B):
        t = y / (B * 0.62)
        gp[0, y] = max(0, int(46 * (1 - t) ** 1.5)) if t < 1 else 0
    maske = gecis.resize((B, B))
    kat.putalpha(Image.composite(maske, Image.new("L", (B, B), 0),
                                 kat.split()[3]))
    return Image.alpha_composite(im, kat)


def simge_ciz(boy, pay_orani=0.10, detay=None):
    """Tek bir simge üret.

    pay_orani: kenarda bırakılan boşluk. Maskelenebilir simgede
    büyütülüyor, çünkü Android kenarlardan %10'a kadar kırpabiliyor.

    detay: büyük boyda ışıma, iris halkası ve üst ışık şeridi eklenir;
    küçük boyda bunlar çamura dönüyor, o yüzden kapanıyor ve göz
    sadeleşiyor. Gerçek simge setleri de boyuta göre ayrı çizim
    kullanıyor — 16 pikselde incelik okunmuyor.
    Verilmezse boya göre kendi karar verir.
    """
    if detay is None:
        detay = boy >= 48
    B = boy * KAT
    im = _gradyan(B).convert("RGBA")
    ciz = ImageDraw.Draw(im)

    orta = B / 2.0
    pay = B * pay_orani
    yay_r = (B - 2 * pay) / 2.0
    yay_kalinlik = max(2, int(B * 0.075))

    # --- Kalan süre yayı: saat 12'den saat yönünde, %72'si dolu ---
    # PIL'de 0 derece saat 3 yönü ve açı saat yönünde artıyor.
    kutu = [orta - yay_r, orta - yay_r, orta + yay_r, orta + yay_r]
    ciz.arc(kutu, start=-90, end=-90 + 360 * 0.72,
            fill=YAY + (255,), width=yay_kalinlik)

    # Yayın iki ucu yuvarlak olsun — PIL arc'ı düz kesiyor.
    # DİKKAT: PIL'de yay kalınlığı sınırlayıcı kutudan İÇERİ doğru
    # büyüyor, yani yayın orta çizgisi yay_r'de değil (yay_r - kalınlık/2)
    # yarıçapında. Başlıkları yay_r'ye koyunca dışarı taşıp çengel gibi
    # görünüyordu.
    orta_r = yay_r - yay_kalinlik / 2.0
    for aci in (-90, -90 + 360 * 0.72):
        r = math.radians(aci)
        ux, uy = orta + orta_r * math.cos(r), orta + orta_r * math.sin(r)
        yr = yay_kalinlik / 2.0
        ciz.ellipse([ux - yr, uy - yr, ux + yr, uy + yr], fill=YAY + (255,))

    # --- GÖZ ---
    goz_g = orta_r * (0.64 if detay else 0.68)
    goz_y = orta_r * (0.38 if detay else 0.42)

    if not detay:
        # Küçük boy: ak, lif, kollaret hepsi çamura dönüyor.
        # Sade badem + tek renk iris.
        kontur = B * 0.042
        ciz.polygon(_badem(orta, orta, goz_g, goz_y), fill=YAY + (255,))
        ciz.polygon(_badem(orta, orta, goz_g - kontur * 1.9, goz_y - kontur),
                    fill=GOZ_ICI + (255,))
        br = goz_y * 0.72
        ciz.ellipse([orta - br, orta - br, orta + br, orta + br],
                    fill=IRIS_GOVDE + (255,))
        pr = br * 0.30
        ciz.ellipse([orta - br * 0.36 - pr, orta - br * 0.38 - pr,
                     orta - br * 0.36 + pr, orta - br * 0.38 + pr],
                    fill=(255, 255, 255, 235))
        return im.resize((boy, boy), Image.LANCZOS)

    # ---- Büyük boy: gerçek bir göz ----
    # Gözün arkasında hafif ışıma; rozet düz zemin olmaktan çıkıyor.
    im = _parilti(im, orta, orta, orta_r * 0.95, YAY, guc=0.13)
    ciz = ImageDraw.Draw(im)

    # 1) Göz akı — badem biçimi. Kar beyazı değil, kırık beyaz.
    ak_nokta = _badem(orta, orta, goz_g, goz_y)
    ciz.polygon(ak_nokta, fill=AK + (255,))

    # 2) İris — göz akının içinde, üstten hafif kesik (üst kapak)
    # 0.96'da iris alttan da kesiliyordu; gerçek gözde alt kenar
    # görünür, yalnızca üst kapak örter.
    iris_r = goz_y * 0.86
    # Bakış YANA çevrik. İki sebep: dosdoğru bakan gerçekçi bir göz
    # simge boyutunda gözetleniyormuş hissi veriyor — oysa uygulamanın
    # işi rahatlatmak. İkincisi zaten uygulamanın söylediği şey bu:
    # "gözünü ekrandan ayır, uzağa bak".
    # 0.30'da iris bademin sağ kenarına dayanıp sıkışıyordu.
    ix, iy = orta + goz_g * 0.17, orta + goz_y * 0.03

    # 2a) Limbal halka (irisin koyu dış kenarı) — gerçek gözde vardır
    ciz.ellipse([ix - iris_r, iy - iris_r, ix + iris_r, iy + iris_r],
                fill=IRIS_LIMBAL + (255,))
    # 2b) Gövde
    gr = iris_r * 0.90
    ciz.ellipse([ix - gr, iy - gr, ix + gr, iy + gr], fill=IRIS_GOVDE + (255,))

    # 2c) Radyal lifler — irisi düz bir daire olmaktan çıkaran şey bu.
    #     Gerçek iriste bebeğinden dışa doğru uzanan kas lifleri var.
    bebek_r = iris_r * 0.40
    lif_kat = Image.new("RGBA", im.size, (0, 0, 0, 0))
    lciz = ImageDraw.Draw(lif_kat)
    # Lifler ince, kısa ve düzensiz olmalı. İlk denemede 96 kalın lif
    # bebekten limbal halkaya kadar uzanıyordu; dişli çark gibi
    # duruyordu. Şimdi 150 ince lif, kollaretten başlayıp irisin
    # dış kenarına VARMADAN bitiyor, boyları ve tonları düzensiz.
    LIF = 150
    for i in range(LIF):
        aci = 2 * math.pi * i / LIF + (((i * 7919) % 31) / 31.0) * 0.02
        bas = 0.34 + 0.10 * ((i * 6607) % 41) / 41.0
        son = 0.66 + 0.22 * ((i * 7919) % 97) / 97.0
        renk = IRIS_LIF_ACIK if ((i * 3) % 5) < 2 else IRIS_LIF_KOYU
        alfa = 55 + int(65 * ((i * 5417) % 53) / 53.0)
        x1 = ix + gr * bas * math.cos(aci)
        y1 = iy + gr * bas * math.sin(aci)
        x2 = ix + gr * son * math.cos(aci)
        y2 = iy + gr * son * math.sin(aci)
        lciz.line([x1, y1, x2, y2], fill=renk + (alfa,),
                  width=max(1, int(B * 0.0035)))
    # Lifler yalnızca irisin içinde görünsün
    iris_maske = Image.new("L", im.size, 0)
    ImageDraw.Draw(iris_maske).ellipse([ix - gr, iy - gr, ix + gr, iy + gr],
                                       fill=255)
    lif_kat.putalpha(Image.composite(lif_kat.split()[3],
                                     Image.new("L", im.size, 0), iris_maske))
    im = Image.alpha_composite(im, lif_kat)
    ciz = ImageDraw.Draw(im)

    # 2d) Kollaret — bebeğin çevresindeki açık halka
    kr = bebek_r * 1.34
    ciz.ellipse([ix - kr, iy - kr, ix + kr, iy + kr],
                outline=KOLLARET + (185,), width=max(1, int(B * 0.013)))

    # 3) Göz bebeği
    ciz.ellipse([ix - bebek_r, iy - bebek_r, ix + bebek_r, iy + bebek_r],
                fill=BEBEK + (255,))

    # 4) Işık yansıması — sol üstte büyük, sağ altta küçük.
    #    Gözü "canlı" yapan tek detay budur.
    # Yansıma bebeğin İÇİNDE kalmalı; kenarına taşınca bebekle
    # birleşip yin-yang gibi bir şekle dönüyordu.
    pr = bebek_r * 0.34
    px, py = ix - bebek_r * 0.34, iy - bebek_r * 0.36
    ciz.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(255, 255, 255, 235))
    kr2 = bebek_r * 0.15
    kx, ky = ix + bebek_r * 0.34, iy + bebek_r * 0.36
    ciz.ellipse([kx - kr2, ky - kr2, kx + kr2, ky + kr2],
                fill=(255, 255, 255, 120))

    # 5) Üst kapak gölgesi — gerçek gözde irisin üstü hep gölgede kalır.
    #    Kaydırılmış bir bademle çizince alt kenarı SERT bir çizgi
    #    bırakıyor, gölge değil gri bant gibi duruyordu. Yukarıdan
    #    aşağı sönen dikey bir geçişle yapılıyor.
    ust = orta - goz_y
    boyu = goz_y * 1.5
    gecis = Image.new("L", (1, B), 0)
    gp = gecis.load()
    for y in range(B):
        t = (y - ust) / boyu
        # 78 -> 96: üst kapak biraz daha inik, bakış "faltaşı gibi
        # açık" değil dingin görünüyor.
        gp[0, y] = 0 if t < 0 or t > 1 else int(96 * (1 - t) ** 1.6)
    golge = Image.new("RGBA", im.size, (4, 26, 32, 255))
    ak_maske = Image.new("L", im.size, 0)
    ImageDraw.Draw(ak_maske).polygon(ak_nokta, fill=255)
    golge.putalpha(Image.composite(gecis.resize((B, B)),
                                   Image.new("L", im.size, 0), ak_maske))
    im = Image.alpha_composite(im, golge)
    ciz = ImageDraw.Draw(im)

    # 6) Kapak çizgisi — bademi zemine oturtan ince kontur
    # Bademin TAMAMI çizilmeli — yalnızca üst yayı çizince alt kenar
    # zemine karışıyor ve göz yarım kalmış gibi duruyordu.
    ciz.line(ak_nokta + [ak_nokta[0]], fill=YAY + (255,),
             width=max(2, int(B * 0.018)), joint="curve")

    im = _ust_isik(im, int(B * 0.22))

    return im.resize((boy, boy), Image.LANCZOS)


def yuvarlat(im, yaricap_orani=0.22):
    """Köşeleri yuvarlat (web manifesti ve .ico için)."""
    boy = im.size[0]
    maske = Image.new("L", (boy * KAT, boy * KAT), 0)
    ImageDraw.Draw(maske).rounded_rectangle(
        [0, 0, boy * KAT - 1, boy * KAT - 1],
        radius=int(boy * KAT * yaricap_orani), fill=255)
    maske = maske.resize((boy, boy), Image.LANCZOS)
    sonuc = im.copy()
    sonuc.putalpha(maske)
    return sonuc


def main():
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Web: köşeleri yuvarlak
    for boy in (192, 512):
        yuvarlat(simge_ciz(boy)).save(os.path.join(kok, "ikon-%d.png" % boy))
        print("ikon-%d.png" % boy)

    # Maskelenebilir: kare kalır, içerik daha küçük — Android kendisi kırpar
    simge_ciz(512, pay_orani=0.22).save(os.path.join(kok, "ikon-maskeli.png"))
    print("ikon-maskeli.png")

    # Windows .ico — küçük boylarda yay inceliyor, payı azaltıyoruz
    boylar = [(16, 0.04), (24, 0.05), (32, 0.06), (48, 0.08),
              (64, 0.09), (128, 0.10), (256, 0.10)]
    kareler = [yuvarlat(simge_ciz(b, p), 0.20) for b, p in boylar]
    kareler[-1].save(os.path.join(kok, "masaustu", "ikon.ico"),
                     format="ICO",
                     sizes=[(b, b) for b, _ in boylar])
    print("masaustu/ikon.ico")


if __name__ == "__main__":
    main()
