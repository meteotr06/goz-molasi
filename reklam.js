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

  /* Reklam birimleri. AdSense'te her yerleşim için AYRI birim
     oluşturursun; böylece hangisinin kazandırdığını görebilirsin.
     Onay gelince buraya numaraları yapıştır — başka bir şey gerekmez.

     ana         : ana ekran, sayaçların altı (yatay)
     rehberUst   : rehber yazısının başı (yatay)
     rehberOrta  : rehber yazısının ortası (yazı arası — en iyi tıklanan)
     rehberAlt   : rehber yazısının sonu (kare) */
  BIRIMLER: {
    ana: '',
    rehberUst: '',
    rehberOrta: '',
    rehberAlt: '',
  },

  // Eski tek-birim ayarı — geriye dönük uyum için duruyor
  BIRIM: '',

  // Otomatik Reklamlar: Vignette (araya giren) dahil.
  // Sıklığı Google ayarlar; kullanıcıyı boğmaz.
  OTOMATIK: false,

  /* ÖNİZLEME KİPİ
     Onay gelmeden reklamın nerede ve ne kadar yer kaplayacağını
     görmek için. Sahte bir kutu çizer, Google'a hiç istek gitmez.
     Adrese ?reklam=onizleme eklersen de açılır — yayındaki siteyi
     bozmadan denemek için. */
  ONIZLEME: false,

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


/** Önizleme: sahte reklam kutusu çizer. Google'a hiç istek gitmez.
    Amaç, onay beklerken yerleşimi görebilmek. */
const OLCU_YAZI = {
  horizontal: '728 × 90 · yatay görüntülü reklam',
  rectangle: '300 × 250 · kare görüntülü reklam',
  fluid: 'yazı arası · genişliğe uyar',
  auto: 'otomatik · ekrana uyar',
};

function onizlemeCiz(kap) {
  const bicim = kap.dataset.bicim || 'horizontal';
  kap.classList.remove('gizli');
  kap.innerHTML = '';

  const etiket = document.createElement('span');
  etiket.className = 'reklam-etiket';
  // Onizleme kipi canlida da acilabiliyor (?reklam=onizleme),
  // o yuzden bu etiket de dilden geciyor. `CS` yoksa Turkcesi.
  etiket.textContent = (typeof CS === 'function')
    ? CS('Reklam · ÖNİZLEME', 'Ad · PREVIEW')
    : 'Reklam · ÖNİZLEME';

  const kutu = document.createElement('div');
  kutu.className = 'reklam-sahte';
  kutu.dataset.bicim = bicim;

  const ic = document.createElement('div');
  ic.className = 'reklam-sahte-ic';
  const b1 = document.createElement('b');
  b1.textContent = 'Reklam buraya gelecek';
  const s1 = document.createElement('span');
  s1.textContent = OLCU_YAZI[bicim] || bicim;
  const s2 = document.createElement('small');
  s2.textContent = 'Sahte kutu — Googleye istek gitmiyor. Birim: '
                 + (kap.dataset.birim || 'ana');
  ic.append(b1, s1, s2);
  kutu.appendChild(ic);
  kap.append(etiket, kutu);
}


/** Reklam durumunu tek bakışta gösterir (konsoldan çağır). */
function reklamDurumu() {
  const d = {
    aktif: REKLAM.AKTIF,
    onizleme: REKLAM.ONIZLEME || new URLSearchParams(location.search).get('reklam') === 'onizleme',
    otomatikVignette: REKLAM.OTOMATIK,
    yayinci: REKLAM.YAYINCI || '(boş)',
    birimler: Object.entries(REKLAM.BIRIMLER || {})
      .map(([k, v]) => k + '=' + (v || '(boş)')).join(' · '),
    reklamsizSurum: reklamsizMi(),
    sayfadaKutuSayisi: document.querySelectorAll('.reklam-alani').length,
    dolduruldu: !!document.querySelector('ins.adsbygoogle[data-ad-status="filled"]'),
    googleIstegi: performance.getEntriesByType('resource')
      .filter((x) => /googlesyndication|doubleclick/.test(x.name)).length,
  };
  console.table(d);
  return d;
}


/** Bir reklam kutusunu kurar.

    Kutu HTML'de şöyle işaretlenir:
      <aside class="reklam-alani gizli" data-birim="rehberOrta"
             data-bicim="fluid"></aside>

    data-birim  : REKLAM.BIRIMLER içindeki anahtar
    data-bicim  : horizontal | rectangle | fluid | auto

    Numara girilmemişse kutu tamamen kaldırılır — boş gri dikdörtgen
    bırakmak hem çirkin hem de AdSense'in hoşlanmadığı bir şey. */
async function reklamiKur(kap) {
  const onizleme = REKLAM.ONIZLEME
    || new URLSearchParams(location.search).get('reklam') === 'onizleme';

  if (onizleme && kap) { onizlemeCiz(kap); return; }

  if (!REKLAM.AKTIF || !REKLAM.YAYINCI || reklamsizMi()) {
    if (kap) kap.remove();
    return;
  }

  // Vignette'i her koşulda dene (banner birimi olmasa bile çalışır)
  otomatikReklamlariAc();

  if (!kap) return;

  const anahtar = kap.dataset.birim || 'ana';
  const bicim = kap.dataset.bicim || 'horizontal';
  const numara = (REKLAM.BIRIMLER && REKLAM.BIRIMLER[anahtar]) || REKLAM.BIRIM;
  if (!numara) { kap.remove(); return; }

  kap.classList.remove('gizli');
  kap.innerHTML = '';

  const etiket = document.createElement('span');
  etiket.className = 'reklam-etiket';
  etiket.textContent = 'Reklam';

  const ins = document.createElement('ins');
  ins.className = 'adsbygoogle';
  ins.style.display = 'block';
  ins.dataset.adClient = REKLAM.YAYINCI;
  ins.dataset.adSlot = numara;
  ins.dataset.adFormat = bicim;
  if (bicim === 'fluid') ins.dataset.adLayout = 'in-article';
  else ins.dataset.fullWidthResponsive = 'true';

  kap.append(etiket, ins);

  try {
    await adsenseYukle();
    (window.adsbygoogle = window.adsbygoogle || []).push({});
  } catch {
    kap.remove();               // engelleyici varsa sessizce kaybol
  }
}


/** Sayfadaki BÜTÜN reklam kutularını kurar.
    Her sayfada tek satır çağırmak yeter: tumReklamlariKur() */
function tumReklamlariKur(kok = document) {
  kok.querySelectorAll('.reklam-alani').forEach((k) => {
    try { reklamiKur(k); } catch {}
  });
}

// Konsoldan durumu görmek için: reklamDurumu()
if (typeof window !== 'undefined') {
  window.reklamDurumu = reklamDurumu;
  window.tumReklamlariKur = tumReklamlariKur;
}

if (typeof module !== 'undefined') {
  module.exports = { REKLAM, reklamiKur, tumReklamlariKur, reklamsizMi,
                     otomatikReklamlariAc, reklamDurumu };
}
