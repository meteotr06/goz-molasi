/* ============================================================
   EGZERSİZ — Mola sırasında ekranda oynayan rehberli göz hareketleri.
   Masaüstü sürümündeki egzersiz.py ile aynı egzersizler, aynı sıralama.

   NEDEN?
   Rakip uygulamalarda mola ekranı "ölü zaman": bir sayıya bakıp
   beklersin. Oysa o 20 saniye asıl işin yapıldığı yer.

   TASARIM KURALI
   Hiçbir animasyon saniyede 3 kereden hızlı yanıp sönmez (WCAG 2.3.1,
   epilepsi riski). Kullanıcı "hareketi azalt" dediyse animasyon durur,
   sadece yönerge yazısı kalır.
   ============================================================ */

class Egzersiz {
  static ad = '';
  static yonerge = '';

  constructor(tuval, renkler) {
    this.t = tuval;
    this.c = tuval.getContext('2d');
    this.renk = renkler;
  }

  /** Tuvali ölç ve temizle. Her çizimden önce çağrılır. */
  _hazirla() {
    const p = this.t.parentElement.getBoundingClientRect();
    const oran = window.devicePixelRatio || 1;
    // Retina ekranda bulanık çıkmasın diye gerçek piksel sayısı kadar tuval
    if (this.t.width !== Math.round(p.width * oran)) {
      this.t.width = Math.round(p.width * oran);
      this.t.height = Math.round(p.height * oran);
    }
    this.c.setTransform(oran, 0, 0, oran, 0, 0);
    this.c.clearRect(0, 0, p.width, p.height);
    this.g = p.width;
    this.y = p.height;
    this.mx = p.width / 2;
    this.my = p.height / 2;
    this.r = Math.min(p.width, p.height) * 0.42;
  }

  /** Yumuşak ışıma — merkezden dışa sönen daire.

      Neden var: düz doldurulmuş şekiller ekranda "yapıştırılmış" gibi
      duruyordu. İnce bir hale, şekli zemine oturtuyor. Bütün
      egzersizler bunu kullanıyor, böylece hepsi aynı dile ait
      görünüyor. */
  _isima(x, y, r, renk, alfa = 0.5) {
    if (r <= 0) return;
    const c = this.c;
    const gecis = c.createRadialGradient(x, y, 0, x, y, r);
    gecis.addColorStop(0, renk);
    gecis.addColorStop(0.45, renk);
    gecis.addColorStop(1, 'transparent');
    const eski = c.globalAlpha;
    c.globalAlpha = eski * alfa;
    c.fillStyle = gecis;
    c.beginPath();
    c.arc(x, y, r, 0, Math.PI * 2);
    c.fill();
    c.globalAlpha = eski;
  }

  ciz(gecen, toplam) {}

  anlikYonerge() { return this.constructor.yonerge; }
}

/* ---------------- Uzağa bak ---------------- */
class UzagaBak extends Egzersiz {
  static ad = 'Uzağa bak';
  static yonerge = 'Pencereden dışarı ya da odanın en uzak köşesine bak';

  /* TASARIM KARARI — bu egzersiz KENDİNİ SİLİYOR.

     Önceki hâli çelişkiliydi: yönerge "pencereden dışarı bak" diyor
     ama ekranda izlenecek bir animasyon oynuyordu. Bakma dediğin
     kişiye bakacak bir şey vermek, uygulamanın bütün amacını
     çürütüyor.

     Yeni davranış: ilk ~3 saniyede halkalar dışa açılıp gözü
     merkezden uzağa yönlendiriyor, sonra animasyon sönüyor. Geriye
     bakılacak bir şey kalmıyor — mola ekranı bilerek sıkıcılaşıyor.

     Diğer egzersizler (göz kırp, yakın-uzak) izlenmeyi GEREKTİRİYOR,
     onlar sönmüyor. */
  ciz(gecen, toplam) {
    this._hazirla();
    const c = this.c;

    // İlk 3 saniyeden sonra sön; 4,5. saniyede tamamen kaybol
    const sonme = 1 - Math.min(1, Math.max(0, (gecen - 3) / 1.5));
    if (sonme <= 0.01) return;

    // Dışa açılan halkalar: gözü merkezden dışarı yönlendiriyor.
    // Uzaklaşma hissi için kalınlık da inceliyor.
    for (let i = 0; i < 3; i++) {
      const evre = ((gecen / 3) + i / 3) % 1;
      const r = this.r * (0.18 + 0.82 * evre);
      c.beginPath();
      c.arc(this.mx, this.my, r, 0, Math.PI * 2);
      c.strokeStyle = this.renk.vurgu;
      c.globalAlpha = Math.max(0.04, (1 - evre) ** 1.6) * 0.75 * sonme;
      c.lineWidth = 2.6 * (1 - evre * 0.65);
      c.stroke();
    }

    // Merkez nokta küçülür: "uzaklaşıyor". Aralık genişletildi
    // (0.22-0.14 çok siliktı), böylece geri çekilme okunuyor.
    c.globalAlpha = sonme;
    const oran = Math.min(1, gecen / Math.max(0.001, toplam));
    const p = this.r * (0.20 - 0.17 * Math.min(1, oran * 3));
    c.beginPath();
    c.arc(this.mx, this.my, Math.max(1, p), 0, Math.PI * 2);
    c.fillStyle = this.renk.vurgu;
    c.fill();
    c.globalAlpha = 1;
  }
}

/* ---------------- Göz kırp ---------------- */
class GozKirp extends Egzersiz {
  static ad = 'Göz kırp';
  static yonerge = 'Kapak kapandığında sen de tam kırp — gözünü sıkıca kapat';
  static DONGU = 2;

  static KANAT = 7;      // diyafram kanadı sayısı

  /* TASARIM KARARI — bu egzersiz bir DİYAFRAM.

     Önceki hâli iki eğriyle çizilmiş yassı bir badem ve içinde düz bir
     daireydi. Ekran görüntüsünde çizgi film gibi duruyordu; uygulamanın
     geri kalanı ise yumuşak halkalardan oluşuyor.

     Diyafram üç işi birden yapıyor:
       • Kapanıp açılması "göz kırp"ı anlatıyor, anlatmak için yazıya
         ihtiyaç bırakmıyor.
       • Dairesel — sayaç halkasıyla, nefes halkalarıyla aynı dilde.
       • Soyut. Çizilmiş bir göze bakmak tuhaf; ışığı kesilen bir
         açıklığa bakmak değil.

     WCAG 2.3.1: döngü 2 saniye, yani saniyede 0,5 kapanış. Sınır
     saniyede 3. Fazlasıyla altında. */
  ciz(gecen, toplam) {
    this._hazirla();
    const c = this.c;
    const R = this.r * 0.80;
    const evre = (gecen % GozKirp.DONGU) / GozKirp.DONGU;
    let aciklik;
    if (evre < 0.12) aciklik = 1 - evre / 0.12;            // hızlı kapanış
    else if (evre < 0.26) aciklik = (evre - 0.12) / 0.14;  // yumuşak açılış
    else aciklik = 1;
    // Yumuşat: doğrusal açıklık mekanik duruyordu
    const a = aciklik * aciklik * (3 - 2 * aciklik);

    // Açıklığın yarıçapı ve kanatların bükülmesi
    const delik = R * (0.06 + 0.62 * a);
    const buk = (1 - a) * 0.55;

    // 1) Açıklıktan sızan ışık. Kapanınca sönüyor — asıl "kırpma"
    //    hissini veren şey bu.
    this._isima(this.mx, this.my, delik * 2.1, this.renk.vurgu, 0.22 + 0.30 * a);

    // 2) Kanatlar
    const n = GozKirp.KANAT;
    const dilim = (Math.PI * 2) / n;
    const koseler = [];
    for (let i = 0; i < n; i++) {
      const t = i * dilim + buk;
      koseler.push([this.mx + delik * Math.cos(t), this.my + delik * Math.sin(t)]);
    }
    for (let i = 0; i < n; i++) {
      const t0 = i * dilim;
      const t1 = t0 + dilim;
      const k0 = koseler[i];
      const k1 = koseler[(i + 1) % n];
      c.beginPath();
      c.moveTo(this.mx + R * Math.cos(t0), this.my + R * Math.sin(t0));
      c.arc(this.mx, this.my, R, t0, t1);
      c.lineTo(k1[0], k1[1]);
      c.lineTo(k0[0], k0[1]);
      c.closePath();
      /* Komşu kanatlar hafif farklı parlaklıkta — düz bir halka değil,
         üst üste binmiş yapraklar gibi okunuyor.

         Doluluk KAPANDIKÇA artıyor. İlk denemede sabitti ve tam
         kapalı kare pasta dilimi gibi duruyordu: merkeze inen ince
         çizgiler, arada boşluk. Göz kapandığında görünmesi gereken
         şey dolu bir yüzey. */
      c.globalAlpha = 0.14 + 0.09 * (i % 2) + 0.30 * (1 - a);
      c.fillStyle = this.renk.vurgu;
      c.fill();
      // Kanat kenarları açıkken belirgin, kapanınca siliniyor —
      // yoksa kapalı gözün üstünde ışın gibi çizgiler kalıyor
      c.globalAlpha = 0.14 + 0.42 * a;
      c.strokeStyle = this.renk.vurgu;
      c.lineWidth = 1.4;
      c.stroke();
    }
    c.globalAlpha = 1;

    // 3) Dış çerçeve
    c.beginPath();
    c.arc(this.mx, this.my, R, 0, Math.PI * 2);
    c.strokeStyle = this.renk.vurgu;
    c.globalAlpha = 0.75;
    c.lineWidth = 2.4;
    c.stroke();
    c.globalAlpha = 1;

    // 4) Sayaç
    const kirpma = Math.floor(gecen / GozKirp.DONGU) + 1;
    const hepsi = Math.max(1, Math.floor(toplam / GozKirp.DONGU));
    c.fillStyle = this.renk.soluk;
    c.font = `${Math.round(this.r * 0.18)}px "Segoe UI", system-ui, sans-serif`;
    c.textAlign = 'center';
    c.fillText(`${Math.min(kirpma, hepsi)} / ${hepsi}`, this.mx, this.my + this.r * 0.99);
  }
}

/* ---------------- Yakın — uzak ---------------- */
class YakinUzak extends Egzersiz {
  static ad = 'Yakın — uzak';
  static yonerge = 'Nokta büyüyünce parmağına, küçülünce uzağa bak';
  static DONGU = 5;

  _evre(gecen) { return (gecen % YakinUzak.DONGU) / YakinUzak.DONGU; }

  ciz(gecen, toplam) {
    this._hazirla();
    const c = this.c;
    const e = this._evre(gecen);
    // Yumuşak gidiş-geliş, ani sıçrama yok
    const yakinlik = (1 - Math.cos(2 * Math.PI * e)) / 2;

    // "Uzak" çerçevesi — nokta uzaklaştıkça belirginleşiyor
    c.beginPath();
    c.arc(this.mx, this.my, this.r * 0.86, 0, Math.PI * 2);
    c.strokeStyle = this.renk.sicak;
    c.globalAlpha = 0.30 + 0.45 * (1 - yakinlik);
    c.lineWidth = 2;
    c.stroke();
    c.globalAlpha = 1;

    /* Derinlik izi: noktanın arkasında, ondan biraz geride kalan iki
       soluk halka. Tek başına büyüyüp küçülen bir daire "yaklaşıyor"
       değil "şişiyor" gibi duruyordu; geride kalan halkalar hareketi
       ileri-geri eksenine oturtuyor. */
    for (let i = 1; i <= 2; i++) {
      const gecikme = 0.10 * i;
      const gy = (1 - Math.cos(2 * Math.PI * Math.max(0, e - gecikme))) / 2;
      c.beginPath();
      c.arc(this.mx, this.my, this.r * (0.10 + 0.55 * gy) + i * 3, 0, Math.PI * 2);
      c.strokeStyle = this.renk.vurgu;
      c.globalAlpha = 0.16 / i;
      c.lineWidth = 2;
      c.stroke();
    }
    c.globalAlpha = 1;

    const p = this.r * (0.10 + 0.55 * yakinlik);
    this._isima(this.mx, this.my, p * 2.4, this.renk.vurgu, 0.30);
    c.beginPath();
    c.arc(this.mx, this.my, p, 0, Math.PI * 2);
    c.fillStyle = this.renk.vurgu;
    c.fill();
  }

  anlikYonerge(gecen) {
    return this._evre(gecen) < 0.5 ? 'Şimdi YAKINA bak — parmağına' : 'Şimdi UZAĞA bak';
  }
}

/* ---------------- Gözünü kapat ---------------- */
class GozKapat extends Egzersiz {
  static ad = 'Gözünü kapat';
  static yonerge = 'Gözlerini kapat, yavaşça nefes al — bitince ses gelecek';

  ciz(gecen, toplam) {
    this._hazirla();
    const c = this.c;
    // 10 saniyelik nefes: 4 sn içeri, 6 sn dışarı
    const e = (gecen % 10) / 10;
    const nefes = (1 - Math.cos(2 * Math.PI * e)) / 2;
    const olcek = 0.70 + 0.30 * nefes;
    // Nefesle birlikte büyüyüp sönen hale. Gözler kapalı olduğu için
    // bu ekranı kimse izlemiyor olabilir — ama göz aralayan biri
    // nerede olduğunu tek bakışta anlasın.
    this._isima(this.mx, this.my, this.r * olcek * 1.15, this.renk.vurgu,
                0.10 + 0.14 * nefes);
    for (let i = 0; i < 5; i++) {
      const r = this.r * olcek * (0.32 + 0.17 * i);
      c.beginPath();
      c.arc(this.mx, this.my, r, 0, Math.PI * 2);
      c.strokeStyle = this.renk.vurgu;
      c.globalAlpha = (0.75 - 0.11 * i) * (0.45 + 0.55 * nefes);
      c.lineWidth = i < 2 ? 3 : 2;
      c.stroke();
    }
    c.globalAlpha = 1;
  }

  anlikYonerge(gecen) {
    const e = (gecen % 10) / 10;
    return (e < 0.4 ? 'Nefes al…' : 'Yavaşça ver…') + '   gözlerin kapalı kalsın';
  }
}

/* ---------------- Boynunu gevşet ---------------- */
class Boyun extends Egzersiz {
  static ad = 'Boynunu gevşet';
  static yonerge = 'Başını yavaşça çevir — omuzlarını geriye at';
  static DONGU = 6;

  _evre(gecen) { return (gecen % Boyun.DONGU) / Boyun.DONGU; }

  ciz(gecen, toplam) {
    this._hazirla();
    const c = this.c;
    /* Baş bir çizgi üzerinde kaymaz, bir YAY çizerek döner. Düz çizgi
       hareketi yanlış anlatıyordu: insan başını sağa-sola kaydırmıyor,
       çeviriyor. Yay üzerinde giden nokta doğru hareketi gösteriyor. */
    const gen = this.r * 0.88;
    const yay = this.r * 0.30;          // yayın ne kadar bombeli olduğu
    const nokta = (o) => [this.mx + gen * o, this.my - yay * (1 - o * o)];

    c.beginPath();
    for (let i = 0; i <= 40; i++) {
      const [x, y] = nokta(-1 + (2 * i) / 40);
      i ? c.lineTo(x, y) : c.moveTo(x, y);
    }
    c.strokeStyle = this.renk.sicak;
    c.globalAlpha = 0.45;
    c.lineWidth = 2;
    c.stroke();
    c.globalAlpha = 1;

    const e = this._evre(gecen);
    // Arkada kalan iz — hareketin yönünü okunur kılıyor
    for (let i = 3; i >= 1; i--) {
      const [ix, iy] = nokta(Math.sin(2 * Math.PI * (e - i * 0.018)));
      c.beginPath();
      c.arc(ix, iy, this.r * (0.17 - 0.028 * i), 0, Math.PI * 2);
      c.fillStyle = this.renk.vurgu;
      c.globalAlpha = 0.13 * (4 - i) / 3;
      c.fill();
    }
    c.globalAlpha = 1;

    const [x, y] = nokta(Math.sin(2 * Math.PI * e));
    this._isima(x, y, this.r * 0.46, this.renk.vurgu, 0.32);
    c.beginPath();
    c.arc(x, y, this.r * 0.17, 0, Math.PI * 2);
    c.fillStyle = this.renk.vurgu;
    c.fill();
  }

  anlikYonerge(gecen) {
    return this._evre(gecen) < 0.5 ? 'Yavaşça SAĞA çevir' : 'Yavaşça SOLA çevir';
  }
}

/* ---------------- Seçim ----------------
   Sıra kasıtlı: "uzağa bak" asıl egzersiz, yarısını o kaplıyor.
   Diğerleri araya girip ekranın ezber olup görünmez hale gelmesini önlüyor. */
const KISA_SIRA = [UzagaBak, GozKirp, UzagaBak, YakinUzak, UzagaBak, Boyun];

function egzersizSec(sayac) {
  return KISA_SIRA[sayac % KISA_SIRA.length];
}

const TUM_EGZERSIZLER = [UzagaBak, GozKirp, YakinUzak, GozKapat, Boyun];

if (typeof module !== 'undefined') {
  module.exports = { egzersizSec, TUM_EGZERSIZLER, Egzersiz };
}
