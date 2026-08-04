# -*- coding: utf-8 -*-
"""
KİLİT — Şifre saklama ve programı ayakta tutan bekçi.

ŞİFRELEME NEDEN BÖYLE?
----------------------
Şifre asla düz metin saklanmaz. Ama düz SHA-256 de yeterli değil:
4 haneli bir şifrede sadece 10.000 ihtimal var; sıradan bir bilgisayar
SHA-256 ile saniyede milyonlarca deneme yapar, yani anında kırar.

Bu yüzden PBKDF2-HMAC-SHA256 kullanıyoruz ve 240.000 tur döndürüyoruz.
Her deneme ~0,1 saniye sürer. 10.000 ihtimal = yaklaşık 17 dakika.
6 haneye çıkarsan 1.000.000 ihtimal = yaklaşık 28 saat.
Tur sayısı dosyada saklanır; ileride artırırsan eski şifreler bozulmaz.

DÜRÜST SINIR
------------
Bu bir dosya şifrelemesi değil, bir kapı kilidi. Dosyayı silen kişi
kilidi de siler. Asıl caydırıcılık bekçi süreçtedir (aşağıda).
"""

import hashlib
import hmac
import json
import os
import secrets
import subprocess
import sys
import time

TUR_SAYISI = 240_000
TEMIZ_CIKIS_DOSYA = "temiz_cikis.bayrak"


# ----------------------------------------------------------------------
# Şifre
# ----------------------------------------------------------------------
def ozet_uret(sifre, tuz=None, tur=TUR_SAYISI):
    """Şifreden saklanabilir bir özet üretir."""
    tuz = tuz or secrets.token_hex(16)
    ham = hashlib.pbkdf2_hmac("sha256", sifre.encode("utf-8"),
                              bytes.fromhex(tuz), tur)
    return {"yontem": "pbkdf2", "tur": tur, "tuz": tuz, "ozet": ham.hex()}


def dogrula(sifre, kayit):
    """Girilen şifre doğru mu?

    Eski sürümden kalan düz SHA-256 kayıtları da kabul eder;
    doğruysa çağıran taraf yeni yönteme yükseltir.
    """
    if not kayit:
        return False, False           # (dogru_mu, yukseltilmeli_mi)

    if kayit.get("yontem") == "pbkdf2":
        ham = hashlib.pbkdf2_hmac("sha256", sifre.encode("utf-8"),
                                  bytes.fromhex(kayit["tuz"]), kayit["tur"])
        # compare_digest: doğru/yanlış karşılaştırmasının süresi
        # şifreye göre değişmesin diye
        dogru = hmac.compare_digest(ham.hex(), kayit["ozet"])
        return dogru, dogru and kayit["tur"] < TUR_SAYISI

    # Eski biçim: {"tuz": ..., "ozet": sha256(tuz|sifre)}
    if "tuz" in kayit and "ozet" in kayit:
        eski = hashlib.sha256(("%s|%s" % (kayit["tuz"], sifre)).encode("utf-8")).hexdigest()
        dogru = hmac.compare_digest(eski, kayit["ozet"])
        return dogru, dogru
    return False, False


def sifre_gucu(sifre):
    """Kullanıcıya 'bu şifre ne kadar dayanır' diye söyleyebilmek için."""
    if not sifre.isdigit():
        return None
    ihtimal = 10 ** len(sifre)
    saniye = ihtimal * 0.1              # deneme başına ~0,1 sn
    if saniye < 3600:
        return "%d dakika" % max(1, saniye // 60)
    if saniye < 86400:
        return "%d saat" % (saniye // 3600)
    return "%d gün" % (saniye // 86400)


# ----------------------------------------------------------------------
# Bekçi süreç
# ----------------------------------------------------------------------
def surec_yasiyor_mu(pid):
    """Süreç GERÇEKTEN çalışıyor mu?

    Dikkat: OpenProcess'in başarılı olması yaşıyor demek DEĞİL. Süreç
    ölse bile başka biri tutamacını açık tuttuğu sürece PID serbest
    kalmaz ve OpenProcess başarılı döner. Bu yüzden ayrıca sürecin
    "işaretli" (signaled = bitmiş) olup olmadığına bakıyoruz.
    """
    try:
        import ctypes
        SYNCHRONIZE = 0x00100000
        WAIT_TIMEOUT = 0x00000102        # hâlâ çalışıyor
        k32 = ctypes.windll.kernel32
        h = k32.OpenProcess(SYNCHRONIZE, False, int(pid))
        if not h:
            return False
        try:
            return k32.WaitForSingleObject(h, 0) == WAIT_TIMEOUT
        finally:
            k32.CloseHandle(h)
    except Exception:
        return False


def bekci_baslat(klasor):
    """Programın kendisini izleyen ikinci bir süreç başlatır.

    Görev Yöneticisi'nden program kapatılırsa bekçi bunu görür ve
    programı yeniden açar. Kullanıcı şifresini girip düzgün kapatırsa
    bir bayrak dosyası bırakılır; bekçi onu görünce sessizce çekilir.
    """
    try:
        os.makedirs(klasor, exist_ok=True)
        bayrak = os.path.join(klasor, TEMIZ_CIKIS_DOSYA)
        if os.path.exists(bayrak):
            os.remove(bayrak)

        komut = [sys.executable]
        if not getattr(sys, "frozen", False):
            komut.append(os.path.abspath(sys.argv[0]))
        komut += ["--bekci", str(os.getpid()), klasor]

        # CREATE_NO_WINDOW: siyah konsol penceresi açılmasın
        subprocess.Popen(komut, creationflags=0x08000000,
                         close_fds=True)
        return True
    except Exception:
        return False


def temiz_cikis_isaretle(klasor):
    """Kullanıcı şifresini girip düzgün kapattı — bekçi karışmasın."""
    try:
        os.makedirs(klasor, exist_ok=True)
        with open(os.path.join(klasor, TEMIZ_CIKIS_DOSYA), "w") as f:
            f.write(str(time.time()))
    except Exception:
        pass


GOSTER_BAYRAK = "goster.bayrak"
_mutex_tutamaci = None


def tek_ornek_al():
    """Program zaten açık mı? Değilse 'benim' de.

    Kullanıcı kısayola iki kez tıklayınca iki kopya açılıyordu; ikisi de
    pencereyi gizlediği için ekranda hiçbir şey görünmüyor, kullanıcı
    "açılmıyor" sanıyordu. Artık ikinci kopya açılmaz; bunun yerine
    zaten açık olana "pencereni göster" der.

    Döner: True = ilk kopya benim, çalışmaya devam et
           False = zaten açık, ben çıkmalıyım
    """
    global _mutex_tutamaci
    try:
        import ctypes
        ERROR_ALREADY_EXISTS = 183
        k32 = ctypes.windll.kernel32
        _mutex_tutamaci = k32.CreateMutexW(None, False, "GozMolasi_TekOrnek_v1")
        return k32.GetLastError() != ERROR_ALREADY_EXISTS
    except Exception:
        return True          # kontrol edilemiyorsa engelleme


def goster_iste(klasor):
    """Çalışan kopyaya 'pencereni aç' mesajı bırak."""
    try:
        os.makedirs(klasor, exist_ok=True)
        with open(os.path.join(klasor, GOSTER_BAYRAK), "w") as f:
            f.write(str(time.time()))
        return True
    except Exception:
        return False


def goster_istendi_mi(klasor):
    """Mesaj var mı? Varsa tüket ve True dön."""
    yol = os.path.join(klasor, GOSTER_BAYRAK)
    if not os.path.exists(yol):
        return False
    try:
        os.remove(yol)
    except Exception:
        pass
    return True


ASGARI_YASAM = 25          # saniye — bundan kısa sürede ölen program çöküyordur


def bekci_calis(izlenen_pid, klasor):
    """Bekçi kipi. Programın bittiğini görene kadar bekler."""
    bayrak = os.path.join(klasor, TEMIZ_CIKIS_DOSYA)
    basladi = time.time()

    while surec_yasiyor_mu(izlenen_pid):
        if os.path.exists(bayrak):
            try:
                os.remove(bayrak)
            except Exception:
                pass
            return 0                      # düzgün kapanış: bekçi çekilir
        time.sleep(2)

    # Süreç bitti. Düzgün kapanış bayrağı var mı?
    time.sleep(1.0)
    if os.path.exists(bayrak):
        try:
            os.remove(bayrak)
        except Exception:
            pass
        return 0

    # Program çok kısa sürede öldüyse bu bir çökmedir, zorla kapatma değil.
    # Yeniden açarsak sonsuz döngüye gireriz — açmıyoruz.
    if time.time() - basladi < ASGARI_YASAM:
        return 0

    # Zorla kapatılmış. Programı geri aç.
    try:
        komut = [sys.executable]
        if not getattr(sys, "frozen", False):
            komut.append(os.path.abspath(sys.argv[0]))
        subprocess.Popen(komut, creationflags=0x08000000, close_fds=True)
    except Exception:
        pass
    return 0
