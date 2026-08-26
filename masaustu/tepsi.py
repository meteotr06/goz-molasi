# -*- coding: utf-8 -*-
"""
TEPSİ — Saatin yanındaki simge ve sağ tık menüsü.

Arka planda çalışan bir program için doğru yer görev çubuğu değil,
saatin yanı. Pencere tamamen gizlenir; program buradan yönetilir.

pystray kendi döngüsünü ayrı bir iş parçacığında çalıştırır. Tkinter
başka bir iş parçacığından çağrılamaz; bu yüzden menüden gelen her
komut `kok.after(0, ...)` ile ana iş parçacığına aktarılıyor.
"""

import threading

try:
    import pystray
    from PIL import Image, ImageDraw
    KULLANILABILIR = True
except Exception:
    KULLANILABILIR = False


def _simge_ciz(boyut=64, zemin="#141130", halka="#7ee0d2", ic="#0f766e"):
    """Simgeyi çiz — ikon.ico bulunamazsa yedek olarak kullanılır."""
    resim = Image.new("RGBA", (boyut, boyut), (0, 0, 0, 0))
    ciz = ImageDraw.Draw(resim)
    p = boyut * 0.06
    ciz.ellipse([p, p, boyut - p, boyut - p], fill=zemin)
    k = boyut * 0.13
    ciz.ellipse([k, k, boyut - k, boyut - k], outline=halka, width=int(boyut * 0.09))
    g = boyut * 0.30
    ciz.ellipse([g, g, boyut - g, boyut - g], fill=ic)
    return resim


class Tepsi:
    def __init__(self, uygulama, ikon_yolu=None):
        self.uyg = uygulama
        self.simge = None
        self.acik = False

        if not KULLANILABILIR:
            return

        resim = None
        if ikon_yolu:
            try:
                resim = Image.open(ikon_yolu)
                resim.load()
                resim = resim.convert("RGBA")
            except Exception:
                resim = None
        if resim is None:
            resim = _simge_ciz()

        self.simge = pystray.Icon("goz_molasi", resim, "Göz Molası",
                                  menu=self._menu())

    # ---------------- Menü ----------------
    def _menu(self):
        A = pystray.MenuItem
        return pystray.Menu(
            A("Göster", self._goster, default=True),
            A("Şimdi mola ver", self._mola),
            pystray.Menu.SEPARATOR,
            A("Duraklat", pystray.Menu(
                A("30 dakika", lambda: self._duraklat(30)),
                A("1 saat", lambda: self._duraklat(60)),
                A("2 saat", lambda: self._duraklat(120)),
            ), visible=lambda e: not self.uyg.duraklatildi_mi()),
            A("Devam et", self._devam, visible=lambda e: self.uyg.duraklatildi_mi()),
            # Sessiz ölçüm: program açık kalır, ölçmeye devam eder,
            # ama mola vermez ve ekrana hiçbir şey çıkarmaz.
            A("Sadece ölç (mola verme)", self._sadece_olc,
              checked=lambda e: bool(self.uyg.ayar.get("sadece_olc"))),
            pystray.Menu.SEPARATOR,
            A("Ayarlar", self._ayarlar),
            A("Çıkış", self._cikis),
        )

    # Menüden gelen her şey ana iş parçacığına aktarılır
    def _ana(self, fn):
        try:
            self.uyg.kok.after(0, fn)
        except Exception:
            pass

    def _goster(self, *a):
        self._ana(self.uyg.pencereyi_goster)

    def _mola(self, *a):
        self._ana(self.uyg.hemen_mola)

    def _duraklat(self, dakika):
        self._ana(lambda: self.uyg.duraklat(dakika))

    def _devam(self, *a):
        self._ana(self.uyg.devam_et)

    def _sadece_olc(self, *a):
        self._ana(self.uyg.sadece_olc_degistir)

    def _ayarlar(self, *a):
        self._ana(self.uyg.ayarlari_ac)

    def _cikis(self, *a):
        self._ana(self.uyg.cik)

    # ---------------- Kontrol ----------------
    def baslat(self):
        if not self.simge:
            return False
        threading.Thread(target=self.simge.run, daemon=True).start()
        self.acik = True
        return True

    def ipucu_yaz(self, metin):
        if self.simge:
            try:
                self.simge.title = metin
            except Exception:
                pass

    def menuyu_tazele(self):
        if self.simge:
            try:
                self.simge.update_menu()
            except Exception:
                pass

    def durdur(self):
        if self.simge:
            try:
                self.simge.stop()
            except Exception:
                pass
        self.acik = False
