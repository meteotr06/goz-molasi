/* ============================================================
   ÇEKİRDEK — Mola zamanlayıcı motoru
   Burada HİÇ arayüz kodu yok. Sadece saf mantık.
   Böylece motoru bozmadan arayüzü istediğin gibi değiştirebilirsin.
   ============================================================ */

/* Durumlar (state):
   'hazir'      : henüz başlamadı
   'calisiyor'  : 20 dakikalık çalışma sayıyor
   'uyari'      : molaya az kaldı, kullanıcı uyarılıyor
   'mola'       : 20 saniyelik mola, ekran kilitli
   'duraklatildi': kullanıcı elle durdurdu
   'bosta'      : cihaza uzun süre dokunulmadı, sayaç kendini durdurdu
*/

const VARSAYILAN_AYARLAR = {
  calismaSuresi: 20 * 60,   // saniye — 20 dakika
  molaSuresi: 20,           // saniye — 20 saniye
  uyariSuresi: 15,          // saniye — molaya kaç saniye kala uyaralım
  bostaEsigi: 90,           // saniye — bu kadar dokunulmazsa sayaç durur
  dinlenmeEsigi: 300,       // saniye — bu kadar uzak kalındıysa gözler zaten dinlendi
  molaAtlanabilir: false,   // VARSAYILAN: mola atlanamaz. 20 sn kesin.
  sesAcik: true,

  uzunMolaEsigi: 7200,      // saniye — 2 saat kesintisiz çalışma (AOA risk eşiği)
  uzunMolaSuresi: 300,      // saniye — 5 dakika
  uzunMolaAcik: false,      // uzun mola önerilsin mi

  // Çalışma saatleri: bu aralığın dışında hatırlatma gelmez.
  // Gece 23:00'te ders çalışan biri sabah 9'da mola istemez.
  saatlerAcik: false,
  basSaat: '09:00',
  bitSaat: '18:00',
};

class MolaMotoru {
  constructor(ayarlar = {}) {
    this.ayarlar = { ...VARSAYILAN_AYARLAR, ...ayarlar };
    this.durum = 'hazir';
    this.oncekiDurum = null;

    // Sayaçları TARİH DAMGASI ile tutuyoruz, tik sayısıyla değil.
    // Sebebi: tarayıcı arka plandaki sekmenin setInterval'ini yavaşlatır
    // (1 dakikaya kadar). Tik sayarsak 20 dakika 35 dakika olur.
    // Date.now() farkı ise her koşulda doğrudur.
    this.hedefZaman = 0;      // bu aşamanın biteceği an (ms)
    this.asamaBaslangic = 0;  // bu aşamanın başladığı an (ms)
    this.sonHareket = Date.now();

    this.istatistik = {
      tamamlananMola: 0,
      atlananMola: 0,
      ekranSuresi: 0,        // saniye — bugün toplam
      kesintisizSure: 0,     // saniye — son gerçek dinlenmeden beri
      uzunMola: 0,
      gun: this._bugun(),
    };
    this.uzunMoladaMi = false;

    this.dinleyiciler = {};   // olay adı -> [fonksiyon]
    this._zamanlayici = null;
  }

  /* ---------- Olay sistemi (arayüz buradan haber alır) ---------- */
  uzerine(olay, fn) {
    (this.dinleyiciler[olay] ||= []).push(fn);
    return this;
  }
  _duyur(olay, veri) {
    (this.dinleyiciler[olay] || []).forEach((fn) => fn(veri));
  }

  /* ---------- Kontrol ---------- */
  basla() {
    this._asamayaGec('calisiyor', this.ayarlar.calismaSuresi);
    if (!this._zamanlayici) {
      // 250ms: göze akıcı gelir, pili yormaz.
      this._zamanlayici = setInterval(() => this.tik(), 250);
    }
    this._duyur('basladi');
  }

  duraklat() {
    if (this.durum === 'mola') return;          // mola duraklatılamaz
    this.kalanDondurulmus = this.kalanSaniye();
    this.oncekiDurum = this.durum;
    this.durum = 'duraklatildi';
    this._duyur('degisti', this.anlikDurum());
  }

  devamEt() {
    if (this.durum !== 'duraklatildi' && this.durum !== 'bosta') return;
    const kalan = this.kalanDondurulmus ?? this.ayarlar.calismaSuresi;
    this._asamayaGec('calisiyor', kalan);
  }

  sifirla() {
    this._asamayaGec('calisiyor', this.ayarlar.calismaSuresi);
  }

  /** Molayı hemen başlat (kullanıcı "şimdi mola ver" derse) */
  molayaGec() {
    this.uzunMoladaMi = false;
    this._asamayaGec('mola', this.ayarlar.molaSuresi);
  }

  /** Uzun mola (varsayılan 5 dk). Kullanıcı izin verdiyse çağrılır. */
  uzunMolayaGec() {
    this.uzunMoladaMi = true;
    this._asamayaGec('mola', this.ayarlar.uzunMolaSuresi);
  }

  /** Molayı atla — istatistiğe kaydedilir, saklamıyoruz */
  molayiAtla() {
    if (this.durum !== 'mola' || !this.ayarlar.molaAtlanabilir) return false;
    this.istatistik.atlananMola++;
    this._duyur('molaAtlandi', this.istatistik);
    this._asamayaGec('calisiyor', this.ayarlar.calismaSuresi);
    return true;
  }

  /** Molayı ertele — sayacı belirtilen saniye kadar ileri al */
  ertele(saniye) {
    if (this.durum !== 'calisiyor' && this.durum !== 'uyari') return false;
    this._asamayaGec('calisiyor', saniye);
    this._duyur('ertelendi', saniye);
    return true;
  }

  /** Kullanıcı fare/klavye/dokunma yaptı — boşta sayacını sıfırla.
      Cihazdan uzun süre uzak kalındıysa gözler zaten dinlendi demektir;
      kaldığı yerden değil, baştan saymaya başlar. */
  hareketVar() {
    const simdi = Date.now();
    const uzaktaKalinan = simdi - this.sonHareket;
    this.sonHareket = simdi;

    if (this.durum === 'bosta') {
      if (uzaktaKalinan > this.ayarlar.dinlenmeEsigi * 1000) {
        this.istatistik.kesintisizSure = 0;   // gerçekten dinlenildi
        this._duyur('dinlenildi', Math.round(uzaktaKalinan / 1000));
        this.sifirla();
      } else {
        this.devamEt();
      }
    }
  }

  /* ---------- Kalp atışı ---------- */
  tik() {
    if (this.durum === 'duraklatildi' || this.durum === 'hazir') return;

    const simdi = Date.now();

    // Çalışma saatleri dışındaysak sayaç işlemez.
    // (Mola başladıysa onu yarıda kesmiyoruz.)
    if (this.durum !== 'mola' && !this.saatUygunMu()) {
      if (this.durum !== 'saatDisi') {
        this.kalanDondurulmus = this.kalanSaniye();
        this.durum = 'saatDisi';
        this._duyur('degisti', this.anlikDurum());
      }
      return;
    }
    if (this.durum === 'saatDisi') {
      // Çalışma saati başladı — temiz bir süreyle başla
      this._asamayaGec('calisiyor', this.ayarlar.calismaSuresi);
    }

    // Cihaz kullanılmıyorsa sayacı boşuna işletme.
    // (Kahve molasındayken "mola ver" demek en sinir bozucu şey.)
    if (this.durum === 'calisiyor' || this.durum === 'uyari') {
      if (simdi - this.sonHareket > this.ayarlar.bostaEsigi * 1000) {
        this.kalanDondurulmus = this.kalanSaniye();
        this.durum = 'bosta';
        this._duyur('degisti', this.anlikDurum());
        return;
      }
      this.istatistik.ekranSuresi += 0.25;
      this.istatistik.kesintisizSure += 0.25;
    }
    if (this.durum === 'bosta') return;

    const kalan = (this.hedefZaman - simdi) / 1000;

    // Çalışma → Uyarı geçişi
    if (this.durum === 'calisiyor' && kalan <= this.ayarlar.uyariSuresi) {
      this.durum = 'uyari';
      this._duyur('uyari', Math.ceil(kalan));
      this._duyur('degisti', this.anlikDurum());
    }

    if (kalan <= 0) {
      if (this.durum === 'mola') {
        if (this.uzunMoladaMi) {
          this.istatistik.uzunMola++;
          this.istatistik.kesintisizSure = 0;   // uzun mola sayacı sıfırlar
          this.uzunMoladaMi = false;
        } else {
          this.istatistik.tamamlananMola++;
        }
        this._duyur('molaBitti', this.istatistik);

        // 2 saati aşan kesintisiz çalışma varsa uzun mola ÖNER (zorlama yok)
        if (this.ayarlar.uzunMolaAcik &&
            this.istatistik.kesintisizSure >= this.ayarlar.uzunMolaEsigi) {
          this._duyur('uzunMolaOnerisi', Math.round(this.istatistik.kesintisizSure));
        }
        this._asamayaGec('calisiyor', this.ayarlar.calismaSuresi);
      } else {
        this._asamayaGec('mola', this.ayarlar.molaSuresi);
      }
      return;
    }

    this._duyur('tik', this.anlikDurum());
  }

  /** Şu an çalışma saatleri içinde miyiz?
      Bitiş saati başlangıçtan küçükse gece yarısını aşan vardiya sayılır
      (örn. 22:00 — 04:00). */
  saatUygunMu(simdi = new Date()) {
    if (!this.ayarlar.saatlerAcik) return true;
    const dk = (s) => {
      const [a, b] = String(s || '0:0').split(':').map(Number);
      return (a || 0) * 60 + (b || 0);
    };
    const su = simdi.getHours() * 60 + simdi.getMinutes();
    const bas = dk(this.ayarlar.basSaat);
    const bit = dk(this.ayarlar.bitSaat);
    if (bas === bit) return true;                 // 24 saat
    return bas < bit ? (su >= bas && su < bit) : (su >= bas || su < bit);
  }

  /* ---------- Yardımcılar ---------- */
  _asamayaGec(yeniDurum, saniye) {
    this.durum = yeniDurum;
    this.asamaBaslangic = Date.now();
    this.hedefZaman = this.asamaBaslangic + saniye * 1000;
    this.kalanDondurulmus = null;
    if (yeniDurum === 'mola') this._duyur('molaBasladi', this.anlikDurum());
    this._duyur('degisti', this.anlikDurum());
  }

  kalanSaniye() {
    // Henüz başlamadıysa tam süreyi göster (00:00 değil)
    if (this.durum === 'hazir') return this.ayarlar.calismaSuresi;
    if (this.durum === 'duraklatildi' || this.durum === 'bosta') {
      return this.kalanDondurulmus ?? 0;
    }
    return Math.max(0, (this.hedefZaman - Date.now()) / 1000);
  }

  /** 0..1 arası ilerleme — halka animasyonu için */
  ilerleme() {
    const toplam = this.durum === 'mola'
      ? this.ayarlar.molaSuresi
      : this.ayarlar.calismaSuresi;
    return 1 - Math.min(1, this.kalanSaniye() / toplam);
  }

  anlikDurum() {
    return {
      durum: this.durum,
      kalan: this.kalanSaniye(),
      ilerleme: this.ilerleme(),
      istatistik: this.istatistik,
    };
  }

  _bugun() {
    // Sıfır doldurma ŞART: "2026-8-3" ile "2026-08-03" karışırsa
    // geçmiş kayıtları eşleşmez ve 7 gün grafiği boş çıkar.
    const d = new Date();
    const ik = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${ik(d.getMonth() + 1)}-${ik(d.getDate())}`;
  }

  /* ---------- Kayıt / geri yükleme ---------- */
  disaAktar() {
    return {
      ayarlar: this.ayarlar,
      istatistik: this.istatistik,
      hedefZaman: this.hedefZaman,
      durum: this.durum,
    };
  }

  iceAktar(veri) {
    if (!veri) return;
    if (veri.ayarlar) this.ayarlar = { ...this.ayarlar, ...veri.ayarlar };
    if (veri.istatistik) {
      // Gün değiştiyse günlük sayaçlar sıfırlanır
      if (veri.istatistik.gun === this._bugun()) {
        this.istatistik = veri.istatistik;
      }
    }
  }
}

/* ============================================================
   GEÇMİŞ — gün gün kayıt, 7 gün grafiği ve seri (streak)
   Masaüstü sürümündeki gecmis.py ile aynı mantık.
   ============================================================ */

const GUNLUK_HEDEF = 8;          // günde bu kadar mola = hedef tuttu
const SAKLANAN_GUN = 120;
const GUN_ADLARI = ['Paz', 'Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt'];

const Gecmis = {
  anahtar: 'goz-molasi-gecmis',

  oku() {
    try {
      const v = JSON.parse(localStorage.getItem(this.anahtar) || '{}');
      return (v && typeof v === 'object') ? v : {};
    } catch { return {}; }
  },

  yaz(veri) {
    // Dosya şişmesin: eskiyenleri at
    const sinir = this.gunAdi(new Date(Date.now() - SAKLANAN_GUN * 86400000));
    const temiz = {};
    for (const [g, d] of Object.entries(veri)) if (g >= sinir) temiz[g] = d;
    try { localStorage.setItem(this.anahtar, JSON.stringify(temiz)); } catch {}
  },

  gunAdi(t = new Date()) {
    return `${t.getFullYear()}-${String(t.getMonth() + 1).padStart(2, '0')}-${String(t.getDate()).padStart(2, '0')}`;
  },

  gunuIsle(gun, istatistik) {
    const veri = this.oku();
    veri[gun] = {
      mola: istatistik.tamamlananMola | 0,
      atlanan: istatistik.atlananMola | 0,
      ekran: Math.round(istatistik.ekranSuresi || 0),
    };
    this.yaz(veri);
  },

  /** Son N gün: [{ad, sayi, bugunMu}, ...] */
  sonGunler(adet = 7, bugunIstatistik = null) {
    const veri = this.oku();
    const bugun = new Date();
    const liste = [];
    for (let i = adet - 1; i >= 0; i--) {
      const t = new Date(bugun.getTime() - i * 86400000);
      const anahtar = this.gunAdi(t);
      const sayi = (i === 0 && bugunIstatistik)
        ? (bugunIstatistik.tamamlananMola | 0)
        : ((veri[anahtar] || {}).mola | 0);
      liste.push({ ad: GUN_ADLARI[t.getDay()], sayi, bugunMu: i === 0 });
    }
    return liste;
  },

  /** Kaç gündür üst üste hedefi tutturuyor?
      Bugün henüz hedefe ulaşmadıysa seri bozulmuş sayılmaz —
      sabahın köründe "serin bitti" demek haksızlık olur. */
  seri(bugunIstatistik = null, hedef = GUNLUK_HEDEF) {
    const veri = this.oku();
    const bugun = new Date();
    const sayiOku = (t, i) => (i === 0 && bugunIstatistik)
      ? (bugunIstatistik.tamamlananMola | 0)
      : ((veri[this.gunAdi(t)] || {}).mola | 0);

    let i = sayiOku(bugun, 0) >= hedef ? 0 : 1;
    let sayac = 0;
    while (i < SAKLANAN_GUN) {
      const t = new Date(bugun.getTime() - i * 86400000);
      if (sayiOku(t, i) >= hedef) { sayac++; i++; } else break;
    }
    return sayac;
  },
};

if (typeof module !== 'undefined') {
  module.exports = { MolaMotoru, VARSAYILAN_AYARLAR, Gecmis, GUNLUK_HEDEF };
}
