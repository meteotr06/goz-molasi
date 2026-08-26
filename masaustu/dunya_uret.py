# -*- coding: utf-8 -*-
"""dunya.py'yi dunya.js'ten ÜRETİR.

NEDEN ÜRETİLİYOR
  bilgiler.py ile bilgiler.js elle ikiz tutuluyor ve dosyanın başında
  "birini güncellersen diğerini de güncelle" notu var. Bugün bu ikizin
  kaydığını yakaladık (biri düz kesme işareti, diğeri tipografik).
  Aynı hatayı yeni bir dosyayla tekrarlamanın anlamı yok.

  Tek kaynak dunya.js. Bu betik ondan dunya.py çıkarıyor.
  dunya.py'yi ELLE DÜZENLEME — ilk üretimde silinir.

ÇALIŞTIR
  python dunya_uret.py
"""
import io
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYNAK = os.path.join(KOK, "dunya.js")
HEDEF = os.path.join(KOK, "masaustu", "dunya.py")

# JS'teki tek tırnaklı metinler; kaçışlı tırnağı da kapsıyor
METIN = re.compile(r"'((?:[^'\\]|\\.)*)'")


def alan_oku(govde, ad):
    """`ad: '...' + '...'` biçimindeki alanı okur, parçaları birleştirir."""
    m = re.search(re.escape(ad) + r"\s*:\s*", govde)
    if not m:
        return None
    kalan = govde[m.end():]
    # Alan bir sonraki `  <ad>:` satırına ya da kaydın sonuna kadar sürer
    son = re.search(r"\n\s{4}[a-z]+\s*:|\n\s{2}\}", kalan)
    parca = kalan[:son.start()] if son else kalan
    yazilar = METIN.findall(parca)
    if not yazilar:
        return None
    return "".join(y.replace("\\'", "'").replace("\\\\", "\\") for y in yazilar)


def main():
    if not os.path.exists(KAYNAK):
        print("KAYNAK YOK:", KAYNAK)
        return 1
    s = io.open(KAYNAK, encoding="utf-8").read()

    bas = s.find("const DUNYA = [")
    if bas == -1:
        print("dunya.js icinde DUNYA dizisi bulunamadi")
        return 1
    govde = s[bas + len("const DUNYA = ["):]
    govde = govde[:govde.find("\n];")]

    kayitlar = []
    for parca in re.split(r"\n  \},?\s*", govde):
        if "baslik" not in parca:
            continue
        b = alan_oku(parca, "baslik")
        m = alan_oku(parca, "metin")
        kn = alan_oku(parca, "kaynak")
        if not (b and m and kn):
            print("EKSIK KAYIT atlandi:", (b or "?")[:40])
            continue
        kayitlar.append((b, m, kn))

    if not kayitlar:
        print("hic kayit okunamadi")
        return 1

    satirlar = [
        "# -*- coding: utf-8 -*-",
        '"""',
        "DUNYADAN - molalarda gosterilen genel kultur kartlari.",
        "",
        "BU DOSYA URETILDI. Elle duzenleme - dunya.js'i degistir ve",
        "  python dunya_uret.py",
        "calistir. Aksi halde web ile masaustu birbirinden kayar.",
        '"""',
        "",
        "DUNYA = [",
    ]
    for b, m, kn in kayitlar:
        satirlar.append("    (")
        satirlar.append("        %r," % b)
        # Uzun metni okunakli parcalara bol
        satirlar.append("        %r," % m)
        satirlar.append("        %r," % kn)
        satirlar.append("    ),")
    satirlar.append("]")
    satirlar.append("")

    io.open(HEDEF, "w", encoding="utf-8", newline="\n").write("\n".join(satirlar))
    print("uretildi: %s  (%d kayit)" % (os.path.basename(HEDEF), len(kayitlar)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
