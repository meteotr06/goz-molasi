# -*- coding: utf-8 -*-
"""EXE İÇERİK DENETİMİ — düzeltmeler gerçekten programa girdi mi?

`exe_tazelik.py` "exe kaynaktan eski mi?" diye sorar — tarihe bakar.
Bu betik farklı bir soru sorar ve daha zor olanıdır:

  > Derleme yapıldı. Peki düzeltmeler GERÇEKTEN içine girdi mi?

  Tarih yeni olabilir ama derleme yarıda kalmış, yanlış klasörden
  yapılmış ya da eski bir kopyayı paketlemiş olabilir. "Derledim"
  bir niyettir; "içinde var" bir ölçümdür.

NASIL — uygulama ÇALIŞTIRILMADAN
  PyInstaller arşivi okunuyor ve `goz_molasi` modülünün derlenmiş
  hâli çıkarılıyor. Değişken ve yöntem adları bytecode içinde metin
  olarak durur; aranan işaret orada varsa kod da oradadır.

  Uygulama AÇILMIYOR. Bu önemli: bu program bir kez kullanıcının
  ekranını kilitledi, ve aile kipi tam ekran engel açabiliyor.

NEDEN BAYT ARAMASI DEĞİL
  Ölçüldü (28.08.2026): `--onefile` arşivi sıkıştırıyor. Ham exe
  içinde `gunluk_sinir_dk` aramak 0 sonuç veriyor; "aile" ise 67
  rastlantısal eşleşme veriyor. Yani ham arama hem KAÇIRIR hem
  YANLIŞ ALARM verir - iki yönlü güvenilmez.

BU DENETİMİN SINIRI — yazıyoruz, gizlemiyoruz
  Ad araması, VAR OLAN bir fonksiyonun İÇİNİN değiştiğini göremez.
  Örnek: `sayi_oku` eski exe'de de var; bu gece ona taşma koruması
  eklendi ama ad aynı kaldı, yani denetim farkı GÖRMEZ. Bu yüzden
  `sayi_oku` işaret listesine konmadı — ayırt etmeyen işaret,
  denetimi kalabalıklaştırır ve yanlış güven verir.

  Listedeki her işaret, gecenin YENİ eklenen bir adı. Yeni ad =
  kesin ayrım. İçerik değişimleri için `exe_tazelik.py` (tarih) ve
  sınama takımı var; üçü birlikte bakılır.

ÇALIŞTIRMA
  python exe_icerik.py
  Çıkış kodu 0 = bütün işaretler içeride, 1 = eksik var,
  2 = ölçülemedi (arşiv okunamadı).
"""
import io
import os
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(BURASI)

# (işaret, hangi düzeltmeyi temsil ediyor)
#
# Her işaret 27-28.08.2026 gecesinde eklenen GERÇEK bir düzeltmenin
# kod içindeki adı. Metin değil AD seçildi: metinler değişir, ad
# değişince zaten kod değişmiş demektir.
ISARETLER = [
    ("ekran_isareti",
     "Aile kipi: çocuk kayıt dosyasını düzenleyip günlük sınırı "
     "kaldıramaz (kertme)"),
    ("_sayac_isaretini_dogrula",
     "Aile kipi: ekran süresi geri alınırsa yakalanır ve ebeveyne "
     "söylenir"),
    ("EK_SURE_AZAMI_SN",
     "Aile kipi: 10 yıllık sahte 'ek süre' sınırı kalıcı olarak "
     "kaldıramaz"),
    ("ayar_uyarisi",
     "Koruma uygulanmıyorsa ekranda yazar (sessizce kapanmaz)"),
    ("_kopru_kalan",
     "Köprü ekranda yazan süreyi söyler — hayalet mola üretmez"),
    ("_kopru_verisi",
     "Köprü: tarayıcı sürümü sayacı devralır, süre başa sarmaz"),
    ("saat_oku",
     "Saat alanları doğrulanır — '25:00' kabul edilmez, hatalı "
     "yazım sessizce varsayılana dönmez"),

    # 29.08.2026 - masaüstüne giren değişiklikler.
    #
    # Liste 28.08'de yazılmıştı ve o günden sonraki düzeltmeleri
    # KAPSAMIYORDU: derleme sonrası araç "yedi işaret de içeride"
    # deyip geçecekti, oysa 29.08 düzeltmesi girmemiş olabilirdi.
    # Bugünün dersi: yeşil sonuç kapsamın doğru olduğunu söylemez.
    ("en yüksek riskin",
     "Sağlık bilgisi kaynağıyla aynı şeyi söylüyor (AOA yanlış "
     "aktarılıyordu: 'risk 2 saati aşınca başlıyor' deniyordu)"),
    ("sayı var ama sınır yok",
     "Oturmak üzerine kaynaklı bilgi kartı (NHS + WHO)"),
    ("sayi_yaz",
     "Sayilar Turkce yazimla ('2.240 dakika', '2240' degil)"),
    ("istatistik_suz",
     "Bozuk kayıt dosyası ekrana çıkmıyor ve çökme üretmiyor "
     "('cok mola', '-99 sn', ValueError)"),
    # 30.08.2026 - masaustu govdesinde 7 boyutlu tarama (34 alt calisan,
    # 25 kusur onaylandi). Asagidakilerin hepsi SESSIZ hatalardi:
    # uygulama calisiyor gorunuyor, sayi ya da koruma yanlis.
    ("ayarlari_suz",
     "Bozuk ayar dosyası uygulamayı AÇILMAZ yapamaz (tek yanlış tür "
     "bütün korumaları sessizce kaldırıyordu)"),
    ("AYAR_DURUMU",
     "Ayar dosyası bozulduysa/kaybolduysa/yazılamadıysa ekranda yazar "
     "— aile kipi sessizce kapanmaz"),
    ("atomik_yaz",
     "Yazma yarıda kesilse de ayarlar, şifre ve geçmiş silinmez"),
    ("SURE_UST_SINIR_SN",
     "24 saatten uzun süre doğru yazılır ('3 gün', '0 sn' değil)"),
    ("SAYIM_TAVANI",
     "Ekran süresi gerçek geçen süreyi sayar (8 saatte ~16 dakika "
     "eksik sayıyordu)"),
    ("gunun_molasi",
     "'Senin durumun' kartı uzun molaları da sayar (aynı ekranda iki "
     "farklı sayı çıkıyordu)"),
    ("dakika_oku",
     "Yasak saati tek çözümleyiciyle okunur — bozuk değerde yasak "
     "sessizce 00:00'a kaymaz"),
    ("sonraki_mola_sn",
     "Ekranda yazan mola süresi AYARDAN türer (ayar 60 sn iken '20 "
     "saniye' yazıyordu)"),
    ("gunun_arsivi",
     "Bozuk geçmiş kaydı sayacı dondurmaz ve 120 günü silmez"),
    ("_saat_sicramasini_yakala",
     "Aile kipi: saati bir gün İLERİ alıp geri getirmek günlük sınırı "
     "sıfırlayamaz"),
    ("bekci_sozu_al",
     "Aile kipi: bekçinin gizli sözü komut satırında durmuyor (Görev "
     "Yöneticisi'nden okunup sahte çıkış bayrağı yazılabiliyordu)"),
    ("erken_olum_karari",
     "Aile kipi: art arda iki kez öldürmek bekçiyi kalıcı kaldıramaz"),
    ("bekci_notu_var_mi",
     "Aile kipi: bekçi öldürülürse uygulama fark eder"),
    ("ONAY_KISAYOL_ANAHTARI",
     "Açılışta başlatmayı Windows'tan kapatırsan geri konulmaz ve "
     "ayardaki kutu doğruyu gösterir"),
    ("_engel_acik_mi",
     "Aile kipi engeli açıkken köprü 'sayıyorum' demez (hayalet mola)"),
]


def modulu_cikar():
    """(veri, hata) döndürür. Uygulama ÇALIŞTIRILMAZ."""
    exe = None
    for ad in sorted(os.listdir(KOK)):
        if ad.lower().endswith(".exe"):
            exe = os.path.join(KOK, ad)
            break
    if not exe:
        return None, "kök klasörde .exe yok"
    try:
        from PyInstaller.archive.readers import CArchiveReader
    except Exception as e:
        return None, "PyInstaller okuyucusu yok (%s)" % type(e).__name__
    try:
        ham = CArchiveReader(exe).extract("goz_molasi")
    except Exception as e:
        return None, "arşiv okunamadı: %s: %s" % (type(e).__name__, e)
    veri = ham[1] if isinstance(ham, tuple) else ham
    if not veri:
        return None, "goz_molasi modülü arşivde bulunamadı"
    return veri, None


def isaretler_kaynakta_mi():
    """Her isaret KAYNAK dosyalarda geciyor mu?

    NIYE AYRI SORU: yanlis yazilmis bir isaret exe'de asla bulunamaz
    ve arac "duzeltme programda YOK" der - oysa duzeltme oradadir.
    Yanlis alarm veren bir bekci once guvenilirligini, sonra
    kullanimini kaybeder. Bu yuzden "liste yanlis" ile "derleme eski"
    ayri ayri soyleniyor.

    Doner: kaynakta bulunamayan isaretler.
    """
    kaynak = ""
    for ad in sorted(os.listdir(BURASI)):
        if ad.endswith(".py"):
            try:
                kaynak += io.open(os.path.join(BURASI, ad),
                                  encoding="utf-8").read()
            except Exception:
                pass
    return [i for i, _ in ISARETLER if i not in kaynak]


def main():
    yanlis = isaretler_kaynakta_mi()
    if yanlis:
        print("LISTE YANLIS — %d isaret KAYNAKTA da yok:" % len(yanlis))
        for i in yanlis:
            print("  - %s" % i)
        print()
        print("Bu bir 'derleme eski' bulgusu DEGIL. Bu isaretler")
        print("exe'de zaten hicbir zaman bulunamaz; arac yanlis alarm")
        print("verir. exe_icerik.py'deki ISARETLER listesini duzelt.")
        return 2

    veri, hata = modulu_cikar()
    if veri is None:
        # ÖLÇÜLEMEDİ, "temiz" DEĞİL. Ölçemediğini geçmiş saymak,
        # bu projede gün boyu kovaladığımız hatanın ta kendisi.
        print("ÖLÇÜLEMEDİ — %s" % hata)
        print("Bu bir 'geçti' değil. exe'nin içeriği hakkında hiçbir")
        print("şey bilmiyoruz.")
        return 2

    print("Okunan modül: %d bayt (uygulama açılmadı)" % len(veri))
    print()
    eksik = []
    for isaret, aciklama in ISARETLER:
        var = isaret.encode("utf-8") in veri
        print("  %-26s %s" % (isaret, "VAR" if var else "EKSİK"))
        print("      %s" % aciklama)
        if not var:
            eksik.append((isaret, aciklama))

    print()
    if not eksik:
        print("SONUÇ: bütün düzeltmeler programın içinde (%d/%d)."
              % (len(ISARETLER), len(ISARETLER)))
        return 0

    print("SONUÇ: %d düzeltme programda YOK:" % len(eksik))
    for isaret, aciklama in eksik:
        print("  - %s" % aciklama)
    print()
    print("Kullanıcı bu programı çalıştırdığında yukarıdaki korumalar")
    print("ÇALIŞMIYOR. Kaynakta düzeltilmiş olması yetmez.")
    print()
    print("Yapılacak: DERLE.bat")
    print("UYARI: DERLE.bat sonunda uygulamayı AÇAR — kullanıcının")
    print("       kendi kararı olmadan çalıştırılmaz.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
