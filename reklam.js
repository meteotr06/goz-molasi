/* ============================================================
   REKLAM — Ana ekrandaki tek reklam alanı.

   KURAL: Reklam SADECE ana ekranda görünür.
   Mola ekranına asla konmaz. Molanın amacı gözünü ekrandan
   ayırman; oraya reklam koymak hem uygulamayı çürütür, hem de
   kimsenin bakmadığı bir yere reklam koymuş olursun.

   NASIL AÇILIR
   ------------
   1. https://adsense.google.com adresinden hesap aç, siteni ekle
      (https://meteotr06.github.io). Google siteyi inceler, 1-14 gün sürer.
   2. Onay gelince "Reklam birimi oluştur" -> Görüntülü reklam -> Yatay.
   3. Sana verdiği iki numarayı aşağıya yapıştır.
   4. AKTIF'i true yap.

   Numaralar boşken hiçbir şey yüklenmez, hiçbir istek gitmez —
   yani reklamsız sürüm de aynı dosyayla çalışır.
   ============================================================ */

const REKLAM = {
  AKTIF: false,                    // numaraları girmeden true yapma
  YAYINCI: '',                     // örn: 'ca-pub-1234567890123456'
  BIRIM: '',                       // örn: '9876543210'

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


/** Reklam alanını kurar. Kapalıysa alanı tamamen kaldırır —
    boş gri kutu bırakmak arayüzü çirkinleştirir. */
function reklamiKur(kap) {
  if (!kap) return;

  if (!REKLAM.AKTIF || !REKLAM.YAYINCI || !REKLAM.BIRIM || reklamsizMi()) {
    kap.remove();
    return;
  }

  kap.classList.remove('gizli');
  kap.innerHTML = `
    <span class="reklam-etiket">Reklam</span>
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="${REKLAM.YAYINCI}"
         data-ad-slot="${REKLAM.BIRIM}"
         data-ad-format="horizontal"
         data-full-width-responsive="true"></ins>`;

  // Betiği sadece gerçekten reklam gösterecekken yüklüyoruz.
  // Baştan yüklemek, reklam kapalıyken bile Google'a istek atardı.
  const betik = document.createElement('script');
  betik.async = true;
  betik.crossOrigin = 'anonymous';
  betik.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
            + encodeURIComponent(REKLAM.YAYINCI);
  betik.onerror = () => kap.remove();      // reklam engelleyici varsa sessizce kaybol
  document.head.appendChild(betik);

  betik.onload = () => {
    try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch {}
  };
}

if (typeof module !== 'undefined') module.exports = { REKLAM, reklamiKur, reklamsizMi };
