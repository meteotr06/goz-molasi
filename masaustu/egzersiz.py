# -*- coding: utf-8 -*-
"""
EGZERSİZ — Mola sırasında ekranda yapılan rehberli göz hareketleri.

NEDEN?
------
Rakip uygulamaların hepsinde mola ekranı "ölü zaman": bir geri sayım
sayısına bakıp beklersin. Oysa o 20 saniye asıl işin yapıldığı yer.
Burada her mola, gözün ne yapması gerektiğini ADIM ADIM gösteren
bir animasyona dönüşüyor.

Egzersizlerin dayanağı:
  • Uzağa bakmak  — 6 m "optik sonsuzluk"; odak kası tamamen gevşer.
  • Göz kırpmak   — ekranda kırpma dakikada 15'ten 5-7'ye düşüyor
                    (AAO 2024); bilinçli kırpma gözyaşı tabakasını yeniler.
  • Yakın-uzak    — odak kasını çalıştırıp "yakın işe bağlı geçici
                    miyopi"nin çözülmesine yardım eder.
  • Göz kapatmak  — kapalı göz de dinlenmedir, kuruluğu azaltır.
  • Boyun/omuz    — molaların bel/boyun ağrısını azalttığına dair
                    (düşük düzeyde) kanıt var; Cochrane 2025.

TASARIM KURALI
--------------
Hiçbir animasyon saniyede 3 kereden hızlı yanıp sönmez (WCAG 2.3.1,
epilepsi riski). Hareketler yavaş ve yumuşak — tam ekran hızlı hareket
denge bozukluğu olan kişilerde rahatsızlık yapar.
"""

import math

import gorunum as gor


class Egzersiz:
    """Ortak iskelet. Her egzersiz kendi çizimini yapar."""

    ad = ""
    yonerge = ""
    etiket = "egzersiz"

    def __init__(self, tuval, mx, my, yaricap, vurgu, ikincil, zemin):
        self.t = tuval
        self.mx, self.my = mx, my
        self.r = yaricap
        self.vurgu = vurgu
        self.ikincil = ikincil
        self.zemin = zemin
        self.hazirla()

    def hazirla(self):
        pass

    def guncelle(self, gecen, toplam):
        pass

    def anlik_yonerge(self, gecen, toplam):
        return self.yonerge

    def temizle(self):
        self.t.delete(self.etiket)


class UzagaBak(Egzersiz):
    """Merkezdeki nokta küçülür, halkalar dışarı doğru açılır —
    sonra HEPSİ SÖNER.

    TASARIM KARARI: önceki hâli çelişkiliydi. Yönerge "pencereden
    dışarı bak" diyor ama ekranda 20 saniye boyunca izlenecek bir
    animasyon oynuyordu. Bakma dediğin kişiye bakacak bir şey vermek
    uygulamanın bütün amacını çürütüyor.

    Yeni davranış: ilk 3 saniyede halkalar gözü merkezden dışarı
    yönlendiriyor, sonra animasyon sönüyor. Geriye bakılacak bir şey
    kalmıyor — mola ekranı bilerek sıkıcılaşıyor.

    Göz kırpma ve yakın-uzak egzersizleri izlenmeyi GEREKTİRDİĞİ için
    onlar sönmüyor.
    """

    ad = "Uzağa bak"
    yonerge = "Pencereden dışarı ya da odanın en uzak köşesine bak"

    def hazirla(self):
        self.halkalar = []
        for i in range(3):
            self.halkalar.append(self.t.create_oval(
                0, 0, 0, 0, outline=self.vurgu, width=2, tags=self.etiket))
        self.nokta = self.t.create_oval(0, 0, 0, 0, fill=self.vurgu,
                                        outline="", tags=self.etiket)

    def guncelle(self, gecen, toplam):
        # 3. saniyeden sonra sön, 4,5.'de tamamen kaybol
        sonme = 1.0 - min(1.0, max(0.0, (gecen - 3.0) / 1.5))
        if sonme <= 0.01:
            for h in self.halkalar:
                self.t.itemconfigure(h, outline=self.zemin)
            self.t.itemconfigure(self.nokta, fill=self.zemin)
            return

        # Nokta küçülür: "uzaklaşıyor". Aralık genişletildi
        # (0.22-0.14 çok silikti), geri çekilme artık okunuyor.
        oran = min(1.0, gecen / max(0.001, toplam))
        p = max(1.0, self.r * (0.20 - 0.17 * min(1.0, oran * 3)))
        self.t.coords(self.nokta, self.mx - p, self.my - p, self.mx + p, self.my + p)
        self.t.itemconfigure(self.nokta, fill=gor.karistir(
            self.zemin, self.vurgu, sonme))

        # Halkalar 3 saniyelik döngüyle dışarı açılır
        for i, h in enumerate(self.halkalar):
            evre = ((gecen / 3.0) + i / 3.0) % 1.0
            r = self.r * (0.18 + 0.78 * evre)
            self.t.coords(h, self.mx - r, self.my - r, self.mx + r, self.my + r)
            # Dışa gittikçe soluklaşsın; sönme çarpanıyla birlikte
            self.t.itemconfigure(h, outline=gor.karistir(
                self.zemin, self.vurgu,
                max(0.04, (1.0 - evre) ** 1.6) * 0.8 * sonme))


class GozKirp(Egzersiz):
    """Ritmik göz kırpma rehberi.

    Ekranda kırpma sayısı dakikada 15'ten 5-7'ye düşüyor. Burada
    2 saniyede bir kapanan bir göz kapağı gösteriliyor; kullanıcı
    onunla birlikte TAM kırpıyor (kapağın yüzeyi tamamen örtmesi şart).
    """

    ad = "Göz kırp"
    yonerge = "Kapak kapandığında sen de tam kırp — gözünü sıkıca kapat"
    DONGU = 2.0

    KANAT = 7          # diyafram kanadı sayısı

    # TASARIM KARARI — bu egzersiz bir DİYAFRAM.
    #
    # Önceki hâli iki yarım daireden yapılmış yassı bir badem ve içinde
    # düz bir daireydi. Ekranda çizgi film gibi duruyordu; uygulamanın
    # geri kalanı ise yumuşak halkalardan oluşuyor.
    #
    # Diyafram üç işi birden yapıyor:
    #   • Kapanıp açılması "göz kırp"ı anlatıyor, yazıya gerek bırakmıyor.
    #   • Dairesel — sayaç halkasıyla, nefes halkalarıyla aynı dilde.
    #   • Soyut. Çizilmiş bir göze bakmak tuhaf; ışığı kesilen bir
    #     açıklığa bakmak değil.
    #
    # WEB SÜRÜMÜYLE AYNI: egzersiz.js içindeki GozKirp ile aynı geometri
    # ve aynı zamanlama. Birini değiştirirsen diğerini de değiştir.
    #
    # WCAG 2.3.1: döngü 2 saniye = saniyede 0,5 kapanış. Sınır 3.

    def hazirla(self):
        self.kanatlar = []
        for _ in range(self.KANAT):
            self.kanatlar.append(self.t.create_polygon(
                0, 0, 0, 0, 0, 0, fill=self.vurgu, outline=self.vurgu,
                width=1.4, tags=self.etiket))
        self.cerceve = self.t.create_oval(
            self.mx - self.r * 0.80, self.my - self.r * 0.80,
            self.mx + self.r * 0.80, self.my + self.r * 0.80,
            outline=self.vurgu, width=2.4, tags=self.etiket)
        self.sayi = self.t.create_text(self.mx, self.my + self.r * 0.99, text="",
                                       fill=self.ikincil, tags=self.etiket)

    def guncelle(self, gecen, toplam):
        R = self.r * 0.80
        evre = (gecen % self.DONGU) / self.DONGU
        if evre < 0.12:
            aciklik = 1.0 - (evre / 0.12)
        elif evre < 0.26:
            aciklik = (evre - 0.12) / 0.14
        else:
            aciklik = 1.0
        # Yumuşat: doğrusal açıklık mekanik duruyordu
        a = aciklik * aciklik * (3 - 2 * aciklik)

        delik = R * (0.06 + 0.62 * a)
        buk = (1 - a) * 0.55
        n = self.KANAT
        dilim = 2 * math.pi / n

        koseler = []
        for i in range(n):
            t = i * dilim + buk
            koseler.append((self.mx + delik * math.cos(t),
                            self.my + delik * math.sin(t)))

        # Kanat rengi: kapandıkça koyulaşıyor (tkinter'da globalAlpha yok,
        # o yüzden saydamlık yerine RENK KARIŞTIRIYORUZ). Web'deki
        # alpha 0.14-0.53 aralığının karşılığı.
        for i in range(n):
            t0 = i * dilim
            t1 = t0 + dilim
            k0 = koseler[i]
            k1 = koseler[(i + 1) % n]
            # Dış yay: düz kenar yerine birkaç ara nokta — yuvarlak dursun
            noktalar = []
            adim = 5
            for j in range(adim + 1):
                t = t0 + (t1 - t0) * j / adim
                noktalar.extend([self.mx + R * math.cos(t),
                                 self.my + R * math.sin(t)])
            noktalar.extend([k1[0], k1[1], k0[0], k0[1]])
            oran = 0.14 + 0.09 * (i % 2) + 0.30 * (1 - a)
            self.t.coords(self.kanatlar[i], *noktalar)
            self.t.itemconfigure(
                self.kanatlar[i],
                fill=gor.karistir(self.zemin, self.vurgu, oran),
                outline=gor.karistir(self.zemin, self.vurgu, 0.14 + 0.42 * a))

        kirpma = int(gecen / self.DONGU) + 1
        toplam_kirpma = max(1, int(toplam / self.DONGU))
        self.t.itemconfigure(self.sayi,
                             text="%d / %d" % (min(kirpma, toplam_kirpma), toplam_kirpma))


class YakinUzak(Egzersiz):
    """Odak kasını çalıştırma: sırayla yakına ve uzağa bak.

    Nokta büyüyünce 'yakın' (parmağına bak), küçülünce 'uzak'.
    Yakın işten sonra odak kası kasılı kalır; bu geçiş onu çözer.
    """

    ad = "Yakın — uzak"
    yonerge = "Nokta büyüyünce parmağına, küçülünce uzağa bak"
    DONGU = 5.0

    def hazirla(self):
        self.hale = self.t.create_oval(0, 0, 0, 0, fill="", outline=self.ikincil,
                                       width=2, tags=self.etiket)
        self.nokta = self.t.create_oval(0, 0, 0, 0, fill=self.vurgu, outline="",
                                        tags=self.etiket)

    def _evre(self, gecen):
        return (gecen % self.DONGU) / self.DONGU

    def guncelle(self, gecen, toplam):
        e = self._evre(gecen)
        # Yumuşak gidiş-geliş (kosinüs), ani sıçrama yok
        yakinlik = (1 - math.cos(2 * math.pi * e)) / 2
        p = self.r * (0.10 + 0.52 * yakinlik)
        self.t.coords(self.nokta, self.mx - p, self.my - p, self.mx + p, self.my + p)
        h = self.r * 0.78
        self.t.coords(self.hale, self.mx - h, self.my - h, self.mx + h, self.my + h)
        self.t.itemconfigure(self.hale, outline=gor.karistir(
            self.zemin, self.ikincil, 0.30 + 0.45 * (1 - yakinlik)))

    def anlik_yonerge(self, gecen, toplam):
        e = self._evre(gecen)
        return "Şimdi YAKINA bak — parmağına" if e < 0.5 else "Şimdi UZAĞA bak"


class GozKapat(Egzersiz):
    """Gözü tamamen kapatma. Ekranda gösterilecek bir şey yok;
    sadece yumuşak bir nefes ritmi ve 'ses gelince aç' güveni."""

    ad = "Gözünü kapat"
    yonerge = "Gözlerini kapat, yavaşça nefes al — bitince ses gelecek"

    def hazirla(self):
        self.katmanlar = []
        for i in range(5):
            self.katmanlar.append(self.t.create_oval(
                0, 0, 0, 0, fill="", outline="", tags=self.etiket))

    def guncelle(self, gecen, toplam):
        # 10 saniyelik nefes: 4 sn içeri, 6 sn dışarı.
        # Nefesin nerede olduğunu gözü kapalıyken de "hissettirmek" için
        # halkalar belirgin; ama hareket yavaş, göz kamaştırmıyor.
        e = (gecen % 10.0) / 10.0
        nefes = (1 - math.cos(2 * math.pi * e)) / 2
        olcek = 0.70 + 0.30 * nefes
        for i, k in enumerate(self.katmanlar):
            r = self.r * olcek * (0.32 + 0.17 * i)
            self.t.coords(k, self.mx - r, self.my - r, self.mx + r, self.my + r)
            # Nefes alırken parlar, verirken söner
            guc = (0.75 - 0.11 * i) * (0.45 + 0.55 * nefes)
            self.t.itemconfigure(k, outline=gor.karistir(self.zemin, self.vurgu, guc),
                                 width=3 if i < 2 else 2)

    def anlik_yonerge(self, gecen, toplam):
        e = (gecen % 10.0) / 10.0
        return ("Nefes al…" if e < 0.4 else "Yavaşça ver…") + \
               "   gözlerin kapalı kalsın"


class Boyun(Egzersiz):
    """Boyun ve omuz gevşetme. Göz molası aynı zamanda duruş molası."""

    ad = "Boynunu gevşet"
    yonerge = "Başını yavaşça çevir — omuzlarını geriye at"
    DONGU = 6.0

    def hazirla(self):
        self.yol = self.t.create_line(0, 0, 0, 0, fill=self.ikincil,
                                      width=2, tags=self.etiket)
        self.top = self.t.create_oval(0, 0, 0, 0, fill=self.vurgu, outline="",
                                      tags=self.etiket)

    def _evre(self, gecen):
        return (gecen % self.DONGU) / self.DONGU

    def guncelle(self, gecen, toplam):
        gen = self.r * 0.85
        self.t.coords(self.yol, self.mx - gen, self.my, self.mx + gen, self.my)
        e = self._evre(gecen)
        x = self.mx + gen * math.sin(2 * math.pi * e)
        p = self.r * 0.16
        self.t.coords(self.top, x - p, self.my - p, x + p, self.my + p)

    def anlik_yonerge(self, gecen, toplam):
        e = self._evre(gecen)
        return "Yavaşça SAĞA çevir" if e < 0.5 else "Yavaşça SOLA çevir"


# ----------------------------------------------------------------------
# Seçim
# ----------------------------------------------------------------------
# Sıra kasıtlı: "uzağa bak" asıl egzersiz, üçte ikisini o kaplıyor.
# Diğerleri araya girip ekranın ezber olup görünmez hale gelmesini önlüyor.
KISA_SIRA = [UzagaBak, GozKirp, UzagaBak, YakinUzak, UzagaBak, Boyun]
UZUN_SIRA = [GozKapat, UzagaBak, YakinUzak, GozKapat, Boyun, UzagaBak]


def sec(sayac, uzun_mu=False):
    """Kaçıncı mola olduğuna göre egzersiz seç."""
    sira = UZUN_SIRA if uzun_mu else KISA_SIRA
    return sira[sayac % len(sira)]


def tumu():
    return [UzagaBak, GozKirp, YakinUzak, GozKapat, Boyun]
