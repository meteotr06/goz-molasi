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

/** '21:30' -> 1290 dakika. Okunamazsa null — ASLA 0 değil.

    Masaüstünde (30.08.2026) tam buradan bir hata çıktı: saat okunamayınca
    sessizce 0 dönüyordu, yani yasak penceresi 00:00'a kayıyordu. Ebeveyn
    "21:00" yazdığını sanıyor, çocuk her gece serbest kalıyordu. Okunamayan
    değer null döner ve çağıran bunu AYRI bir durum olarak ele alır. */
function dakikaOku(metin) {
  const m = /^(\d{1,2}):(\d{2})$/.exec(String(metin ?? '').trim());
  if (!m) return null;
  const s = +m[1], d = +m[2];
  if (s > 23 || d > 59) return null;
  return s * 60 + d;
}

const VARSAYILAN_AYARLAR = {
  /* ---- AİLE KİPİ ----
     Windows sürümünün karşılığı, ama ZAYIF olanı. Orada bekçi süreç
     var: program öldürülünce geri açılıyor. Tarayıcıda bu YOK — çocuk
     başka tarayıcı açabilir, gizli sekme kullanabilir, site verilerini
     silebilir.

     Bu yüzden ekranda "kilit" demiyoruz, "sınır" diyoruz. Olmayan bir
     korumaya güvendirmek, hiç koruma koymamaktan kötüdür: ebeveyn
     çocuğun kısıtlı olduğunu sanır ve bakmayı bırakır. */
  kip: 'bireysel',          // 'bireysel' | 'aile'
  gunlukSinirDk: 0,         // 0 = sınır yok
  yasakAcik: false,
  yasakBas: '21:00',
  yasakBit: '07:00',
  ekSureBitis: 0,           // ebeveyn verdiyse: bu ana kadar engel yok
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
  /* Gunluk mola hedefi. Once `GUNLUK_HEDEF` sabitiydi; seri,
     haftalik grafik ve etiketler hep ona bakiyordu. Artik
     kullanici seciyor ve TEK KAYNAK burasi. */
  gunlukHedef: 8,
  /* Mola ekrani gorunumu. Karartma 0..0.55 - tam karartma mola
     ekranindaki sayiyi ve ipucunu da okunmaz yapar. */
  molaKarartma: 0.15,
  molaIcerik: 'tam',        // 'tam' | 'sayac' | 'nefes'
  molaSesTonu: 'yumusak',   // 'yumusak' | 'zil' | 'yok'
  saatlerAcik: false,
  /* HAFTA SONU. 'ayni' = hafta ici ile ayni · 'kapali' = sayac hic
     islemez · 'ayri' = kendi saat araligi. Tek ayar, uc secenek. */
  haftaSonu: 'ayni',
  haftaSonuBas: '11:00',
  haftaSonuBit: '20:00',
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
    /* "KAPALI" BIR ARALIK DISI DEGER DEGIL, BIR SECIMDIR.

       `bostaEsigi` kapatildiginda arayuz 1e9 yaziyor ("bir daha asla
       bosta sayma"). Bu deger [10, 3600] araliginin disinda oldugu
       icin asagidaki kural onu VARSAYILANA (90) ceviriyordu: kutu
       "kapali" gorunurken motor 90 saniyelik esikle calisiyordu.

       OLCULDU (03.09.2026, gercek formdan): kutu kapatildi, kayda
       1000000000 yazildi, yenilemeden sonra kutu False gorunuyor ama
       `molaMotoru.ayarlar.bostaEsigi` = 90. Ayar yalan soyluyordu.

       Kullanicinin kapattigi bir ayari sessizce geri acmak, hic
       kapatilamamasindan kotudur: kullanici kapattigini SANIYOR. */
    const kapaliSecimi = (ad === 'bostaEsigi' && s >= enCok * 1000);
    c[ad] = (kapaliSecimi || (Number.isFinite(s) && s >= enAz && s <= enCok))
      ? s
      : VARSAYILAN_AYARLAR[ad];
  }
  return c;
}

/* İSTATİSTİK SINIRLARI — bir günde olabilecek en büyük değerler. */
// Gunluk hedef 1..30: bir gunde 30'dan cok mola hedeflemek
// gercekci degil, 0 ise hedef diye bir sey kalmaz.
SURE_SINIRLARI.gunlukHedef = [1, 30];
// Karartma 0..0.55: ustu metni okunmaz yapiyor.
SURE_SINIRLARI.molaKarartma = [0, 0.55];

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
  /* SAATLIK DIZI — acikca ele alinmali.

     Bu islev yalnizca `ISTATISTIK_SINIRLARI` anahtarlarini kopyaliyor;
     kural yazilmasaydi `saatlik` her geri yuklemede SESSIZCE DUSER,
     grafik de her acilista bosalirdi. Sebebi de kimse bulamazdi.

     Bozuk kova sifirlanir, kirpilmaz - yanindaki sayilarla ayni
     gerekce: sinira cekmek "makul gorunen bir yalan" uretir. */
  const s24 = ham && ham.saatlik;
  c.saatlik = new Array(24).fill(0);
  if (Array.isArray(s24)) {
    for (let i = 0; i < 24; i++) {
      const v = Number(s24[i]);
      c.saatlik[i] = (Number.isFinite(v) && v >= 0 && v <= 3600) ? v : 0;
    }
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
      /* Saatlik dagilim: 24 kova, her biri o saatte gecen saniye.
         `ekranSuresi` ile AYNI yerde artiyor ki ikisi ayrisamasin. */
      saatlik: new Array(24).fill(0),
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
  /* Ikinci bir deger tasiyabiliyor. Sebebi olculdu: `molaBitti`
     dinleyicisi molanin UZUN mu oldugunu `this.uzunMoladaMi`den
     okuyordu, ama cekirdek o bayragi duyurudan ONCE sifirliyor -
     dinleyici her zaman false goruyor ve bes dakikalik uzun mola
     25 yerine 10 puan getiriyordu. Bir bilgiyi dinleyiciye TAHMIN
     ETTIRMEK yerine olayla birlikte GONDERIYORUZ. */
  _duyur(olay, veri, ek) {
    (this.dinleyiciler[olay] || []).forEach((fn) => fn(veri, ek));
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
    return this._molayiAtlayarakBitir();
  }

  /** ACİL ÇIKIŞ — "mola atlanabilsin" KAPALI iken bile molayı bitirir.

      Neden var: ayar kapalıyken çıkış yolu hiç yoktu ve mola süresi
      üç dakikaya, uzun mola yirmi dakikaya çıkabiliyor. Telefonda
      yirmi dakikalık, çıkılamayan tam ekran demekti. Arayüz bu yolu
      yalnızca molanın 20. saniyesinden sonra ve basılı tutunca açıyor;
      çekirdek tarafında bir eşik yok, karar tek yerde (arayüzde)
      kalsın diye — iki eşik iki ayrı doğru demekti.

      İstatistikte ATLANAN MOLA sayılır: yapılmamış bir molayı
      yapılmış saymak istatistiği yalancı yapardı. */
  molayiAcilBitir() {
    if (this.durum !== 'mola') return false;
    return this._molayiAtlayarakBitir();
  }

  /** Atlama ve acil çıkışın ORTAK gövdesi — tek yer.
      İkiye ayırmak, yarın birine eklenen bir satırın öbüründe
      unutulması demekti. */
  _molayiAtlayarakBitir() {
    this.istatistik.atlananMola++;
    /* UZUN MOLA BAYRAGI BURADA DA TEMIZLENIYOR.

       Eskiden bayragi yalnizca mola TAMAMLANINCA (tik icinde) false
       yapiyorduk. Uzun molayi ATLAYAN biri icin bayrak true kaliyor
       ve bir SONRAKI normal mola "uzun mola" sayiliyordu: tamamlanan
       mola artmiyor, yedi gun grafiginde bugunun cubugu buyumuyor,
       seri ilerlemiyor. Ustelik `kesintisizSure` sifirlanip iki
       saatlik uzun mola sayaci basa donuyordu - kisi hic
       dinlenmedigi halde.

       Atlanan mola `uzunMola` sayilmiyor: yapilmamis bir mola
       yapilmis sayilamaz. `kesintisizSure`ye de dokunulmuyor -
       dinlenilmedi. */
    this.uzunMoladaMi = false;
    this._duyur('molaAtlandi', this.istatistik);
    this._asamayaGec('calisiyor', this.ayarlar.calismaSuresi);
    return true;
  }

  /** Molayı ertele — mola en az `saniye` sonraya kalsın.

      ERTELEME KISALTAMAZ. Eskiden kalan süreyi doğrudan `saniye`ye
      AYARLIYORDU: yirmi dakika kalmışken "5 dk ertele" demek süreyi
      5 dakikaya indiriyor, yani molayı on beş dakika ÖNE çekiyordu.
      Düğmenin adı "ertele" olduğu için kullanıcı bunun tersini bekler
      ve ekranda gördüğü sayı da o an değişip gider.
      ÖLÇÜLDÜ (04.09.2026): 1199 sn -> 299 sn.

      Amaçlanan yolda (uyarı balonu, ~15 sn kala) sonuç aynı kalıyor:
      max(15, 300) = 300. Yani düzeltme doğru davranışı bozmuyor,
      yalnızca yanlış olanı imkânsız kılıyor. */
  ertele(saniye) {
    if (this.durum !== 'calisiyor' && this.durum !== 'uyari') return false;
    const hedef = Math.max(this.kalanSaniye(), +saniye || 0);
    this._asamayaGec('calisiyor', hedef);
    this._duyur('ertelendi', hedef);
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
        /* SIFIRLANDI MI, OLAYLA BIRLIKTE GIDIYOR.

           Olay sifirlama KARARINDAN ONCE yayiliyordu ve arayuz
           kosulsuz "sayac bastan basladi" yaziyordu. Telefon
           varsayilaninda (`uzakKalincaSifirla: false`) o dalda
           `sifirla()` degil `devamEt()` cagriliyor - yani sayac
           kaldigi yerden devam etmisken kullaniciya sifirlandigi
           soyleniyordu. Kullanicinin aylardir bildirdigi "sayac
           sifirlaniyor" sikayetinin bir kismi bu CUMLEDEN geliyor
           olabilir: sayi dogru, cumle yanlis. */
        const sifirlanacak = this.ayarlar.uzakKalincaSifirla !== false;
        this._duyur('dinlenildi', Math.round(uzaktaKalinan / 1000),
                    sifirlanacak);
        /* AYARA BAK — "uzun süre uzak kalınca sıfırla" KAPALI olabilir.

           Bu canlı yol o ayara HİÇ bakmıyordu. `sayaciGeriYukle` (kapat-aç
           yolu) bakıyor, burası bakmıyordu; yani aynı ayar iki yolda iki
           türlü davranıyordu.

           Neden ağır: TELEFONDA bu ayar VARSAYILAN KAPALI (dokunmatik
           göçü, arayuz.js). Yani kullanıcı hiç dokunmadan "sıfırlama"
           demiş oluyor, ama uygulama açıkken telefon cebe girip 15+
           dakika sonra çıkınca sayaç yine de başa dönüyordu.

           ÖLÇÜLDÜ (03.09.2026): ayar AÇIK -> 1200 sn (sıfırlandı),
           ayar KAPALI -> 1200 sn (yine sıfırlandı). İki dal aynı.

           Kullanıcının aylardır bildirdiği "sayaç kendini sıfırlıyor"
           şikâyetinin kaynağı büyük olasılıkla burası. Dün gece
           üretememiştim çünkü kapat-aç yolunu ölçmüştüm — o yol zaten
           doğruydu.

           `kesintisizSure` yine sıfırlanıyor: kişi gerçekten uzaktaydı,
           bu bir OLGU. Ayar sayacı ilgilendiriyor, istatistiği değil. */
        if (this.ayarlar.uzakKalincaSifirla === false) {
          this.devamEt();
        } else {
          this.sifirla();
        }
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
    this.istatistik.saatlik = new Array(24).fill(0);
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
    /* GUN DEGISIMI BURADA DA DENETLENIYOR.

       `_gunuTazele()` YALNIZ `tik()` icinden cagriliyordu ve o cagri
       `askida` denetiminin ARDINDAYDI: askiya alinmis bir sekme gun
       degisimini HIC gormuyordu. Aksamdan acik kalmis ikinci sekme
       ertesi gun hala `istatistik.gun = DUN` tasiyor; liderligi
       devralinca dunun sayilariyla yazmaya basliyordu. Gun damgalari
       uyusmadigi icin `kaydet()`in "artan sayaclar azalmaz"
       birlestirmesi de atlaniyor - koruma tam ihtiyac duyulan anda
       devre disi kaliyordu.

       Askidan cikmak, "bu sekme yeniden sorumlu" demek; sorumlulugu
       almadan once hangi gunde oldugunu bilmeli. */
    if (this._gunuTazele()) this._duyur('degisti', this.anlikDurum());
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
      /* EKRAN GÖRÜNÜYORSA GÖZ ÇALIŞIYOR — DOKUNMASA DA.

         KULLANICININ BİLDİRDİĞİ KUSUR (03.09.2026): "süresi sıfırlanıyor
         ve mola kolayca devreye girmiyor — en çok mobilde ama bütün
         cihazlarda."

         ÖLÇÜLDÜ (telefon kipinde, sayfa GÖRÜNÜR, kullanıcı okuyor ve
         dokunmuyor): 90 saniye sonra durum `bosta` oldu ve sayaç
         1106 saniyede DONDU. Bir daha inmedi. Yani mola hiç gelmiyor;
         sonra dönünce de sıfırlanmış buluyor.

         Kök sebep: "dokunmadı" ile "ekrana bakmıyor" aynı sayılıyordu.
         Bu ders zaten `hareketVar()` içinde YAZILI ("uzun bir metni
         okuyan biri ekrana bakıyor — tam da mola gereken durum") ama
         yalnız SIFIRLAMA tarafına uygulanmış; DURDURMA tarafı hâlâ
         girdiye bakıyordu.

         Bir göz molası uygulamasında doğru ölçüt görünürlüktür: ekran
         açık ve sayfa öndeyse gözler çalışıyordur. Sayfa gizlendiğinde
         (arka plan, kilit) zaten `visibilitychange` ile duruyor.

         Masaüstünde kullanıcı ekranı açık bırakıp kalkabilir; o zaman
         mola boş odaya gelir - zararsız. Şimdiki davranış ise molanın
         HİÇ gelmemesi, yani uygulamanın işini hiç yapmaması. */
      const ekrandaMi = (typeof document === 'undefined')
        || document.visibilityState !== 'hidden';
      if (!ekrandaMi
          && simdi - this.sonHareket > this.ayarlar.bostaEsigi * 1000) {
        this.kalanDondurulmus = this.kalanSaniye();
        this.durum = 'bosta';
        this._duyur('degisti', this.anlikDurum());
        return;
      }
      /* EKRAN SURESI DUVAR SAATIYLE OLCULUR, TIK SAYISIYLA DEGIL.

         Once her tikte sabit `0.25` ekleniyordu, yani "tikler saniyede
         dort kez gelir" VARSAYILIYORDU. Tarayici arka plandaki sekmenin
         zamanlayicisini kisiyor (dakikada bire kadar): sayac gercekte
         gecen surenin cok altinda kaliyordu.

         OLCULDU (03.09.2026): 40 tik ardarda cagrildi, gercekte 0 saniye
         gecti, `ekranSuresi`ne 10 SANIYE eklendi. Yani sayi tik
         sayisinin turevi, surenin degil.

         NEDEN AGIR: aile kipinin GUNLUK EKRAN SURESI SINIRI bu sayidan
         besleniyor. Ebeveyn "60 dk" koyuyor, cocuk sekmeyi arka plana
         atip telefonu saatlerce kullaniyor, sinir HIC dolmuyor ve engel
         ekrani cikmiyor. Cekirdegin kendi yorumu bunu zaten yaziyor:
         "olmayan bir korumaya guvendirmek, hic koruma koymamaktan
         kotudur."

         UST SINIR 2 SANIYE: sekme gizliyken ya da kisilmisken aradaki
         buyuk bosluk EKRAN SURESI SAYILMAMALI - kullanici o sirada bu
         uygulamaya bakmiyordu. Kisilmis ama ONDEKI bir sekmede tikler
         saniyede bire duser; orada 1 saniye eklenir ve dogru olur.

         UC SAYI DA AYNI DELTAYI KULLANIYOR: ayri ayri artsalardi biri
         otekinden kayardi - bu depoda bilinen sinif. */
      const oncekiTik = this._sonTikAni || simdi;
      this._sonTikAni = simdi;
      const delta = Math.min(2, Math.max(0, (simdi - oncekiTik) / 1000));

      this.istatistik.ekranSuresi += delta;
      this.istatistik.kesintisizSure += delta;
      /* Saatlik kova. `ekranSuresi` ile ayni satirda artiyor: ikisi
         ayri yerlerde artsaydi biri kacirdiginda toplamlar sessizce
         uyusmaz olurdu. */
      const saat = new Date().getHours();
      if (!Array.isArray(this.istatistik.saatlik)) {
        this.istatistik.saatlik = new Array(24).fill(0);
      }
      this.istatistik.saatlik[saat] = (this.istatistik.saatlik[saat] || 0) + delta;
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
        const uzunMuydu = !!this.uzunMoladaMi;
        if (this.uzunMoladaMi) {
          this.istatistik.uzunMola++;
          this.istatistik.kesintisizSure = 0;   // uzun mola sayacı sıfırlar
          this.uzunMoladaMi = false;
        } else {
          this.istatistik.tamamlananMola++;
        }
        /* Molanin UZUN mu oldugu bilgisi olayla birlikte gidiyor:
           bayrak yukarida zaten sifirlandi, dinleyici okuyamaz. */
        this._duyur('molaBitti', this.istatistik, uzunMuydu);

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
    const gun = simdi.getDay();               // 0 pazar · 6 cumartesi
    const haftaSonu = (gun === 0 || gun === 6);
    const hs = this.ayarlar.haftaSonu || 'ayni';

    /* HAFTA SONU KARARI BURADA — tek karar yeri.
       Ikinci bir yere koymak, iki yerin birbirinden ayrismasi
       demekti; bu depoda bilinen sinif. Suren mola yarida kesilmez:
       cagiran taraf zaten `durum !== 'mola'` kosuluyla giriyor. */
    if (haftaSonu && hs === 'kapali') return false;

    const ayriSaat = (haftaSonu && hs === 'ayri');
    // "Hafta sonu ayri saat" secildiyse genel saat anahtari KAPALI olsa
    // bile hafta sonu araligi uygulanir - kullanici o araligi bilerek
    // yazdi; yok saymak sessizce ayari cope atmak olurdu.
    if (!this.ayarlar.saatlerAcik && !ayriSaat) return true;

    const dk = (s) => {
      const [a, b] = String(s || '0:0').split(':').map(Number);
      return (a || 0) * 60 + (b || 0);
    };
    const su = simdi.getHours() * 60 + simdi.getMinutes();
    const bas = dk(ayriSaat ? this.ayarlar.haftaSonuBas : this.ayarlar.basSaat);
    const bit = dk(ayriSaat ? this.ayarlar.haftaSonuBit : this.ayarlar.bitSaat);
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
    /* ASAMANIN GERCEK SURESI — TEK KAYNAK.

       Arayuz mola ekraninda `ayarlar.molaSuresi` kullaniyordu. UZUN
       MOLADA (`uzunMolaSuresi`, varsayilan 300 sn) ve TANITIM MOLASINDA
       (6 sn) o deger YANLIS.

       OLCULDU (03.09.2026): uzun mola baslatildi, ekran 299'dan geri
       sayarken ekran okuyucu "Goz molasi basladi. 30 saniye." dedi.
       Az goren kullanici icin ekrandaki sayiyi hic gormeden TEK bilgi
       kaynagi o cumle. Ayrica "Az kaldi" esigi de o yanlis sayidan
       hesaplandigi icin 4,5 DAKIKA erken cikiyordu.

       Suresi saklanan tek yer burasi; her asama gecisi buradan geciyor,
       yani ikinci bir kaynak dogmasi mumkun degil. */
    this.asamaSuresi = saniye;
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

  /** Şu anda engel var mı? Yoksa null.

      Döner: { sebep, kalanSn } — `sebep`:
        'yasak'       yasak saatleri içinde
        'yasak-bozuk' saat ayarı okunamıyor (SESSİZCE geçmiyoruz)
        'sinir'       günlük ekran süresi doldu

      `simdi` dışarıdan verilebiliyor: sınama gerçek saati beklemesin. */
  engelDurumu(simdi = new Date()) {
    if (this.ayarlar.kip !== 'aile') return null;

    // Ebeveyn ek süre verdiyse hiçbir engel uygulanmaz.
    if (Number(this.ayarlar.ekSureBitis || 0) > simdi.getTime()) return null;

    if (this.ayarlar.yasakAcik) {
      const bas = dakikaOku(this.ayarlar.yasakBas);
      const bit = dakikaOku(this.ayarlar.yasakBit);
      if (bas === null || bit === null) {
        // Uydurma bir pencere UYGULAMIYORUZ. Yanlış saatte engellemek
        // de, hiç engellememek de sessiz bir yalan olurdu.
        return { sebep: 'yasak-bozuk', kalanSn: 0 };
      }
      const dk = simdi.getHours() * 60 + simdi.getMinutes();
      // Gece yarısını aşan aralık (21:00–07:00) ters okunmalı.
      const icinde = bas <= bit ? (dk >= bas && dk < bit)
                                : (dk >= bas || dk < bit);
      if (icinde) {
        const kalan = ((bit - dk) + 1440) % 1440;
        return { sebep: 'yasak', kalanSn: kalan * 60 };
      }
    }

    const sinirDk = Number(this.ayarlar.gunlukSinirDk || 0);
    if (sinirDk > 0) {
      const gecen = Number(this.istatistik?.ekranSuresi || 0);
      if (gecen >= sinirDk * 60) return { sebep: 'sinir', kalanSn: 0 };
    }
    return null;
  }

  anlikDurum() {
    return {
      durum: this.durum,
      kalan: this.kalanSaniye(),
      // Asamanin GERCEK suresi: arayuz "kac saniye" derken bunu
      // kullanmali, ayardaki mola suresini degil.
      asamaSuresi: this.asamaSuresi,
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
    /* `typeof ... === 'number'` SART, `+eskiFark` YETMEZ.

       `+null` sifira donuyor ve `Number.isFinite(0)` DOGRU. Sifir da
       gecerli bir saat farki (UTC). Yani alan EKSIKSE kullaniciya
       "cihazin saati degismis gorunuyor" deniyordu - kendinden emin
       ve YANLIS bir aciklama. Olculdu (03.09.2026): `saatFarki: null`
       olan bir kayitla Turkiye saatinde tam bu mesaj cikti.

       Bozuk ya da eksik bir alan, uydurma bir sebep uretmemeli:
       bilinmiyorsa "saat degisti" demek yerine susmak dogru. */
    const eskiFark = veri.saatFarki;
    const saatDegisti = typeof eskiFark === 'number'
      && Number.isFinite(eskiFark)
      && eskiFark !== new Date().getTimezoneOffset();

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

    /* 'bosta' ICINDE DONDURULMUS KALAN SURE GERI YUKLENIYOR.

       Sekme gizliyken sayac 'bosta'ya giriyor ve o andaki kalan sure
       `kalanDondurulmus` olarak diske yaziliyor — ama `hedefZaman`
       donmuyor, saat ilerlemeye devam ediyor. Geri yuklerken donmus
       deger YALNIZCA 'duraklatildi' dalinda okunuyordu; 'bosta' icin
       hic okunmuyordu.

       Sonuc: 18:00'de donan sayac, on dakika sonra uygulama acilinca
       18:00'den degil 8:00'den basliyordu; yeterince beklenmisse
       hedef gecmis olup tumden sifirlaniyordu. Ayni durum iki yoldan
       iki farkli sayi veriyordu: sekmeye DONMEK donmus degeri
       kullaniyor, KAPAT-AC kullanmiyordu.

       'saatDisi' de ayni sekilde donuyor, o da dahil. */
    const donmusHam = +veri.kalanDondurulmus;
    const donmusGecerli = (veri.durum === 'bosta' || veri.durum === 'saatDisi')
      && Number.isFinite(donmusHam) && donmusHam > 0
      && donmusHam <= this.ayarlar.calismaSuresi;
    const kalan = donmusGecerli ? donmusHam : (hedef - simdi) / 1000;
    if (kalan > 0 && kalan <= this.ayarlar.calismaSuresi) {
      this._kalpAtisiBaslat();
      this.hedefZaman = donmusGecerli ? (simdi + donmusHam * 1000) : hedef;
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
      /* PUSU KURMA, TEKLIF ET.

         Burada eskiden `simdi + 25000` vardi: uygulamayi acan
         kullaniciya 25 saniye sonra tam ekran mola DUSUYORDU. Kullanici
         bunu kusur olarak bildirdi (03.09.2026): "bak yine en basta
         actigimda kendisi acti".

         Ama molayi tumden dusurmek de YANLIS olurdu -- ayni kullanici
         daha once tam tersini sikayet etmisti: "mola hic gelmiyor".
         Iki sikayet ayni koda bakiyor.

         Cozum ikisini de karsiliyor: sayac NORMAL suresiyle basliyor
         (pusu yok), `gecikmisMola` yine kuruluyor ve arayuz kullaniciya
         DUGMEYLE soruyor. Mola kaybolmuyor, dayatilmiyor. Karar
         kullanicida -- zaten uygulamanin butun mantigi bu. */
      this.hedefZaman = simdi + this.ayarlar.calismaSuresi * 1000;
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

/* ACIL CIKIS ESIGI. Kural tek cumle: hicbir molada bundan fazla
   cikissiz kalinmaz. Yirmi saniye uygulamanin kendi sozu (20-20-20);
   20 sn'lik molada dugme hic gorunmez, cunku mola zaten bitmistir. */
const ACIL_CIKIS_ESIGI = 20;

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
    /* SAATLIK DAGILIM DA SAKLANIYOR.

       Kullanicinin gosterdigi ekranda gunler arasinda gezilebiliyor ve
       her gunun SAAT dagilimi goruluyordu. Bizde saatlik dizi yalnizca
       BUGUN icin bellekte duruyordu; gun degisince siliniyordu, yani
       dun hangi saatte ekranda oldugunu bilmenin hicbir yolu yoktu.

       Her kova TAM SAYI saniye olarak yaziliyor: kesirli saniyeleri
       saklamak kaydi buyutur ve hicbir seye yaramaz.

       Artan sayac kurali burada da gecerli - bir gunun saatlik degeri
       geri gidemez; hangi sekme yazarsa yazsin buyuk olan kalir. */
    const eskiSaatlik = Array.isArray(eski.saatlik) ? eski.saatlik : [];
    const yeniSaatlik = Array.isArray(istatistik.saatlik) ? istatistik.saatlik : [];
    const saatlik = new Array(24);
    for (let s = 0; s < 24; s++) {
      saatlik[s] = buyuk(Math.round(+eskiSaatlik[s] || 0),
                         Math.round(+yeniSaatlik[s] || 0));
    }
    veri[gun] = {
      mola: buyuk(eski.mola, istatistik.tamamlananMola),
      atlanan: buyuk(eski.atlanan, istatistik.atlananMola),
      ekran: buyuk(eski.ekran, Math.round(istatistik.ekranSuresi || 0)),
      saatlik,
    };
    this.yaz(veri);
  },

  /** Son N gün: [{ad, sayi, bugunMu}, ...] */
  /** Bugun, onceki gunlerin ortalamasina gore nerede?

      Doner: null (karsilastirilamaz) ya da
             { fark, ortalama, gunSayisi }
      `fark` TAM SAYI: mola sayisi bir adet olcusudur, "1,3 mola fazla"
      demek anlamsizdir.

      PAYDA: onceki gunlerin hepsi degil, ILK DOLU GUNDEN itibaren
      olanlar. Uygulamayi yeni kuran biri icin bastaki sifirlar "o gun
      mola vermedi" demek degil, "o gun uygulama yoktu" demek - onlari
      saymak ortalamayi haksiz yere dusurur ve kullaniciya her gun
      "ortalamanin ustundesin" der. Ovmek de yaniltmaktir.

      En az IKI gun yoksa null: tek gunluk gecmisten ortalama cikarmak
      uydurmadir. */
  /** ORTALAMA TABANI — ilk dolu günden itibaren olan günler.

      Baştaki sıfırlar "o gün mola vermedi" değil "o gün uygulama
      yoktu" demek; onları bölene katmak ortalamayı haksız yere
      düşürür. `gunlukKarsilastirma` bu ilkeyi zaten uyguluyordu ama
      HAFTALIK KARTIN BÜYÜK SAYISI ayrıca 7'ye bölüyordu — aynı kartta
      birbirini tutmayan iki ortalama. Bölen artık tek yerde. */
  /** Bir gunun saatlik dagilimi. Kayit yoksa `null` -- BOS DIZI DEGIL:
      "o gun hic ekranda degildin" ile "o gunun kaydi yok" ayri seyler
      ve arayuz ikisini ayri gostermeli. */
  saatlikGun(anahtar) {
    const veri = this.oku();
    const k = veri[anahtar];
    if (!k || !Array.isArray(k.saatlik)) return null;
    const c = new Array(24);
    for (let s = 0; s < 24; s++) c[s] = Math.max(0, +k.saatlik[s] || 0);
    return c;
  },

  /** Bugunden geriye `adet` gunun anahtarlari (eskiden yeniye). */
  gunAnahtarlari(adet = 7) {
    const bugun = new Date();
    const liste = [];
    for (let i = adet - 1; i >= 0; i--) {
      liste.push(this.gunAdi(new Date(bugun.getTime() - i * 86400000)));
    }
    return liste;
  },

  ortalamaTabani(gunler) {
    if (!Array.isArray(gunler)) return [];
    const ilk = gunler.findIndex((g) => g && (g.sayi | 0) > 0);
    return ilk === -1 ? [] : gunler.slice(ilk);
  },

  gunlukKarsilastirma(gunler) {
    if (!Array.isArray(gunler) || !gunler.length) return null;
    const bugun = gunler.find((g) => g && g.bugunMu);
    if (!bugun) return null;
    const oncekiler = gunler.filter((g) => g && !g.bugunMu);
    const temel = this.ortalamaTabani(oncekiler);
    if (temel.length < 2) return null;
    const toplam = temel.reduce((t, g) => t + (g.sayi | 0), 0);
    const ortalama = toplam / temel.length;
    return {
      fark: Math.round((bugun.sayi | 0) - ortalama),
      ortalama: Math.round(ortalama * 10) / 10,
      gunSayisi: temel.length,
    };
  },

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

  /** HAFTALIK ÖZET — rapor ekranının tek veri kaynağı.

      Döner:
        { gunler, doluGun, yeterliVeri, toplamMola, toplamAtlanan,
          toplamEkran, ortalama, enIyi, enSakin, hedefTutan, hedef,
          oncekiToplam, fark }

      `gunler[i].veriVar` BU İŞLEVİN EN ÖNEMLİ ALANI: o gün için hiç
      kayıt yoksa `false`. "O gün 0 mola verdi" ile "o gün uygulama
      yoktu" farklı şeylerdir; ikisini karıştıran bir rapor kullanıcıya
      "en kötü günün pazartesi" der — hâlbuki pazartesi uygulamayı
      henüz kurmamıştı. `gunlukKarsilastirma` bu tuzağı zaten biliyor,
      burada da aynı ilke.

      YETERSİZ VERİDE SONUÇ YOK: üç dolu günün altında `yeterliVeri`
      false döner ve arayüz sonuç cümlesi kurmaz. İki günlük geçmişten
      "en iyi günün" çıkarmak uydurma bir kesinlik verir. */
  haftaOzeti(bugunIstatistik = null, hedef = GUNLUK_HEDEF, adet = 7) {
    const veri = this.oku();
    const bugun = new Date();
    const gunAl = (geriGun) => {
      const t = new Date(bugun.getTime() - geriGun * 86400000);
      const anahtar = this.gunAdi(t);
      const kayit = veri[anahtar];
      const bugunMu = geriGun === 0;
      const canli = bugunMu && bugunIstatistik;
      return {
        anahtar,
        ad: GUN_ADLARI[t.getDay()],
        mola: canli ? (bugunIstatistik.tamamlananMola | 0) : ((kayit || {}).mola | 0),
        atlanan: canli ? (bugunIstatistik.atlananMola | 0) : ((kayit || {}).atlanan | 0),
        ekran: canli ? Math.round(bugunIstatistik.ekranSuresi || 0)
                     : ((kayit || {}).ekran | 0),
        /* Kayıt YOKSA veri yok. Kayıt varsa sıfır bile olsa veridir:
           o gün uygulama açıktı ve mola verilmedi — bu bir bilgidir.

           BUGÜN AYRI: `bugunIstatistik` her zaman veriliyor, yani
           bugünü koşulsuz "dolu gün" saymak eşiği tümden işlevsiz
           bırakıyordu — iki günlük geçmişi olan yeni kullanıcı üç gün
           sayılıp sonuç cümlesi görüyordu. Bugün ancak GERÇEKTEN bir
           şey olduysa sayılıyor. */
        veriVar: !!kayit || !!(canli && (
          (bugunIstatistik.tamamlananMola | 0) > 0
          || (bugunIstatistik.atlananMola | 0) > 0
          || Math.round(bugunIstatistik.ekranSuresi || 0) > 0)),
        bugunMu,
      };
    };

    const gunler = [];
    for (let i = adet - 1; i >= 0; i--) gunler.push(gunAl(i));
    const dolu = gunler.filter((g) => g.veriVar);

    const topla = (liste, alan) => liste.reduce((t, g) => t + (g[alan] | 0), 0);
    const toplamMola = topla(dolu, 'mola');

    // Önceki dönem: aynı uzunlukta, bir dönem geride. Orada da yalnız
    // DOLU günler sayılıyor; yoksa "geçen hafta 0'dı, bu hafta harika"
    // gibi uydurma bir ilerleme çıkardı.
    const oncekiler = [];
    for (let i = adet * 2 - 1; i >= adet; i--) oncekiler.push(gunAl(i));
    const oncekiDolu = oncekiler.filter((g) => g.veriVar);
    const oncekiToplam = oncekiDolu.length ? topla(oncekiDolu, 'mola') : null;

    /* EN IYI / EN SAKIN YALNIZ TAMAMLANMIS GUNLERDEN.

       Bugun daha bitmedi. Sabah dokuzda "en sakin gunun bugun" demek
       haksiz ve her sabah tekrarlanirdi. Olculdu: iki gunluk gecmiste
       "En sakin gunun Cum: 0 mola" ciktiginda o gun BUGUNDU. */
    let enIyi = null;
    let enSakin = null;
    const tamamlanan = dolu.filter((g) => !g.bugunMu);
    if (tamamlanan.length >= 3) {
      const sirali = tamamlanan.slice().sort((a, b) => b.mola - a.mola);
      enIyi = sirali[0];
      const son = sirali[sirali.length - 1];
      // Hepsi aynıysa "en sakin gün" diye bir şey yok.
      if (son.mola !== enIyi.mola) enSakin = son;
    }

    return {
      gunler,
      doluGun: dolu.length,
      yeterliVeri: dolu.length >= 3,
      // Sonuc cumlesi icin ayri esik: bugun sayilmaz.
      tamamlananGun: tamamlanan.length,
      toplamMola,
      toplamAtlanan: topla(dolu, 'atlanan'),
      toplamEkran: topla(dolu, 'ekran'),
      ortalama: dolu.length
        ? Math.round((toplamMola / dolu.length) * 10) / 10 : null,
      enIyi,
      enSakin,
      hedefTutan: dolu.filter((g) => g.mola >= hedef).length,
      hedef,
      oncekiToplam,
      fark: oncekiToplam === null ? null : toplamMola - oncekiToplam,
    };
  },

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
  module.exports = { MolaMotoru, VARSAYILAN_AYARLAR, dakikaOku, Gecmis, GUNLUK_HEDEF,
    ACIL_CIKIS_ESIGI,
                     istatistikSuz };
}
