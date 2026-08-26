# -*- coding: utf-8 -*-
"""
GÖRÜNÜM — Temalar, renkler ve çizim yardımcıları.

Tkinter'da CSS gibi gradyan yok. Burada gradyanı elle çiziyoruz:
tuvale yüzlerce ince yatay çizgi atıp renkleri arada yumuşatıyoruz.
Bir kez çizilir, sonra durur — performans sorunu olmaz.

TEMA MANTIĞI
------------
`PANEL` ve `MOLA_GRADYAN` sözlük/listeleri program boyunca aynı nesne
olarak kalır; tema değişince İÇERİKLERİ değiştirilir (yerinde güncelleme).
Böylece `P = gor.PANEL` diye referans tutan kodlar bozulmaz.

RENK SEÇİMİ
-----------
Mola ekranı her temada KOYU kalır. Amaç gözü dinlendirmek; parlak bir
ekran tam tersini yapar. Açık tema seçilse bile mola ekranı koyu gökyüzü
tonlarında kalır — sadece rengi temaya uyar.
"""

# ============================================================
# CANLILIK — renklerin doygunluğunu, açıklığa dokunmadan değiştirir
#
# Neden OKLab? Bu renk uzayında L "algılanan açıklık", C ise
# doygunluk. Yalnızca C'yi çarpınca renk canlanır ya da soluklaşır
# ama yazı/zemin kontrastı yerinde kalır. HSV'de doygunluk artırmak
# algılanan açıklığı da kaydırıyor ve okunaklılık bozuluyordu.
# Web sürümü aynı işi CSS'in oklch() işleviyle yapıyor.
# Kaynak: Björn Ottosson, "A perceptual color space for image
# processing" (2020) — OKLab dönüşüm katsayıları.
# ============================================================

def _cozgu(deger):
    """sRGB kanalı (0..1) -> doğrusal ışık"""
    return deger / 12.92 if deger <= 0.04045 else ((deger + 0.055) / 1.055) ** 2.4


def _sikistir(deger):
    """Doğrusal ışık -> sRGB kanalı (0..1)"""
    return deger * 12.92 if deger <= 0.0031308 else 1.055 * (deger ** (1 / 2.4)) - 0.055


def _oklab(r, g, b):
    r, g, b = _cozgu(r), _cozgu(g), _cozgu(b)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    t = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, t = l ** (1 / 3) if l > 0 else 0, m ** (1 / 3) if m > 0 else 0, t ** (1 / 3) if t > 0 else 0
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * t,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * t,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * t)


def _dogrusal_rgb(L, A, B):
    l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3
    m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3
    t = (L - 0.0894841775 * A - 1.2914855480 * B) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * t,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * t,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * t)


def _sigiyor_mu(L, A, B):
    """Renk sRGB'nin içinde mi?"""
    return all(-0.0001 <= k <= 1.0001 for k in _dogrusal_rgb(L, A, B))


def _oklab_ters(L, A, B):
    return tuple(min(1.0, max(0.0, _sikistir(min(1.0, max(0.0, k)))))
                 for k in _dogrusal_rgb(L, A, B))


def canlilik_uygula(renk, carpan):
    """Rengin doygunluğunu çarpanla ölçekle, açıklığını koru."""
    if carpan == 1.0:
        return renk
    h = renk.lstrip("#")
    if len(h) != 6:
        return renk
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    L, A, B = _oklab(r, g, b)
    A, B = A * carpan, B * carpan

    # sRGB dışına taştıysa KANALLARI KIRPMA — açıklık kayar ve
    # canlılığın bütün amacı bozulur. Bunun yerine doygunluğu
    # sığana kadar geri çek; açıklık ve renk tonu aynı kalır.
    # (CSS Color 4'ün gamut eşleme yaklaşımının basit hâli.)
    if not _sigiyor_mu(L, A, B):
        alt, ust = 0.0, 1.0
        for _ in range(24):
            orta = (alt + ust) / 2
            if _sigiyor_mu(L, A * orta, B * orta):
                alt = orta
            else:
                ust = orta
        A, B = A * alt, B * alt

    r, g, b = _oklab_ters(L, A, B)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


TEMALAR = {
    "gece": {
        "ad": "Gece moru",
        "panel": {
            "zemin": "#141130", "zemin2": "#1c1840",
            "kart": "#241f4d", "kart2": "#2c2659", "cizgi": "#3a3268",
            "yazi": "#f2ecff", "soluk": "#a99bd0",
            "vurgu": "#7ee0d2", "sicak": "#ffc46b", "uyari": "#ff9f6b",
            "ana_yazi": "#0d2b28",
        },
        "mola": ["#0c1533", "#1b1a46", "#2f2154", "#4a2a56", "#6b3350"],
        "mola_yazi": "#fdf3ff", "mola_soluk": "#c3a8d8",
        "mola_halka": "#ffc46b", "mola_parilti": "#7ee0d2",
        "grafik": ["#7ee0d2", "#ffc46b", "#c39bff", "#ff8f7a", "#8fd3ff"],
    },
    "dinginlik": {
        "ad": "Dinginlik",
        "panel": {
            "zemin": "#102830", "zemin2": "#16353f", "kart": "#1c4149",
            "kart2": "#234e57", "cizgi": "#2f646c",
            "yazi": "#e8f2ef", "soluk": "#9fbfba",
            "vurgu": "#8fd8c8", "sicak": "#f0cfa0", "uyari": "#e8a38f",
            "ana_yazi": "#06231f",
        },
        "mola": ["#081a20", "#0f2b33", "#174049", "#21575e", "#2f6f70"],
        "mola_yazi": "#eef7f4", "mola_soluk": "#a8c9c4",
        "mola_halka": "#f0cfa0", "mola_parilti": "#8fd8c8",
        "grafik": ["#8fd8c8", "#f0cfa0", "#9cc8d8", "#e8a38f", "#b5d4a8"],
    },
    "okyanus": {
        "ad": "Okyanus",
        "panel": {
            "zemin": "#0a1826", "zemin2": "#102538",
            "kart": "#16304a", "kart2": "#1d3d5c", "cizgi": "#28527a",
            "yazi": "#e9f4ff", "soluk": "#93b6d4",
            "vurgu": "#5fd3e8", "sicak": "#ffb877", "uyari": "#ff9b7a",
            "ana_yazi": "#062330",
        },
        "mola": ["#04121f", "#0a2338", "#123a52", "#1b5266", "#2d6b6e"],
        "mola_yazi": "#eaf7ff", "mola_soluk": "#9dc6dd",
        "mola_halka": "#ffb877", "mola_parilti": "#5fd3e8",
        "grafik": ["#5fd3e8", "#ffb877", "#8fb4ff", "#7ae0b0", "#ff9b7a"],
    },
    "orman": {
        "ad": "Orman",
        "panel": {
            "zemin": "#0f1c17", "zemin2": "#152a22",
            "kart": "#1b382c", "kart2": "#224638", "cizgi": "#2f5c48",
            "yazi": "#ecf7f0", "soluk": "#9ec4ae",
            "vurgu": "#8fe08a", "sicak": "#ffd27a", "uyari": "#ffab6b",
            "ana_yazi": "#0a2312",
        },
        "mola": ["#08150f", "#0e251a", "#163a27", "#245139", "#40643a"],
        "mola_yazi": "#f0fbf2", "mola_soluk": "#a8ceb6",
        "mola_halka": "#ffd27a", "mola_parilti": "#8fe08a",
        "grafik": ["#8fe08a", "#ffd27a", "#7fd8c0", "#c9e07a", "#ffab6b"],
    },
    "safak": {
        "ad": "Şafak",
        "panel": {
            "zemin": "#1d1220", "zemin2": "#2a1729",
            "kart": "#361d33", "kart2": "#43253d", "cizgi": "#5a3450",
            "yazi": "#ffeef4", "soluk": "#d3a4bb",
            "vurgu": "#ff9eb5", "sicak": "#ffd08a", "uyari": "#ffb07a",
            "ana_yazi": "#3a0d1e",
        },
        "mola": ["#150a16", "#2a1226", "#472034", "#6b3140", "#8f4a44"],
        "mola_yazi": "#fff2f6", "mola_soluk": "#dbb0c2",
        "mola_halka": "#ffd08a", "mola_parilti": "#ff9eb5",
        "grafik": ["#ff9eb5", "#ffd08a", "#c9a0ff", "#ffab8f", "#8fd3ff"],
    },
    "gunbatimi": {
        "ad": "Gün batımı",
        "panel": {
            "zemin": "#231318", "zemin2": "#31191c",
            "kart": "#3d2124", "kart2": "#4b292a", "cizgi": "#653a37",
            "yazi": "#fff0ea", "soluk": "#d5a89b",
            "vurgu": "#ffb08a", "sicak": "#ffd68a", "uyari": "#ff9a76",
            "ana_yazi": "#3a1508",
        },
        "mola": ["#190b10", "#30141a", "#542323", "#7d3a2c", "#a55a36"],
        "mola_yazi": "#fff4ec", "mola_soluk": "#dcb1a0",
        "mola_halka": "#ffd68a", "mola_parilti": "#ffb08a",
        "grafik": ["#ffb08a", "#ffd68a", "#e79bb5", "#ff8f6b", "#c9a6ff"],
    },
    "buz": {
        "ad": "Buz",
        "panel": {
            "zemin": "#0d1620", "zemin2": "#13212e", "kart": "#1a2c3d",
            "kart2": "#22384c", "cizgi": "#2f4d68",
            "yazi": "#eaf4fb", "soluk": "#9db8cc",
            "vurgu": "#a8dcf0", "sicak": "#ffd9a0", "uyari": "#ffb38a",
            "ana_yazi": "#08202c",
        },
        "mola": ["#060e16", "#0d1c28", "#16303f", "#204558", "#365e6f"],
        "mola_yazi": "#f0f9ff", "mola_soluk": "#a9c6d8",
        "mola_halka": "#ffd9a0", "mola_parilti": "#a8dcf0",
        "grafik": ["#a8dcf0", "#ffd9a0", "#b9b3f0", "#8fd8c4", "#ffb38a"],
    },
    "lavanta": {
        "ad": "Lavanta",
        "panel": {
            "zemin": "#181530", "zemin2": "#211c42", "kart": "#2b2454",
            "kart2": "#352c66", "cizgi": "#463b80",
            "yazi": "#f0ecff", "soluk": "#b0a4dc",
            "vurgu": "#c0a9ff", "sicak": "#ffd28f", "uyari": "#ffa8c4",
            "ana_yazi": "#1b0d3d",
        },
        "mola": ["#0f0c22", "#1b1640", "#2d245e", "#443577", "#61478a"],
        "mola_yazi": "#f6f2ff", "mola_soluk": "#bfb0e4",
        "mola_halka": "#ffd28f", "mola_parilti": "#c0a9ff",
        "grafik": ["#c0a9ff", "#ffd28f", "#8fd8f0", "#ffa8c4", "#9ee8b8"],
    },
    "komur": {
        "ad": "Kömür (renksiz)",
        "panel": {
            "zemin": "#141416", "zemin2": "#1c1c1f", "kart": "#242427",
            "kart2": "#2e2e32", "cizgi": "#3d3d42",
            "yazi": "#f0f0f2", "soluk": "#a5a5ad",
            "vurgu": "#d8d8de", "sicak": "#c8b48a", "uyari": "#c99a80",
            "ana_yazi": "#151517",
        },
        "mola": ["#0a0a0b", "#161618", "#232326", "#323236", "#434349"],
        "mola_yazi": "#f4f4f6", "mola_soluk": "#adadb5",
        "mola_halka": "#c8b48a", "mola_parilti": "#d8d8de",
        "grafik": ["#d8d8de", "#c8b48a", "#a9b3c4", "#c99a80", "#93a08c"],
    },
    "kiraz": {
        "ad": "Kiraz",
        "panel": {
            "zemin": "#1a0f14", "zemin2": "#26151b", "kart": "#331b22",
            "kart2": "#40232a", "cizgi": "#57323a",
            "yazi": "#ffeef1", "soluk": "#d0a3ac",
            "vurgu": "#ff9aa8", "sicak": "#ffcf8a", "uyari": "#ff8f80",
            "ana_yazi": "#3d0d18",
        },
        "mola": ["#120810", "#241019", "#401b26", "#612635", "#8a3a44"],
        "mola_yazi": "#fff0f3", "mola_soluk": "#d9adb8",
        "mola_halka": "#ffcf8a", "mola_parilti": "#ff9aa8",
        "grafik": ["#ff9aa8", "#ffcf8a", "#f0a8d0", "#ff8f80", "#d8b0e8"],
    },
    "bakir": {
        "ad": "Bakır",
        "panel": {
            "zemin": "#191512", "zemin2": "#221d18", "kart": "#2c251e",
            "kart2": "#372e26", "cizgi": "#4b3f33",
            "yazi": "#f8f2e9", "soluk": "#bfae97",
            "vurgu": "#e8b478", "sicak": "#f5d49a", "uyari": "#e09a75",
            "ana_yazi": "#2a1a0a",
        },
        "mola": ["#0f0c09", "#1b1611", "#2b231a", "#3e3123", "#56422c"],
        "mola_yazi": "#fbf5ec", "mola_soluk": "#c4b39c",
        "mola_halka": "#f5d49a", "mola_parilti": "#e8b478",
        "grafik": ["#e8b478", "#f5d49a", "#c8b89a", "#e09a75", "#b0c095"],
    },
    "beyaz": {
        "ad": "Beyaz",
        "panel": {
            "zemin": "#ffffff", "zemin2": "#f4f6f7", "kart": "#ffffff",
            "kart2": "#f2f5f6", "cizgi": "#dfe5e6",
            "yazi": "#16232a", "soluk": "#5a6b72",
            "vurgu": "#0f8c78", "sicak": "#9a6410", "uyari": "#b8503a",
            # Beyaz yazı bu vurguda 4.16 veriyordu (eşik 4.5); koyu yazı 5.05.
            "ana_yazi": "#00120e",
        },
        "mola": ["#081a20", "#0f2b33", "#174049", "#21575e", "#2f6f70"],
        "mola_yazi": "#eef7f4", "mola_soluk": "#a8c9c4",
        "mola_halka": "#f0cfa0", "mola_parilti": "#8fd8c8",
        "grafik": ["#0f8c78", "#9a6410", "#1668a8", "#b8503a", "#436b20"],
    },
    "gokyuzu": {
        "ad": "Gökyüzü",
        "panel": {
            "zemin": "#f6faff", "zemin2": "#eaf2fb", "kart": "#ffffff",
            "kart2": "#eff5fd", "cizgi": "#d8e4f2",
            "yazi": "#17222f", "soluk": "#566577",
            "vurgu": "#1668a8", "sicak": "#96590d", "uyari": "#b04a49",
            "ana_yazi": "#ffffff",
        },
        "mola": ["#071019", "#0d1e2e", "#163047", "#204561", "#2f5d78"],
        "mola_yazi": "#eff6fd", "mola_soluk": "#a6c0d8",
        "mola_halka": "#f0cfa0", "mola_parilti": "#8fc4e8",
        "grafik": ["#1668a8", "#96590d", "#0f8c78", "#b04a49", "#6a5aa8"],
    },
    "kum": {
        "ad": "Kum",
        "panel": {
            "zemin": "#fbf7f0", "zemin2": "#f4ede1", "kart": "#ffffff",
            "kart2": "#f7f1e7", "cizgi": "#e5dccb",
            "yazi": "#2b2419", "soluk": "#6d6151",
            "vurgu": "#8f5d0c", "sicak": "#8a5a1c", "uyari": "#b05436",
            "ana_yazi": "#ffffff",
        },
        "mola": ["#100c07", "#1d160e", "#2f2317", "#453221", "#5e442b"],
        "mola_yazi": "#fbf5ec", "mola_soluk": "#c8b69c",
        "mola_halka": "#f0cfa0", "mola_parilti": "#d8b078",
        "grafik": ["#8f5d0c", "#b05436", "#4c7a26", "#1668a8", "#7a5a8a"],
    },
    "zeytin": {
        "ad": "Zeytin",
        "panel": {
            "zemin": "#f7f8f1", "zemin2": "#edf0e3", "kart": "#ffffff",
            "kart2": "#f2f5ea", "cizgi": "#dde2ce",
            "yazi": "#1f2718", "soluk": "#5c6650",
            "vurgu": "#436b20", "sicak": "#8d6410", "uyari": "#a85a34",
            "ana_yazi": "#ffffff",
        },
        "mola": ["#0b1109", "#151f11", "#23331b", "#344828", "#4a5f34"],
        "mola_yazi": "#f2f7ee", "mola_soluk": "#b3c4a6",
        "mola_halka": "#f0cfa0", "mola_parilti": "#9ec87a",
        "grafik": ["#436b20", "#8d6410", "#1668a8", "#a85a34", "#6a5aa8"],
    },
    "acik": {
        "ad": "Açık (gündüz)",
        "panel": {
            "zemin": "#eef2fa", "zemin2": "#e3eaf6",
            "kart": "#ffffff", "kart2": "#f0f4fb", "cizgi": "#d3ddec",
            "yazi": "#1a2338", "soluk": "#5f6c88",
            # Açık zeminde vurgu rengi koyu olmalı: #0f9b8a beyaz kartta
            # sadece 3.46 kontrast veriyordu (yazı için sınır 4.5).
            "vurgu": "#0a6d62", "sicak": "#8f540c", "uyari": "#a8451a",
            "ana_yazi": "#ffffff",
        },
        # Açık temada bile mola ekranı koyu: göz dinlenecek
        "mola": ["#101a33", "#1d2a4d", "#2f3d63", "#455073", "#5c6482"],
        "mola_yazi": "#f4f8ff", "mola_soluk": "#b9c6e0",
        "mola_halka": "#ffc46b", "mola_parilti": "#7ee0d2",
        "grafik": ["#0a6d62", "#8f540c", "#5346a8", "#a8451a", "#1f6693"],
    },
}

VARSAYILAN_TEMA = "gece"

# --- Program boyunca aynı kalan nesneler (tema değişince içerikleri değişir) ---
PANEL = {}
MOLA_GRADYAN = []
GRAFIK_RENKLERI = []

MOLA_YAZI = ""
MOLA_SOLUK = ""
KEHRIBAR = ""
NANE = ""
HALKA_IZ = ""


# Canlılık YALNIZCA vurgu renklerine uygulanır. Zemin, kart ve yazı
# renkleri dokunulmaz kalır: onları oynatmak okunaklılığı bozar.
_CANLI_ALANLAR = ("vurgu", "sicak", "uyari")


def tema_uygula(ad, canlilik=1.0):
    """Temayı değiştir. Sözlükleri YERİNDE günceller ki
    `P = gorunum.PANEL` diye tutulan referanslar bozulmasın.

    canlilik: 1.0 temanın kendi renkleri. 0.6 daha sakin,
    1.5 daha canlı. Açıklık değişmez, sadece doygunluk."""
    global MOLA_YAZI, MOLA_SOLUK, KEHRIBAR, NANE, HALKA_IZ
    t = TEMALAR.get(ad) or TEMALAR[VARSAYILAN_TEMA]
    c = max(0.6, min(1.5, float(canlilik or 1.0)))

    PANEL.clear()
    PANEL.update(t["panel"])
    for alan in _CANLI_ALANLAR:
        if alan in PANEL:
            PANEL[alan] = canlilik_uygula(PANEL[alan], c)

    # Mola ekranı 20 saniye tam ekran duruyor; en canlı ayarda bile
    # gözü yormasın diye gradyanda çarpanı kısıyoruz (web ile aynı).
    mola_c = 1 + (c - 1) * 0.6
    MOLA_GRADYAN[:] = [canlilik_uygula(r, mola_c) for r in t["mola"]]
    GRAFIK_RENKLERI[:] = [canlilik_uygula(r, c) for r in t["grafik"]]

    MOLA_YAZI = t["mola_yazi"]
    MOLA_SOLUK = t["mola_soluk"]
    KEHRIBAR = canlilik_uygula(t["mola_halka"], c)
    NANE = canlilik_uygula(t["mola_parilti"], c)
    HALKA_IZ = karistir(MOLA_GRADYAN[2], "#ffffff", 0.12)
    return t


def tema_listesi():
    return [(a, t["ad"]) for a, t in TEMALAR.items()]


# ----------------------------------------------------------------------
# Renk yardımcıları
# ----------------------------------------------------------------------
def _onalti(renk):
    renk = renk.lstrip("#")
    return tuple(int(renk[i:i + 2], 16) for i in (0, 2, 4))


def _metin(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(k))) for k in rgb)


def karistir(renk1, renk2, oran):
    """İki rengi oran kadar karıştır. oran=0 -> renk1, oran=1 -> renk2."""
    a, b = _onalti(renk1), _onalti(renk2)
    return _metin([a[i] + (b[i] - a[i]) * oran for i in range(3)])


def parlaklik_degeri(renk):
    """0 (siyah) .. 1 (beyaz). Açık tema mı koyu tema mı anlamak için."""
    r, g, b = _onalti(renk)
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0


def acik_tema_mi():
    return parlaklik_degeri(PANEL.get("zemin", "#000000")) > 0.5


# ----------------------------------------------------------------------
# Çizim
# ----------------------------------------------------------------------
def gradyan_ciz(tuval, genislik, yukseklik, duraklar, etiket="gradyan"):
    """Tuvale yukarıdan aşağıya gradyan çizer."""
    if yukseklik <= 0:
        return
    bolum = len(duraklar) - 1
    for y in range(yukseklik):
        konum = (y / max(1, yukseklik - 1)) * bolum
        i = min(int(konum), bolum - 1)
        renk = karistir(duraklar[i], duraklar[i + 1], konum - i)
        tuval.create_line(0, y, genislik, y, fill=renk, tags=etiket)


def gradyan_rengi(duraklar, oran):
    """Gradyanın belli bir yerindeki rengi hesapla (0..1)."""
    bolum = len(duraklar) - 1
    konum = max(0.0, min(1.0, oran)) * bolum
    i = min(int(konum), bolum - 1)
    return karistir(duraklar[i], duraklar[i + 1], konum - i)


def parilti_ciz(tuval, x, y, yaricap, renk, zemin_renk, katman=22,
                etiket="parilti", guc=0.55):
    """Sahte radyal parıltı: içten dışa doğru zemine karışan halkalar.

    Tkinter'da saydamlık yok; her halkayı zemin rengiyle biraz daha
    karıştırarak yumuşak bir ışık hissi veriyoruz.
    """
    for i in range(katman, 0, -1):
        oran = i / katman
        k = (1 - oran) ** 2 * guc
        # En dıştaki halkalarda karışım oranı sıfıra düşüyor ve MERKEZİN
        # zemin rengiyle düz bir daire boyanıyor. Arkadaki asıl zemin bir
        # gradyan olduğu için o daire kenarı belli bir leke bırakıyordu —
        # yumuşak ışıma değil, sınırı görünen koyu bir daire. Katkısı
        # görünmeyecek kadar az olan halkaları hiç çizmiyoruz.
        if k < 0.03:
            continue
        r = yaricap * oran
        tuval.create_oval(x - r, y - r, x + r, y + r,
                          fill=karistir(zemin_renk, renk, k),
                          outline="", tags=etiket)


# Açılışta varsayılan temayı yükle
tema_uygula(VARSAYILAN_TEMA)
