/* ============================================================
   ARAYÜZ — Motoru ekrana bağlayan katman
   cekirdek.js'yi hiç değiştirmeden burayı istediğin gibi
   düzenleyebilirsin.
   ============================================================ */

(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const KAYIT_ANAHTARI = 'goz-molasi-v1';

  /* ---------- Öğeler ---------- */
  const og = {
    govde: document.body,
    sure: $('sureYazi'),
    durum: $('durumYazi'),
    halka: $('halkaDolu'),
    aciklama: $('aciklama'),
    baslat: $('baslatDugme'),
    mola: $('molaDugme'),
    sifirla: $('sifirlaDugme'),
    bildirim: $('bildirimDugme'),
    kur: $('kurDugme'),
    tema: $('temaDugme'),
    paylas: $('paylasDugme'),
    ayarAc: $('ayarDugme'),

    istMola: $('istMola'),
    istAtlanan: $('istAtlanan'),
    istSure: $('istSure'),

    haftaGrafik: $('haftaGrafik'),
    seriRozet: $('seriRozet'),
    haftaOzet: $('haftaOzet'),
    hedefSayi: $('hedefSayi'),

    anaBaslik: $('anaBilgiBaslik'),
    anaMetin: $('anaBilgiMetin'),
    anaKaynak: $('anaBilgiKaynak'),

    balon: $('uyariBalon'),
    balonMetin: $('uyariMetin'),
    ertele: $('erteleDugme'),

    molaEkran: $('molaEkran'),
    molaBaslik: $('molaBaslik'),
    molaAlt: $('molaAlt'),
    molaHalka: $('molaHalka'),
    molaSayi: $('molaSayi'),
    egzersizTuval: $('egzersizTuval'),
    nedenKart: $('nedenKart'),
    bitisKart: $('bitisKart'),
    bitisBaslik: $('bitisBaslik'),
    bitisAlt: $('bitisAlt'),
    bitisKapat: $('bitisKapat'),
    etkinlikDugme: $('etkinlikDugme'),
    etkinlikDurum: $('etkinlikDurum'),
    istSureEtiket: $('istSureEtiket'),
    sureKutucuk: $('sureKutucuk'),
    ayHava: $('ayHava'),
    havaDurum: $('havaDurum'),
    havaKonumSatir: $('havaKonumSatir'),
    konumBulDugme: $('konumBulDugme'),
    konumSilDugme: $('konumSilDugme'),
    sehirAlan: $('sehirAlan'),
    sehirSonuc: $('sehirSonuc'),
    nedenBaslik: $('nedenBaslik'),
    nedenMetin: $('nedenMetin'),
    nedenKaynak: $('nedenKaynak'),
    atla: $('atlaDugme'),
    okuyucu: $('ekranOkuyucu'),

    pencere: $('ayarPencere'),
    ayCalisma: $('ayCalisma'),
    ayMola: $('ayMola'),
    ayUyari: $('ayUyari'),
    ayAtla: $('ayAtla'),
    aySes: $('aySes'),
    ayBosta: $('ayBosta'),
    ayOtomatik: $('ayOtomatik'),
    ayTitresim: $('ayTitresim'),
    ayArkaPlan: $('ayArkaPlan'),
    arkaPlanNot: $('arkaPlanNot'),
    temaSeridi: $('temaSeridi'),
    ayCanlilik: $('ayCanlilik'),
    ayCanlilikDeger: $('ayCanlilikDeger'),
    canlilikDurum: $('canlilikDurum'),
    temaAdi: $('temaAdi'),
    hazirSureler: $('hazirSureler'),
    ayCalismaDeger: $('ayCalismaDeger'),
    ayMolaDeger: $('ayMolaDeger'),
    ayUyariDeger: $('ayUyariDeger'),
    sureOzeti: $('sureOzeti'),
    ayUzunMola: $('ayUzunMola'),
    uzunMolaAyar: $('uzunMolaAyar'),
    ayUzunSure: $('ayUzunSure'),
    ayUzunSureDeger: $('ayUzunSureDeger'),
    uzunMolaNe: $('uzunMolaNe'),
    aySaatler: $('aySaatler'),
    saatAyar: $('saatAyar'),
    ayBasSaat: $('ayBasSaat'),
    ayBitSaat: $('ayBitSaat'),
    ayarKaydet: $('ayarKaydet'),
    ayarVazgec: $('ayarVazgec'),

    ayKilitAlan: $('ayKilitAlan'),
    kilitDurum: $('kilitDurum'),
    kilitKur: $('kilitKurDugme'),
    kilitKaldir: $('kilitKaldirDugme'),
    sifrePencere: $('sifrePencere'),
    sifreForm: $('sifreForm'),
    sifreAlan: $('sifreAlan'),
    sifreHata: $('sifreHata'),
    sifreAciklama: $('sifreAciklama'),
    sifreVazgec: $('sifreVazgec'),
    hepsiniSil: $('hepsiniSilDugme'),
    sifirlamaDurum: $('sifirlamaDurum'),
  };

  const CEVRE_ANA  = 2 * Math.PI * 88;   // ana halkanın çevresi
  const CEVRE_MOLA = 2 * Math.PI * 92;   // mola halkasının çevresi
  const BOSTA_ESIGI = 90;                // saniye

  /* ---------- Kayıtlı ayarları oku ---------- */
  let kayit = {};
  try { kayit = JSON.parse(localStorage.getItem(KAYIT_ANAHTARI) || '{}'); } catch { kayit = {}; }

  const motor = new MolaMotoru();
  motor.iceAktar(kayit);
  let bostaAcik = kayit.bostaAcik !== false;
  let otomatikBasla = kayit.otomatikBasla !== false;   // varsayılan: açık
  let titresimAcik = kayit.titresimAcik !== false;     // varsayılan: açık (telefonda)
  let arkaPlanAcik = kayit.arkaPlanAcik === true;      // varsayılan: KAPALI (pil)
  if (!bostaAcik) motor.ayarlar.bostaEsigi = 1e9;
  let tema = kayit.tema || 'otomatik';
  temaUygula(tema);

  /* ============================================================
     KİLİT (KATI MOD)
     Şifre konunca molayı atlamak, duraklatmak, sıfırlamak ve
     ayarları değiştirmek şifre ister.

     Şifre DÜZ METİN olarak saklanmaz; tuzlanıp özeti (SHA-256)
     saklanır. Yine de bu bir cihaz güvenliği değildir — amacı
     refleksle "atla"ya basmayı zorlaştırmak. Bunu kullanıcıya
     ayarlar penceresinde açıkça yazıyoruz.
     ============================================================ */
  /* TEK SEFERLİK KİLİT SIFIRLAMA
     Geliştirme sırasında bazı tarayıcılarda test şifresi kaldı ve
     kullanıcı ayarlara giremez oldu. Bu sürüm, daha önce kalmış her
     şifreyi bir kez temizler. Kullanıcı isterse yeniden koyabilir.
     Damga bir kez yazılır; sonraki açılışlarda tekrar silmez. */
  const KILIT_SIFIRLAMA_DAMGASI = 'v1-agustos-2026';
  if (kayit.kilitSifirlandi !== KILIT_SIFIRLAMA_DAMGASI) {
    kayit.kilitOzeti = null;
    kayit.kilitTuz = null;
    kayit.kilitSifirlandi = KILIT_SIFIRLAMA_DAMGASI;
    try {
      localStorage.setItem(KAYIT_ANAHTARI, JSON.stringify(kayit));
    } catch {}
  }

  let kilitOzeti = kayit.kilitOzeti || null;
  let kilitTuz = kayit.kilitTuz || null;
  let yanlisSayisi = 0;
  let bekletmeBitis = 0;
  let sifreCoz = null;

  async function ozetle(metin, tuz) {
    const veri = new TextEncoder().encode(`${tuz}|${metin}`);
    if (window.crypto?.subtle) {
      const tampon = await crypto.subtle.digest('SHA-256', veri);
      return [...new Uint8Array(tampon)].map((b) => b.toString(16).padStart(2, '0')).join('');
    }
    // Güvenli bağlam yoksa (örn. dosyaya çift tıklayarak açınca) yedek yöntem.
    let h = 5381;
    for (const k of veri) h = ((h * 33) ^ k) >>> 0;
    return 'yedek' + h.toString(16);
  }

  function yeniTuz() {
    const d = new Uint8Array(8);
    (window.crypto || {}).getRandomValues?.(d);
    return [...d].map((b) => b.toString(16).padStart(2, '0')).join('') || String(Date.now());
  }

  /** Şifre sorar. Kilit yoksa doğrudan izin verir. */
  function sifreSor(aciklama) {
    if (!kilitOzeti) return Promise.resolve(true);

    const kalanBekleme = Math.ceil((bekletmeBitis - Date.now()) / 1000);
    og.sifreAciklama.textContent = kalanBekleme > 0
      ? `Çok fazla yanlış deneme. ${kalanBekleme} saniye bekle.`
      : aciklama;
    og.sifreAlan.value = '';
    og.sifreHata.textContent = '';
    og.sifreAlan.disabled = kalanBekleme > 0;
    if (!og.sifrePencere.open) og.sifrePencere.showModal();
    setTimeout(() => og.sifreAlan.focus(), 30);
    return new Promise((coz) => { sifreCoz = coz; });
  }

  function sifreKapat(sonuc) {
    if (og.sifrePencere.open) og.sifrePencere.close();
    const c = sifreCoz;
    sifreCoz = null;
    c?.(sonuc);
  }

  og.sifreForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (bekletmeBitis > Date.now()) return;
    const girilen = og.sifreAlan.value;
    if (await ozetle(girilen, kilitTuz) === kilitOzeti) {
      yanlisSayisi = 0;
      sifreKapat(true);
    } else {
      yanlisSayisi++;
      og.sifreAlan.value = '';
      if (yanlisSayisi >= 3) {
        bekletmeBitis = Date.now() + 30000;
        yanlisSayisi = 0;
        og.sifreHata.textContent = 'Çok fazla yanlış deneme — 30 saniye bekle.';
        og.sifreAlan.disabled = true;
        setTimeout(() => {
          og.sifreAlan.disabled = false;
          og.sifreHata.textContent = '';
          og.sifreAlan.focus();
        }, 30000);
      } else {
        og.sifreHata.textContent = `Şifre yanlış. Kalan deneme: ${3 - yanlisSayisi}`;
      }
    }
  });
  /* ŞİFREMİ UNUTTUM
     Web'de şifreyi gizli tutmanın bir sınırı var: kullanıcı zaten
     tarayıcı ayarlarından site verisini silip kilidi kaldırabiliyor.
     Sıfırlamayı şifrenin arkasına saklamak güvenlik katmıyor, sadece
     dürüst kullanıcıyı kilitli bırakıyor. O yüzden açık bir çıkış yolu
     veriyoruz — ama ne olacağını net söyleyerek. */
  $('sifreUnuttum').addEventListener('click', () => {
    const onay = confirm(
      ['Şifreni sıfırlamanın tek yolu tüm verileri silmek.',
       '',
       'Silinecekler: şifre, ayarların, bugünkü sayaçlar ve 7 günlük geçmiş.',
       'Uygulama ilk günkü haline döner.',
       '',
       'Devam edilsin mi?'].join('\n'));
    if (!onay) return;
    silindi = true;
    try {
      localStorage.removeItem(KAYIT_ANAHTARI);
      localStorage.removeItem('goz-molasi-gecmis');
      localStorage.removeItem('goz-molasi-kurulum-kapatildi');
    } catch {}
    location.reload();
  });

  og.sifreVazgec.addEventListener('click', () => sifreKapat(false));
  og.sifrePencere.addEventListener('cancel', (e) => { e.preventDefault(); sifreKapat(false); });

  /* ============================================================
     MOLA BİTİŞİ KARTI
     Mola biter bitmez ana ekranda birkaç saniye görünür.
     Reklam İÇERMEZ: birden beliren reklam AdSense ihlalidir ve
     zaten molanın hemen ardından reklam göstermek uygulamayı
     çürütür. Reklam sayfadaki sabit yerinde durmaya devam eder.
     ============================================================ */
  const BITIS_SURE = 14000;
  let bitisZaman = 0;

  function bitisKartiniGoster(istatistik, atlandiMi = false) {
    const bugun = (istatistik && istatistik.tamamlananMola) | 0;
    const seri = Gecmis.seri(istatistik);

    og.bitisBaslik.textContent = atlandiMi ? 'Mola atlandı' : 'Mola tamam';

    const parcalar = [];
    if (!atlandiMi && bugun > 0) parcalar.push(`Bugün ${bugun}. molan`);
    if (seri >= 2) parcalar.push(`${seri} gündür üst üste`);
    const dk = Math.max(1, Math.round(motor.ayarlar.calismaSuresi / 60));
    parcalar.push(`sonraki mola ${dk} dakika sonra`);
    og.bitisAlt.textContent = parcalar.join(' · ');

    og.bitisKart.hidden = false;
    // hidden kalkar kalkmaz sınıf eklersek geçiş çalışmaz: aynı karede
    // display:none'dan çıkıyor, tarayıcı başlangıç değerini görmüyor.
    // requestAnimationFrame KULLANMIYORUZ — sekme arka plandayken hiç
    // çalışmıyor ve kart sonsuza kadar opaklık 0'da kalıyordu (kutu
    // yer kaplıyor ama görünmüyor). Zorunlu yeniden akış (reflow)
    // arka planda da çalışır.
    void og.bitisKart.offsetHeight;
    og.bitisKart.classList.add('gorunur');

    clearTimeout(bitisZaman);
    bitisZaman = setTimeout(bitisKartiniGizle, BITIS_SURE);
  }

  function bitisKartiniGizle() {
    clearTimeout(bitisZaman);
    og.bitisKart.classList.remove('gorunur');
    setTimeout(() => { og.bitisKart.hidden = true; }, 400);
  }

  og.bitisKapat.addEventListener('click', bitisKartiniGizle);

  /* ---- Cihaz etkinliği izni: ayarlardaki düğme ---- */
  async function etkinlikDurumunuGoster() {
    const d = await etkinlikIzniDurumu();
    const acik = !!etkinlikDedektoru;

    if (d === 'desteklenmiyor') {
      og.etkinlikDugme.disabled = true;
      og.etkinlikDugme.textContent = 'Desteklenmiyor';
      og.etkinlikDurum.textContent =
        'Bu tarayıcı cihaz etkinliğini paylaşmıyor (Chrome ve Edge destekliyor). ' +
        'Sayaç yalnızca bu sekmedeki hareketi görüyor.';
      return;
    }
    if (acik) {
      og.etkinlikDugme.textContent = 'Kapat';
      og.etkinlikDurum.textContent =
        'Açık — sekme arka plandayken de cihazda hareket olup olmadığı görülüyor. ' +
        'Sadece "etkin mi, ekran kilitli mi" bilgisi; ne yaptığın değil.';
    } else if (d === 'denied') {
      og.etkinlikDugme.textContent = 'İzin ver';
      og.etkinlikDurum.textContent =
        'İzin reddedilmiş. Adres çubuğundaki kilit simgesinden açabilirsin.';
    } else {
      og.etkinlikDugme.textContent = 'İzin ver';
      og.etkinlikDurum.textContent =
        'Kapalı — sayaç yalnızca bu sekmedeki hareketi görüyor. ' +
        'Başka pencerede çalışırken "boşta" sanılabilir.';
    }
  }

  og.etkinlikDugme.addEventListener('click', async () => {
    if (etkinlikDedektoru) {
      etkinligiDurdur();
    } else {
      og.etkinlikDugme.disabled = true;
      await etkinligiBaslat(true);
      og.etkinlikDugme.disabled = false;
    }
    og.ayCanlilik.value = canlilikOku();
    canlilikUygula(canlilikOku());
    etkinlikDurumunuGoster();
  });

  /* ============================================================
     MOLALARDA HAVA DURUMU
     Konum tarayıcıdan ya da şehir aramasıyla alınır. Konum yoksa
     hava kartı sıraya hiç girmez; molalar eskisi gibi çalışır.
     ============================================================ */
  const HAVA_ACIK_ANAHTAR = 'goz-molasi-hava-acik';
  let havaAcik = (() => {
    try { return localStorage.getItem(HAVA_ACIK_ANAHTAR) !== '0'; } catch { return true; }
  })();

  MolaIcerik.havaAyarla(havaAcik);

  function havaDurumunuGoster(mesaj) {
    const konum = MolaIcerik.konumOku();
    og.havaKonumSatir.classList.toggle('gizli', !og.ayHava.checked);
    og.konumSilDugme.classList.toggle('gizli', !konum);
    if (mesaj) { og.havaDurum.textContent = mesaj; return; }
    if (!og.ayHava.checked) {
      og.havaDurum.textContent = 'Kapalı — molalarda yalnızca göz bilgisi gösterilir';
    } else if (konum) {
      og.havaDurum.textContent = (konum.ad ? konum.ad + ' · ' : '') +
        'her birkaç molada bir hava durumu gösterilir';
    } else {
      og.havaDurum.textContent = 'Açık — önce konum ver ya da şehir ara';
    }
  }

  og.ayHava.addEventListener('change', () => havaDurumunuGoster());

  og.konumBulDugme.addEventListener('click', async () => {
    og.konumBulDugme.disabled = true;
    havaDurumunuGoster('Konum alınıyor…');
    const s = await MolaIcerik.konumuBul();
    og.konumBulDugme.disabled = false;
    havaDurumunuGoster(s.hata || null);
  });

  og.konumSilDugme.addEventListener('click', () => {
    MolaIcerik.konumSil();
    og.sehirAlan.value = '';
    og.sehirSonuc.innerHTML = '';
    havaDurumunuGoster('Konum unutuldu.');
  });

  // Yazarken her tuşta ağa çıkmayalım — 350 ms bekle
  let sehirZaman = 0;
  og.sehirAlan.addEventListener('input', () => {
    clearTimeout(sehirZaman);
    const q = og.sehirAlan.value;
    if (q.trim().length < 2) { og.sehirSonuc.innerHTML = ''; return; }
    sehirZaman = setTimeout(async () => {
      const liste = await MolaIcerik.sehirAra(q);
      og.sehirSonuc.innerHTML = '';
      if (!liste.length) {
        og.sehirSonuc.textContent = 'Sonuç yok.';
        return;
      }
      liste.forEach((y) => {
        const d = document.createElement('button');
        d.type = 'button';
        d.className = 'sehir-secenek';
        d.innerHTML = '';
        const ad = document.createElement('b'); ad.textContent = y.ad;
        const alt = document.createElement('span'); alt.textContent = y.alt;
        d.append(ad, alt);
        d.addEventListener('click', () => {
          MolaIcerik.sehirSec(y);
          og.sehirSonuc.innerHTML = '';
          og.sehirAlan.value = '';
          havaDurumunuGoster(y.ad + ' seçildi.');
        });
        og.sehirSonuc.appendChild(d);
      });
    }, 350);
  });

  const ASIL_BASLIK = document.title;

  function kilitDurumunuGoster() {
    const acik = !!kilitOzeti;
    og.kilitDurum.textContent = acik
      ? 'Açık — şifreyi değiştirme ve verileri silme korumalı'
      : 'Kapalı — verileri silmek serbest';
    og.kilitKur.textContent = acik ? 'Şifreyi değiştir' : 'Şifreyi koy';
    og.kilitKaldir.classList.toggle('gizli', !acik);
    og.atla.textContent = atlaEtiketi();
    // HTML'deki başlığı koruyoruz. Eskiden sabit bir metin yazılıyordu ve
    // sayfanın arama için yazılmış <title>'ını eziyordu — Googlebot sayfayı
    // çalıştırdığı için ezilmiş halini görüyordu.
    document.title = acik ? '🔒 ' + ASIL_BASLIK : ASIL_BASLIK;
  }

  og.kilitKur.addEventListener('click', async () => {
    if (kilitOzeti && !(await sifreSor('Şifreyi değiştirmek için önce mevcut şifreni gir.'))) return;
    const yeni = (og.ayKilitAlan.value || '').trim();
    if (!/^\d{4,8}$/.test(yeni)) {
      og.kilitDurum.textContent = 'Şifre 4–8 rakam olmalı.';
      og.ayKilitAlan.focus();
      return;
    }
    kilitTuz = yeniTuz();
    kilitOzeti = await ozetle(yeni, kilitTuz);
    og.ayKilitAlan.value = '';
    kilitDurumunuGoster();
    kaydet();
  });

  og.kilitKaldir.addEventListener('click', async () => {
    if (!(await sifreSor('Kilidi kaldırmak için şifreni gir.'))) return;
    kilitOzeti = null;
    kilitTuz = null;
    og.ayKilitAlan.value = '';
    kilitDurumunuGoster();
    kaydet();
  });

  /* ============================================================
     SES — Tarayıcı, kullanıcı sayfaya dokunmadan ses çaldırmaz.
     Bu yüzden ilk dokunuşta ses motorunu "uyandırıyoruz".
     ============================================================ */
  let sesMotoru = null;
  function sesiUyandir() {
    try {
      sesMotoru ||= new (window.AudioContext || window.webkitAudioContext)();
      if (sesMotoru.state === 'suspended') sesMotoru.resume();
    } catch { /* ses yoksa uygulama yine çalışır */ }
  }
  document.addEventListener('pointerdown', sesiUyandir, { once: true });
  document.addEventListener('keydown', sesiUyandir, { once: true });

  function calSes(frekans = 880, sure = 0.5) {
    if (!motor.ayarlar.sesAcik || !sesMotoru || sesMotoru.state !== 'running') return;
    const t = sesMotoru.currentTime;
    const osc = sesMotoru.createOscillator();
    const kazanc = sesMotoru.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(frekans, t);
    kazanc.gain.setValueAtTime(0.0001, t);
    kazanc.gain.exponentialRampToValueAtTime(0.25, t + 0.02);
    kazanc.gain.exponentialRampToValueAtTime(0.0001, t + sure);
    osc.connect(kazanc).connect(sesMotoru.destination);
    osc.start(t);
    osc.stop(t + sure + 0.05);
  }

  /* ============================================================
     TİTREŞİM — telefonda sesten daha güvenilir.
     Telefon sessizdeyken ses duyulmaz ama titreşim hissedilir.
     ============================================================ */
  function titret(desen) {
    if (!titresimAcik || !navigator.vibrate) return;
    try { navigator.vibrate(desen); } catch {}
  }

  /* ============================================================
     ARKA PLANDA ÇALIŞMAYA DEVAM
     Tarayıcılar arka plandaki sekmenin zamanlayıcısını yavaşlatır,
     telefon kilitlenince tamamen dondurur. Sekmede SES ÇALIYORSA
     tarayıcı onu "işitilebilir" sayar ve kısmayı uygulamaz.
     Bu yüzden duyulmayan bir ses döngüsü çalıyoruz.

     Pil tüketir; bu yüzden varsayılan KAPALI ve kullanıcıya
     ne olduğunu açıkça yazıyoruz.
     ============================================================ */
  let sessizSes = null;

  function arkaPlanKipi(ac) {
    if (ac) {
      if (sessizSes) return;
      try {
        sesiUyandir();
        if (!sesMotoru) return;
        // Neredeyse tamamen sessiz ama "ses çalıyor" sayılan bir sinyal
        const osc = sesMotoru.createOscillator();
        const kazanc = sesMotoru.createGain();
        osc.frequency.value = 30;              // duyulmayacak kadar alçak
        kazanc.gain.value = 0.0001;            // duyulmayacak kadar kısık
        osc.connect(kazanc).connect(sesMotoru.destination);
        osc.start();
        sessizSes = { osc, kazanc };
      } catch { sessizSes = null; }
    } else if (sessizSes) {
      try { sessizSes.osc.stop(); sessizSes.osc.disconnect(); } catch {}
      sessizSes = null;
    }
  }

  /* ============================================================
     EKRAN UYANIK TUTMA — mola ekranı açıkken telefon uyumasın
     ============================================================ */
  let uyanikKilit = null;
  async function uyanikTut() {
    try { uyanikKilit = await navigator.wakeLock.request('screen'); } catch { uyanikKilit = null; }
  }
  function uyanikBirak() {
    try { uyanikKilit?.release(); } catch {}
    uyanikKilit = null;
  }

  /* ============================================================
     BİLDİRİM — sekme arka plandayken haber verir
     ============================================================ */
  function bildirimGonder(baslik, metin) {
    if (!('Notification' in window) || Notification.permission !== 'granted') return;
    navigator.serviceWorker?.ready
      .then((kayitli) => kayitli.active?.postMessage({ tur: 'bildirim', baslik, metin }))
      .catch(() => {});
  }

  og.bildirim.addEventListener('click', async () => {
    if (!('Notification' in window)) {
      og.bildirim.textContent = '🔕 Bu tarayıcı bildirim desteklemiyor';
      return;
    }
    // iOS'ta izin isteği MUTLAKA bir dokunuşun içinden çağrılmalı
    const sonuc = await Notification.requestPermission();
    bildirimDurumunuGoster(sonuc);
  });

  function bildirimDurumunuGoster(izin = (window.Notification?.permission)) {
    if (!('Notification' in window)) { og.bildirim.classList.add('gizli'); return; }
    if (izin === 'granted') {
      og.bildirim.textContent = '🔔 Bildirimler açık';
      og.bildirim.disabled = true;
    } else if (izin === 'denied') {
      og.bildirim.textContent = '🔕 Bildirimlere izin verilmedi';
      og.bildirim.disabled = true;
    }
  }

  /* ============================================================
     PAYLAŞ
     Telefonda cihazın kendi paylaşım penceresi açılır (WhatsApp,
     Telegram…). Masaüstünde o pencere yok, linki panoya kopyalıyoruz.
     ============================================================ */
  const PAYLASIM = {
    title: 'Göz Molası — 20·20·20',
    text: 'Her 20 dakikada 20 saniyelik göz molası hatırlatıyor, molada ne yapman '
        + 'gerektiğini gösteriyor. Kurulum yok:',
    url: 'https://meteotr06.github.io/goz-molasi/',
  };

  og.paylas.addEventListener('click', async () => {
    if (navigator.share) {
      try { await navigator.share(PAYLASIM); return; } catch { /* iptal etti */ return; }
    }
    try {
      await navigator.clipboard.writeText(`${PAYLASIM.text} ${PAYLASIM.url}`);
      const eski = og.paylas.textContent;
      og.paylas.textContent = '✓';
      og.paylas.title = 'Link kopyalandı';
      setTimeout(() => { og.paylas.textContent = eski; og.paylas.title = 'Paylaş'; }, 1800);
    } catch {
      prompt('Linki kopyala:', PAYLASIM.url);
    }
  });

  /* ============================================================
     UYGULAMA OLARAK KURMA
     Tarayıcı "bu sayfa kurulabilir" dediğinde düğmeyi gösteriyoruz.
     Kendi düğmemiz olması önemli: tarayıcının kendi kurulum çubuğu
     telefonda çoğu zaman görünmüyor ya da kapatılıyor.
     ============================================================ */
  let kurulumOlayi = null;
  const serit = $('kurulumSerit');
  const iosPencere = $('iosPencere');
  const KURULUM_KAPATILDI = 'goz-molasi-kurulum-kapatildi';

  /** Zaten uygulama olarak açıldıysa hiçbir davet gösterme */
  const uygulamaKipi = window.matchMedia('(display-mode: standalone)').matches
    || window.navigator.standalone === true;

  const iOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  const android = /android/i.test(navigator.userAgent);

  function kurulumKapatildiMi() {
    try { return localStorage.getItem(KURULUM_KAPATILDI) === 'evet'; } catch { return false; }
  }

  function seridiGoster(baslik, aciklama, dugmeYazi) {
    if (uygulamaKipi || kurulumKapatildiMi()) return;
    $('kurulumBaslik').textContent = baslik;
    $('kurulumAciklama').textContent = aciklama;
    $('kurulumEvet').textContent = dugmeYazi;
    serit.classList.remove('gizli');
  }

  function seridiGizle(kalici = false) {
    serit.classList.add('gizli');
    if (kalici) { try { localStorage.setItem(KURULUM_KAPATILDI, 'evet'); } catch {} }
  }

  $('kurulumHayir').addEventListener('click', () => seridiGizle(true));
  $('iosTamam').addEventListener('click', () => iosPencere.close());

  $('kurulumEvet').addEventListener('click', async () => {
    if (kurulumOlayi) {
      kurulumOlayi.prompt();
      const { outcome } = await kurulumOlayi.userChoice;
      kurulumOlayi = null;
      if (outcome === 'accepted') seridiGizle(true);
      return;
    }
    if (iOS) { iosPencere.showModal(); return; }
    // Masaüstü: tarayıcının kurulum simgesini göster
    $('kurulumAciklama').textContent =
      'Adres çubuğunun sağındaki ⊕ / kurulum simgesine bas';
    $('kurulumAciklama').style.color = 'var(--vurgu)';
  });

  /* Android/Chrome/Edge: tarayıcı "bu kurulabilir" dediğinde */
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();               // kendi davetimizi gösteriyoruz
    kurulumOlayi = e;
    og.kur.classList.remove('gizli');
    seridiGoster('Uygulama olarak kur',
                 'Ana ekranına ekle, internetsiz de çalışsın', 'Kur');
  });

  window.addEventListener('appinstalled', () => {
    og.kur.classList.add('gizli');
    kurulumOlayi = null;
    seridiGizle(true);
  });

  og.kur.addEventListener('click', () => $('kurulumEvet').click());
  if (uygulamaKipi) og.kur.classList.add('gizli');

  /* iPhone'da beforeinstallprompt YOK — hiç tetiklenmez.
     Beklersek kullanıcı kurulabileceğini hiç öğrenemez. */
  if (iOS && !uygulamaKipi) {
    og.kur.textContent = '⬇ Ana ekrana ekle';
    og.kur.classList.remove('gizli');
    seridiGoster('Ana ekrana ekle',
                 'Uygulama gibi açılsın, internetsiz de çalışsın', 'Nasıl?');
  }

  /* Masaüstü tarayıcılarda beforeinstallprompt gecikebilir ya da hiç
     gelmeyebilir. 3 saniye sonra hâlâ gelmediyse yine de haber ver. */
  if (!iOS && !android && !uygulamaKipi) {
    setTimeout(() => {
      if (!kurulumOlayi && serit.classList.contains('gizli')) {
        seridiGoster('Uygulama olarak kurulabilir',
                     'Tarayıcı çubuğu olmadan, kendi penceresinde çalışır',
                     'Nasıl?');
      }
    }, 3000);
  }

  /* ACİL SIFIRLAMA — adrese ?sifirla=1 eklenince
     Şifresini unutan kullanıcı için son çıkış. Sessizce silmiyor;
     ne olacağını söyleyip onay alıyor, yoksa birine gönderilen bir
     link ayarlarını silebilirdi. */
  if (new URLSearchParams(location.search).get('sifirla') === '1') {
    setTimeout(() => {
      const onay = confirm(
        ['SIFIRLAMA',
         '',
         'Şifre, ayarlar, sayaçlar ve 7 günlük geçmiş silinecek.',
         'Uygulama ilk günkü haline dönecek.',
         '',
         'Devam edilsin mi?'].join('\n'));
      if (!onay) return;
      silindi = true;
      try {
        localStorage.removeItem(KAYIT_ANAHTARI);
        localStorage.removeItem('goz-molasi-gecmis');
        localStorage.removeItem('goz-molasi-kurulum-kapatildi');
      } catch {}
      location.replace(location.pathname);
    }, 300);
  }

  /* Ana ekran kısayolundan "Şimdi mola ver" ile açıldıysa */
  if (new URLSearchParams(location.search).get('eylem') === 'mola') {
    setTimeout(() => { motor.basla(); motor.molayaGec(); }, 400);
  }

  /* ============================================================
     GÖRÜNÜM GÜNCELLEME
     ============================================================ */
  const DURUM_ADI = {
    hazir: 'Hazır',
    calisiyor: 'Çalışıyor',
    uyari: 'Mola geliyor',
    mola: 'Mola',
    duraklatildi: 'Duraklatıldı',
    bosta: 'Boşta — sayaç durdu',
    saatDisi: 'Çalışma saati dışı',
  };

  function ss(saniye) {
    const t = Math.max(0, Math.ceil(saniye));
    const dk = Math.floor(t / 60);
    const sn = t % 60;
    return `${String(dk).padStart(2, '0')}:${String(sn).padStart(2, '0')}`;
  }

  function ekraniCiz(d) {
    og.govde.dataset.durum = d.durum;
    og.durum.textContent = DURUM_ADI[d.durum] || '';

    if (d.durum === 'mola') {
      og.sure.textContent = `${Math.ceil(d.kalan)}`;
      og.molaSayi.textContent = Math.ceil(d.kalan);
      og.molaHalka.style.strokeDashoffset = CEVRE_MOLA * d.ilerleme;
    } else {
      og.sure.textContent = ss(d.kalan);
      og.halka.style.strokeDashoffset = CEVRE_ANA * d.ilerleme;
    }

    og.baslat.textContent =
      d.durum === 'calisiyor' || d.durum === 'uyari' ? '⏸ Duraklat' : '▶ Başlat';

    og.istMola.textContent = d.istatistik.tamamlananMola;
    og.istAtlanan.textContent = d.istatistik.atlananMola;
    og.istSure.textContent = `${Math.floor(d.istatistik.ekranSuresi / 60)} dk`;
    // Etiket dürüst olsun: izin yoksa bu sayı cihazın değil, sekmenin süresi
    if (og.istSureEtiket) {
      og.istSureEtiket.textContent = etkinlikDedektoru
        ? 'cihaz başında süre' : 'takip edilen süre';
      og.sureKutucuk.title = etkinlikDedektoru
        ? 'Cihaz etkinliği izniyle ölçülüyor — sekme arka plandayken de sayar.'
        : 'Bu sayaç yalnızca uygulama açıkken işler. Ayarlardan "Cihaz etkinliğini izle"yi açarsan arka planda da sayar.';
    }

    haftayiCiz();
  }

  /* ============================================================
     SON 7 GÜN + SERİ
     Grafik her tikte değil, yalnızca veri değişince çizilir.
     ============================================================ */
  let haftaImza = null;
  og.hedefSayi.textContent = GUNLUK_HEDEF;

  function haftayiCiz() {
    const gunler = Gecmis.sonGunler(7, motor.istatistik);
    const imza = gunler.map((g) => g.sayi).join(',');
    if (imza === haftaImza) return;
    haftaImza = imza;

    const toplam = gunler.reduce((t, g) => t + g.sayi, 0);
    const s = Gecmis.seri(motor.istatistik);
    og.seriRozet.textContent = s > 0 ? `🔥 ${s} gün üst üste` : '';
    og.haftaGrafik.innerHTML = '';
    og.haftaGrafik.parentElement.querySelector('.hafta-not')?.remove();

    // Hiç mola yoksa yedi tane 3 piksellik kütük göstermek bozuk duruyor
    if (toplam === 0) {
      const bos = document.createElement('p');
      bos.className = 'hafta-bos';
      bos.textContent = 'Henüz mola yok. İlk molanı tamamladığında ' +
                        'buraya günlük çubuğun düşecek.';
      og.haftaGrafik.appendChild(bos);
      og.haftaOzet.textContent = '';
      return;
    }

    // Kaç günde veri var? Tek günlük veriyle grafik teknik olarak
    // doğru ama görsel olarak bomboş duruyor: hedef 8, bugün 1 ise
    // çubuk %12 yükseklikte kalıyor ve kart 240 piksel boşluk oluyor.
    const doluGun = gunler.filter((g) => g.sayi > 0).length;
    if (doluGun <= 1) {
      og.haftaOzet.textContent = `Bugün ${toplam} mola · geçmiş birikiyor`;
    } else {
      const ortalama = Math.round((toplam / 7) * 10) / 10;
      og.haftaOzet.textContent = `${toplam} mola · günde ortalama ${ortalama}`;
    }

    const enb = Math.max(GUNLUK_HEDEF, ...gunler.map((g) => g.sayi));

    // Grafiğin tamamını ekran okuyucuya tek cümlede anlat
    og.haftaGrafik.setAttribute('role', 'img');
    og.haftaGrafik.setAttribute('aria-label',
      'Son yedi gün: ' + gunler.map((g) => `${g.bugunMu ? 'bugün' : g.ad} ${g.sayi}`).join(', ') +
      `. Toplam ${toplam} mola, günlük hedef ${GUNLUK_HEDEF}.`);

    for (const g of gunler) {
      const hucre = document.createElement('div');
      hucre.className = 'gun'
        + (g.sayi >= GUNLUK_HEDEF ? ' hedefte' : '')
        + (g.bugunMu ? ' bugun' : '');
      // Fare üstüne gelince kesin sayı görünsün
      hucre.title = `${g.bugunMu ? 'Bugün' : g.ad}: ${g.sayi} mola`
                  + (g.sayi >= GUNLUK_HEDEF ? ' — hedef tamam' : '');

      const sayi = document.createElement('b');
      sayi.textContent = g.sayi || '';

      const alan = document.createElement('span');
      alan.className = 'cubuk-alan';
      const cubuk = document.createElement('i');
      cubuk.style.height = Math.max(3, Math.round((g.sayi / enb) * 100)) + '%';
      alan.appendChild(cubuk);

      const ad = document.createElement('span');
      ad.textContent = g.bugunMu ? 'Bugün' : g.ad;

      hucre.append(sayi, alan, ad);
      og.haftaGrafik.appendChild(hucre);
    }

    // Hedef çizgisi: çubuk alanının içinde, en büyük değere göre oranlı
    const cizgi = document.createElement('div');
    cizgi.className = 'hedef-cizgi';
    cizgi.style.setProperty('--hedef-oran', GUNLUK_HEDEF / enb);
    og.haftaGrafik.appendChild(cizgi);

    // Tek günlük veriyle grafik boş görünüyor; ne olduğunu söyleyelim
    if (doluGun <= 1) {
      const not = document.createElement('p');
      not.className = 'hafta-not';
      not.textContent = 'Grafik her gün biraz daha dolacak. '
                      + `Kesikli çizgi günlük hedef: ${GUNLUK_HEDEF} mola.`;
      og.haftaGrafik.after(not);
    }
  }

  /* ---------- Ana ekrandaki bilgi kartı ---------- */
  let bilgiSirasi = Math.floor(Math.random() * BILGILER.length);
  function bilgiGoster(hedefBaslik, hedefMetin, hedefKaynak, indeks) {
    const b = BILGILER[indeks % BILGILER.length];
    hedefBaslik.textContent = b.baslik;
    hedefMetin.textContent = b.metin;
    hedefKaynak.textContent = `Kaynak: ${b.kaynak}`;
    return b;
  }
  bilgiGoster(og.anaBaslik, og.anaMetin, og.anaKaynak, bilgiSirasi);
  og.anaBilgiTiklama = $('anaBilgi');
  og.anaBilgiTiklama.style.cursor = 'pointer';
  og.anaBilgiTiklama.title = 'Başka bir bilgi göster';
  og.anaBilgiTiklama.addEventListener('click', () => {
    bilgiSirasi++;
    bilgiGoster(og.anaBaslik, og.anaMetin, og.anaKaynak, bilgiSirasi);
  });

  /* ============================================================
     MOLA EKRANI
     ============================================================ */
  let nedenZaman = null;
  let molaAcik = false;

  /* ---------- Rehberli egzersiz ----------
     Mola ekranı boş bir geri sayım değil: ne yapman gerektiğini
     gösteren bir animasyon oynuyor. Masaüstü sürümüyle aynı beş
     egzersiz, aynı sırayla. */
  let egzersiz = null;
  let egzersizBaslangic = 0;
  let egzersizKare = null;
  let sonYonerge = null;

  // Kullanıcı "hareketi azalt" dediyse animasyon oynatmıyoruz —
  // tam ekran hareket denge bozukluğu olanlarda rahatsızlık yapar.
  const hareketAzalt = window.matchMedia?.('(prefers-reduced-motion: reduce)');

  function egzersizRenkleri() {
    const s = getComputedStyle(document.documentElement);
    return {
      vurgu: s.getPropertyValue('--vurgu').trim() || '#7ee0d2',
      sicak: s.getPropertyValue('--uyari').trim() || '#ffc46b',
      soluk: s.getPropertyValue('--mola-soluk').trim() || '#c3a8d8',
      zemin: s.getPropertyValue('--mola-3').trim() || '#2f2154',
    };
  }

  function egzersiziBaslat() {
    const sayac = motor.istatistik.tamamlananMola + motor.istatistik.atlananMola;
    const Sinif = egzersizSec(sayac);
    egzersiz = new Sinif(og.egzersizTuval, egzersizRenkleri());
    egzersizBaslangic = Date.now();
    sonYonerge = null;

    og.molaBaslik.textContent = Sinif.ad;
    og.molaAlt.textContent = Sinif.yonerge;

    // İlk kareyi hemen çiz — rAF beklemeden ekranda bir şey olsun
    try { egzersiz.ciz(0, motor.ayarlar.molaSuresi); } catch {}

    if (hareketAzalt?.matches) {
      // Hareket hassasiyeti olan kullanıcı: animasyon yok, yazı rehberlik eder
      return;
    }
    const dongu = () => {
      if (!molaAcik || !egzersiz) return;
      const gecen = (Date.now() - egzersizBaslangic) / 1000;
      try {
        egzersiz.ciz(gecen, motor.ayarlar.molaSuresi);
        const y = egzersiz.anlikYonerge(gecen);
        if (y !== sonYonerge) { sonYonerge = y; og.molaAlt.textContent = y; }
      } catch { egzersiz = null; return; }   // egzersiz çökse bile mola sürsün
      egzersizKare = requestAnimationFrame(dongu);
    };
    egzersizKare = requestAnimationFrame(dongu);
  }

  function egzersiziDurdur() {
    if (egzersizKare) cancelAnimationFrame(egzersizKare);
    egzersizKare = null;
    egzersiz = null;
  }

  function molaEkraniAc() {
    molaAcik = true;
    og.molaEkran.classList.add('acik');
    // Doğrudan çağırıyoruz, requestAnimationFrame ile değil:
    // sekme arka plandayken rAF hiç çalışmıyor ve egzersiz hiç
    // başlamıyordu. Mola ekranı görünmezken bile başlığın ve
    // yönergenin doğru olması gerekiyor.
    egzersiziBaslat();

    // "Neden?" kartı molanın ilk beşte birinde belirsin (20 sn'de 4. saniye).
    // Önce gözünü ekrandan ayırmasını istiyoruz; hemen okunacak bir şey
    // versek gözü ekranda tutmuş olurduk. Kısa molalarda gecikme de kısalır.
    const nedenGecikme = Math.min(4000, motor.ayarlar.molaSuresi * 200);
    og.nedenKart.classList.remove('gorunur');
    clearTimeout(nedenZaman);
    nedenZaman = setTimeout(async () => {
      // Her molada FARKLI TÜRDE kart: göz bilgisi, hava durumu,
      // kişisel özet, pratik ipucu. Sırayı MolaIcerik tutuyor.
      let k = null;
      try { k = await MolaIcerik.sonraki(motor.istatistik); } catch {}
      if (!k) {                                   // en kötü ihtimalde eski davranış
        bilgiSirasi++;
        k = { tur: 'bilgi', ...BILGILER[bilgiSirasi % BILGILER.length] };
      }
      // Mola bu arada bittiyse kartı hiç açma
      if (!molaAcik) return;

      og.nedenBaslik.textContent = `${MolaIcerik.ETIKET[k.tur] || 'Neden?'} — ${k.baslik}`;
      og.nedenMetin.textContent = k.metin;
      og.nedenKaynak.textContent = k.kaynak ? `Kaynak: ${k.kaynak}` : '';
      og.nedenKart.dataset.tur = k.tur;
      og.nedenKart.classList.add('gorunur');

      // Ana ekrandaki kart göz bilgisi kalsın — orada hava durumu
      // göstermek sayfanın amacını bulanıklaştırıyor.
      if (k.tur === 'bilgi') {
        og.anaBaslik.textContent = k.baslik;
        og.anaMetin.textContent = k.metin;
        og.anaKaynak.textContent = k.kaynak ? `Kaynak: ${k.kaynak}` : '';
      }
    }, nedenGecikme);

    // Atla düğmesi ayardan kapalıysa hiç gösterme
    og.atla.classList.toggle('gizli', !motor.ayarlar.molaAtlanabilir);

    og.okuyucu.textContent = `Mola başladı. ${motor.ayarlar.molaSuresi} saniye boyunca uzağa bak.`;
    calSes(660, 0.55);
    titret([120, 80, 120]);         // iki kısa: "dur"
    uyanikTut();
    bildirimGonder('Göz molası', 'Gözünü ekrandan ayır, 6 metre uzağa bak.');
    og.molaEkran.focus?.();
  }

  function molaEkraniKapat() {
    molaAcik = false;
    egzersiziDurdur();
    og.molaEkran.classList.remove('acik');
    og.nedenKart.classList.remove('gorunur');
    clearTimeout(nedenZaman);
    uyanikBirak();
    holdIptal();
  }

  /* ---------- "Basılı tut" ile atlama ----------
     Tek tıkla atlanabilse refleks olurdu. 800 ms basılı tutmak
     küçük ama gerçek bir engel: kazara atlamayı bitirir,
     acil durumda ise seni hapsetmez. */
  let holdZaman = null;
  const HOLD_SURE = 800;

  function holdBasla(e) {
    e.preventDefault();
    if (holdZaman) return;
    og.atla.textContent = 'Bırakma…';
    og.atla.style.transition = `background ${HOLD_SURE}ms linear`;
    og.atla.style.background = 'rgba(255,255,255,0.34)';
    holdZaman = setTimeout(async () => {
      holdIptal();
      motor.molayiAtla();
    }, HOLD_SURE);
  }
  function atlaEtiketi() {
    return 'Atlamak için basılı tut';
  }
  function holdIptal() {
    clearTimeout(holdZaman);
    holdZaman = null;
    og.atla.textContent = atlaEtiketi();
    og.atla.style.transition = 'background .2s ease';
    og.atla.style.background = '';
  }
  og.atla.addEventListener('pointerdown', holdBasla);
  og.atla.addEventListener('pointerup', holdIptal);
  og.atla.addEventListener('pointerleave', holdIptal);
  og.atla.addEventListener('pointercancel', holdIptal);
  // Klavye kullanıcısı için: boşluk/enter basılı tutmak da çalışsın
  og.atla.addEventListener('keydown', (e) => {
    if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) holdBasla(e);
  });
  og.atla.addEventListener('keyup', holdIptal);

  /* ============================================================
     UYARI BALONU
     ============================================================ */
  let balonZaman = null;
  function balonGoster(saniye) {
    og.balonMetin.textContent = `${Math.ceil(saniye)} sn sonra göz molası`;
    og.balon.classList.add('acik');
    calSes(1100, 0.18);
    bildirimGonder('Mola geliyor', `${Math.ceil(saniye)} saniye sonra göz molası.`);
    clearTimeout(balonZaman);
    balonZaman = setTimeout(balonGizle, saniye * 1000);
  }
  function balonGizle() {
    og.balon.classList.remove('acik');
    clearTimeout(balonZaman);
  }
  og.ertele.addEventListener('click', async () => {
    motor.ertele(5 * 60);
    balonGizle();
  });

  /* ============================================================
     MOTOR OLAYLARI
     ============================================================ */
  motor
    .uzerine('tik', ekraniCiz)
    .uzerine('degisti', (d) => { ekraniCiz(d); kaydet(); })
    .uzerine('uyari', (kalan) => balonGoster(kalan))
    .uzerine('molaBasladi', () => { balonGizle(); molaEkraniAc(); })
    .uzerine('molaBitti', () => {
      // Şifre penceresi açıkken mola kendi kendine bittiyse pencereyi de kapat
      if (og.sifrePencere.open) sifreKapat(false);
      molaEkraniKapat();
      calSes(990, 0.4);
      titret(200);                  // tek uzun: "devam"
      og.okuyucu.textContent = 'Mola bitti, devam edebilirsin.';
      bildirimGonder('Mola bitti', 'Gözlerin dinlendi. Devam edebilirsin.');
      bitisKartiniGoster(motor.istatistik);
    })
    .uzerine('dinlenildi', (sn) => {
      const dk = Math.max(1, Math.round(sn / 60));
      const mesaj = `${dk} dakika ekrandan uzak kaldın — gözlerin zaten dinlendi, sayaç baştan başladı.`;
      og.okuyucu.textContent = mesaj;
      const eski = og.aciklama.textContent;
      og.aciklama.textContent = mesaj;
      setTimeout(() => { og.aciklama.textContent = eski; }, 8000);
    })
    .uzerine('molaAtlandi', () => {
      molaEkraniKapat();
      og.okuyucu.textContent = 'Mola atlandı.';
      bitisKartiniGoster(motor.istatistik, true);
    });

  /* ============================================================
     DÜĞMELER VE KISAYOLLAR
     ============================================================ */
  og.baslat.addEventListener('click', async () => {
    if (motor.durum === 'calisiyor' || motor.durum === 'uyari') {
      motor.duraklat();
    } else if (motor.durum === 'duraklatildi' || motor.durum === 'bosta') {
      motor.devamEt();
    } else {
      motor.basla();
    }
  });
  og.mola.addEventListener('click', () => {
    if (motor.durum === 'hazir') motor.basla();
    motor.molayaGec();
  });
  og.sifirla.addEventListener('click', async () => {
    motor.sifirla();
  });

  document.addEventListener('keydown', (e) => {
    // e.target her zaman bir Element olmayabilir (document olabilir)
    if (e.target instanceof Element && e.target.matches('input, select, textarea')) return;
    if (og.pencere.open || og.sifrePencere.open) return;
    if (e.key === ' ' && !molaAcik) { e.preventDefault(); og.baslat.click(); }
    if ((e.key === 'm' || e.key === 'M') && !molaAcik) og.mola.click();
  });

  /* Mola ekranı açıkken Esc ile kaçış yok — atlamak için basılı tutulmalı */
  document.addEventListener('keydown', (e) => {
    if (molaAcik && e.key === 'Escape') e.preventDefault();
  }, true);

  /* ============================================================
     TEMA
     ============================================================ */
  /* Masaüstü sürümüyle aynı beş palet + "sistemle aynı".
     Renkler CSS'te tanımlı; buradaki değerler sadece seçici dairelerde
     önizleme göstermek için. */
  const TEMALAR = [
    { id: 'otomatik', ad: 'Sistemle aynı', zemin: '#141130', a: '#7ee0d2', b: '#ffc46b' },
    { id: 'koyu',     ad: 'Gece moru',     zemin: '#141130', a: '#7ee0d2', b: '#ffc46b' },
    { id: 'dinginlik',ad: 'Dinginlik',     zemin: '#102830', a: '#8fd8c8', b: '#f0cfa0' },
    { id: 'okyanus',  ad: 'Okyanus',       zemin: '#0a1826', a: '#5fd3e8', b: '#ffb877' },
    { id: 'orman',    ad: 'Orman',         zemin: '#0f1c17', a: '#8fe08a', b: '#ffd27a' },
    { id: 'safak',    ad: 'Şafak',         zemin: '#1d1220', a: '#ff9eb5', b: '#ffd08a' },
    { id: 'gunbatimi',ad: 'Gün batımı',    zemin: '#231318', a: '#ffb08a', b: '#ffd68a' },
    { id: 'buz',      ad: 'Buz',           zemin: '#0d1620', a: '#a8dcf0', b: '#ffd9a0' },
    { id: 'lavanta',  ad: 'Lavanta',       zemin: '#181530', a: '#c0a9ff', b: '#ffd28f' },
    { id: 'kiraz',    ad: 'Kiraz',         zemin: '#1a0f14', a: '#ff9aa8', b: '#ffcf8a' },
    { id: 'bakir',    ad: 'Bakır',         zemin: '#191512', a: '#e8b478', b: '#f5d49a' },
    { id: 'komur',    ad: 'Kömür (renksiz)', zemin: '#141416', a: '#d8d8de', b: '#c8b48a' },
    { id: 'acik',     ad: 'Açık (gündüz)', zemin: '#fdf6f0', a: '#0a6d62', b: '#8f540c' },
    { id: 'kagit',    ad: 'Kâğıt (açık)',   zemin: '#faf7f2', a: '#0f8a76', b: '#9a6410' },
  ];
  const temaSirasi = TEMALAR.map((t) => t.id);

  /* ---- Canlılık ----
     Tema paletleri stil.css'te ham duruyor; buradaki çarpan OKLCH'de
     yalnızca doygunluğu değiştiriyor, açıklığa dokunmuyor. Yani renk
     canlanır ama yazı kontrastı yerinde kalır. */
  const CANLILIK_ANAHTAR = 'goz-molasi-canlilik';

  function canlilikOku() {
    const d = parseInt(localStorage.getItem(CANLILIK_ANAHTAR) || '100', 10);
    return Number.isFinite(d) ? Math.min(150, Math.max(60, d)) : 100;
  }

  function canlilikUygula(yuzde, kaydet = false) {
    document.documentElement.style.setProperty('--canlilik', (yuzde / 100).toFixed(2));
    if (kaydet) { try { localStorage.setItem(CANLILIK_ANAHTAR, String(yuzde)); } catch {} }
    if (og.canlilikDurum) {
      const ad = yuzde <= 75 ? 'Sakin' : yuzde >= 130 ? 'Canlı' : 'Dengeli';
      if (og.ayCanlilikDeger) og.ayCanlilikDeger.textContent = `${ad} · %${yuzde}`;
      const destek = CSS.supports('color', 'oklch(from white l c h)');
      og.canlilikDurum.textContent = destek
        ? `${ad} (%${yuzde}) — yazı okunaklılığı değişmez, sadece renklerin doygunluğu`
        : 'Bu tarayıcı canlılık ayarını desteklemiyor; tema renkleri olduğu gibi kullanılıyor.';
      og.ayCanlilik.disabled = !destek;
    }
  }

  canlilikUygula(canlilikOku());
  og.ayCanlilik.addEventListener('input', () => canlilikUygula(+og.ayCanlilik.value, true));


  /* ============================================================
     HAZIR SÜRELER
     Telefonda sayı kutusuna elle yazmak zahmetli. Sık kullanılan
     dörtlü tek dokunuşla seçiliyor; elle değiştirme de duruyor.
     ============================================================ */
  const SURE_SECENEKLERI = [
    { dk: 20, sn: 20, ad: '20 dk · 20 sn', not: 'Klasik 20-20-20 kuralı' },
    { dk: 10, sn: 20, ad: '10 dk · 20 sn', not: '2023 çalışması bunu öneriyor' },
    { dk: 30, sn: 30, ad: '30 dk · 30 sn', not: 'Daha seyrek, daha uzun' },
    { dk: 45, sn: 60, ad: '45 dk · 1 dk', not: 'Odak bloğu sevenler için' },
  ];

  function hazirSureleriKur() {
    og.hazirSureler.innerHTML = SURE_SECENEKLERI.map((s, i) => `
      <button type="button" class="sure-sec" data-i="${i}" aria-pressed="false">
        <b>${s.ad}</b><span>${s.not}</span>
      </button>`).join('');

    og.hazirSureler.querySelectorAll('.sure-sec').forEach((d) => {
      d.addEventListener('click', () => {
        const s = SURE_SECENEKLERI[+d.dataset.i];
        og.ayCalisma.value = s.dk;
        og.ayMola.value = s.sn;
        // Ön uyarı mola süresinden uzun olmasın
        og.ayUyari.value = Math.min(15, Math.max(5, Math.round(s.dk * 60 * 0.02)));
        hazirSureleriTazele();
      });
    });
    hazirSureleriTazele();
  }

  /** Kaydırıcı değerlerini, hazır seçim işaretini ve özeti tazele */
  function hazirSureleriTazele() {
    const dk = +og.ayCalisma.value;
    const sn = +og.ayMola.value;
    const uy = +og.ayUyari.value;

    og.ayCalismaDeger.textContent = `${dk} dk`;
    og.ayMolaDeger.textContent = sn >= 60
      ? (sn % 60 === 0 ? `${sn / 60} dk` : `${Math.floor(sn / 60)} dk ${sn % 60} sn`)
      : `${sn} sn`;
    og.ayUyariDeger.textContent = uy === 0 ? 'kapalı' : `${uy} sn`;

    og.hazirSureler.querySelectorAll('.sure-sec').forEach((d) => {
      const s = SURE_SECENEKLERI[+d.dataset.i];
      d.setAttribute('aria-pressed', (s.dk === dk && s.sn === sn) ? 'true' : 'false');
    });

    ozetiYaz(dk, sn);
    uzunMolayiTazele();
  }

  /** Seçilen süreler günde ne demek? Sonucu görmeden ayar yapmak zor. */
  function ozetiYaz(dk, sn) {
    const saat = 8;
    const molaSayisi = Math.floor((saat * 60) / dk);
    const toplamSn = molaSayisi * sn;
    const toplam = toplamSn >= 60
      ? `${Math.round(toplamSn / 60)} dakika`
      : `${toplamSn} saniye`;

    let not = '';
    if (dk > 30) {
      not = '<span class="uyari-notu">⚠ 30 dakikadan seyrek molanın faydası azalıyor. ' +
            'Amerikan Optometri Birliği 20 dakika öneriyor.</span>';
    } else if (sn < 15) {
      not = '<span class="uyari-notu">⚠ 15 saniyeden kısa mola gözün odak kasının ' +
            'gevşemesine yetmeyebilir.</span>';
    } else if (dk <= 10) {
      not = '<span class="uyari-notu">Sık mola: 2023 çalışması 10 dakikayı destekliyor, ' +
            'ama işini bölebilir.</span>';
    }

    og.sureOzeti.innerHTML =
      `8 saatlik bir günde <b>${molaSayisi} mola</b> · toplam <b>${toplam}</b> göz dinlenmesi` + not;
  }

  function uzunMolayiTazele() {
    const acik = og.ayUzunMola.checked;
    og.uzunMolaAyar.classList.toggle('gizli', !acik);
    const dk = +og.ayUzunSure.value;
    og.ayUzunSureDeger.textContent = `${dk} dk`;
    og.uzunMolaNe.textContent =
      `2 saat kesintisiz çalışınca ${dk} dakikalık uzun mola önerilir. Zorlama yok, sorar.`;
  }

  function saatleriTazele() {
    og.saatAyar.classList.toggle('gizli', !og.aySaatler.checked);
  }

  ['input', 'change'].forEach((olay) => {
    og.ayCalisma.addEventListener(olay, hazirSureleriTazele);
    og.ayMola.addEventListener(olay, hazirSureleriTazele);
    og.ayUyari.addEventListener(olay, hazirSureleriTazele);
    og.ayUzunSure.addEventListener(olay, uzunMolayiTazele);
  });
  og.ayUzunMola.addEventListener('change', uzunMolayiTazele);
  og.aySaatler.addEventListener('change', saatleriTazele);

  function temaSeciciyiKur() {
    og.temaSeridi.innerHTML = TEMALAR.map((t) => `
      <button type="button" class="tema-sec" data-tema="${t.id}" role="radio"
              aria-checked="${t.id === tema}" title="${t.ad}" aria-label="${t.ad}"
              style="background:${t.zemin}">
        <i class="nokta1" style="background:${t.a}"></i>
        <i class="nokta2" style="background:${t.b}"></i>
      </button>`).join('');

    og.temaSeridi.querySelectorAll('.tema-sec').forEach((d) => {
      d.addEventListener('click', () => {
        tema = d.dataset.tema;
        temaUygula(tema);
        temaSeciciyiTazele();
        kaydet();
      });
    });
    temaSeciciyiTazele();
  }

  function temaSeciciyiTazele() {
    og.temaSeridi.querySelectorAll('.tema-sec').forEach((d) => {
      d.setAttribute('aria-checked', d.dataset.tema === tema ? 'true' : 'false');
    });
    const s = TEMALAR.find((t) => t.id === tema);
    og.temaAdi.textContent = s ? s.ad : 'Seçince hemen uygulanır';
  }

  function temaUygula(t) {
    document.documentElement.dataset.tema = t;
    // Tarayıcı çubuğunun rengi de temayla uyumlu olsun
    const renk = getComputedStyle(document.documentElement)
      .getPropertyValue('--zemin').trim() || '#141130';
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', renk);
  }
  og.tema.addEventListener('click', () => {
    tema = temaSirasi[(temaSirasi.indexOf(tema) + 1) % temaSirasi.length];
    temaUygula(tema);
    temaSeciciyiTazele();
    kaydet();
  });

  /* ============================================================
     AYARLAR PENCERESİ
     ============================================================ */
  function ayarlariPencereyeYaz() {
    og.ayCalisma.value = Math.max(1, Math.round(motor.ayarlar.calismaSuresi / 60));
    og.ayMola.value = motor.ayarlar.molaSuresi;
    og.ayUyari.value = motor.ayarlar.uyariSuresi;
    og.ayAtla.checked = motor.ayarlar.molaAtlanabilir;
    og.aySes.checked = motor.ayarlar.sesAcik;
    og.ayBosta.checked = bostaAcik;
    og.ayOtomatik.checked = otomatikBasla;
    og.ayTitresim.checked = titresimAcik;
    og.ayArkaPlan.checked = arkaPlanAcik;
    // Desteklenmiyorsa boşuna umut verme
    if (!navigator.vibrate) {
      og.ayTitresim.disabled = true;
      og.ayTitresim.closest('.satir').querySelector('small').textContent =
        'Bu cihaz titreşimi desteklemiyor';
    }
    og.ayUzunMola.checked = !!motor.ayarlar.uzunMolaAcik;
    og.ayUzunSure.value = Math.round(motor.ayarlar.uzunMolaSuresi / 60);
    og.aySaatler.checked = !!motor.ayarlar.saatlerAcik;
    etkinlikDurumunuGoster();
    og.ayHava.checked = havaAcik;
    havaDurumunuGoster();
    og.ayBasSaat.value = motor.ayarlar.basSaat;
    og.ayBitSaat.value = motor.ayarlar.bitSaat;
    saatleriTazele();

    temaSeciciyiTazele();          // tema açılır liste değil, renk daireleri
    hazirSureleriTazele();
    og.ayKilitAlan.value = '';
    kilitDurumunuGoster();
  }
  og.ayarAc.addEventListener('click', () => { ayarlariPencereyeYaz(); og.pencere.showModal(); });
  og.ayarVazgec.addEventListener('click', () => og.pencere.close());
  og.ayarKaydet.addEventListener('click', async () => {
    havaAcik = og.ayHava.checked;
    try { localStorage.setItem(HAVA_ACIK_ANAHTAR, havaAcik ? '1' : '0'); } catch {}
    MolaIcerik.havaAyarla(havaAcik);

    const dk = Math.min(90, Math.max(1, +og.ayCalisma.value || 20));
    const ml = Math.min(180, Math.max(5, +og.ayMola.value || 20));
    let uy = Math.min(60, Math.max(0, +og.ayUyari.value || 0));
    if (uy >= dk * 60) uy = 0;              // uyarı, çalışmadan uzun olamaz

    motor.ayarlar.calismaSuresi = dk * 60;
    motor.ayarlar.molaSuresi = ml;
    motor.ayarlar.uyariSuresi = uy;
    motor.ayarlar.molaAtlanabilir = og.ayAtla.checked;
    motor.ayarlar.sesAcik = og.aySes.checked;
    bostaAcik = og.ayBosta.checked;
    otomatikBasla = og.ayOtomatik.checked;
    titresimAcik = og.ayTitresim.checked;
    arkaPlanAcik = og.ayArkaPlan.checked;
    arkaPlanKipi(arkaPlanAcik);
    motor.ayarlar.bostaEsigi = bostaAcik ? BOSTA_ESIGI : 1e9;
    motor.ayarlar.uzunMolaAcik = og.ayUzunMola.checked;
    motor.ayarlar.uzunMolaSuresi = Math.max(60, +og.ayUzunSure.value * 60);
    motor.ayarlar.saatlerAcik = og.aySaatler.checked;
    motor.ayarlar.basSaat = og.ayBasSaat.value || '09:00';
    motor.ayarlar.bitSaat = og.ayBitSaat.value || '18:00';
    // Tema zaten daireye tıklanır tıklanmaz uygulandı, burada bir şey yapmıyoruz

    og.aciklama.textContent =
      `${dk} dakikada bir ekran ${ml} saniyeliğine kapanır. ` +
      'O sırada 6 metre uzağa bak.';

    if (motor.durum !== 'hazir') motor.sifirla();
    kaydet();
    og.pencere.close();
  });

  /* ---------- Tüm verileri sıfırla ----------
     Şifreni unutursan buradan çıkarsın. Kilitliyken yine şifre ister;
     şifreyi de bilmiyorsan tarayıcının "site verilerini temizle"
     seçeneği kalır — bunu OKU.md'de açıkça yazdık. */
  let silmeOnayi = false;
  let silmeZaman = null;
  og.hepsiniSil.addEventListener('click', async () => {
    if (!silmeOnayi) {
      if (!(await sifreSor('Verileri silmek için şifre gerekli.'))) return;
      silmeOnayi = true;
      og.hepsiniSil.textContent = 'Emin misin? Tekrar bas';
      og.sifirlamaDurum.textContent = 'Bu işlem geri alınamaz.';
      clearTimeout(silmeZaman);
      silmeZaman = setTimeout(() => {
        silmeOnayi = false;
        og.hepsiniSil.textContent = 'Sıfırla';
        og.sifirlamaDurum.textContent = 'Ayarlar, sayaçlar ve şifre silinir';
      }, 6000);
      return;
    }
    clearTimeout(silmeZaman);
    silindi = true;
    try { localStorage.removeItem(KAYIT_ANAHTARI); } catch {}
    location.reload();
  });

  /* ============================================================
     KAYIT — ayarlar, istatistik ve sayacın bitiş anı
     ============================================================ */
  let silindi = false;   // sıfırlamadan sonra kayıt geri yazılmasın

  function kaydet() {
    if (silindi) return;
    // Günün özetini kalıcı geçmişe de yaz (7 gün grafiği ve seri için)
    try {
      Gecmis.gunuIsle(motor.istatistik.gun || Gecmis.gunAdi(), motor.istatistik);
    } catch {}
    try {
      localStorage.setItem(KAYIT_ANAHTARI, JSON.stringify({
        ...motor.disaAktar(),
        bostaAcik,
        otomatikBasla,
        titresimAcik,
        arkaPlanAcik,
        tema,
        kilitOzeti,
        kilitTuz,
        kilitSifirlandi: KILIT_SIFIRLAMA_DAMGASI,
        kayitAni: Date.now(),
      }));
    } catch {}
  }
  setInterval(kaydet, 15000);
  window.addEventListener('pagehide', kaydet);

  /* ============================================================
     HAREKET TAKİBİ — cihaz kullanılmıyorsa sayaç dursun
     ============================================================ */
  ['pointerdown', 'pointermove', 'keydown', 'wheel', 'touchstart'].forEach((olay) =>
    window.addEventListener(olay, () => motor.hareketVar(), { passive: true })
  );

  /* ============================================================
     CİHAZ ETKİNLİĞİ (Idle Detection API)

     Sorun: yukarıdaki olaylar yalnızca BU SEKMEDE olan hareketi
     görüyor. Kullanıcı başka pencerede çalışırken sekme "hareket
     yok" sanıp sayacı durduruyordu; "ekran süresi 1 dakika"
     görünmesinin sebebi de buydu — cihazın değil, sekmenin süresi.

     Çözüm: IdleDetector. İzin verilirse tarayıcı, sekme arka planda
     olsa bile cihazda hareket olup olmadığını söylüyor. İzin
     ZORUNLU ve kullanıcı hareketiyle isteniyor (ayarlardaki düğme).
     Desteklemeyen tarayıcıda (Firefox, Safari) her şey eskisi gibi
     çalışmaya devam ediyor.

     Ne öğreniyoruz: yalnızca "etkin mi / boşta mı" ve "ekran kilitli
     mi". Ne yazdığını, hangi uygulamada olduğunu DEĞİL — tarayıcı
     zaten söylemiyor.
     ============================================================ */
  const ETKINLIK_ANAHTAR = 'goz-molasi-etkinlik-izni';
  let etkinlikDedektoru = null;

  function etkinlikDesteklenirMi() {
    return typeof window.IdleDetector === 'function';
  }

  async function etkinlikIzniDurumu() {
    if (!etkinlikDesteklenirMi()) return 'desteklenmiyor';
    try {
      const d = await navigator.permissions.query({ name: 'idle-detection' });
      return d.state;                 // granted | denied | prompt
    } catch { return 'bilinmiyor'; }
  }

  /** İzni ister ve dinlemeye başlar. Tarayıcı bunu yalnızca bir
      tıklamanın ardından soruyor, o yüzden ayarlardaki düğmeden. */
  async function etkinligiBaslat(izinIste = false) {
    if (!etkinlikDesteklenirMi() || etkinlikDedektoru) return false;
    try {
      if (izinIste) {
        const izin = await IdleDetector.requestPermission();
        if (izin !== 'granted') return false;
      } else if ((await etkinlikIzniDurumu()) !== 'granted') {
        return false;                 // sessizce vazgeç, soru sorma
      }

      const d = new IdleDetector();
      d.addEventListener('change', () => {
        // active + unlocked = kişi gerçekten cihazın başında
        if (d.userState === 'active' && d.screenState === 'unlocked') {
          motor.hareketVar();
        }
      });
      // 60 sn, tarayıcının izin verdiği en kısa eşik
      await d.start({ threshold: 60000 });
      etkinlikDedektoru = d;
      try { localStorage.setItem(ETKINLIK_ANAHTAR, '1'); } catch {}
      return true;
    } catch {
      return false;
    }
  }

  function etkinligiDurdur() {
    try { etkinlikDedektoru?.abort?.(); } catch {}
    etkinlikDedektoru = null;
    try { localStorage.removeItem(ETKINLIK_ANAHTAR); } catch {}
  }

  // Daha önce izin verilmişse sessizce yeniden bağlan
  try {
    if (localStorage.getItem(ETKINLIK_ANAHTAR) === '1') etkinligiBaslat(false);
  } catch {}

  /* ============================================================
     ARKA PLAN SORUNU
     Tarayıcı, arka plandaki sekmenin zamanlayıcısını yavaşlatır.
     Bizim motor Date.now() farkı kullandığı için süre şaşmaz;
     sekmeye dönüldüğünde bir kez elle tetikleyip yakalatıyoruz.
     ============================================================ */
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
      motor.hareketVar();
      motor.tik();
      ekraniCiz(motor.anlikDurum());
    }
  });
  window.addEventListener('pageshow', () => { motor.tik(); ekraniCiz(motor.anlikDurum()); });

  /* ============================================================
     AÇILIŞ
     ============================================================ */
  og.aciklama.textContent =
    `${Math.round(motor.ayarlar.calismaSuresi / 60)} dakikada bir ekran ` +
    `${motor.ayarlar.molaSuresi} saniyeliğine kapanır. O sırada 6 metre uzağa bak.`;

  ekraniCiz(motor.anlikDurum());
  bildirimDurumunuGoster();
  kilitDurumunuGoster();
  temaSeciciyiKur();
  hazirSureleriKur();

  /* Açılışta kendiliğinden başla.
     Sekme kapalıyken geçen süreyi mola yağmuruna çevirmiyoruz;
     temiz bir 20 dakikayla başlıyoruz.

     "Cihaza bakılmaya başlandığında başlasın" isteği burada
     iki parçayla karşılanıyor:
       1) Uygulama açılır açılmaz sayaç döner (bu satır),
       2) Kimse dokunmuyorsa 90 sn sonra sayaç kendini durdurur ve
          ilk dokunuşta yeniden başlar (motor.hareketVar).
     Yani bilgisayar açıkken sen yokken sayaç boşa dönmez. */
  const oncedenCalisiyordu =
    kayit.durum === 'calisiyor' || kayit.durum === 'uyari' || kayit.durum === 'mola';
  if (otomatikBasla || oncedenCalisiyordu) motor.basla();

  // Hata ayıklama / test için: konsoldan molaMotoru.ayarlar ile oynayabilirsin
  window.molaMotoru = motor;

  // Kaydedilmiş arka plan tercihini uygula (ses ancak dokunuştan sonra açılır)
  if (arkaPlanAcik) {
    document.addEventListener('pointerdown', () => arkaPlanKipi(true), { once: true });
  }

  /* Telefonda tarayıcı, ekran kilitlenince zamanlayıcıyı donduruyor.
     Bunu söylemezsek kullanıcı "hatırlatmadı, bozuk" sanıyor. */
  if (/android|iphone|ipad|ipod/i.test(navigator.userAgent)) {
    const not = document.createElement('span');
    not.className = 'kaynak';
    not.style.display = 'block';
    not.style.marginTop = '8px';
    not.textContent = 'Telefonda: uygulama açıkken hatırlatır. Ekran kilitliyken '
      + 'tarayıcılar sayacı dondurur — bu bir telefon sınırı, uygulama hatası değil. '
      + 'Ayarlardan “Arka planda çalışmaya devam et” bunu büyük ölçüde çözer.';
    document.querySelector('.alt-bilgi')?.appendChild(not);
  }

  // Reklam alanı — numaralar girilmemişse kendini tamamen kaldırır
  try { tumReklamlariKur(); } catch {}

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }
})();
