# -*- coding: utf-8 -*-
"""
İZLEYİCİ — Windows'a soru soran katman.

Burada tkinter yok, arayüz yok. Sadece işletim sistemine
"kullanıcı kaç saniyedir boşta?", "önde hangi program var?",
"bu program tam ekran mı?" diye soran fonksiyonlar var.

Hepsi ctypes ile standart Windows API çağrısı — ek kurulum gerekmez.
"""

import ctypes
import ctypes.wintypes as wt
import os

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# ---------------------------------------------------------------------
# ÖNEMLİ: Dönüş tiplerini açıkça bildiriyoruz.
# ctypes, bildirmezsek her fonksiyonun 32 bitlik int döndürdüğünü varsayar.
# GetAsyncKeyState aslında 16 bitlik SHORT döndürür; üst 16 bit çöp kalır
# ve "& 0x8000" testi rastgele True çıkabilir. Bu, acil çıkış kısayolunun
# kimse basmadan tetiklenmesine ve molaların sessizce iptal olmasına
# yol açıyordu.
# ---------------------------------------------------------------------
user32.GetAsyncKeyState.restype = ctypes.c_short
user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetForegroundWindow.restype = wt.HWND
user32.GetSystemMetrics.restype = ctypes.c_int
user32.GetSystemMetrics.argtypes = [ctypes.c_int]
user32.GetWindowTextLengthW.restype = ctypes.c_int
kernel32.GetTickCount.restype = wt.DWORD


def dpi_farkindaligi_ac():
    """Windows'a 'ben ölçeklemeyi kendim hallederim' de.

    Bunu demezsek: ekran %125 ölçekteyse Windows programı bulanık şekilde
    büyütür, pencere içeriği taşar ve GetSystemMetrics gerçek piksel yerine
    küçültülmüş değer döndürür (1920x1200 ekran 1536x960 görünür).
    Mola ekranının tüm ekranı kaplaması için gerçek piksel şart.
    """
    try:
        # 2 = PROCESS_PER_MONITOR_DPI_AWARE (Windows 8.1+)
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
        return True
    except Exception:
        try:
            user32.SetProcessDPIAware()
            return True
        except Exception:
            return False


def olcek():
    """Ekranın büyütme oranı: %100 -> 1.0, %125 -> 1.25, %150 -> 1.5"""
    try:
        ekran = user32.GetDC(0)
        LOGPIXELSX = 88
        dpi = ctypes.windll.gdi32.GetDeviceCaps(ekran, LOGPIXELSX)
        user32.ReleaseDC(0, ekran)
        return max(1.0, dpi / 96.0)
    except Exception:
        return 1.0

# Sanal ekran ölçüleri (tüm monitörleri kapsayan dikdörtgen)
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79


class _SonGirdi(ctypes.Structure):
    _fields_ = [("cbSize", wt.UINT), ("dwTime", wt.DWORD)]


def bosta_saniye():
    """Kullanıcı kaç saniyedir klavye/fareye dokunmadı?

    Bu, tarayıcı sürümünden çok daha güvenilir: sadece bu pencerede değil,
    TÜM bilgisayarda hareket olup olmadığını bilir.
    """
    bilgi = _SonGirdi()
    bilgi.cbSize = ctypes.sizeof(_SonGirdi)
    if not user32.GetLastInputInfo(ctypes.byref(bilgi)):
        return 0.0
    return (kernel32.GetTickCount() - bilgi.dwTime) / 1000.0


def sanal_ekran():
    """(sol, ust, genislik, yukseklik) — bütün monitörleri kapsayan alan."""
    return (
        user32.GetSystemMetrics(SM_XVIRTUALSCREEN),
        user32.GetSystemMetrics(SM_YVIRTUALSCREEN),
        user32.GetSystemMetrics(SM_CXVIRTUALSCREEN),
        user32.GetSystemMetrics(SM_CYVIRTUALSCREEN),
    )


def on_pencere():
    """Önde duran pencerenin (baslik, program_adi) bilgisi.

    Örn: ("Belge1 - Word", "WINWORD.EXE")
    Bulunamazsa ("", "").
    """
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return ("", "")

    uzunluk = user32.GetWindowTextLengthW(hwnd)
    tampon = ctypes.create_unicode_buffer(uzunluk + 1)
    user32.GetWindowTextW(hwnd, tampon, uzunluk + 1)
    baslik = tampon.value or ""

    pid = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    program = ""
    if pid.value:
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        tutamac = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
        if tutamac:
            try:
                boy = wt.DWORD(260)
                yol = ctypes.create_unicode_buffer(boy.value)
                if kernel32.QueryFullProcessImageNameW(tutamac, 0, yol, ctypes.byref(boy)):
                    program = os.path.basename(yol.value)
            finally:
                kernel32.CloseHandle(tutamac)

    return (baslik, program)


def tam_ekran_mi():
    """Öndeki pencere ekranın tamamını kaplıyor mu?

    Video, oyun, sunum ve görüntülü görüşmeler genelde böyledir.
    Molayı ertelemek için kullanıyoruz — sunumun ortasında ekranı
    kapatmak, uygulamanın silinme sebebi #1.
    """
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return False

    # Masaüstünün kendisi tam ekran sayılmaz
    kabuk = user32.GetShellWindow()
    if hwnd == kabuk or hwnd == user32.GetDesktopWindow():
        return False

    dikdortgen = wt.RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(dikdortgen)):
        return False

    ekran_g = user32.GetSystemMetrics(0)
    ekran_y = user32.GetSystemMetrics(1)
    pencere_g = dikdortgen.right - dikdortgen.left
    pencere_y = dikdortgen.bottom - dikdortgen.top

    # Birkaç piksel tolerans (kenarlıksız pencereler tam oturmayabilir)
    return pencere_g >= ekran_g - 2 and pencere_y >= ekran_y - 2


# Görüntülü görüşme / toplantı programları.
# Bunlardan biri öndeyken mola vermek, uygulamanın silinme sebebi #1.
TOPLANTI_PROGRAMLARI = {
    "zoom.exe", "teams.exe", "ms-teams.exe", "msteams.exe",
    "webex.exe", "webexmta.exe", "ciscowebexstart.exe",
    "skype.exe", "lync.exe", "outlook.exe",
    "discord.exe", "slack.exe", "gotomeeting.exe",
    "anydesk.exe", "teamviewer.exe",
    "obs64.exe", "obs32.exe",
}

# Tarayıcı sekmesi başlığında görüşme belirtisi
TOPLANTI_IPUCLARI = ("meet.google", "google meet", "zoom", "teams",
                     "webex", "whereby", "jitsi", "görüşme")


def mikrofon_kamera_kullanimda():
    """Şu anda mikrofonu veya kamerayı kullanan bir program var mı?

    Windows, hangi programın ne zaman mikrofon/kamera kullandığını kayıt
    defterinde tutuyor (gizlilik göstergesi de bunu okuyor).
    `LastUsedTimeStop` değeri 0 ise o program AYNI ANDA kullanıyor demektir.

    Bu, program adına bakmaktan çok daha kesin: adı listede olmayan bir
    görüşme programı da yakalanır, açık ama görüşmede olmayan Teams ise
    boşuna mola erteletmez.

    Döner: (kullaniliyor_mu, "mikrofon"/"kamera"/"", program_adi)
    """
    try:
        import winreg
    except ImportError:
        return (False, "", "")

    KOK = (r"SOFTWARE\Microsoft\Windows\CurrentVersion"
           r"\CapabilityAccessManager\ConsentStore")

    for tur, yol in (("mikrofon", "microphone"), ("kamera", "webcam")):
        for alt_yol in (yol, yol + r"\NonPackaged"):
            try:
                anahtar = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                         KOK + "\\" + alt_yol)
            except OSError:
                continue
            try:
                i = 0
                while True:
                    try:
                        ad = winreg.EnumKey(anahtar, i)
                    except OSError:
                        break
                    i += 1
                    try:
                        with winreg.OpenKey(anahtar, ad) as alt:
                            durdurma, _ = winreg.QueryValueEx(alt, "LastUsedTimeStop")
                            if durdurma == 0:
                                # "#" ile kodlanmış yol: C:#Program Files#...#zoom.exe
                                program = ad.replace("#", "\\").split("\\")[-1]
                                return (True, tur, program or ad)
                    except OSError:
                        continue
            finally:
                anahtar.Close()

    return (False, "", "")


def toplantida_mi():
    """Görüşmede miyiz? Üç kademeli kontrol, en güveniliriden başlayarak.

    1. Mikrofon/kamera GERÇEKTEN kullanılıyor mu (kayıt defteri) — kesin.
    2. Öndeki program bilinen bir görüşme programı mı — muhtemel.
    3. Pencere başlığında görüşme belirtisi var mı — ipucu.

    1. kademe olmasaydı: açık ama görüşmede olmayan Teams boşuna mola
    erteletirdi; listede olmayan bir görüşme programı ise hiç yakalanmazdı.
    """
    kullaniliyor, tur, program = mikrofon_kamera_kullanimda()
    if kullaniliyor:
        return True, "%s (%s kullanımda)" % (program, tur)

    baslik, program = on_pencere()
    if program and program.lower() in TOPLANTI_PROGRAMLARI:
        return True, program
    dusuk = (baslik or "").lower()
    for ipucu in TOPLANTI_IPUCLARI:
        if ipucu in dusuk:
            return True, program or baslik[:40]
    return False, ""


def one_getir(hwnd):
    """Pencereyi zorla öne getir.

    Windows, odak çalmayı engellemek için kilit koyar. Bilinen çözüm:
    kısa bir ALT tuşu darbesi göndermek kilidi açar.
    """
    try:
        VK_MENU = 0x12
        KEYEVENTF_KEYUP = 0x0002
        user32.keybd_event(VK_MENU, 0, 0, 0)
        user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
        user32.SetForegroundWindow(hwnd)
        user32.BringWindowToTop(hwnd)
    except Exception:
        pass


def pencereyi_koyulastir(hwnd, zemin_renk, yazi_renk, kenar_renk=None):
    """Windows'un başlık çubuğunu uygulamanın rengine boyar.

    Varsayılan başlık çubuğu bembeyaz; koyu bir uygulamanın üstünde
    yamalı duruyor. Windows 11 bu üç özelliği destekliyor:
      35 = başlık çubuğu rengi
      36 = başlık yazısı rengi
      34 = kenarlık rengi
      20 = koyu mod (Windows 10 için yedek)
      33 = köşe biçimi (2 = yuvarlak)
    Desteklemeyen sürümlerde sessizce hiçbir şey olmaz.
    """
    def cevir(onalti):
        o = onalti.lstrip("#")
        r, g, b = int(o[0:2], 16), int(o[2:4], 16), int(o[4:6], 16)
        return b << 16 | g << 8 | r          # Windows BGR ister

    try:
        dwm = ctypes.windll.dwmapi
        ayarla = dwm.DwmSetWindowAttribute

        # Windows 10: koyu mod
        koyu = ctypes.c_int(1)
        ayarla(wt.HWND(hwnd), 20, ctypes.byref(koyu), ctypes.sizeof(koyu))

        # Windows 11: tam renk denetimi
        for ozellik, renk in ((35, zemin_renk), (36, yazi_renk),
                              (34, kenar_renk or zemin_renk)):
            d = ctypes.c_int(cevir(renk))
            ayarla(wt.HWND(hwnd), ozellik, ctypes.byref(d), ctypes.sizeof(d))

        # Yuvarlak köşe
        kose = ctypes.c_int(2)
        ayarla(wt.HWND(hwnd), 33, ctypes.byref(kose), ctypes.sizeof(kose))
        return True
    except Exception:
        return False


def kisayol_basili_mi(*tuslar):
    """Verilen tuşların HEPSİ şu anda basılı mı?

    Acil çıkış kısayolu için: Ctrl+Alt+Shift.
    """
    VK = {"ctrl": 0x11, "alt": 0x12, "shift": 0x10}
    for t in tuslar:
        durum = user32.GetAsyncKeyState(VK[t])
        # Üst bit (0x8000) = tuş ŞU AN basılı. Alt bit "en son çağrıdan beri
        # basıldı" demek; onu kullansaydık eski basışlar da sayılırdı.
        if not (durum & 0x8000):
            return False
    return True
