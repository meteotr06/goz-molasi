/* K-58 SINAMASI — "kendini sıfırlıyor" (06.09.2026)
   Bu üç sınama ÖNCE bozuk kodda koşturuldu ve ÜÇÜ DE KALDI verdi.
   Kırmızı görülmeden yazılan sınama, sınama değildir. */
/* Tarayicida kosar (K-95: file:// degil, sunucu uzerinden).
   cekirdek.js MolaMotoru'yu kuresel tanimliyor. */
const Motor = (typeof MolaMotoru !== 'undefined') ? MolaMotoru : require('../cekirdek.js').MolaMotoru;
if (typeof document === 'undefined') globalThis.document = { visibilityState: 'visible', hidden: false };
const gorunurluk = (v) => { try { Object.defineProperty(document, 'visibilityState', { value: v, configurable: true }); } catch (e) {} };

const S = [];
const ekle = (ad, gecti, ayrinti) => S.push({ ad, durum: gecti ? 'GEÇTİ' : 'KALDI', ayrinti });
const yakin = (a, b, pay) => Math.abs(a - b) <= pay;
const AYAR = { calismaSuresi: 1200, molaSuresi: 20, dinlenmeEsigi: 300, bostaEsigi: 90 };

/* S-1 — DOKUNMADAN ÇALIŞAN KULLANICI, KISA SEKME DEĞİŞİMİ.
   16 dakika okuyup hiç tuşa basmayan biri 3 saniyeliğine sekme
   değiştirince sayaç BAŞTAN BAŞLIYOR. Sebep: yokluk süresi gerçek
   gizlenme anından değil, SON DOKUNUŞTAN ölçülüyor. */
{
  const m = new Motor({ ...AYAR, uzakKalincaSifirla: true });
  m.basla();
  m.sonHareket = Date.now() - 16 * 60e3;   // 16 dk dokunulmadı ama ekrandaydı
  m.hedefZaman = Date.now() + 240e3;        // 4:00 kaldı
  /* SIFIRDAN FARKLI BIR DEGER SART.
     Ilk yazilisinda `kesintisizSure !== 0` diye bakiliyordu ama deger
     zaten 0'dan basliyordu: sinama hicbir sey olcmuyordu, sadece
     kirmizi gorunuyordu. Simdi 600 kuruluyor; sifirlanirsa yakalanir. */
  m.istatistik.kesintisizSure = 600;
  gorunurluk('hidden');
  m.gizlendi();
  gorunurluk('visible');
  m.hareketVar();                            // 3 sn sonra geri döndü
  const kalan = Math.round(m.kalanSaniye());
  ekle('S-1 kısa yokluk sayacı sıfırlamaz', yakin(kalan, 240, 3), `kalan ${kalan} sn (beklenen ~240)`);
  ekle('S-1b seri (kesintisizSure) korunur', m.istatistik.kesintisizSure === 600,
       `kesintisizSure ${m.istatistik.kesintisizSure} (beklenen 600)`);
}

/* S-1c — KARŞI SINAMA: gerçek uzun yokluk HÂLÂ sıfırlamalı.
   Düzeltme istenen davranışı bozmamalı. */
{
  const m = new Motor({ ...AYAR, uzakKalincaSifirla: true });
  m.basla();
  m.hedefZaman = Date.now() + 240e3;
  m.gizlendi();
  if (m.gizlenmeAni !== undefined) m.gizlenmeAni = Date.now() - 20 * 60e3;
  else m.sonHareket = Date.now() - 20 * 60e3;
  m.hareketVar();
  const kalan = Math.round(m.kalanSaniye());
  ekle('S-1c gerçek 20 dk yokluk hâlâ sıfırlar', yakin(kalan, 1200, 3), `kalan ${kalan} sn (beklenen 1200)`);
}

/* S-2 — İLERLEME HALKASI HER DÖNÜŞTE DOLUYA SIÇRIYOR.
   devamEt() kalan süreyi _asamayaGec'e veriyor, o da onu aşamanın
   TOPLAM süresi sanıyor: asamaSuresi 1200'den 720'ye düşüyor,
   ilerleme() 0 çıkıyor, halka tamamen dolu çiziliyor. */
{
  const m = new Motor({ ...AYAR, uzakKalincaSifirla: false });
  m.basla();
  m.hedefZaman = Date.now() + 720e3;        // 12:00 kaldı = %40 ilerledi
  const i1 = m.ilerleme();
  m.gizlendi();
  m.hareketVar();
  const i2 = m.ilerleme();
  ekle('S-2 ilerleme dönüşte korunur', Math.abs(i2 - i1) < 0.02, `${i1.toFixed(3)} → ${i2.toFixed(3)}`);
  ekle('S-2b aşama süresi 1200 kalır', m.asamaSuresi === 1200, `asamaSuresi ${m.asamaSuresi}`);
  // On uygulama değişimi: bozuk kodda asamaSuresi erir
  for (let i = 0; i < 10; i++) { m.gizlendi(); m.hareketVar(); }
  ekle('S-2c on dönüşten sonra da 1200', m.asamaSuresi === 1200, `asamaSuresi ${m.asamaSuresi}`);
}

/* S-3 — 'uyari' AŞAMASI HİÇ DONDURULMUYOR.
   gizlendi() ilk satırda 'calisiyor' değilse dönüyor; molaya son
   saniyelerde gizlenen sayfa donmuyor, dönüşte 00:00 çıkıyor. */
{
  const m = new Motor({ ...AYAR, uzakKalincaSifirla: false });
  m.basla();
  m.hedefZaman = Date.now() + 10e3;
  m.tik();
  const uyaridaMi = m.durum === 'uyari';
  m.gizlendi();
  ekle('S-3 uyarı aşaması da dondurulur',
       uyaridaMi && m.durum === 'bosta' && yakin(m.kalanDondurulmus, 10, 2),
       `tik sonrası ${uyaridaMi ? 'uyari' : m.durum}, gizlendi sonrası ${m.durum}, donmuş ${m.kalanDondurulmus}`);
}

/* S-4 — DONMUŞ KALAN SIFIRSA MOLA HAK EDİLMİŞTİR.
   `?? ` sıfırı yakalamaz; kalanDondurulmus 0 ise sayaç 0 ile kurulup
   mola anında düşer ya da borç silinir. */
{
  const m = new Motor({ ...AYAR, uzakKalincaSifirla: false });
  m.basla();
  m.durum = 'bosta';
  m.kalanDondurulmus = 0;
  m.devamEt();
  ekle('S-4 donmuş kalan 0 → molaya geçilir', m.durum === 'mola', `durum ${m.durum}`);
}

const kaldi = S.filter((r) => r.durum === 'KALDI').length;
const ozet = (S.length - kaldi) + '/' + S.length + ' gecti, ' + kaldi + ' kaldi';
if (typeof document !== 'undefined' && document.body) {
  document.body.innerHTML =
    '<h1 id="ozet" data-kaldi="' + kaldi + '">' + ozet + '</h1>' +
    S.map((r) => '<div class="' + (r.durum === 'KALDI' ? 'k' : 'g') + '">' +
      (r.durum === 'KALDI' ? 'X' : 'OK') + ' ' + r.ad + ' - ' + r.ayrinti + '</div>').join('');
}
S.forEach((r) => console.log((r.durum === 'KALDI' ? 'X ' : 'OK ') + r.ad + ' - ' + r.ayrinti));
console.log(ozet);
globalThis.SINAMA_SONUC = { ozet: ozet, kaldi: kaldi, S: S };
