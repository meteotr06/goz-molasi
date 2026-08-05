/* ============================================================
   REKLAM

   İKİ AYRI YÖNTEM VAR — farkını bilmek önemli:

   1) BANNER (elle yerleştirilen birim)
      Ana ekranda, sayaçların altında duran tek şerit.
      Yerini sen seçersin.

   2) OTOMATİK REKLAMLAR + VIGNETTE (araya giren tam ekran)
      "Molalarda çıksın" isteğinin DOĞRU yolu budur.
      Google, sayfa geçişlerinde tam ekran reklam gösterir;
      nereye ve ne sıklıkta koyacağına kendi karar verir.

      Neden elle yapmıyoruz? AdSense'in normal reklam birimini
      tam ekran bir örtünün (mola ekranı) içine koymak politika
      ihlali: "araya giren reklam" manuel birimle konulamaz ve
      kaza ile tıklanabilecek yerleşim sayılır. Hesap kapatılabilir.
      Vignette ise Google'ın kendi onayladığı yöntem.

   MOLA EKRANINA ELLE REKLAM KOYULMAZ.
   Molanın amacı gözünü ekrandan ayırman. Oraya reklam koymak hem
   uygulamayı çürütür hem de hesabı riske atar.

   ------------------------------------------------------------
   NASIL AÇILIR
   1. AdSense'te site onaylansın (1-14 gün).
   2. Banner için: Reklamlar -> Reklam birimi oluştur ->
      Görüntülü reklam -> Yatay. Verdiği numarayı BIRIM'e yaz.
   3. Vignette için: AdSense -> Reklamlar -> siteye tıkla ->
      "Otomatik reklamlar"ı aç -> "Vignette reklamları"nı seç.
      Burada OTOMATIK'i true yapman yeterli.
   4. AKTIF'i true yap.
   ============================================================ */

const REKLAM = {
  // Site onaylanıp reklam birimi oluşturulunca true yap.
  // Onay gelmeden açarsan boş yer görünür, kullanıcıyı rahatsız eder.
  AKTIF: false,

  YAYINCI: 'ca-pub-4471538043632173',   // hesap numarası — hazır
  BIRIM: '',                            // banner birimi — onaydan sonra

  // Otomatik Reklamlar: Vignette (araya giren) dahil.
  // Sıklığı Google ayarlar; kullanıcıyı boğmaz.
  OTOMATIK: false,

  // Reklamsız sürüm satın alanlar için (ileride)
  REKLAMSIZ_ANAHTARI: 'goz-molasi-reklamsiz',
};


function reklamsizMi() {
  try {
    return localStorage.getItem(REKLAM.REKLAMSIZ_ANAHTARI) === 'evet';
  } catch {
    return false;
  }
}


/** AdSense betiğini bir kez yükler. */
let _betikSozu = null;
function adsenseYukle() {
  if (_betikSozu) return _betikSozu;
  _betikSozu = new Promise((coz, hata) => {
    const betik = document.createElement('script');
    betik.async = true;
    betik.crossOrigin = 'anonymous';
    betik.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
              + encodeURIComponent(REKLAM.YAYINCI);
    betik.onload = coz;
    betik.onerror = hata;       // reklam engelleyici varsa buraya düşer
    document.head.appendChild(betik);
  });
  return _betikSozu;
}


/** Otomatik reklamlar (Vignette dahil) — araya giren tam ekran reklamlar.
    Yerleştirmeyi ve sıklığı Google yönetir. */
async function otomatikReklamlariAc() {
  if (!REKLAM.OTOMATIK) return;
  try {
    await adsenseYukle();
    (window.adsbygoogle = window.adsbygoogle || []).push({
      google_ad_client: REKLAM.YAYINCI,
      enable_page_level_ads: true,
      overlays: { bottom: true },
    });
  } catch { /* engelleyici var, sessizce geç */ }
}


/** Ana ekrandaki banner. Kapalıysa alanı tamamen kaldırır —
    boş gri kutu bırakmak arayüzü çirkinleştirir. */
async function reklamiKur(kap) {
  if (!REKLAM.AKTIF || !REKLAM.YAYINCI || reklamsizMi()) {
    if (kap) kap.remove();
    return;
  }

  // Vignette'i her koşulda dene (banner birimi olmasa bile çalışır)
  otomatikReklamlariAc();

  if (!kap) return;
  if (!REKLAM.BIRIM) { kap.remove(); return; }

  kap.classList.remove('gizli');
  kap.innerHTML = `
    <span class="reklam-etiket">Reklam</span>
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="${REKLAM.YAYINCI}"
         data-ad-slot="${REKLAM.BIRIM}"
         data-ad-format="horizontal"
         data-full-width-responsive="true"></ins>`;

  try {
    await adsenseYukle();
    (window.adsbygoogle = window.adsbygoogle || []).push({});
  } catch {
    kap.remove();               // engelleyici varsa sessizce kaybol
  }
}

if (typeof module !== 'undefined') {
  module.exports = { REKLAM, reklamiKur, reklamsizMi, otomatikReklamlariAc };
}
