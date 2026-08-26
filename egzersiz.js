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

  ciz(gecen, toplam) {
    this._hazirla();
    const c = this.c;
    const g = this.r * 0.78;
    const evre = (gecen % GozKirp.DONGU) / GozKirp.DONGU;
    let aciklik;
    if (evre < 0.12) aciklik = 1 - evre / 0.12;          // hızlı kapanış
    else if (evre < 0.26) aciklik = (evre - 0.12) / 0.14;  // yumuşak açılış
    else aciklik = 1;
    const yuk = Math.max(g * 0.05, g * 0.55 * aciklik);

    // Badem şekli: iki eğri
    c.beginPath();
    c.moveTo(this.mx - g, this.my);
    c.quadraticCurveTo(this.mx, this.my - yuk * 2, this.mx + g, this.my);
    c.quadraticCurveTo(this.mx, this.my + yuk * 2, this.mx - g, this.my);
    c.fillStyle = this.renk.vurgu;
    c.fill();

    // Göz bebeği
    const p = Math.min(g * 0.30, yuk * 0.9);
    if (p > 1) {
      c.beginPath();
      c.arc(this.mx, this.my, p, 0, Math.PI * 2);
      c.fillStyle = this.renk.zemin;
      c.fill();
    }

    // Sayaç
    const kirpma = Math.floor(gecen / GozKirp.DONGU) + 1;
    const hepsi = Math.max(1, Math.floor(toplam / GozKirp.DONGU));
    c.fillStyle = this.renk.soluk;
    c.font = `${Math.round(this.r * 0.20)}px "Segoe UI", system-ui, sans-serif`;
    c.textAlign = 'center';
    c.fillText(`${Math.min(kirpma, hepsi)} / ${hepsi}`, this.mx, this.my + this.r * 0.82);
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

    c.beginPath();
    c.arc(this.mx, this.my, this.r * 0.86, 0, Math.PI * 2);
    c.strokeStyle = this.renk.sicak;
    c.globalAlpha = 0.30 + 0.45 * (1 - yakinlik);
    c.lineWidth = 2;
    c.stroke();
    c.globalAlpha = 1;

    const p = this.r * (0.10 + 0.55 * yakinlik);
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
    const gen = this.r * 0.88;
    c.beginPath();
    c.moveTo(this.mx - gen, this.my);
    c.lineTo(this.mx + gen, this.my);
    c.strokeStyle = this.renk.sicak;
    c.globalAlpha = 0.55;
    c.lineWidth = 2;
    c.stroke();
    c.globalAlpha = 1;

    const x = this.mx + gen * Math.sin(2 * Math.PI * this._evre(gecen));
    c.beginPath();
    c.arc(x, this.my, this.r * 0.17, 0, Math.PI * 2);
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
