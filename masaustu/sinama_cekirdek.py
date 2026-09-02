# -*- coding: utf-8 -*-
"""`sinama.js` dosyasını KOŞAN taraf — çekirdek senaryoları.

NEDEN BU DOSYA VAR
  `sinama.js` depoda duruyordu ve çekirdeğin en can alıcı yerlerini
  sınıyordu: sayaç geri yükleme, saat oyunları, mola akışı. Ama
  **kimse çağırmıyordu**. Kayıtta (`sinama.py` içindeki SINAMALAR)
  yoktu, hiçbir HTML sayfası yüklemiyordu, `DERLE.bat` bilmiyordu.
  Yani yazılmış ama ölü bir bekçiydi; deponun "20 sınama geçti"
  raporunda bu 11 senaryo hiç yoktu.

  Bu depoda aynı sınıf ÜÇÜNCÜ kez çıkıyor:
    1. `exe_icerik.py` vardı, `DERLE.bat` çağırmıyordu.
    2. Damga bekçisinin kapsamı elle tutuluyordu, dar kalmıştı.
    3. `sinama.js` — bu.
  Ortak ders: bir bekçinin VAR olması ölçülmez, ÇAĞRILDIĞI ölçülür.

NASIL
  `sinama.js` tarayıcı konsolu için yazılmış: gerçek DOM istiyor
  (sekme düğmesi, taşma ölçümü) ve `MolaMotoru` küresel adını
  kullanıyor. O yüzden burada gerçek sayfa açılıyor — makinede zaten
  kurulu başsız Edge ile, indirme gerekmiyor.

  Tarayıcı yoksa ATLANDI der ve 0 döner: ölçemediğine "geçti"
  demiyoruz, ama ortam eksikliği de kırmızı sayılmaz.
"""
import io
import json
import os
import sys

BURASI = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(BURASI)
sys.path.insert(0, BURASI)

# Kaç senaryo koştuğunun kaydı — sayı düşerse fark edilsin diye.
KAYIT = os.path.join(KOK, ".cekirdek_kayit.json")


def main():
    kaynak_yolu = os.path.join(KOK, "_sinama", "sinama.js")
    if not os.path.exists(kaynak_yolu):
        # Dosya artik DEPODA IZLENIYOR (`_sinama/` altinda). Eskiden
        # kokteydi ve `.gitignore` onu disliyordu; yani 66 senaryo tek
        # bir diskte duruyordu, yedegi yoktu. Simdi eksik olmasi
        # gercek bir kusur - o yuzden sessizce atlanmiyor.
        print("_sinama/sinama.js YOK — çekirdek senaryoları ölçülemiyor.")
        return 1
    kaynak = io.open(kaynak_yolu, encoding="utf-8").read()

    try:
        import ekran_denetle as ED
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        print("ATLANDI — %s" % e)
        return 0

    port = ED.bos_port()
    srv = ED.sunucu_baslat(port)
    try:
        with sync_playwright() as p:
            t = p.chromium.launch(channel="msedge")
            s = t.new_page(viewport={"width": 390, "height": 844},
                           locale="tr-TR")
            hatalar = []
            s.on("pageerror", lambda e: hatalar.append(str(e)[:110]))
            s.goto("http://127.0.0.1:%d/index.html" % port,
                   wait_until="load", timeout=30000)
            s.wait_for_timeout(1500)
            ham = s.evaluate(kaynak)
            t.close()
    except Exception as e:
        print("ATLANDI — tarayıcı açılamadı: %s" % str(e).splitlines()[0][:70])
        return 0
    finally:
        srv.shutdown()

    r = json.loads(ham) if isinstance(ham, str) else ham
    for satir in r["hepsi"]:
        print("  " + satir)
    print()
    print("çekirdek senaryoları: %d/%d geçti" % (r["gecti"], r["toplam"]))

    # SENARYO SAYISI DÜŞERSE KIRMIZI.
    #
    # "66/66 geçti" ile "40/40 geçti" ekranda aynı derecede yeşil
    # görünür. Sessizce kaybolan senaryolar raporda hiç belli olmaz;
    # "hepsi geçti" güvencesi boş çıkar. Bir bekçinin VAR olması
    # yetmediği gibi, KAÇ ŞEY ölçtüğü de ölçülmeli.
    #
    # Sayı elle yazılmıyor (elle tutulan kapsam çürür — bu depoda
    # işaret listesi ve damga kapsamı tam öyle çürüdü). Damga
    # bekçisinin yöntemi: ölçülen sayı kayda geçer, düşerse kırmızı,
    # artarsa kayıt yenilenir. Bilerek senaryo kaldırılırsa:
    #     python masaustu/sinama_cekirdek.py --kaydet
    taban = 0
    if os.path.exists(KAYIT):
        try:
            taban = int(json.load(io.open(KAYIT, encoding="utf-8-sig"))
                        .get("senaryo", 0))
        except Exception:
            taban = 0
    if "--kaydet" in sys.argv or r["toplam"] > taban:
        io.open(KAYIT, "w", encoding="utf-8").write(json.dumps(
            {"senaryo": r["toplam"]}, ensure_ascii=False, indent=1) + "\n")
        if r["toplam"] > taban and taban:
            print("  (taban %d -> %d yükseldi)" % (taban, r["toplam"]))
    elif r["toplam"] < taban:
        print()
        print("SENARYO KAYBI — önce %d senaryo koşuyordu, şimdi %d."
              % (taban, r["toplam"]))
        print("Eksik %d senaryo sessizce düştü; \"hepsi geçti\" artık"
              % (taban - r["toplam"]))
        print("bir şey söylemiyor. Bilerek kaldırıldıysa:")
        print("           python masaustu/sinama_cekirdek.py --kaydet")
        return 1
    if hatalar:
        print("SAYFA HATASI: %s" % hatalar[0])
        return 1
    if r["kaldi"]:
        print("KALDI — %d senaryo" % r["kaldi"])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
