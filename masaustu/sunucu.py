# -*- coding: utf-8 -*-
"""Sınama için basit yerel sunucu — limanı ORTAMDAN okur.

NİYE VAR
  `python -m http.server 8455` limanı komuta gömüyordu. Aynı makinede
  başka bir oturumun sunucusu o limanı tuttuğunda önizleme hiç
  açılmıyor ve ölçüm yapılamıyor hâle geliyor (29.08.2026'da yaşandı:
  liman "arsa" oturumundaydı).

  Burası `PORT` ortam değişkenini okuyor; koşum ortamı hangi limanı
  verirse onu kullanıyor. Değişken yoksa 8456'ya düşüyor.

NE SUNUYOR
  Proje kökünü (bu dosyanın bir üstü). Yalnızca yerel arayüze bağlanır
  (127.0.0.1) — ağdaki başka makineler erişemez.
"""
import functools
import http.server
import os
import socketserver

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMAN = int(os.environ.get("PORT") or 8456)


class Sessiz(http.server.SimpleHTTPRequestHandler):
    """Her istek için satır basmasın; ölçüm çıktısını boğuyordu."""

    def log_message(self, bicim, *arg):
        pass


def main():
    isleyici = functools.partial(Sessiz, directory=KOK)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", LIMAN), isleyici) as s:
        print("sunucu hazır: http://127.0.0.1:%d  (kök: %s)" % (LIMAN, KOK))
        s.serve_forever()


if __name__ == "__main__":
    main()
