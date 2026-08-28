# -*- coding: utf-8 -*-
"""İç sınama sayfaları yayına sızıyor mu? (depo denetimi)

NİYE VAR
  K-48 diyor ki iç sınama sayfaları yayına gitmez. Kural vardı ve
  YİNE DE delindi — çünkü kural, dosyaları **tek tek adıyla**
  sayıyordu:

      sinama-web.html
      test-*.html

  Kural yazıldıktan sonra eklenen `sinama-donus.html` bu listeye
  girmedi. Kimse fark etmedi; dosya depoya alındı ve GitHub Pages
  onu olduğu gibi yayınladı.

  Ölçüldü (28.08.2026, canlı adres):
      sinama-donus.html -> 200      <-- yayında
      sinama-web.html   -> 404      <-- doğru

  Ad listesi, yazıldıktan sonra doğan dosyayı göremez. Desen görür.
  `.gitignore` artık `sinama-*.html` diyor; bu sınama da deseni
  değil SONUCU ölçüyor: depoda izlenen bir iç sınama sayfası var mı.

NE ÖLÇÜYOR
  İki şey:

  1) Kökte izlenen bir iç sınama sayfası var mı. İzlenmeyen dosya
     yayına gidemez; kökte izlenen dosya gider.

  2) `.nojekyll` dosyası var mı. Sınama takımı artık `_sinama/`
     altında duruyor ve depoda izleniyor — GitHub Pages Jekyll
     kullandığı ve alt tire ile başlayan klasörleri yayınlamadığı
     için siteye çıkmıyor. Ölçüldü (28.08.2026, canlı adres):

         _sinama/deneme.html -> 404      ana sayfa -> 200

     AMA bu koruma tek bir dosyaya bağlı: depoya `.nojekyll`
     eklenirse Jekyll kapanır ve `_sinama/` bir anda YAYINA ÇIKAR.
     Kimse bunu sınama sayfalarıyla ilişkilendirmez; bu yüzden
     burada denetleniyor.

NE ÖLÇMÜYOR
  Canlı sitede şu an ne durduğunu. Depodan düşürmek, canlıdan
  düşmesi için yeterli değil — bir sonraki yayın gerekir. Canlı
  ölçüm ayrı yapılır (curl ile adres denetimi).

ÇALIŞTIR
  python sinama_yayin.py
"""
import os
import subprocess
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Yayina gitmemesi gereken ic sayfa desenleri.
DESENLER = ("sinama-", "test-")

# Bu klasordekiler depoda DURABILIR: Jekyll alt tire ile baslayan
# klasorleri yayinlamiyor (olculdu; bkz. yukaridaki aciklama).
GUVENLI_KLASOR = "_sinama/"


def izlenenler():
    try:
        c = subprocess.run(
            ["git", "ls-files"],
            cwd=KOK, capture_output=True, text=True, timeout=30,
        )
    except Exception as e:
        return None, "git calistirilamadi: %s" % e
    if c.returncode != 0:
        return None, "git ls-files basarisiz: %s" % (c.stderr or "").strip()
    return [s.strip() for s in c.stdout.splitlines() if s.strip()], None


def main():
    dosyalar, hata = izlenenler()
    if hata:
        # Depo yoksa SESSIZ GECMIYORUZ: olcemedigimizi soyluyoruz.
        print("OLCULEMEDI - %s" % hata)
        return 1

    sizanlar = []
    for y in dosyalar:
        # `_sinama/` altindakiler yayinlanmiyor; sorun degil.
        if y.startswith(GUVENLI_KLASOR):
            continue
        ad = y.rsplit("/", 1)[-1].lower()
        if not ad.endswith(".html"):
            continue
        if any(ad.startswith(d) for d in DESENLER):
            sizanlar.append(y)

    korunan = len([y for y in dosyalar if y.startswith(GUVENLI_KLASOR)])
    print("izlenen dosya: %d" % len(dosyalar))
    print("guvenli klasorde: %d (Jekyll yayinlamaz)" % korunan)

    if os.path.exists(os.path.join(KOK, ".nojekyll")):
        print()
        print("BASARISIZ - depoda `.nojekyll` var.")
        print("  Jekyll kapali demektir; `_sinama/` klasoru YAYINA CIKAR")
        print("  ve butun ic sinama sayfalari herkese acilir.")
        print("  Yapilacak: `.nojekyll` dosyasini sil, ya da sinama")
        print("  takimini depo disina tasi.")
        return 1
    if sizanlar:
        print("BASARISIZ - ic sinama sayfasi DEPODA izleniyor:")
        for y in sizanlar:
            print("  - %s" % y)
        print()
        print("Yapilacak: git rm --cached <dosya>   (disktan silmez)")
        print("           ve .gitignore deseni kapsiyor mu bak.")
        return 1

    print("TAMAM - izlenen ic sinama sayfasi yok (desen: %s)"
          % ", ".join(d + "*.html" for d in DESENLER))
    return 0


if __name__ == "__main__":
    sys.exit(main())
