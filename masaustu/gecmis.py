# -*- coding: utf-8 -*-
"""
GEÇMİŞ — Gün gün kayıt ve seri (streak) hesabı.

Bugünkü sayaçlar `istatistik.json`'da tutuluyor; gün değişince sıfırlanıyor.
Burada ise her günün özeti kalıcı olarak saklanıyor, böylece "son 7 gün"
grafiği ve "kaç gündür üst üste hedefi tutturdum" sayısı çıkarılabiliyor.

Dosya küçük kalsın diye sadece son 120 gün saklanır.
"""

import json
import os
from datetime import date, timedelta

SAKLANAN_GUN = 120
GUNLUK_HEDEF = 8          # günde bu kadar mola = "hedef tuttu"

GUN_ADLARI = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]

# ---- GÜN KAYDININ ALANLARI: TEK KAYNAK ----
# geçmişteki ad -> (istatistik.json'daki ad, bir günde olabilecek en
# büyük değer)
#
# NİYE TEK SÖZLÜK: yazan (`gunu_isle`) ve okuyan (`gunun_molasi`) taraf
# alan adlarını ayrı ayrı elle yazıyordu. Bu projede aynı hata bir kez
# yaşandı: 29.08.2026'da istatistik süzgeci elle "mola"/"atlanan" diye
# yazılmış alanları süzüyordu, oysa sayaçların adı "tamamlanan"/
# "ertelenen"di — süzgeç ÇALIŞIYOR GÖRÜNÜYORDU. İki taraf aynı sözlükten
# üretilince bu uyuşmazlık bir daha oluşamaz.
# Sınırlar `Uygulama.IST_ALANLARI` ile aynı (mola 1000, saniye 86400);
# goz_molasi buradan içeri aktarılamaz, çünkü gecmis'i O import ediyor.
ALANLAR = {
    "mola":     ("tamamlanan", 1000),
    "uzun":     ("uzun_mola", 1000),
    "ekran_sn": ("ekran_sn", 86400),
}

# Bozuk dosya kenara alındıysa (yol, sebep). `goz_molasi.ayar_uyarisi`
# bunu okuyup ekranda söylüyor. Sessizce düzeltmek bu projede hata
# sayılıyor: kullanıcı 120 günlük geçmişinin neden sıfırlandığını
# EKRANDA görmeli.
son_bozulma = None

# Son `oku` dosyayı AÇAMADI mı? (kilit / izin / disk — içerik bozukluğu
# DEĞİL) Bu durumda `gunu_isle` o turda YAZMAZ: okunamamış bir dosyanın
# üstüne tek günlük veri basmak 120 günü silmek demek.
okunamadi = False


def _yol(klasor):
    return os.path.join(klasor, "gecmis.json")


def sayac_oku(kayit, ad, en_cok):
    """Bir gün kaydındaki sayacı GÜVENLE okur. Okuyamazsa 0.

    NİYE VAR — ölçüldü (29.08.2026): `int(d.get("mola", 0))` korumasızdı
    ve gecmis.json'daki tek bir bozuk değer altı ayrı biçimde çökertiyordu
    (metin -> ValueError, null -> TypeError, gün kaydının kendisi metin/
    liste -> AttributeError, 1e400 -> OverflowError, NaN -> ValueError).
    Çökme `_ciz` içinde oluyordu ve `_tik`'teki `kok.after(250, self._tik)`
    satırı `_ciz`'den SONRA geldiği için döngü YENİDEN KURULMADAN
    kesiliyordu: pencere açık ve normal görünüyor, sayaç KALICI donuyor,
    mola hiç gelmiyor. Ölçüldü: tik 3 kez çağrıldı, çökmeden sonra hiç.

    Sınır dışı değer KIRPILMAZ, SIFIRLANIR: 1000000000 molayı 1000'e
    kırpmak, bozuk veriden üretilmiş ama İNANDIRICI bir sayı üretir
    (aynı kural: `Uygulama.istatistik_suz`).
    """
    if not isinstance(kayit, dict):
        return 0                       # gün kaydının kendisi metin/liste
    d = kayit.get(ad, 0)
    # bool, int'in alt türü: True'nun "1 mola" sayılmasını istemiyoruz.
    if isinstance(d, bool) or not isinstance(d, (int, float)):
        return 0
    # NaN ve ±sonsuz da buradan düşüyor: ikisiyle de karşılaştırma False.
    if not (0 <= d <= en_cok):
        return 0
    return int(d)


def gunun_molasi(kayit):
    """Bir gün kaydındaki toplam mola (kısa + uzun)."""
    return sum(sayac_oku(kayit, ad, ALANLAR[ad][1]) for ad in ("mola", "uzun"))


def istatistigin_molasi(istatistik):
    """Bellekteki bugünkü istatistikten toplam mola.

    Bu yol da korumasızdı: istatistik.json bozulunca `tamamlanan` "uc"
    ya da null olabiliyor ve aynı çökme buradan da geliyordu.
    """
    return sum(sayac_oku(istatistik, ALANLAR[ad][0], ALANLAR[ad][1])
               for ad in ("mola", "uzun"))


def _kenara_al(yol, sebep):
    """Bozuk dosyayı SİLME, `.bozuk` adıyla yanında bırak.

    Ölçüldü (29.08.2026): eski `oku` bozuk dosyada `{}` dönüyordu; hemen
    ardından `gunu_isle` bu BOŞ sözlüğe bugünü ekleyip `yaz` ile üstüne
    basıyordu. Tek bir yarım yazma 120 günlük geçmişi geri dönülmez
    biçimde siliyordu (120 gün / seri=120 -> 1 gün / seri=0). Artık dosya
    duruyor: geri alınabilir. Aynı kurtarma ayarlar.json'da zaten vardı
    (`goz_molasi.ayarlari_oku`), geçmişe konmamıştı.
    """
    global son_bozulma
    hedef = yol + ".bozuk"
    # ÖNCEKİ YEDEĞİ EZME — ölçüldü (29.08.2026): ikinci bir bozulma,
    # birinci bozulmanın 120 günlük yedeğini bir günlük dosyayla
    # değiştiriyordu (8528 bayt -> 77 bayt). Kurtarılacak veriyi taşıyan
    # yedek, en değerli olan İLK yedektir; sonrakiler numara alır.
    if os.path.exists(hedef):
        n = 2
        while n < 50 and os.path.exists("%s.bozuk%d" % (yol, n)):
            n += 1
        hedef = "%s.bozuk%d" % (yol, n)
    try:
        os.replace(yol, hedef)
    except Exception:
        hedef = yol                    # taşıyamadık; hiç değilse söyleyelim
    son_bozulma = (hedef, str(sebep))


def oku(klasor):
    global okunamadi
    okunamadi = False
    yol = _yol(klasor)
    try:
        with open(yol, "r", encoding="utf-8-sig") as f:
            veri = json.load(f)
    except FileNotFoundError:
        return {}                      # ilk çalıştırma: bozukluk değil
    except OSError:
        # DOSYA AÇILAMADI — içerik bozuk DEĞİL. Antivirüs, yedekleme ya
        # da eşitleme aracı dosyayı bir an kilitleyebiliyor; bu yol
        # `_hafta_ciz` üzerinden saniyede dört kez geçiliyor, yani günde
        # ~345.000 kez. Ölçüldü (29.08.2026): tek bir PermissionError'da
        # `_kenara_al` SAĞLAM 120 günlük dosyayı .bozuk'a taşıyordu ve
        # sonraki yazma yerine 1 günlük dosya koyuyordu (120 gün -> 1).
        # Geçici engelde dosyaya DOKUNMA, yalnız bu turu atla.
        okunamadi = True
        return {}
    except Exception as hata:
        # JSONDecodeError / UnicodeDecodeError: içerik GERÇEKTEN bozuk.
        _kenara_al(yol, hata)
        return {}
    if isinstance(veri, dict):
        return veri
    _kenara_al(yol, "üst düzey tür sözlük değil: %s" % type(veri).__name__)
    return {}


def atomik_yaz(yol, veri, girinti=1, sirali=False):
    """JSON'u ÖNCE geçici dosyaya yazar, SONRA `os.replace` ile taşır.

    NİYE — ölçüldü (29.08.2026): `open(yol, "w")` dosyayı yazmadan ÖNCE
    buduyor. Yazma yarıda kesilirse (elektrik, taskkill, Windows
    kapanışı — kapanışta da yazılıyor, yani sürecin öldürülme riskinin
    en yüksek olduğu anda) diskte 0 baytlık ya da yarım bir dosya
    kalıyordu. Üç bozulma biçiminin üçünde de aynı kayıp ölçüldü.
    `os.replace` aynı sürücüde atomiktir: ya eski dosya durur, ya yeni;
    ikisinin arası yoktur.

    `fsync`: `replace` atomik ama içeriğin diske İNMESİ garanti değil.
    Ani güç kesintisinde NUL dolgu bir dosya kalabiliyor (ölçüldü).

    True/False döner — çağıran taraf yazmanın GERÇEKTEN olduğunu
    bilebilsin diye; eski hâlde `except: pass` ile yutuluyordu.
    """
    gecici = yol + ".yeni"
    try:
        klasor = os.path.dirname(yol)
        if klasor:
            os.makedirs(klasor, exist_ok=True)
        with open(gecici, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=girinti,
                      sort_keys=sirali)
            f.flush()
            os.fsync(f.fileno())
        os.replace(gecici, yol)
        return True
    except Exception:
        # Yarım geçici dosyayı bırakma; ASIL dosyaya dokunma.
        try:
            if os.path.exists(gecici):
                os.remove(gecici)
        except Exception:
            pass
        return False


def yaz(klasor, veri):
    try:
        # Eskiyenleri at
        sinir = (date.today() - timedelta(days=SAKLANAN_GUN)).isoformat()
        veri = {g: d for g, d in veri.items() if g >= sinir}
    except Exception:
        return False
    return atomik_yaz(_yol(klasor), veri, girinti=1, sirali=True)


def gunu_isle(klasor, gun, istatistik):
    """Bir günün özetini geçmişe yaz. GERİYE GİTMEZ.

    Ölçüldü (29.08.2026): istatistik.json yarım kalırsa açılışta sayaçlar
    0 okunuyordu ve 30 saniye sonraki ilk kayıt günün 9 molasını 0 ile
    eziyordu — oysa TAM O ANDA gecmis.json'da doğru değer duruyordu
    ({'mola': 9, 'uzun': 2}). Gün içi sayaçlar yalnız ileri gider; geri
    gitmeleri veri kaybı işaretidir, o yüzden büyük olan kalır. Eski
    davranış "üstüne yazar, toplamaz" idi ve günü geri getirilemez
    biçimde sıfırlıyordu.

    Alan adları ALANLAR'dan üretiliyor; elle ikinci bir liste yok.
    """
    veri = oku(klasor)
    if okunamadi:
        # Dosya bir an açılamadı (kilit/izin). Diskte NE olduğunu
        # bilmiyoruz; üstüne tek günlük veri basmak 120 günü silmek
        # olurdu. Bu tur atlanır — 30 saniye sonra yeniden denenecek.
        return veri
    eski = veri.get(gun)
    veri[gun] = {
        ad: max(sayac_oku(istatistik, ist_ad, en_cok),
                sayac_oku(eski, ad, en_cok))
        for ad, (ist_ad, en_cok) in ALANLAR.items()
    }
    yaz(klasor, veri)
    return veri


def son_gunler(klasor, adet=7, bugun_istatistik=None):
    """Son N günü [(gun_adi, mola_sayisi, bugun_mu), ...] olarak döndürür.

    Bugünün verisi henüz geçmişe yazılmamış olabilir; o yüzden anlık
    istatistiği dışarıdan alıp üstüne biniyoruz.
    """
    veri = oku(klasor)
    bugun = date.today()
    sonuc = []
    for i in range(adet - 1, -1, -1):
        g = bugun - timedelta(days=i)
        anahtar = g.isoformat()
        if i == 0 and bugun_istatistik is not None:
            sayi = istatistigin_molasi(bugun_istatistik)
        else:
            sayi = gunun_molasi(veri.get(anahtar))
        sonuc.append((GUN_ADLARI[g.weekday()], sayi, i == 0))
    return sonuc


def seri(klasor, bugun_istatistik=None, hedef=GUNLUK_HEDEF):
    """Kaç gündür üst üste günlük hedefi tutturuyor?

    Bugün henüz hedefe ulaşmadıysa seri bozulmuş sayılmaz — dün'den
    geriye doğru sayılır. Sabahın köründe "serin bitti" demek haksızlık.
    """
    veri = oku(klasor)
    bugun = date.today()

    def gunun_sayisi(g):
        if g == bugun and bugun_istatistik is not None:
            return istatistigin_molasi(bugun_istatistik)
        return gunun_molasi(veri.get(g.isoformat()))

    sayac = 0
    # Bugün hedefi tutturduysa bugünden, tutturmadıysa dünden başla
    baslangic = 0 if gunun_sayisi(bugun) >= hedef else 1
    i = baslangic
    while i < SAKLANAN_GUN:
        if gunun_sayisi(bugun - timedelta(days=i)) >= hedef:
            sayac += 1
            i += 1
        else:
            break
    return sayac
