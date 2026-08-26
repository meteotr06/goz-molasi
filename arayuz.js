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

  function kilitDurumunuGoster() {
    const acik = !!kilitOzeti;
    og.kilitDurum.textContent = acik
      ? 'Açık — şifreyi değiştirme ve verileri silme korumalı'
      : 'Kapalı — verileri silmek serbest';
    og.kilitKur.textContent = acik ? 'Şifreyi değiştir' : 'Şifreyi koy';
    og.kilitKaldir.classList.toggle('gizli', !acik);
    og.atla.textContent = atlaEtiketi();
    document.title = acik ? '🔒 Göz Molası — 20·20·20' : 'Göz Molası — 20·20·20';
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

    const enb = Math.max(GUNLUK_HEDEF, ...gunler.map((g) => g.sayi));
    // Hedef çizgisinin yüksekliği çubuk alanına göre
    og.haftaGrafik.style.setProperty('--hedef-yuksekligi',
      `calc(${(GUNLUK_HEDEF / enb) * 100}% - ${(GUNLUK_HEDEF / enb) * 16}px + 18px)`);

    og.haftaGrafik.innerHTML = gunler.map((g) => {
      const yuzde = enb ? Math.round((g.sayi / enb) * 100) : 0;
      const siniflar = ['gun'];
      if (g.sayi >= GUNLUK_HEDEF) siniflar.push('hedefte');
      if (g.bugunMu) siniflar.push('bugun');
      return `<div class="${siniflar.join(' ')}">
                <b>${g.sayi || ''}</b>
                <i style="height:${Math.max(3, yuzde)}%"></i>
                <span>${g.bugunMu ? 'Bugün' : g.ad}</span>
              </div>`;
    }).join('');

    const s = Gecmis.seri(motor.istatistik);
    og.seriRozet.textContent = s > 0 ? `🔥 ${s} gün üst üste` : '';
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
    { id: 'okyanus',  ad: 'Okyanus',       zemin: '#0a1826', a: '#5fd3e8', b: '#ffb877' },
    { id: 'orman',    ad: 'Orman',         zemin: '#0f1c17', a: '#8fe08a', b: '#ffd27a' },
    { id: 'safak',    ad: 'Şafak',         zemin: '#1d1220', a: '#ff9eb5', b: '#ffd08a' },
    { id: 'gunbatimi',ad: 'Gün batımı',    zemin: '#231318', a: '#ffb08a', b: '#ffd68a' },
    { id: 'buz',      ad: 'Buz',           zemin: '#0d1620', a: '#a8dcf0', b: '#ffd9a0' },
    { id: 'lavanta',  ad: 'Lavanta',       zemin: '#181530', a: '#c0a9ff', b: '#ffd28f' },
    { id: 'komur',    ad: 'Kömür (renksiz)', zemin: '#141416', a: '#d8d8de', b: '#c8b48a' },
    { id: 'acik',     ad: 'Açık (gündüz)', zemin: '#fdf6f0', a: '#0a6d62', b: '#8f540c' },
  ];
  const temaSirasi = TEMALAR.map((t) => t.id);

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
      `Sayaç çalışıyor. ${dk} dakika sonra ekran ${ml} saniyeliğine kapanacak, ` +
      'bu sırada gözünü 6 metre uzağa çevir. Bilgisayara dokunmazsan sayaç durur.';

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
    `Sayaç çalışıyor. ${Math.round(motor.ayarlar.calismaSuresi / 60)} dakika sonra ekran ` +
    `${motor.ayarlar.molaSuresi} saniyeliğine kapanacak, bu sırada gözünü 6 metre uzağa çevir. ` +
    'Cihaza dokunmazsan sayaç kendini durdurur.';

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
  try { reklamiKur($('reklamAlani')); } catch {}

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }
})();
