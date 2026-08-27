# -*- coding: utf-8 -*-
"""YERLEŞİM SINAMASI — panelde hiçbir şey üst üste binmesin.

NEDEN VAR
  "Arka planda çalışıyorum" şeridi panele sonradan eklendi ama kendine
  yer açılmamıştı: doğrudan sayaç kartının içine düşüyordu. Aynı şekilde
  öneri şeridi de "Programı kapat" düğmesinin üstüne biniyordu. İkisi de
  ancak ekran görüntüsüyle fark edildi.

  Bu sınama paneli GERÇEKTEN kurar (sahte çizim değil), sonra
  goz_molasi.py'nin kaydettiği yerleşim kutularını denetler.

NE DENETLER
  1. Panel her temada hatasız kuruluyor mu
  2. İki kutu üst üste biniyor mu
  3. Kutular pencerenin dışına taşıyor mu
  4. Yazılar pencerenin dışına taşıyor mu
  5. Arka plan şeridinin metni ilk açılışta dolu mu
  6. Şeridin yazısı kendi kutusunun içinde mi

ÇALIŞTIRMA
  python sinama_yerlesim.py
"""
import io
import os
import sys
import time
import tkinter as tk

import gorunum as gor
import ogeler as og
import goz_molasi as gm

# Tasarım ölçüsü; goz_molasi.py ile aynı olmak zorunda
TASARIM_G, TASARIM_Y = 580, 888


class SahtePanel(gm.Uygulama):
    """Uygulama.__init__ atlanır — zamanlayıcı, tepsi simgesi ve izin
    pencereleri açılmasın. Yalnızca _panel_kur'un ihtiyacı kurulur."""

    def __init__(self, tema, olcek):
        self.o = olcek
        self.ayar = {}
        self.tepsi = None
        self.baslangic_ani = time.time()
        self.ist = {
            "gun": time.strftime("%Y-%m-%d"),
            "tamamlanan": 3, "ertelenen": 1, "uzun_mola": 1,
            "ekran_sn": 13860.0, "kesintisiz_sn": 900.0,
            "programlar": {"chrome.exe": 2400, "code.exe": 1800},
        }
        gor.tema_uygula(tema, 1.0)

        self.kok = tk.Tk()
        self.kok.withdraw()                 # ekranda görünmesin
        # Gerçek uygulama yazı tiplerini de ölçekliyor. Bunu yapmazsak
        # küçük ölçekte yazılar olduğu gibi kalıp haksız yere taşıyor.
        try:
            self.kok.tk.call("tk", "scaling", self.o * 96.0 / 72.0)
        except Exception:
            pass
        self.G, self.Y = self.ol(TASARIM_G), self.ol(TASARIM_Y)
        self.kok.geometry("%dx%d" % (self.G, self.Y))
        self.yt = og.yazi_tipi_sec(self.kok)
        self._panel_kur()
        self.kok.update_idletasks()

    def kapat(self):
        try:
            self.kok.destroy()
        except Exception:
            pass


BURASI = os.path.dirname(os.path.abspath(__file__))


def kesisiyor_mu(a, b, pay=0):
    """İki dikdörtgen üst üste biniyor mu? pay kadar değme serbest."""
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return (ax1 + pay < bx2 and bx1 + pay < ax2 and
            ay1 + pay < by2 and by1 + pay < ay2)


def denetle(tema, olcek, hatalar):
    etiket = "%s / ölçek %.2f" % (tema, olcek)
    try:
        p = SahtePanel(tema, olcek)
    except Exception as e:
        hatalar.append("[%s] panel KURULAMADI: %r" % (etiket, e))
        return

    try:
        kutular = getattr(p, "yerlesim_kutulari", None)
        if not kutular:
            hatalar.append("[%s] yerlesim_kutulari kaydı yok" % etiket)
            return

        # 2) Kutular üst üste biniyor mu
        for i in range(len(kutular)):
            ad_a, ax1, ay1, ax2, ay2 = kutular[i]
            for j in range(i + 1, len(kutular)):
                ad_b, bx1, by1, bx2, by2 = kutular[j]
                if kesisiyor_mu((ax1, ay1, ax2, ay2), (bx1, by1, bx2, by2)):
                    hatalar.append(
                        "[%s] ÜST ÜSTE BİNİYOR: '%s' (%d-%d) ile '%s' (%d-%d)"
                        % (etiket, ad_a, ay1, ay2, ad_b, by1, by2))

        # 3) Kutular pencerenin dışına taşıyor mu
        for ad, x1, y1, x2, y2 in kutular:
            if x1 < 0 or y1 < 0 or x2 > p.G or y2 > p.Y:
                hatalar.append(
                    "[%s] PENCERE DIŞINDA: '%s' (%d,%d)-(%d,%d), pencere %dx%d"
                    % (etiket, ad, x1, y1, x2, y2, p.G, p.Y))

        # 4) Yazılar pencerenin dışına taşıyor mu
        for oge in p.t.find_all():
            if p.t.type(oge) != "text":
                continue
            if not (p.t.itemcget(oge, "text") or "").strip():
                continue
            kutu = p.t.bbox(oge)
            if not kutu:
                continue
            x1, y1, x2, y2 = kutu
            if x1 < -1 or y1 < -1 or x2 > p.G + 1 or y2 > p.Y + 1:
                hatalar.append(
                    "[%s] YAZI TAŞIYOR: %r (%d,%d)-(%d,%d), pencere %dx%d"
                    % (etiket, (p.t.itemcget(oge, "text") or "")[:40],
                       x1, y1, x2, y2, p.G, p.Y))

        # 5) Şerit metni ilk açılışta dolu mu
        metin = (p.t.itemcget(p.arka_serit, "text") or "").strip()
        if not metin:
            hatalar.append("[%s] arka plan şeridi BOŞ — ilk açılışta metin yok"
                           % etiket)

        # 6) Şeridin yazısı kendi kutusunun içinde mi
        serit = next((k for k in kutular if k[0] == "arka plan şeridi"), None)
        if serit and metin:
            sx1, sy1, sx2, sy2 = serit[1], serit[2], serit[3], serit[4]
            for oge in (p.arka_serit, p.arka_serit_alt):
                kutu = p.t.bbox(oge)
                if not kutu:
                    continue
                if kutu[1] < sy1 or kutu[3] > sy2 or kutu[2] > sx2:
                    hatalar.append(
                        "[%s] ŞERİT YAZISI KUTUNUN DIŞINDA: %s, kutu (%d-%d)"
                        % (etiket, kutu, sy1, sy2))
    finally:
        p.kapat()


def pencere_sigiyor_mu(hatalar):
    """Pencere BU ekranın çalışma alanına sığıyor mu?

    goz_molasi.py'nin yaptığı hesabın aynısı. Eskiden "ekran yüksekliği
    - 80" deniyordu ve 1920x1200 / %125 bir makinede pencere 3 piksel
    taşıyordu: alttaki 'Programı kapat' düğmesi görev çubuğunun altında
    kalıyor, tıklanamıyordu."""
    import izleyici as iz
    iz.dpi_farkindaligi_ac()
    _, _, kul_g, kul_y = iz.calisma_alani()
    baslik, kenar = iz.pencere_cercevesi()

    o = iz.olcek()
    ic_y = kul_y - baslik - 2 * kenar
    ic_g = kul_g - 2 * kenar
    o = max(0.62, min(o, ic_y / float(TASARIM_Y), ic_g / float(TASARIM_G)))

    tam_y = int(round(TASARIM_Y * o)) + baslik + 2 * kenar
    tam_g = int(round(TASARIM_G * o)) + 2 * kenar
    if tam_y > kul_y or tam_g > kul_g:
        hatalar.append(
            "PENCERE EKRANA SIĞMIYOR: %dx%d isteniyor, çalışma alanı %dx%d "
            "(ölçek %.4f)" % (tam_g, tam_y, kul_g, kul_y, o))
    else:
        print("Pencere: %dx%d, çalışma alanı %dx%d, ölçek %.4f — sığıyor"
              % (tam_g, tam_y, kul_g, kul_y, o))


def uyarilar_sigiyor_mu(hatalar):
    """Aile kipi uyarilari ipucu satirina SIGIYOR mu?

    NEDEN VAR — 27.08.2026'da olculdu:
      Aile kipi uyarilari `ipucu_yazi` tuval metnini eziyor. O metinde
      `width=` YOK (satir kirilmaz) ve anchor="e" (saga yasli), yani
      uzun metin panelin SOL kenarindan tasiyor.

      Sekiz uyaridan UCU tasiyordu; en genisi 704 px, alan 540 px.
      Normal ipucu metni 93-128 px, yani uyarilar 5-7 kati.

      Bu sinamanin kendisi de bir kor noktaydi: yerlesim sinamasi
      paneli varsayilan halinde olcuyordu, uyari durumunu HIC
      kurmuyordu. Gorunmeyen durum, denetlenmemis durumdur.

      Kirpilan uyari, hic olmayan uyaridir. Ustelik bu metinler
      "koruma uygulanmiyor" diyen metinler - ebeveynin gormesi
      gereken tek sey.
    """
    import ast
    import tkinter as tk

    TASARIM_G = 580
    SAG_PAY = 40                    # G - kenar - o(22), en genis hâli
    KULLANILABILIR = TASARIM_G - SAG_PAY

    kaynak = io.open(
        os.path.join(BURASI, "goz_molasi.py"), encoding="utf-8").read()
    uyarilar = []
    for d in ast.walk(ast.parse(kaynak)):
        if isinstance(d, ast.FunctionDef) and d.name == "ayar_uyarisi":
            for alt in ast.walk(d):
                if isinstance(alt, ast.Return) and alt.value is not None:
                    try:
                        deger = ast.literal_eval(alt.value)
                    except Exception:
                        continue
                    if isinstance(deger, str) and deger.strip():
                        uyarilar.append(deger)

    if not uyarilar:
        hatalar.append("ayar_uyarisi icinde hic uyari metni bulunamadi "
                       "- denetim bos gecmis olabilir")
        return

    kok = tk.Tk()
    kok.withdraw()
    t = tk.Canvas(kok, width=TASARIM_G, height=200)
    kok.update_idletasks()
    for u in uyarilar:
        oge = t.create_text(0, 0, anchor="w", text=u, font=("Segoe UI", 9))
        x1, _, x2, _ = t.bbox(oge)
        t.delete(oge)
        if x2 - x1 > KULLANILABILIR:
            hatalar.append(
                "uyari %d px, sigmasi gereken %d px: %r"
                % (x2 - x1, KULLANILABILIR, u[:44]))
    kok.destroy()
    print("Uyari metni: %d tanesi olculdu (sinir %d px)"
          % (len(uyarilar), KULLANILABILIR))


def main():
    hatalar = []
    pencere_sigiyor_mu(hatalar)
    uyarilar_sigiyor_mu(hatalar)
    # Her tema ayrı denenir: renk değil YERLEŞİM aynı olmalı, ama
    # tema değişince panel baştan çiziliyor — o yol da sınansın.
    temalar = list(gor.TEMALAR.keys())
    # Ölçekler: en küçük (küçük ekran), normal, büyük (%150 Windows)
    olcekler = (0.62, 1.0, 1.5)

    for olcek in olcekler:
        for tema in temalar:
            denetle(tema, olcek, hatalar)

    toplam = len(temalar) * len(olcekler)
    print("Denenen: %d durum (%d tema x %d ölçek)"
          % (toplam, len(temalar), len(olcekler)))
    if hatalar:
        print("\nBAŞARISIZ — %d sorun:" % len(hatalar))
        for h in hatalar:
            print("  -", h)
        return 1
    print("TAMAM — çakışma yok, taşma yok, şerit dolu.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
