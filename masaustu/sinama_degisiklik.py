# -*- coding: utf-8 -*-
"""K-44 "neler değişti" bildiriminin sessizce kaybolmasını önler.

NİYE VAR
  Bu bildirim sınıfının hepsi AYNI ŞEKİLDE bozuluyor: uygulama
  çalışır, hata çıkmaz, bildirim yalnızca hiç görünmez. Kimse fark
  etmez. Bir günde üç kez yakalandı:

    09 Hesap Araçları : kayıt 51, yayın damgası 52  → şerit yok
    05 masaüstü       : `son("1.1")` → None          → kart yok
    05 web            : damga v94, kayıt 93          → şerit yok

  Üçü de "iki elle yazılan sayı tutmalı" varsayımından çıktı. Web
  tarafında varsayım kaldırıldı (eşitlik yerine ">"), ama geri
  gelmesin diye ölçüyoruz.

NE ÖLÇÜLMÜYOR
  Şeridin ekranda GÖRÜNDÜĞÜ. O tarayıcı işi; burada dosyalar arası
  tutarlılık ölçülüyor. Bu sınama geçse de tarayıcıda ölçmek gerekir.

ÇALIŞTIR
  python sinama_degisiklik.py
"""
import io
import os
import re
import subprocess
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = []


def oku(ad):
    return io.open(os.path.join(KOK, ad), encoding="utf-8").read()


def bak(kosul, mesaj):
    if not kosul:
        h.append(mesaj)
    return kosul


# ---------- 1) Dosya gerçekten yükleniyor mu ----------
# Bir kardeş oturum 09'da bunu yaşadı: çok satırlı dizgide `+`
# unutulunca dosya HİÇ yüklenmedi ve o dosyaya bağlı 42 araç birden
# çalışmaz oldu. "Çıktı göründü" yetmiyor; dosya yüklendi mi ölçülüyor.
js = oku("degisiklikler.js")
bak("const DEGISIKLIKLER" in js, "degisiklikler.js: dizi tanımı yok")

# Bitişik iki dizgi (`'a' 'b'`) JS'te sözdizimi hatası — `+` unutulmuş demek
# Not: dosyada iki birleştirme biçimi var — Türkçe blok satır SONUNDA
# `+` koyuyor, İngilizce blok satır BAŞINDA. İkisi de geçerli JS, o
# yüzden sonraki satıra da bakılıyor. İlk hâli yalnız sona baktı ve
# 12 sahte hata verdi; tarayıcının kendisi de ölçülmek zorunda.
satirlar = js.split("\n")
for i, satir in enumerate(satirlar):
    s = satir.strip()
    if not s.endswith("'") or s.endswith("',") or s.endswith("' +"):
        continue
    sonraki = next((x.strip() for x in satirlar[i + 1:] if x.strip()), "")
    if not sonraki.startswith("+"):
        h.append("degisiklikler.js:%d: dizge `+` ya da `,` olmadan bitiyor"
                 % (i + 1))

# ---------- 2) index.html yüklüyor, sw.js önbelliyor ----------
html = oku("index.html")
sw = oku("sw.js")
bak('src="degisiklikler.js' in html, "index.html: degisiklikler.js yüklenmiyor")
bak("'./degisiklikler.js'" in sw, "sw.js: degisiklikler.js önbellek listesinde yok")

# Damga index.html içindeki diğerleriyle aynı olmalı
damgalar = set(re.findall(r'\?s=v(\d+)"', html))
bak(len(damgalar) <= 1, "index.html: karışık damga %s" % sorted(damgalar))

# ---------- 3) İki dil de dolu ----------
# Ölçüldü: İngilizce kipte başlık İngilizce, özet Türkçe çıkıyordu —
# kullanıcı tek kutuda iki dil okuyordu.
kayitlar = re.findall(r"\{\s*surum:\s*(\d+)(.*?)\n  \},", js, re.S)
bak(bool(kayitlar), "degisiklikler.js: hiç kayıt çıkmadı (desen değişmiş olabilir)")
for surum, icerik in kayitlar:
    for alan in ("ozet", "ozetEn", "tarih", "tarihEn", "maddeler", "maddelerEn"):
        bak(re.search(r"\b%s:" % alan, icerik),
            "kayıt %s: `%s` alanı yok" % (surum, alan))
    tr = re.search(r"\bmaddeler:\s*\[(.*?)\n    \],", icerik, re.S)
    en = re.search(r"\bmaddelerEn:\s*\[(.*?)\n    \],", icerik, re.S)
    if tr and en:
        say = lambda b: len(re.findall(r"',\s*\n", b + "',\n"))
        bak(say(tr.group(1)) == say(en.group(1)),
            "kayıt %s: madde sayıları farklı (tr %d, en %d)"
            % (surum, say(tr.group(1)), say(en.group(1))))

# ---------- 4) Web eşitlik varsayımına dönmemiş ----------
# Damga her yayında artıyor, kayıt artmıyor. Eşitlik arayan kod
# sessizce hiç çıkmaz — düzeltilen hata tam buydu.
arayuz = oku("arayuz.js")
bak("d.surum === damga" not in arayuz and "d.surum === surum" not in arayuz,
    "arayuz.js: damgaya EŞİTLİK aranıyor — bu sessizce hiç çıkmamak demek")
bak("d.surum > onceki" in arayuz, "arayuz.js: `> onceki` karşılaştırması yok")

# ---------- 5) İşaret `kaydet()` tarafından silinmiyor ----------
# `kaydet()` ayar nesnesini alan alan yeniden kuruyor; listede olmayan
# her alan 15 saniyede bir siliniyor. İşaret oraya konsaydı kullanıcı
# şeridi kapatır, sonra her açılışta yine görürdü.
bak("GORULEN_ANAHTARI = 'goz-molasi-gorulen'" in arayuz,
    "arayuz.js: görülen sürüm ayrı anahtarda tutulmuyor")
bak("gorulenSurum" not in arayuz.split("function kaydet()")[-1][:900],
    "arayuz.js: işaret `kaydet()` alanları arasına girmiş — 15 sn'de silinir")

# ---------- 6) Üretilen masaüstü dosyası taze ----------
u = subprocess.run([sys.executable, os.path.join(KOK, "masaustu",
                                                 "degisiklikler_uret.py")],
                   capture_output=True, text=True, encoding="utf-8")
bak(u.returncode == 0, "degisiklikler_uret.py hata verdi: %s" % u.stderr.strip())
py = oku(os.path.join("masaustu", "degisiklikler.py"))
bak("Family mode" not in py,
    "degisiklikler.py: İngilizce metin sızmış (masaüstü tek dilli)")
bak(py.count("'surum':") == len(kayitlar),
    "degisiklikler.py: kayıt sayısı degisiklikler.js ile tutmuyor")

if h:
    print("HATA:")
    for x in h:
        print("  -", x)
    sys.exit(1)
print("TAMAM — %d kayıt, iki dil dolu, damga eşitliği aranmıyor, işaret ayrı."
      % len(kayitlar))
