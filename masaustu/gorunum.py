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


def tema_uygula(ad):
    """Temayı değiştir. Sözlükleri YERİNDE günceller ki
    `P = gorunum.PANEL` diye tutulan referanslar bozulmasın."""
    global MOLA_YAZI, MOLA_SOLUK, KEHRIBAR, NANE, HALKA_IZ
    t = TEMALAR.get(ad) or TEMALAR[VARSAYILAN_TEMA]

    PANEL.clear()
    PANEL.update(t["panel"])

    MOLA_GRADYAN[:] = t["mola"]
    GRAFIK_RENKLERI[:] = t["grafik"]

    MOLA_YAZI = t["mola_yazi"]
    MOLA_SOLUK = t["mola_soluk"]
    KEHRIBAR = t["mola_halka"]
    NANE = t["mola_parilti"]
    HALKA_IZ = karistir(t["mola"][2], "#ffffff", 0.12)
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
        r = yaricap * oran
        c = karistir(zemin_renk, renk, (1 - oran) ** 2 * guc)
        tuval.create_oval(x - r, y - r, x + r, y + r,
                          fill=c, outline="", tags=etiket)


# Açılışta varsayılan temayı yükle
tema_uygula(VARSAYILAN_TEMA)
