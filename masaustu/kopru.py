# -*- coding: utf-8 -*-
"""KÖPRÜ — Windows sürümü ile tarayıcı sürümünü aynı sayaçta buluşturur.

SORUN
  İki sürüm iki ayrı yere yazıyor:
    Windows  -> %APPDATA%\\GozMolasi\\durum.json
    Tarayıcı -> tarayıcının localStorage'ı
  Biri 8 dakikadayken öbürü 20:00 gösteriyordu. Kullanıcının sözüyle:
  "süre başa sarmasın".

  Tarayıcı, güvenlik gereği bilgisayardaki dosyaları okuyamaz. Bu bir
  izin meselesi değil, kaldırılabilecek bir duvar değil. Tek yol:
  Windows sürümünün, tarayıcının SORABİLECEĞİ bir adres açması.

ÜÇ GÜVENLİK KARARI — hepsi bilerek dar tutuldu

  1. YALNIZCA OKUMA. Yazma ucu YOK.
     Yazma ucu olsaydı, açtığınız herhangi bir web sayfası sayacınızı
     sıfırlayabilir, aile kipindeki bir çocuk da tarayıcıdan sınırı
     kaldırabilirdi. Köprü sayacı ANLATIR, değiştirmez.

  2. YALNIZCA BU BİLGİSAYAR (127.0.0.1).
     Ağa açılmıyor. Aynı Wi-Fi'daki başka bir cihaz bu adresi göremez.

  3. KAYNAK LİSTESİ. `Access-Control-Allow-Origin: *` DEĞİL.
     `*` olsaydı ziyaret ettiğiniz her site "bu kişide Göz Molası var,
     bugün şu kadar ekran süresi olmuş" bilgisini okuyabilirdi. Ekran
     süresi kişisel veridir. Yalnızca uygulamanın kendi sayfalarına
     izin veriliyor.

ÖLÇÜLDÜ (27.08.2026)
  Sayfa http://localhost:8455 iken  -> köprüyü OKUDU
  Sayfa https://meteotr06.github.io -> ENGELLENDİ (ERR_BLOCKED_BY_CLIENT;
    bu makinedeki bir tarayıcı eklentisi kesiyor)
  Bu yüzden yayındaki sayfanın köprüyü göreceği SÖZÜ VERİLMİYOR.
  Garanti edilen yol: sayfayı yerelden açmak.
"""
import json
import threading
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8452          # 8451 dosya sunucusunun (Telefona Sunucu Ac.bat)

# Yalnızca uygulamanın kendi sayfaları. Yerel portu tek tek yazmak yerine
# önekle bakıyoruz; kullanıcı sunucuyu hangi portta açarsa açsın çalışsın.
IZINLI_ONEK = ("http://localhost:", "http://127.0.0.1:", "http://[::1]:")
# YAYINDAKI ADRES BILEREK LISTEDE DEGIL.
#
# Once vardi, cikarildi. Iki sebep:
#   1) Olculdu (27.08.2026): yayindaki sayfa zaten ulasamiyor
#      (ERR_BLOCKED_BY_CLIENT - tarayici eklentisi kesiyor). Yani izin
#      FAYDA saglamiyordu.
#   2) O izin, sayfadaki HER betige geciyordu - reklam betikleri dahil.
#      Proje AdSense onayi bekliyor. Ele gecirilmis tek bir reklam ya da
#      tek bir XSS, `ekran_sn` degerini okuyup disari yollayabilirdi:
#      hem "bu kisi su an bilgisayarinin basinda" sinyali hem de iyi bir
#      parmak izi. Ayrica o adreste dort uygulama birden duruyor; izin
#      hepsine veriliyordu.
#
# Riski bugunden aliyor, faydayi hic vermiyordu. Yerelden acilan sayfa
# zaten calisiyor ve garanti edilen yol o.
IZINLI_TAM = ()


def _izinli_mi(kaynak):
    if not kaynak:
        return False
    if kaynak in IZINLI_TAM:
        return True
    return any(kaynak.startswith(o) for o in IZINLI_ONEK)


class Kopru:
    """Uygulamanın içinde yaşayan küçük okuma ucu.

    `veri_uret` her istekte çağrılır ve sözlük döndürmelidir. Anlık
    değeri kopyalamak yerine fonksiyon almasının sebebi: sayaç sürekli
    değişiyor, köprü her zaman TAZE olanı vermeli.
    """

    def __init__(self, veri_uret, port=PORT):
        self.veri_uret = veri_uret
        self.port = port
        self.sunucu = None
        self.hata = None

    def baslat(self):
        """Ayrı bir iş parçacığında başlatır. Başarısızlık uygulamayı
        ÇÖKERTMEZ — köprü bir kolaylık, uygulamanın kendisi değil."""
        kopru = self

        class Islem(BaseHTTPRequestHandler):
            # Askidaki bir baglanti butun kopruyu kilitlemesin.
            # `telnet 127.0.0.1 8452` yazip bekleyen biri, zaman asimi
            # olmadan `readline()` icinde sunucuyu SONSUZA KADAR tutuyordu
            # ve bu hicbir yerde gorunmuyordu. Aile kipinde bunu bir cocuk
            # uc kelimeyle yapabilirdi.
            timeout = 5

            def _konak_yerel_mi(self):
                """DNS REBINDING savunmasi.

                CORS tek basina yetmiyor: saldirgan `kotu.example`
                alanini 8452 portunda yayinlar, A kaydini 127.0.0.1'e
                dondururse tarayici icin bu AYNI-KAYNAK olur ve CORS hic
                devreye girmez. Transmission ve Zoom ayni yoldan dustu.
                Savunma: Host basligi yerel degilse cevap verme.
                """
                konak = (self.headers.get("Host") or "").rsplit(":", 1)[0]
                return konak.strip("[]") in ("127.0.0.1", "localhost", "::1")

            def _yanit(self, kod, govde=b"", tur="application/json"):
                kaynak = self.headers.get("Origin")
                self.send_response(kod)
                self.send_header("Content-Type", tur)
                self.send_header("Content-Length", str(len(govde)))
                # Onbellek YASAK: sayaç her saniye değişiyor, bayat
                # bir cevap "süre başa sardı" hissinin ta kendisidir.
                self.send_header("Cache-Control", "no-store")
                if _izinli_mi(kaynak):
                    self.send_header("Access-Control-Allow-Origin", kaynak)
                    self.send_header("Vary", "Origin")
                self.end_headers()
                if govde:
                    self.wfile.write(govde)

            def do_OPTIONS(self):
                self._yanit(204)

            def do_GET(self):
                if not self._konak_yerel_mi():
                    self._yanit(403, b'{"hata":"konak"}')
                    return
                if self.path.split("?")[0] != "/durum":
                    self._yanit(404, b'{"hata":"yok"}')
                    return
                try:
                    veri = kopru.veri_uret()
                except Exception as e:
                    self._yanit(500, json.dumps(
                        {"hata": type(e).__name__}).encode("utf-8"))
                    return
                self._yanit(200, json.dumps(veri).encode("utf-8"))

            # Sunucu günlüğü konsola akmasın; uygulama penceresiz çalışıyor.
            def log_message(self, *a):
                pass

        # IKINCI KOPYA TESPITI - olculdu (27.08.2026).
        # Windows'ta SO_REUSEADDR ayni adrese IKINCI bind'e izin veriyor:
        # ikinci kopya OSError ALMIYOR, `baslat()` True donuyor, ama tek
        # bir istek bile ona gelmiyor. Yani kopru "acildim" saniyordu.
        # Hatanin olmamasi, calistigi anlamina gelmez.
        if self.port and self._baskasi_dinliyor():
            self.hata = "port %d zaten kullaniliyor (baska bir kopya?)" % self.port
            return False
        try:
            self.sunucu = ThreadingHTTPServer(("127.0.0.1", self.port),
                                             Islem)
        except OSError as e:
            # Port dolu olabilir (ikinci kopya, başka program). Köprüsüz
            # devam ediyoruz; kullanıcı bunu Bilgiler sekmesinde görecek.
            self.hata = str(e)
            return False
        # Port 0 istendiyse isletim sistemi bos bir port secer; hangisini
        # sectigini buradan ogreniyoruz. Sinamalar bunu kullaniyor:
        # sabit port, bir onceki kosunun artigi yuzunden tutulu olabilir
        # ve sinama KODLA ilgisiz bir sebeple duser. Kararsiz sinama,
        # basarisiz sinamadan kotudur - insan onu ciddiye almayi birakir.
        self.port = self.sunucu.server_address[1]
        t = threading.Thread(target=self.sunucu.serve_forever, daemon=True)
        t.start()
        return True

    def _baskasi_dinliyor(self):
        """Bu portu baska biri tutuyor mu? Baglanmayi DENEYEREK bakar."""
        s = socket.socket()
        s.settimeout(0.4)
        try:
            s.connect(("127.0.0.1", self.port))
            return True
        except OSError:
            return False
        finally:
            s.close()

    def durdur(self):
        if self.sunucu:
            try:
                self.sunucu.shutdown()
                # server_close() SART: shutdown() yalnizca dongusu
                # durduruyor, soketi kapatmiyor. Kapatmayi cop
                # toplayiciya birakmak, portun ne zaman birakilacagini
                # belirsiz yapar.
                self.sunucu.server_close()
            except Exception:
                pass
            self.sunucu = None

    def acik_mi(self):
        return self.sunucu is not None
