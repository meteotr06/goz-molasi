# -*- coding: utf-8 -*-
"""DAMGA DENETİMİ — dosya değişti ama sürüm damgası aynı mı kaldı?

NEDEN VAR
  `surum_ekle.py`, HTML'deki betik adlarına `?s=v79` gibi bir damga
  basıyor. Damga `sw.js` içindeki SURUM'dan geliyor. Bir dosyayı
  değiştirip SURUM'u artırmayı unutursan damga aynı kalır.

  KİMİ ETKİLER — ölçüldü:
    • Servis işçisi KURULU kullanıcı: etkilenmez. Bizim işçi "önce ağ"
      + `cache: 'no-cache'` çalışıyor, damga aynı olsa da güncel
      dosyayı alıyor. Bunu deneyerek ölçtüm: damgayı artırmadan
      dunya.js'e kayıt ekledim, sayfa yeni kodu okudu.
    • Servis işçisi HENÜZ KURULMAMIŞ kullanıcı (ilk ziyaret, önbellek
      temizlenmiş, işçi kaydı silinmiş): **etkilenir.** Onun için
      tarayıcı önbelleğini kıran tek şey damga.

  Yani bu denetim "her şey bozulur" diye değil, ölçülmüş dar bir
  kitleyi korumak için var. Korkunun büyüklüğünü ölçmeden düzeltmeye
  kalkmıyoruz.

NASIL
  `surum_ekle.py` her çalıştığında damgalanan dosyaların özetini
  `.damga_kayit.json` içine yazar. Bu betik özetleri yeniden hesaplar:
  bir dosya değişmiş ama SURUM aynıysa hata verir.

ÇALIŞTIRMA
  python damga_denetle.py
"""
import hashlib
import io
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYIT = os.path.join(KOK, ".damga_kayit.json")

# surum_ekle.py'nin damgaladığı dosyalar — EN AZ bunlar izlenir.
# Asıl kapsam `damgalanan_dosyalar()` ile sw.js'ten türetiliyor.
DAMGALANAN_ASGARI = [
    "stil.css", "cekirdek.js", "dil.js", "bilgiler.js", "bilgiler_en.js",
    "mola_icerik.js", "arayuz.js", "egzersiz.js", "reklam.js", "dunya.js",
]


def damgalanan_dosyalar():
    """İzlenen dosyalar: SERVİS İŞÇİSİ NEYİ ÖNBELLEĞE ALIYORSA O.

    Kapsam ELLE YAZILMIYOR. Kural şu: servis işçisi bir dosyayı
    önbelleğe alıyorsa, o dosya değişip SURUM artmadığında kurulu
    kullanıcı ESKİSİNİ görmeye devam eder. Yani izlenmesi gereken küme,
    önbellek listesinin ta kendisidir.

    NİYE: 29.08.2026'da bu liste elle yazılıydı ve yalnızca 10 CSS/JS
    dosyası vardı. sw.js ise 23 dosya önbelleğe alıyordu — ikonlar,
    dört sayfa, manifest.json ve paylaşım görselleri listede YOKTU.
    Aynı gün ikonlar değiştirilirken ölçüldü: ikonu değiştirip damgayı
    unutmak sessizce geçiyordu.

    Döner: (dosya_listesi, hata_metni). Liste okunamazsa SESSİZCE eski
    listeye dönmez — bu projede sessiz düşüş hata sayılıyor.
    """
    try:
        sw = io.open(os.path.join(KOK, "sw.js"), encoding="utf-8").read()
    except Exception as e:
        return [], "sw.js okunamadı: %s" % e
    m = re.search(r"const\s+DOSYALAR\s*=\s*\[(.*?)\]", sw, re.S)
    if not m:
        return [], ("sw.js içinde DOSYALAR listesi bulunamadı — damga "
                    "bekçisi kapsamını türetemiyor")
    adlar = [a for a in re.findall(r"'\./([^']*)'", m.group(1)) if a]
    if not adlar:
        return [], "sw.js DOSYALAR listesi boş okundu"
    for a in DAMGALANAN_ASGARI:
        if a not in adlar:
            adlar.append(a)
    return adlar, None


def surum_oku():
    sw = io.open(os.path.join(KOK, "sw.js"), encoding="utf-8").read()
    m = re.search(r"SURUM\s*=\s*'goz-molasi-(v\d+)'", sw)
    return m.group(1) if m else None


def ozetler():
    d = {}
    for ad in damgalanan_dosyalar()[0]:
        y = os.path.join(KOK, ad)
        if not os.path.exists(y):
            continue
        h = hashlib.sha256(open(y, "rb").read()).hexdigest()[:16]
        d[ad] = h
    return d


def kaydet():
    """surum_ekle.py bunu çağırır."""
    io.open(KAYIT, "w", encoding="utf-8").write(json.dumps(
        {"surum": surum_oku(), "ozetler": ozetler()},
        ensure_ascii=False, indent=1) + "\n")


SAYFALAR = ["index.html", "rehber.html", "guide.html", "gizlilik.html"]


def damga_tutarli_mi(surum):
    """HER sayfadaki HER damga, sw.js'teki SURUM ile aynı mı?

    27.08.2026'da ölçüldü: `kopru.js` eklerken index.html'i ELLE
    v83'e çektim, öbür üç sayfa v82'de kaldı. Takım YEŞİL geçti —
    bu denetim yalnızca "dosya değişti ama SURUM artmadı" diye
    bakıyordu, TERSİNİ hiç sormuyordu.

    Aynı hata Planlayıcı'da da bulundu: `stil.css?v=17` iken
    betikler `?v=19` idi. Geride kalan CSS olunca kimse fark etmez,
    çünkü uygulama çalışır — yalnızca GÖRÜNÜM eski kalır.

    Kök sebep her iki durumda da aynı: elle damgalamak. Aracı var
    (`surum_ekle.py`) ve tek yerden basıyor.

    ⚠️ BU DENETİM HER PROJEYE UYMAZ — başka projeye kopyalamadan önce oku.
    Burada geçerli olmasının sebebi, `surum_ekle.py`'nin BÜTÜN dosyalara
    AYNI sürümü basması. İki geçerli strateji var:
      • tek tip damga (burası): hepsi aynı sürüm
      • dosya başına damga (06 Planlayıcı): her dosya kendi son
        değişim sürümünde kalır — daha az gereksiz indirme
    İkincisinde farklı sayılar görmek NORMALDİR. 27.08.2026'da ölçüldü:
    Planlayıcı'da `stil.css?v=17` / betikler `?v=19` "hata" sanıldı;
    canlı ve yerel stil.css'in md5'i BİREBİR AYNI çıktı — damga doğru
    çalışıyordu. Görünüşe bakan denetim yanlış alarm üretti.
    Doğru soru "damgalar eşit mi" değil, "kullanıcı eski dosyayı alıyor
    mu" — onu ölçmek için canlı ile yereli karşılaştır.
    """
    kalan = []
    for sayfa in SAYFALAR:
        yol = os.path.join(KOK, sayfa)
        if not os.path.exists(yol):
            continue
        metin = io.open(yol, encoding="utf-8-sig").read()
        for damga in set(re.findall(r"\?s=(v\d+)", metin)):
            if damga != surum:
                kalan.append("%s -> %s (sw.js: %s)" % (sayfa, damga, surum))
    return kalan


def onbellekte_eksik():
    """HTML'e eklenen yerel dosya, sw.js'in önbellek listesinde var mı?

    Yeni bir betik eklerken sw.js listesini güncellemeyi unutmak
    sessiz bir hata: çevrimiçiyken her şey çalışır, ÇEVRİMDIŞIYKEN
    o dosya gelmez ve uygulama yarım açılır. `kopru.js` eklenirken
    bu tam bir adım uzaktaydı.
    """
    sw = io.open(os.path.join(KOK, "sw.js"), encoding="utf-8-sig").read()
    liste = set(re.findall(r"'\./([^']+)'", sw))
    kalan = []
    for sayfa in SAYFALAR:
        yol = os.path.join(KOK, sayfa)
        if not os.path.exists(yol):
            continue
        metin = io.open(yol, encoding="utf-8-sig").read()
        for dosya in set(re.findall(r'(?:src|href)="([a-zA-Z0-9_.-]+\.(?:js|css))\?s=', metin)):
            if dosya not in liste:
                kalan.append("%s -> %s sw.js önbellek listesinde YOK" % (sayfa, dosya))
    return kalan


def main():
    surum = surum_oku()
    if not surum:
        print("BAŞARISIZ — sw.js içinde SURUM bulunamadı")
        return 1

    if not os.path.exists(KAYIT):
        kaydet()
        print("İlk kayıt oluşturuldu (%s). Bundan sonra denetlenecek." % surum)
        return 0

    # Bu iki denetim KAYITTAN BAĞIMSIZ: dosya değişmemiş olsa da
    # tutarsızlık durabilir. Erken dönüşlerin ÖNÜNDE olmalılar.
    _, kapsam_hatasi = damgalanan_dosyalar()
    if kapsam_hatasi:
        print("BAŞARISIZ — %s" % kapsam_hatasi)
        return 1

    sorunlar = damga_tutarli_mi(surum) + onbellekte_eksik()
    if sorunlar:
        print("BAŞARISIZ — damga/önbellek tutarsız:")
        for s in sorunlar:
            print("  -", s)
        print()
        print("Yapılacak: python masaustu/surum_ekle.py")
        print("           (elle damgalama; araç tek yerden basıyor)")
        return 1

    eski = json.load(io.open(KAYIT, encoding="utf-8-sig"))
    simdi = ozetler()

    degisen = [a for a in simdi
               if eski.get("ozetler", {}).get(a) != simdi[a]]

    if not degisen:
        print("TAMAM — önbelleğe alınan %d dosyanın hiçbiri değişmemiş (%s)."
              % (len(simdi), surum))
        return 0

    if eski.get("surum") == surum:
        print("BAŞARISIZ — %d dosya değişti ama SURUM hâlâ %s:"
              % (len(degisen), surum))
        for a in degisen:
            print("  -", a)
        print()
        print("Servis işçisi kurulu olmayan kullanıcı ESKİ kodu görür.")
        print("Yapılacak: sw.js içindeki SURUM'u artır, sonra")
        print("           python masaustu/surum_ekle.py")
        return 1

    kaydet()
    print("TAMAM — %d/%d dosya değişti, SURUM %s -> %s."
          % (len(degisen), len(simdi), eski.get("surum"), surum))
    return 0


if __name__ == "__main__":
    sys.exit(main())
