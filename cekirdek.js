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
  // SEKME KAPALIYKEN geçen süre için AYRI eşik. Neden ayrı:
  // masaüstünde program hep açık, orada '5 dakika girdi yok'
  // gerçekten 'gözler dinlendi' demek. Web'de sekmenin kapalı
  // olması kişinin ekrandan uzaklaştığını GÖSTERMEZ — sekme
  // değiştirmiş, başka pencereye geçmiş olabilir. 5 dakikayı
  // aynen uygulayınca kullanıcı uygulamayı her açtığında 20:00
  // görüyor ve mola hiç gelmiyordu. 20 dakika, normal bir
  // çalışma ritminde sekme kapatıp açmayı tolere ediyor.
  kapaliDevamEsigi: 1200,   // saniye — 20 dk
  /* UZUN UZAK KALMA SAYACI SIFIRLASIN MI?
     Varsayılan açık: 5 dakikadan uzun uzaklaşmada gözler gerçekten
     dinlenmiştir, sayacı baştan başlatmak doğrudur.

     Ama bu bizim kararımız ve kullanıcı katılmayabilir — haklı
     olabileceği bir yer var: telefonda başka uygulamaya geçmek
     "ekrandan uzaklaşmak" değildir, hâlâ ekrana bakılıyor.
     Kapatan kullanıcıda sayaç hiç sıfırlanmaz; geçen süre gerçek
     saatten hesaplanır ve mola hak edildiyse verilir. */
  uzakKalincaSifirla: true,
  molaAtlanabilir: false,   // VARSAYILAN: mola atlanamaz. 20 sn kesin.
  sesAcik: true,

  uzunMolaEsigi: 7200,      // saniye — 2 saat kesintisiz çalışma.
  // AOA "en yüksek risk" grubunu günde İKİ SAAT VE ÜZERİ kesintisiz
  // ekran kullananlar diye tanımlıyor; bir eşik değil, risk grubu.
  // Eskiden burada "AOA risk eşiği" yazıyordu — kaynağın söylediğini
  // eşiğe çeviren bu okuma, kullanıcıya gösterilen metne de geçmişti.
  uzunMolaSuresi: 300,      // saniye — 5 dakika
  uzunMolaAcik: false,      // uzun mola önerilsin mi

  // Çalışma saatleri: bu aralığın dışında hatırlatma gelmez.
  // Gece 23:00'te ders çalışan biri sabah 9'da mola istemez.
  saatlerAcik: false,
  basSaat: '09:00',
  bitSaat: '18:00',
};

/* SÜRE AYARLARININ SINIRLARI — tek yerde.

   Arayüzdeki kaydırıcı 0 girilmesine izin vermiyor ama ayarlar bir de
   DEPODAN geliyor ve orada doğrulama yoktu. Ölçüldü: `calismaSuresi`
   0 / negatif / null / NaN olunca uygulama doğrudan MOLA durumunda
   başlıyor ve mola hiç bitmiyor; `"yirmi"` yazınca ekranda `NaN:NaN`.

   Kullanıcı bunu arayüzden yapamaz — ama depo elle düzenlenebilir,
   eski sürümden bozuk veri gelebilir, başka bir sekme bozuk yazabilir.
   "Kullanıcı giremiyor" korumanın kendisi değil, yalnızca bir yolun
   kapalı olmasıdır.

   TEK SÜZGEÇ, İKİ ÇAĞRI YERİ: yapıcı ve `iceAktar`. İki ayrı
   doğrulama listesi er geç ayrışır — bu projede damgada tam bunu
   yaşadık. */
const SURE_SINIRLARI = {
  calismaSuresi:    [60, 4 * 3600],
  molaSuresi:       [5, 600],
  uyariSuresi:      [0, 300],
  bostaEsigi:       [10, 3600],
  dinlenmeEsigi:    [30, 4 * 3600],
  kapaliDevamEsigi: [30, 8 * 3600],
  uzunMolaEsigi:    [600, 12 * 3600],
  uzunMolaSuresi:   [30, 3600],
};

function ayarlariSuz(ayarlar) {
  const c = { ...ayarlar };
  for (const [ad, [enAz, enCok]] of Object.entries(SURE_SINIRLARI)) {
    if (!(ad in c)) continue;
    const s = Number(c[ad]);
    // Sayı değilse ya da aralık dışıysa varsayılana dön. Sessizce
    // kırpmak yerine varsayılan: 0 girilmişse niyet belirsizdir,
    // 60'a kırpmak kullanıcının istemediği bir değeri "seçilmiş"
    // gibi gösterirdi.
    c[ad] = (Number.isFinite(s) && s >= enAz && s <= enCok)
      ? s
      : VARSAYILAN_AYARLAR[ad];
  }
  return c;
}

/* İSTATİSTİK SINIRLARI — bir günde olabilecek en büyük değerler. */
const ISTATISTIK_SINIRLARI = {
  tamamlananMola: 1000,
  atlananMola: 1000,
  uzunMola: 1000,
  ekranSuresi: 86400,
  kesintisizSure: 86400,
};

const GUN_BICIMI = /^\d{4}-\d{2}-\d{2}$/;

/** Depodan gelen istatistiği süzer.

    Ölçüldü (29.08.2026): bozuk depoyla açılınca ekranda mola sayısı
    olarak "cok" ve "-3" yazıyordu. Ayarlar `ayarlariSuz()`ten geçiyor
    ama istatistik HAM atanıyordu — süzgeç, ayarların süzgecinin tam
    yanında eksikti.

    Ekranda görünen sayı bu; sessiz yanlış sayının tam merkezi. Negatif
    bir değer ayrıca seri hesabına ve 7 gün grafiğine de giriyordu. */
function istatistikSuz(ham) {
  const c = {};
  for (const [ad, enCok] of Object.entries(ISTATISTIK_SINIRLARI)) {
    const s = Number(ham && ham[ad]);
    // KIRPMIYORUZ, SIFIRLIYORUZ. Yanı başındaki `ayarlariSuz()` de
    // aynı gerekçeyle böyle: sınırın dışındaki bir değeri sınıra
    // çekmek, kullanıcıya MAKUL GÖRÜNEN bir yalan gösterir.
    // Ölçüldü: `atlananMola: 1e12` kırpılınca ekranda "1000 atlanan
    // mola" yazıyordu — bozuk veriden üretilmiş, inandırıcı bir sayı.
    // 0 hem doğru hem de "burada veri yok" diyor.
    c[ad] = (Number.isFinite(s) && s >= 0 && s <= enCok) ? s : 0;
  }
  const g = ham && ham.gun;
  c.gun = (typeof g === 'string' && GUN_BICIMI.test(g)) ? g : null;
  return c;
}

class MolaMotoru {
  constructor(ayarlar = {}) {
    this.ayarlar = ayarlariSuz({ ...VARSAYILAN_AYARLAR, ...ayarlar });
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
    this._isci = null;      // arka planda kısılmayan kalp atışı
  }

  /* ---------- Olay sistemi (arayüz buradan haber alır) ---------- */
  /** Bu sekme sayacı işletmesin mi? Çok sekmeli kullanımda
      yalnızca lider sekme işletir. */
  askida = false;

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
    this._kalpAtisiBaslat();
    this._duyur('basladi');
  }

  /** Kalp atışını başlat.

      NEDEN WORKER? Tarayıcı, arka plandaki sekmenin setInterval'ini
      dakikada bire kadar yavaşlatıyor. Ölçtüm: sekme arka plandayken
      sayaç sıfıra ulaştığı hâlde mola bitmiyordu — 20 saniyelik mola
      bir dakikaya kadar uzayabiliyor.

      Bu tam da uygulamanın tasarlandığı durum: "gözünü ekrandan ayır"
      dediğimiz kişi başka pencereye geçiyor, sekme arka plana düşüyor.
      Molanın zamanında bitmesi şart.

      Worker'lar bu kısıtlamaya tabi değil. Worker kurulamazsa
      (eski tarayıcı, katı güvenlik ayarı) setInterval'e düşüyoruz —
      o zaman mola geç bitebilir ama çalışmaya devam eder. */
  _kalpAtisiBaslat() {
    // Askıdaki sekme, durum geçişi olsa bile sayacı işletmez.
    if (this.askida) return;
    if (this._zamanlayici || this._isci) return;

    try {
      const kod = 'let z=null;onmessage=e=>{' +
                  'if(e.data==="dur"){clearInterval(z);z=null;return;}' +
                  'if(!z)z=setInterval(()=>postMessage(1),250);};';
      const url = URL.createObjectURL(new Blob([kod], { type: 'text/javascript' }));
      this._isci = new Worker(url);
      URL.revokeObjectURL(url);
      this._isci.onmessage = () => this.tik();
      this._isci.postMessage('basla');
      return;
    } catch {
      this._isci = null;
    }

    // 250ms: göze akıcı gelir, pili yormaz.
    this._zamanlayici = setInterval(() => this.tik(), 250);
  }

  _kalpAtisiDurdur() {
    if (this._isci) {
      try { this._isci.postMessage('dur'); this._isci.terminate(); } catch {}
      this._isci = null;
    }
    if (this._zamanlayici) {
      clearInterval(this._zamanlayici);
      this._zamanlayici = null;
    }
  }

  /**
   * Duraklat. `saniye` verilirse SÜRELİ duraklatma olur ve süre
   * dolunca kendiliğinden devam eder.
   *
   * NEDEN DUVAR SAATİ, ZAMANLAYICI DEĞİL:
   * Önceden bu iş arayüzde `setTimeout` ile yapılıyordu ve sekme
   * kapanınca zamanlayıcı ölüyordu. Ölçüldü: kullanıcı "5 dakika
   * duraklat" diyor, sekmeyi kapatıyor, geri dönüyor ve uygulama
   * KALICI olarak duraklamış oluyordu. Ekranda her şey normal
   * görünüyor ama bir daha hiç mola gelmiyor.
   *
   * Bitiş ANI saklanınca çalışan bir zamanlayıcıya gerek kalmıyor:
   * sekme kapalıyken de saat ilerliyor. Masaüstü sürümü bunu zaten
   * böyle yapıyor (`duraklama_bitis`).
   */
  duraklat(saniye = 0) {
    if (this.durum === 'mola') return;          // mola duraklatılamaz
    this.kalanDondurulmus = this.kalanSaniye();
    this.oncekiDurum = this.durum;
    this.durum = 'duraklatildi';
    const sn = Number(saniye);
    this.duraklatmaBitis = (Number.isFinite(sn) && sn > 0)
      ? Date.now() + sn * 1000
      : 0;                                      // 0 = süresiz
    this._duyur('degisti', this.anlikDurum());
  }

  /** Süreli duraklatmanın bitmesi gerekiyor mu? */
  duraklatmaDoldu() {
    return this.durum === 'duraklatildi'
      && this.duraklatmaBitis > 0
      && Date.now() >= this.duraklatmaBitis;
  }

  devamEt() {
    if (this.durum !== 'duraklatildi' && this.durum !== 'bosta') return;
    this.duraklatmaBitis = 0;
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
      // Sayacı sıfırlamak "gözlerin dinlendi, baştan başla" demektir.
      // Bunu YALNIZCA gerçekten uzaklaşıldıysa yapmalı: ekran
      // kilitlendiyse (kesin kanıt) ya da girdi eşiğin epey üstünde
      // bir süre gelmediyse.
      //
      // Eskiden tek ölçüt 5 dakika hareketsizlikti. Ama "klavyeye
      // dokunmadı" ile "makineden uzaklaştı" aynı şey değil: uzun bir
      // metni okuyan biri ekrana bakıyor — tam da mola gereken durum —
      // ve sayacı sıfırlanıyordu. Masaüstü sürümünde ölçtüm: 132
      // dakika ekran süresine karşılık 0 mola.
      const uzunEsik = Math.max(this.ayarlar.dinlenmeEsigi, 900) * 1000;
      const gercektenUzaklasti = this.ekranKilitlendi || uzaktaKalinan > uzunEsik;
      this.ekranKilitlendi = false;
      if (gercektenUzaklasti) {
        this.istatistik.kesintisizSure = 0;   // gerçekten dinlenildi
        this._duyur('dinlenildi', Math.round(uzaktaKalinan / 1000));
        this.sifirla();
      } else {
        this.devamEt();
      }
    }
  }

  /** Ekran kilitlendi — kişi gerçekten uzaklaştı demektir.
      IdleDetector izni verilmişse arayüz bunu bildiriyor. */
  ekranKilitlendiBildir() {
    this.ekranKilitlendi = true;
  }

  /* ---------- Kalp atışı ---------- */
  /* GÜN DEĞİŞTİ Mİ? Sekme açıkken de bakılmalı.

     Gün karşılaştırması yalnızca `iceAktar` içinde vardı, yani
     AÇILIŞTA. Bu uygulama açık bırakılmak için yapılmış bir sayaç;
     gece yarısını açık geçmek normal kullanımdır.

     Ölçüldü: sekme gece yarısını açık geçince `istatistik.gun` dünde
     kalıyor ve BUGÜNÜN molaları DÜNE yazılıyor. Bugün 0 görünüyor,
     dün şişiyor. Çökme yok, uyarı yok — sadece yanlış sayı.

     Kalıcı geçmişe artık `Math.max` ile yazdığımız için şişen dünkü
     sayı geri de alınamıyordu: bir düzeltme, başka bir hatanın
     sonucunu kalıcı yapmıştı. İkisi birlikte kapanmalıydı. */
  _gunuTazele() {
    const bugun = this._bugun();
    if (this.istatistik.gun === bugun) return false;
    this.istatistik.gun = bugun;
    this.istatistik.tamamlananMola = 0;
    this.istatistik.atlananMola = 0;
    this.istatistik.ekranSuresi = 0;
    this.istatistik.uzunMola = 0;
    // `kesintisizSure` SIFIRLANMAZ: gece yarısı geçti diye kişinin
    // kesintisiz çalışması bitmiş olmuyor.
    return true;
  }

  /* ASKIYA ALMA — bu sekme sayacı İŞLETMESİN.

     Neden gerekli: `liderligiBirak()` ikinci sekmede kalp atışını
     durduruyordu, ama `_asamayaGec()` HER durum geçişinde kalp
     atışını yeniden başlatıyor (o da ayrı bir düzeltmeydi: kayıttan
     geri yüklenen sayaç hiç işlemiyordu). İki koruma birbirini
     iptal ediyordu.

     Ölçüldü (28.08.2026): iki sekme açıkken ikinci sekme kendini
     "ikinci sekme" olarak gösteriyor AMA sayacı işliyordu; üstelik
     liderden 8 saniye ayrışmıştı — aynı uygulamanın iki penceresi
     iki ayrı sayı gösteriyordu.

     Tek bayrak, tek boğaz: `tik()` ve `_kalpAtisiBaslat()` ikisi de
     bayrağa bakıyor. Böylece hangi yoldan gelinirse gelinsin askıya
     alınmış sekme sayacı ilerletemez. */
  askiyaAl() {
    this.askida = true;
    this._kalpAtisiDurdur();
  }

  askidanCikar() {
    this.askida = false;
  }

  tik() {
    if (this.askida) return;
    if (this._gunuTazele()) this._duyur('degisti', this.anlikDurum());

    // SÜRELİ DURAKLATMA BİTTİ Mİ? Bu satır olmadan süre dolsa bile
    // sayaç duraklamış kalıyordu — `tik` duraklatıldı durumunda hemen
    // dönüyor ve kimse süreyi kontrol etmiyordu.
    if (this.duraklatmaDoldu()) {
      this.devamEt();
      this._duyur('degisti', this.anlikDurum());
      return;
    }
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

  /**
   * KÖPRÜ DEVRALMA — Windows sürümünden gelen CANLI sayacı benimser.
   *
   * NEDEN AYRI BİR YOL: Önce `sayaciGeriYukle` kullanılıyordu ve bu
   * ciddi bir tasarım hatasıydı. O işlev "sekme KAPALIYDI, diskteki
   * anlık görüntüden devam et" durumu için yazılmış; içinde iki kural
   * var ve ikisi de canlı veride zararlı:
   *
   *   1. `kalan <= 0` ise "kaçırılmış mola" sayıp 25 saniye sonraya
   *      mola kuruyor. Windows boştayken köprü 0 gönderiyordu (orada
   *      sayaç donuyor ama `hedef` ilerlemiyordu) — tarayıcı 25
   *      saniyede bir sahte mola veriyordu. Öğle molasında ~50 sahte
   *      mola, hepsi istatistiğe KALICI yazılıyordu.
   *   2. `kalan > calismaSuresi` ise reddediyor. Masaüstünde "Ders"
   *      kipi (25 dk) seçiliyse tarayıcının 20 dk sınırını aşıyor ve
   *      devralma HER SEFERİNDE sessizce başarısız oluyordu.
   *
   * Köprü canlı ve yetkili bir kaynak; diskten okunan bayat bir
   * görüntü değil. O yüzden hiçbir tahmin kuralı uygulanmaz:
   * gelen sayı NE İSE o kurulur.
   *
   * Çağıran taraf `sayiyor` alanını kontrol etmekle yükümlü —
   * Windows saymıyorken burası çağrılmamalı.
   */
  kopruyuBenimse(kalanSn) {
    const kalan = Number(kalanSn);
    if (!Number.isFinite(kalan) || kalan < 0) return false;
    this._asamayaGec('calisiyor', kalan);
    return true;
  }

  /* ---------- Yardımcılar ---------- */
  _asamayaGec(yeniDurum, saniye) {
    this.durum = yeniDurum;
    this.asamaBaslangic = Date.now();
    this.hedefZaman = this.asamaBaslangic + saniye * 1000;
    this.kalanDondurulmus = null;
    // Kalp atışı BURADA başlıyor, yalnızca basla() içinde değil.
    // Önceden yalnızca basla() başlatıyordu; sayaç kayıttan geri
    // yüklendiğinde basla() çalışmadığı için kalp atışı hiç
    // başlamıyor, sayaç ekranda duruyor gibi görünüp mola HİÇ
    // gelmiyordu. Sayfayı yenileyen herkes bundan etkileniyordu.
    this._kalpAtisiBaslat();
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
      // Süreli duraklatmanın bitiş anı. Sekme kapalıyken saat
      // ilerlediği için, açılışta süre dolmuşsa devam edilir.
      duraklatmaBitis: this.duraklatmaBitis || 0,
      kalanDondurulmus: this.kalanDondurulmus ?? null,
      // Ne zaman kaydedildi — geri yüklerken "ne kadar kapalı kaldı"
      // sorusunun cevabı bu.
      kayitAni: Date.now(),
      /* SAAT DİLİMİ FARKI. Yaz saati geçişinde ya da kullanıcı
         saati elle değiştirince `Date.now()` sıçrar ve geçen süre
         YANLIŞ hesaplanır. Ölçüldü: saat 1 saat ileri alınınca
         uygulama "60 dakika kapalıydı" diyordu — kullanıcı hiç
         ayrılmamışken. Fark değiştiyse ölçümün güvenilmez
         olduğunu biliyoruz ve öyle söylüyoruz. */
      saatFarki: new Date().getTimezoneOffset(),
    };
  }

  iceAktar(veri) {
    if (!veri) return;
    // Depodan gelen ayar da süzgeçten geçer — asıl bozuk veri
    // buradan giriyordu.
    if (veri.ayarlar) {
      this.ayarlar = ayarlariSuz({ ...this.ayarlar, ...veri.ayarlar });
    }
    if (veri.istatistik) {
      // Gün değiştiyse günlük sayaçlar sıfırlanır.
      // SÜZGEÇ ŞART: bozuk depo doğrudan EKRANA çıkıyordu
      // (ölçüldü — "cok" ve "-3" mola sayısı olarak görünüyordu).
      const temiz = istatistikSuz(veri.istatistik);
      if (temiz.gun && temiz.gun === this._bugun()) {
        this.istatistik = temiz;
      }
    }
    this.geriYuklendi = this.sayaciGeriYukle(veri);
  }

  /** Kalan süreyi kayıttan geri yükler.

      Eskiden disaAktar hedefZaman ve durum'u YAZIYOR ama iceAktar
      onları HİÇ OKUMUYORDU. Sonuç: sayfa her açıldığında sayaç
      sıfırdan başlıyordu ve iki sekme açıksa ikisi birbirinin
      kaydını eziyordu. Masaüstü sürümünde aynı hata durum.json ile
      çözülmüştü; web tarafına bakılmamış.

      Kurallar (masaüstündekiyle aynı):
        • Kapalı kalınan süre dinlenme eşiğinden uzunsa gözler zaten
          dinlenmiştir — temiz bir süre başlar.
        • Hedef henüz geçmemişse kaldığı yerden devam eder.
        • Hedef kapalıyken geçtiyse: kısa kapanmaysa molayı kısa bir
          payla verir, uzun kapanmaysa temiz başlar. */
  sayaciGeriYukle(veri) {
    /* Her cagride bayraklar sifirlanir. Bu islev birden fazla kez
       cagrilabiliyor; onceki cagridan kalan bir bayrak, ekranla
       CELISEN bir cumle yazdiriyordu. */
    this.sifirlanmaSebebi = null;
    this.gecikmisMola = null;
    const hedef = +veri.hedefZaman;
    const kayitAni = +veri.kayitAni;
    if (!Number.isFinite(hedef) || !Number.isFinite(kayitAni)) return false;
    /* Mola ekranı açıkken kapanmışsa sayaç geri yüklenmiyor —
       molanın ortasından devam etmenin anlamı yok. AMA sebebi
       yazıyoruz: eskiden bu satır sebebi KURMADAN dönüyordu ve
       kullanıcı sayacın neden başa döndüğünü hiç öğrenmiyordu.
       Sessiz sıfırlama, kullanıcıya "bozuk" gibi görünüyor. */
    if (veri.durum === 'mola' || veri.durum === 'hazir') {
      this.sifirlanmaSebebi = {
        tur: 'mola-sirasinda',
        dakika: Math.round((Date.now() - kayitAni) / 60000),
      };
      return false;
    }

    const simdi = Date.now();
    const kapaliKalan = (simdi - kayitAni) / 1000;
    // Sekme kapalıyken geçen süre için dinlenmeEsigi DEĞİL
    // kapaliDevamEsigi kullanılır — sebebi ayarın yanında yazılı.
    /* SAAT AYARI DEĞİŞMİŞ Mİ? Değiştiyse "ne kadar kapalı kaldı"
       ölçümü güvenilmez: yaz saati geçişi ya da elle saat değişimi
       geçen süreyi olduğundan büyük/küçük gösterir. Kullanıcıya
       "kapalıydın" demek YANLIŞ olur — hiç ayrılmamış olabilir. */
    const eskiFark = veri.saatFarki;
    const saatDegisti = Number.isFinite(+eskiFark)
      && +eskiFark !== new Date().getTimezoneOffset();

    /* Kullanıcı "uzak kalınca sıfırlama" ayarını kapattıysa süre
       sınırı yok: ne kadar uzak kalırsa kalsın sayaç devam eder.
       Saatin geriye alınması (kapaliKalan < 0) yine ayrı tutuluyor —
       o bir tercih değil, bozuk veri. */
    const sifirlansin = this.ayarlar.uzakKalincaSifirla !== false;
    const esik = sifirlansin
      ? (this.ayarlar.kapaliDevamEsigi || this.ayarlar.dinlenmeEsigi)
      : Infinity;
    if (kapaliKalan < 0 || kapaliKalan > esik) {
      // Kullanıcıya NEDEN sıfırlandığını söyleyebilmek için sebebi
      // tutuyoruz. Sessizce sıfırlanan sayaç "bozuk" gibi duruyor.
      this.sifirlanmaSebebi = saatDegisti
        ? { tur: 'saat-degisti' }
        : { tur: 'uzun-kapali', dakika: Math.round(kapaliKalan / 60) };
      return false;
    }

    const kalan = (hedef - simdi) / 1000;
    if (kalan > 0 && kalan <= this.ayarlar.calismaSuresi) {
      this._kalpAtisiBaslat();
      this.hedefZaman = hedef;
      /* SURELI DURAKLATMA sekme kapaliyken de biter.
         Olculdu: eskiden "5 dakika duraklat" deyip sekmeyi kapatan
         kullanici geri donunce KALICI olarak duraklamis oluyordu -
         sureyi geri acacak setTimeout sekmeyle birlikte olmustu.
         Bitis ANI saklandigi icin artik calisan bir zamanlayiciya
         gerek yok: saat sekme kapaliyken de ilerledi. */
      const bitis = +veri.duraklatmaBitis || 0;
      const sureDoldu = bitis > 0 && simdi >= bitis;
      this.durum = (veri.durum === 'duraklatildi' && !sureDoldu)
        ? 'duraklatildi' : 'calisiyor';
      if (this.durum === 'duraklatildi') {
        this.duraklatmaBitis = bitis;
        // Kaydedilmis donmus deger varsa ONU kullan: duraklatilmis
        // sayacta `hedef - simdi` ilerlemeye devam eder ve kalan
        // sureyi sessizce eritir.
        const donmus = +veri.kalanDondurulmus;
        this.kalanDondurulmus = Number.isFinite(donmus) && donmus > 0
          ? donmus : kalan;
      } else {
        this.duraklatmaBitis = 0;
      }
      this.sonHareket = simdi;
      return true;
    }
    /* MOLA SEN UZAKTAYKEN GELDİ.

       Bu pencere 60 SANİYEYDİ ve telefondaki asıl hata buydu: molanın
       düştüğü andan itibaren bir dakika içinde dönmediysen sayaç başa
       sarıyordu. Başka bir uygulamaya geçip dönmek dakikalar sürer,
       yani telefonda bu pencere pratikte hiç tutmuyordu. Kullanıcının
       gördüğü şey "sayaç hep yeniden başlıyor" ve "mola hiç gelmiyor"
       oluyordu — ölçüldü: 25 dk uzak kalınca ekran 20:00.

       Yeni pencere `dinlenmeEsigi`. O ayarın tanımı zaten bu: bundan
       kısa bir uzaklaşmada gözler dinlenmiş sayılmaz. Mola hâlâ borç,
       o yüzden veriliyor. */
    /* Ayar kapalıyken pencere sınırsız: mola ne zaman düşmüş olursa
       olsun, dönüşte veriliyor. Kullanıcının istediği tam buydu —
       "kapansa bile molalar çalışsın". */
    const molaPenceresi = (this.ayarlar.uzakKalincaSifirla === false)
      ? Infinity
      : (this.ayarlar.dinlenmeEsigi || 300);
    if (kalan <= 0 && kapaliKalan <= molaPenceresi) {
      this._kalpAtisiBaslat();
      this.hedefZaman = simdi + 25000;
      this.durum = 'calisiyor';
      this.sonHareket = simdi;
      this.gecikmisMola = { dakika: Math.round(kapaliKalan / 60) };
      return true;
    }

    /* Buraya düşmek = gerçekten uzun kalınmış. Sayaç temiz başlıyor ve
       bu DOĞRU: o kadar süre uzaktaysan gözlerin dinlendi. Yanlış olan,
       eskiden bunun sessizce olmasıydı. */
    this.sifirlanmaSebebi = saatDegisti
      ? { tur: 'saat-degisti' }
      : { tur: 'uzun-kapali', dakika: Math.round(kapaliKalan / 60) };
    return false;
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

  /* ARTAN SAYAÇLAR ASLA AZALMAZ.

     Ölçüldü (iki sekme): B sekmesinde 9 mola birikti ve kayda yazıldı.
     Sonra hâlâ 3'te olan ESKİ A sekmesi kapandı; `pagehide` → `kaydet()`
     → günlük geçmiş 3'e GERİ DÖNDÜ. Kayıp oturumluk değil KALICI:
     7 gün grafiği ve seri sayısı buradan besleniyor, yani kullanıcı
     kendini gerçekte olduğundan az dinlenmiş sanıyor.

     Çökme yok, uyarı yok — sadece yanlış sayı. Sessiz yanlış sayının
     tam tanımı.

     Bir günün tamamlanmış mola sayısı geriye gidemez; hangi sekme
     yazarsa yazsın büyük olan kalır. Doğru gün için doğru: aynı gün
     içinde bu sayılar yalnızca artar. */
  gunuIsle(gun, istatistik) {
    const veri = this.oku();
    const eski = veri[gun] || {};
    const buyuk = (a, b) => Math.max(a | 0, b | 0);
    veri[gun] = {
      mola: buyuk(eski.mola, istatistik.tamamlananMola),
      atlanan: buyuk(eski.atlanan, istatistik.atlananMola),
      ekran: buyuk(eski.ekran, Math.round(istatistik.ekranSuresi || 0)),
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
  /* Seri, SAKLANAN_GUN'e takılabilir: daha eski veri silindiği için
     bilinemez. Arayüz bunu "120+" diye göstersin diye pencereyi
     dışarı açıyoruz. Ölçüldü: 3 yıllık kesintisiz seri "120 gün"
     görünüyordu — yanlış değil ama EKSİK, ve eksik olduğu
     söylenmiyordu. */
  saklananGun: SAKLANAN_GUN,

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
  module.exports = { MolaMotoru, VARSAYILAN_AYARLAR, Gecmis, GUNLUK_HEDEF,
                     istatistikSuz };
}
