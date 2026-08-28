# -*- coding: utf-8 -*-
"""degisiklikler.py'yi degisiklikler.js'ten ÜRETİR.

NEDEN ÜRETİLİYOR
  Aynı metni iki dosyada elle tutmak, ikisinin ayrışması demektir.
  Bu projede bir kez yaşandı: `bilgiler.py` ile `bilgiler.js` ikiz
  tutuluyordu ve kaydılar (biri düz kesme işareti, öbürü tipografik).
  `dunya.js` → `dunya.py` için kurulan desen aynı sebeple var.

  Burada risk daha büyük: web şeridi ile masaüstü kartı AYNI
  düzeltmeleri anlatmalı. Ayrışırlarsa kullanıcı iki farklı şey okur
  ve hangisinin doğru olduğunu bilemez.

  Tek kaynak `degisiklikler.js`. Bu dosyayı ELLE DÜZENLEME —
  üretimde silinir.

ÇALIŞTIR
  python degisiklikler_uret.py
"""
import io
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYNAK = os.path.join(KOK, "degisiklikler.js")
HEDEF = os.path.join(KOK, "masaustu", "degisiklikler.py")

# Tek tırnaklı JS metni; kaçışlı tırnağı da kapsıyor
METIN = re.compile(r"'((?:[^'\\]|\\.)*)'")


def coz(ham):
    """JS'te `+` ile bölünmüş metin parçalarını tek metne indirger."""
    parcalar = METIN.findall(ham)
    if not parcalar:
        return None
    birlesik = "".join(parcalar)
    return birlesik.replace("\\'", "'").replace("\\\\", "\\")


def main():
    if not os.path.exists(KAYNAK):
        print("KAYNAK YOK: %s" % KAYNAK)
        return 2
    js = io.open(KAYNAK, encoding="utf-8").read()

    # Yorumları at: içlerinde tırnak var ve ayrıştırmayı bozuyorlar
    govde = js.split("const DEGISIKLIKLER", 1)
    if len(govde) != 2:
        print("DEGISIKLIKLER dizisi bulunamadı")
        return 2
    govde = govde[1]

    kayitlar = []
    # Her kayıt bir `{ ... }` bloğu; `surum:` ile başlayanları alıyoruz
    for blok in re.findall(r"\{\s*surum:\s*(\d+)(.*?)\n  \},", govde, re.S):
        surum = int(blok[0])
        icerik = blok[1]
        tarih_m = re.search(r"tarih:\s*'([^']*)'", icerik)
        # Masaustu ayri surumleniyor; anahtari da ayri.
        mas_m = re.search(r"masaustuSurum:\s*'([^']*)'", icerik)
        ozet_m = re.search(r"ozet:\s*((?:'(?:[^'\\]|\\.)*'\s*\+?\s*)+)", icerik)
        gozden = "ayarGozdenGecir: true" in icerik
        maddeler_m = re.search(r"maddeler:\s*\[(.*?)\n    \],", icerik, re.S)
        maddeler = []
        if maddeler_m:
            # Her madde `,` ile ayrılmış ama metin içinde de virgül var;
            # bu yüzden satır bazlı değil, tırnak grubu bazlı ayırıyoruz.
            for parca in re.split(r"',\s*\n", maddeler_m.group(1)):
                m = coz(parca if parca.rstrip().endswith("'") else parca + "'")
                if m:
                    maddeler.append(m)
        kayitlar.append({
            "surum": surum,
            "tarih": tarih_m.group(1) if tarih_m else "",
            "masaustu_surum": mas_m.group(1) if mas_m else None,
            "ozet": coz(ozet_m.group(1)) if ozet_m else "",
            "ayar_gozden_gecir": gozden,
            "maddeler": maddeler,
        })

    if not kayitlar:
        print("HİÇ KAYIT ÇIKMADI — üretim yapılmadı.")
        print("Sıfır sonuç 'başarı' değildir; desen değişmiş olabilir.")
        return 1

    satirlar = [
        "# -*- coding: utf-8 -*-",
        '"""ÜRETİLMİŞ DOSYA — degisiklikler.js\'ten.',
        "",
        "ELLE DÜZENLEME. Değişiklik metnini `degisiklikler.js` içinde",
        "değiştir, sonra `python masaustu/degisiklikler_uret.py` çalıştır.",
        '"""',
        "",
        "DEGISIKLIKLER = [",
    ]
    for k in kayitlar:
        satirlar.append("    {")
        satirlar.append("        %r: %d," % ("surum", k["surum"]))
        satirlar.append("        %r: %r," % ("tarih", k["tarih"]))
        satirlar.append("        %r: %r," % ("masaustu_surum",
                                             k["masaustu_surum"]))
        satirlar.append("        %r: %r," % ("ozet", k["ozet"]))
        satirlar.append("        %r: %r," % ("ayar_gozden_gecir",
                                             k["ayar_gozden_gecir"]))
        satirlar.append("        'maddeler': [")
        for m in k["maddeler"]:
            satirlar.append("            %r," % m)
        satirlar.append("        ],")
        satirlar.append("    },")
    satirlar.append("]")
    satirlar.append("")
    satirlar.append("")
    satirlar.append("def son(surum=None):")
    satirlar.append('    """Verilen sürümün kaydını döndürür; yoksa None."""')
    satirlar.append("    for k in DEGISIKLIKLER:")
    satirlar.append("        if surum is None or k.get('masaustu_surum') == surum:")
    satirlar.append("            return k")
    satirlar.append("    return None")
    satirlar.append("")

    io.open(HEDEF, "w", encoding="utf-8", newline="\n").write(
        "\n".join(satirlar))
    print("Üretildi: %s" % os.path.basename(HEDEF))
    for k in kayitlar:
        print("  sürüm %d — %d madde" % (k["surum"], len(k["maddeler"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
