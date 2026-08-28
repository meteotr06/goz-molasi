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
    ayDil: $('ayDil'),
    ikinciSekme: $('ikinciSekme'),
    buradaDevam: $('buradaDevamDugme'),
    kipDugmeler: $('kipDugmeler'),
    tanitimKart: $('tanitimKart'),
    tanitimMetin: $('tanitimMetin'),
    tanitimGoster: $('tanitimGoster'),
    tanitimAnladim: $('tanitimAnladim'),
    tanitimKapat: $('tanitimKapat'),
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
    ayMolaKilit: $('ayMolaKilit'),
    okuyucu: $('ekranOkuyucu'),

    pencere: $('ayarPencere'),
    ayCalisma: $('ayCalisma'),
    ayMola: $('ayMola'),
    ayUyari: $('ayUyari'),
    ayAtla: $('ayAtla'),
    aySes: $('aySes'),
    ayBosta: $('ayBosta'),
    ayUzakSifirla: $('ayUzakSifirla'),
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

  /* SIRA ÖNEMLİ: `iceAktar` geri yükleme kararını BURADA veriyor.
     Ayarı ondan sonra vermek, kararın eski ayarla alınması demek.
     Ölçüldü: ayar kapalıyken ekran 20:00'a döndü AMA not "sayaç
     sıfırlanmadı" dedi — motor iki kez çağrılınca iki bayrak birden
     kalmıştı ve kullanıcı ekranla çelişen bir cümle okuyordu. */
  let bostaAcik = kayit.bostaAcik !== false;
  // Varsayilan acik: kayitta yoksa bugunku davranis surer.
  let uzakSifirla = kayit.uzakSifirla !== false;
  // Varsayilan ACIK: kullanici bunu acikca istedi.
  let molaKilit = kayit.molaKilit !== false;
  motor.ayarlar.uzakKalincaSifirla = uzakSifirla;
  if (!bostaAcik) motor.ayarlar.bostaEsigi = 1e9;
  motor.iceAktar(kayit);
  let otomatikBasla = kayit.otomatikBasla !== false;   // varsayılan: açık
  let titresimAcik = kayit.titresimAcik !== false;     // varsayılan: açık (telefonda)
  let arkaPlanAcik = kayit.arkaPlanAcik === true;      // varsayılan: KAPALI (pil)
  // İlk açılışta beyaz. Ana ekranın aydınlık olması mola ekranıyla
  // çelişmiyor: mola ekranı her temada koyu kalıyor.
  let tema = kayit.tema || 'beyaz';
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
        og.sifreHata.textContent = C('Çok fazla yanlış deneme — 30 saniye bekle.');
        og.sifreAlan.disabled = true;
        setTimeout(() => {
          og.sifreAlan.disabled = false;
          og.sifreHata.textContent = '';
          og.sifreAlan.focus();
        }, 30000);
      } else {
    const kalanDeneme = 3 - yanlisSayisi;
    og.sifreHata.textContent = CS(
      `Şifre yanlış. Kalan deneme: ${kalanDeneme}`,
      `Wrong password. Attempts left: ${kalanDeneme}`);
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

  /** Ana ekrandaki açıklama. Sayı içerdiği için sözlükte anahtar
      olarak tutulamıyor; iki dilde ayrı kalıp. */
  function aciklamaMetni(dk, sn) {
    return CS(
      `${dk} dakikada bir ekran ${sn} saniyeliğine kapanır. ` +
        'O sırada 6 metre uzağa bak.',
      `Every ${dk} minutes the screen goes dark for ${sn} seconds. ` +
        'Look 6 metres away.');
  }

  /* ============================================================
     TEK SEKME — lider seçimi

     Sorun: uygulama iki sekmede açıksa her sekme kendi sayacını
     işletiyor. Ekran süresi iki kat sayılıyor, sekmeler birbirinin
     kaydını eziyor ve sayaçlar farklı gösteriyor (ölçtüm: biri 36:20
     derken öteki 36:56).

     Çözüm WhatsApp Web'inkiyle aynı: tek sekme sayar, diğerleri
     "buradan devam et" der. Veriler ortak depoda olduğu için geçiş
     sırasında hiçbir şey kaybolmuyor.

     Yöntem: her sekme kendine bir kimlik üretiyor ve lider olduğunda
     depoya iki saniyede bir kalp atışı yazıyor. Kalp atışı altı
     saniyeden eskiyse lider ölmüş sayılıyor ve boştaki sekme
     devralıyor — yani sekme çökse bile kilitli kalmıyor.
     ============================================================ */
  const LIDER_ANAHTAR = 'goz-molasi-lider';
  const LIDER_ARALIK = 2000;
  const LIDER_OLU = 6000;
  const SEKME_KIMLIGI = Math.random().toString(36).slice(2) + Date.now().toString(36);
  let liderMiyim = false;
  let liderZaman = 0;

  function liderOku() {
    try { return JSON.parse(localStorage.getItem(LIDER_ANAHTAR) || 'null'); }
    catch { return null; }
  }

  function liderDamgala() {
    try {
      localStorage.setItem(LIDER_ANAHTAR,
        JSON.stringify({ kimlik: SEKME_KIMLIGI, an: Date.now() }));
    } catch {}
  }

  /** Başka bir sekme şu an canlı lider mi? */
  function baskaLiderVar() {
    const l = liderOku();
    return !!(l && l.kimlik !== SEKME_KIMLIGI && (Date.now() - l.an) < LIDER_OLU);
  }

  function lideriDevral() {
    liderMiyim = true;
    liderDamgala();
    og.ikinciSekme.hidden = true;
    // Sayaç kaydı ortak; devralan sekme kaldığı yerden sürdürür.
    try { motor.sayaciGeriYukle(JSON.parse(localStorage.getItem(KAYIT_ANAHTARI) || '{}')); } catch {}
    motor._kalpAtisiBaslat();
    ekraniCiz(motor.anlikDurum());
    clearInterval(liderZaman);
    liderZaman = setInterval(liderNobeti, LIDER_ARALIK);
  }

  function liderligiBirak() {
    liderMiyim = false;
    og.ikinciSekme.hidden = false;
    // Sayaç bu sekmede işlemesin; ölçüm çift sayılmasın.
    try { motor._kalpAtisiDurdur(); } catch {}
  }

  /** İki saniyede bir: liderim damgala, değilsem devralınabilir mi bak. */
  function liderNobeti() {
    if (liderMiyim) {
      const l = liderOku();
      // Başka sekme devraldıysa sessizce geri çekil
      if (l && l.kimlik !== SEKME_KIMLIGI && (Date.now() - l.an) < LIDER_OLU) {
        liderligiBirak();
        return;
      }
      liderDamgala();
    } else if (!baskaLiderVar()) {
      lideriDevral();          // lider öldü, boşluğu doldur
    }
  }

  function tekSekmeyiKur() {
    if (baskaLiderVar()) {
      liderligiBirak();
    } else {
      lideriDevral();
    }
    clearInterval(liderZaman);
    liderZaman = setInterval(liderNobeti, LIDER_ARALIK);
    // Sekme kapanırken bayrağı bırak ki diğeri hemen devralsın
    window.addEventListener('pagehide', () => {
      if (liderMiyim) { try { localStorage.removeItem(LIDER_ANAHTAR); } catch {} }
    });

    // Arka plandaki sekmenin zamanlayıcısı da kısılıyor: lider sekme
    // kapandığında bekleyen sekme dakikalarca fark etmeyebiliyordu.
    // Ölçtüm — beş saniye sonra hâlâ devralmamıştı. Sekmeye dönüldüğü
    // anda kontrol ediyoruz.
    const hemenBak = () => { if (!liderMiyim && !baskaLiderVar()) lideriDevral(); };
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden) hemenBak();
    });
    window.addEventListener('focus', hemenBak);

    // Lider bayrağı silinince (diğer sekme kapandı) haberdar ol
    window.addEventListener('storage', (e) => {
      if (e.key === LIDER_ANAHTAR && !e.newValue) hemenBak();
    });
  }

  og.buradaDevam.addEventListener('click', lideriDevral);

  /* ============================================================
     KİPLER

     Rakiplerin kullanıcılarının yıllardır istediği ama hiçbirinde
     olmayan şey. Stretchly'de bunun için açık bir istek var: insanlar
     yaptıkları işe göre farklı mola düzeni istiyor ve her seferinde
     ayarlara girip elle değiştirmekten şikâyetçi.

     Kip, ayarların TAMAMINI değil yalnızca zamanlamayla ilgili
     olanları değiştiriyor. Tema, canlılık, hava durumu gibi kişisel
     tercihler kipten kipe taşınıyor — onlar "ne yaptığına" bağlı değil.
     ============================================================ */
  const KIPLER = [
    // Çalışma kipi uygulamanın VARSAYILANIYLA birebir aynı olmalı;
    // yoksa yeni kullanıcıda hiçbir kip seçili görünmüyor.
    { id: 'calisma', ad: 'Çalışma', not: '20 dk · 20 sn',
      ayar: { calismaSuresi: 1200, molaSuresi: 20, uyariSuresi: 15,
              molaAtlanabilir: false, sesAcik: true, uzunMolaAcik: false } },
    { id: 'ders', ad: 'Ders', not: '25 dk · 30 sn',
      ayar: { calismaSuresi: 1500, molaSuresi: 30, uyariSuresi: 15,
              molaAtlanabilir: false, sesAcik: true, uzunMolaAcik: true } },
    { id: 'toplanti', ad: 'Toplantı', not: 'sessiz, seyrek',
      ayar: { calismaSuresi: 3600, molaSuresi: 20, uyariSuresi: 0,
              molaAtlanabilir: true, sesAcik: false, uzunMolaAcik: false } },
    { id: 'film', ad: 'Film · oyun', not: 'neredeyse hiç',
      ayar: { calismaSuresi: 5400, molaSuresi: 20, uyariSuresi: 0,
              molaAtlanabilir: true, sesAcik: false, uzunMolaAcik: false } },
  ];

  /** Şu anki ayarlar hangi kipe uyuyor? Hiçbirine uymuyorsa null —
      kullanıcı elle ayar yaptıysa hiçbir kip seçili görünmemeli. */
  function acikKip() {
    const bul = KIPLER.find((k) =>
      Object.keys(k.ayar).every((alan) => motor.ayarlar[alan] === k.ayar[alan]));
    return bul ? bul.id : null;
  }

  function kipleriTazele() {
    const simdiki = acikKip();
    og.kipDugmeler.querySelectorAll('.kip-sec').forEach((d) => {
      d.setAttribute('aria-pressed', String(d.dataset.kip === simdiki));
    });
  }

  function kipiUygula(k) {
    Object.assign(motor.ayarlar, k.ayar);
    kaydet();
    // Sayaç yeni süreyle baştan başlasın; yarım kalmış eski süreyle
    // devam etmek kafa karıştırıyor.
    if (motor.durum !== 'mola') motor.sifirla();
    og.aciklama.textContent = aciklamaMetni(
      Math.round(k.ayar.calismaSuresi / 60), k.ayar.molaSuresi);
    // Kip ADI sozlukte var ama cumle kalibi koda gomuluydu:
    // Ingilizce kipte ekran okuyucu "Film - gaming kipine gecildi"
    // diyordu. Sayi/degisken iceren metinler CS ile iki dilli olur.
    og.okuyucu.textContent = CS(`${C(k.ad)} kipine geçildi.`,
                                `Switched to ${C(k.ad)} mode.`);
    kipleriTazele();
    ekraniCiz(motor.anlikDurum());
  }

  function kipleriKur() {
    og.kipDugmeler.innerHTML = '';
    KIPLER.forEach((k) => {
      const d = document.createElement('button');
      d.type = 'button';
      d.className = 'kip-sec';
      d.dataset.kip = k.id;
      d.setAttribute('aria-pressed', 'false');
      const ad = document.createElement('b'); ad.textContent = k.ad;
      const not = document.createElement('span'); not.textContent = k.not;
      d.append(ad, not);
      d.addEventListener('click', () => kipiUygula(k));
      og.kipDugmeler.appendChild(d);
    });
    kipleriTazele();
  }

  /* ============================================================
     İLK AÇILIŞ TANITIMI

     Bu kategoride bırakmanın bir numaralı sebebi, insanın uygulamayı
     açıp ne olacağını anlamaması. Burada anlatmıyoruz, GÖSTERİYORUZ:
     6 saniyelik örnek mola, gerçek mola ekranıyla aynı. Kişi ne
     olacağını yaşayarak öğreniyor.

     Örnek mola istatistiğe SAYILMAZ — 6 saniye, 20 saniyelik bir
     mola değil; sayması rakamları şişirirdi.
     ============================================================ */
  const TANITIM_ANAHTAR = 'goz-molasi-tanitim';
  let tanitimMolasi = false;

  function tanitimGoruldu() {
    try { return localStorage.getItem(TANITIM_ANAHTAR) === '1'; } catch { return true; }
  }
  function tanitimiKapat() {
    try { localStorage.setItem(TANITIM_ANAHTAR, '1'); } catch {}
    og.tanitimKart.hidden = true;
  }

  function tanitimiKurGerekirse() {
    // Daha önce mola tamamlamış biri tanıtımı görmesin — geri dönen
    // kullanıcıya "hoş geldin" göstermek can sıkıyor.
    // Gün SAYISINA değil MOLA sayısına bakmalı: uygulama açılır açılmaz
    // bugün için sıfırlarla dolu bir kayıt yazıyor, o yüzden gün sayısı
    // yeni kullanıcıda da 1 oluyordu ve tanıtım hiç görünmüyordu.
    const gecmisToplam = Object.values(Gecmis.oku())
      .reduce((t, g) => t + ((g && g.mola) | 0), 0);
    const molaVarMi = (motor.istatistik.tamamlananMola | 0) > 0 || gecmisToplam > 0;
    if (tanitimGoruldu() || molaVarMi) return;
    og.tanitimKart.hidden = false;
  }

  og.tanitimKapat.addEventListener('click', tanitimiKapat);
  og.tanitimAnladim.addEventListener('click', tanitimiKapat);

  og.tanitimGoster.addEventListener('click', () => {
    if (motor.durum === 'mola') return;
    tanitimMolasi = true;
    const gercekSure = motor.ayarlar.molaSuresi;
    motor.ayarlar.molaSuresi = 6;
    if (motor.durum === 'hazir' || motor.durum === 'bosta') motor.basla();
    motor.molayaGec();
    // Süreyi hemen geri al: motor asamaya gecerken degeri zaten kopyaladi
    motor.ayarlar.molaSuresi = gercekSure;
    og.tanitimMetin.textContent =
      'İşte böyle görünüyor. Gerçeğinde 20 saniye sürecek ve ' +
      'kapatılamayacak.';
    og.tanitimGoster.textContent = C('Tekrar göster');
    og.tanitimAnladim.textContent = C('Anladım, başla');
  });

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

    og.bitisBaslik.textContent = atlandiMi
      ? CS('Mola atlandı', 'Break skipped')
      : CS('Mola tamam', 'Break done');

    const parcalar = [];
    if (!atlandiMi && bugun > 0) {
      parcalar.push(CS(`Bugün ${bugun}. molan`, `Break ${bugun} today`));
    }
    if (seri >= 2) {
      parcalar.push(CS(`${seri} gündür üst üste`,
                       `${seri} ${seri === 1 ? 'day' : 'days'} in a row`));
    }
    const dk = Math.max(1, Math.round(motor.ayarlar.calismaSuresi / 60));
    // Turkcede tekil/cogul ayrimi yok, Ingilizcede var: "1 minutes"
    // yazan bir uygulama, cevirisine ozen gosterilmemis demektir.
    parcalar.push(CS(`sonraki mola ${dk} dakika sonra`,
                     `next break in ${dk} ${dk === 1 ? 'minute' : 'minutes'}`));
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
      og.etkinlikDugme.textContent = C('Desteklenmiyor');
      og.etkinlikDurum.textContent =
        'Bu tarayıcı cihaz etkinliğini paylaşmıyor (Chrome ve Edge destekliyor). ' +
        'Sayaç yalnızca bu sekmedeki hareketi görüyor.';
      return;
    }
    if (acik) {
      og.etkinlikDugme.textContent = C('Kapat');
      og.etkinlikDurum.textContent =
        'Açık — sekme arka plandayken de cihazda hareket olup olmadığı görülüyor. ' +
        'Sadece "etkin mi, ekran kilitli mi" bilgisi; ne yaptığın değil.';
    } else if (d === 'denied') {
      og.etkinlikDugme.textContent = C('İzin ver');
      og.etkinlikDurum.textContent =
        C('İzin reddedilmiş. Adres çubuğundaki kilit simgesinden açabilirsin.');
    } else {
      og.etkinlikDugme.textContent = C('İzin ver');
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
      og.havaDurum.textContent = C('Kapalı — molalarda yalnızca göz bilgisi gösterilir');
    } else if (konum) {
      og.havaDurum.textContent = (konum.ad ? konum.ad + ' · ' : '') +
        'her birkaç molada bir hava durumu gösterilir';
    } else {
      og.havaDurum.textContent = C('Açık — önce konum ver ya da şehir ara');
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
        og.sehirSonuc.textContent = C('Sonuç yok.');
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
    og.kilitDurum.textContent = C(acik
      ? 'Açık — şifreyi değiştirme ve verileri silme korumalı'
      : 'Kapalı — verileri silmek serbest');
    og.kilitKur.textContent = C(acik ? 'Şifreyi değiştir' : 'Şifreyi koy');
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
      og.kilitDurum.textContent = C('Şifre 4–8 rakam olmalı.');
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
      og.bildirim.textContent = C('🔕 Bu tarayıcı bildirim desteklemiyor');
      return;
    }
    // iOS'ta izin isteği MUTLAKA bir dokunuşun içinden çağrılmalı
    const sonuc = await Notification.requestPermission();
    bildirimDurumunuGoster(sonuc);
  });

  function bildirimDurumunuGoster(izin = (window.Notification?.permission)) {
    if (!('Notification' in window)) { og.bildirim.classList.add('gizli'); return; }
    if (izin === 'granted') {
      og.bildirim.textContent = C('🔔 Bildirimler açık');
      og.bildirim.disabled = true;
    } else if (izin === 'denied') {
      og.bildirim.textContent = C('🔕 Bildirimlere izin verilmedi');
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
      og.paylas.title = C('Link kopyalandı');
      setTimeout(() => { og.paylas.textContent = eski;
                         og.paylas.title = C('Paylaş'); }, 1800);
    } catch {
      prompt(C('Linki kopyala:'), PAYLASIM.url);
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
      C('Adres çubuğunun sağındaki ⊕ / kurulum simgesine bas');
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
    og.kur.textContent = C('⬇ Ana ekrana ekle');
    og.kur.classList.remove('gizli');
    seridiGoster('Ana ekrana ekle',
                 'Uygulama gibi açılsın, internetsiz de çalışsın', C('Nasıl?'));
  }

  /* Masaüstü tarayıcılarda beforeinstallprompt gecikebilir ya da hiç
     gelmeyebilir. 3 saniye sonra hâlâ gelmediyse yine de haber ver. */
  if (!iOS && !android && !uygulamaKipi) {
    setTimeout(() => {
      if (!kurulumOlayi && serit.classList.contains('gizli')) {
        // C() SART: bu iki metinde hic cgiosu harfi YOK, o yuzden
        // harf tabanli dil taramasi onlari GORMUYOR. Ucuncu arguman
        // zaten C() ile sarilmisti; ilk ikisi unutulmus.
        seridiGoster(C('Uygulama olarak kurulabilir'),
                     C('Tarayıcı çubuğu olmadan, kendi penceresinde çalışır'),
                     C('Nasıl?'));
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

  /* Ana ekran kısayolundan açıldıysa (telefonda simgeye basılı tutma).
     Adres çubuğunda ?eylem=... kalmasın diye iş bitince temizleniyor;
     yoksa kullanıcı sayfayı yenilediğinde eylem tekrar çalışıyordu. */
  {
    const eylem = new URLSearchParams(location.search).get('eylem');
    if (eylem === 'mola') {
      setTimeout(() => { motor.basla(); motor.molayaGec(); }, 400);
      history.replaceState(null, '', location.pathname);
    } else if (eylem === 'duraklat') {
      /* Artık motor süreli duraklatmayı kendisi biliyor.
         Eski hâli burada `setTimeout` kuruyordu ve sekme kapanınca o
         zamanlayıcı ölüyordu: kullanıcı "5 dakika duraklat" diyor,
         sekmeyi kapatıyor, geri dönüyor ve uygulama KALICI olarak
         duraklamış oluyordu. Kısayolun adında verilen söz
         tutulmuyordu. */
      setTimeout(() => {
        try { motor.duraklat(5 * 60); } catch {}
      }, 300);
      history.replaceState(null, '', location.pathname);
    }
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
    /* DURAKLATMA TURUNU SOYLE.
       Olculdu: suresiz ve 5 dakikalik duraklatma ekranda BIREBIR
       ayni goruniyordu ("Duraklatildi"). Biri donecek, obru asla -
       kullanici hangisinde oldugunu bilemiyordu.

       Geri sayim DEGIL saat yaziyoruz: duraklatilmisken `tik` ve
       `degisti` yayilmiyor, ekran yenilenmiyor. Canli sayac ilk
       degerinde donup kalir ve yeni bir yalan olurdu. */
    if (d.durum === 'duraklatildi') {
      const bitis = motor.duraklatmaBitis || 0;
      if (bitis > Date.now()) {
        const t = new Date(bitis);
        const ss = `${String(t.getHours()).padStart(2, '0')}:${String(t.getMinutes()).padStart(2, '0')}`;
        og.durum.textContent = CS(`Duraklatıldı · ${ss}'de devam eder`,
                                  `Paused · resumes at ${ss}`);
      } else {
        og.durum.textContent = CS('Duraklatıldı · sen başlatana kadar bekler',
                                  'Paused · waits until you start it');
      }
    } else {
      og.durum.textContent = C(DURUM_ADI[d.durum]) || '';
    }

    if (d.durum === 'mola') {
      og.sure.textContent = `${Math.ceil(d.kalan)}`;
      og.molaSayi.textContent = Math.ceil(d.kalan);
      og.molaHalka.style.strokeDashoffset = CEVRE_MOLA * d.ilerleme;
    } else {
      og.sure.textContent = ss(d.kalan);
      og.halka.style.strokeDashoffset = CEVRE_ANA * d.ilerleme;
    }

    og.baslat.textContent =
      C(d.durum === 'calisiyor' || d.durum === 'uyari' ? '⏸ Duraklat' : '▶ Başlat');

    // Molanın son üç saniyesi. Burada da yapıyoruz çünkü egzersiz
    // döngüsü requestAnimationFrame ile sürülüyor ve o arka plan
    // sekmesinde duruyor; sekmeye dönüldüğünde işaret doğru olsun.
    if (og.molaEkran) {
      og.molaEkran.classList.toggle(
        'bitmek-uzere', d.durum === 'mola' && d.kalan <= 3);
    }

    og.istMola.textContent = d.istatistik.tamamlananMola;
    og.istAtlanan.textContent = d.istatistik.atlananMola;
    og.istSure.textContent = `${Math.floor(d.istatistik.ekranSuresi / 60)}`
                           + CS(' dk', ' min');
    // Etiket dürüst olsun: izin yoksa bu sayı cihazın değil, sekmenin süresi
    if (og.istSureEtiket) {
      // "takip edilen süre" yanıltıyordu: kullanıcı 4 saattir
      // bilgisayarda ama sekme 6 dakika önce açıldıysa 6 dk yazıyor
      // ve "saymamış" sanılıyor. Etiket ne ölçtüğünü açıkça söylüyor.
      og.istSureEtiket.textContent = C(etkinlikDedektoru
        ? 'cihaz başında süre' : 'bu sekmede geçen süre');
      og.sureKutucuk.title = etkinlikDedektoru
        ? C('Cihaz etkinliği izniyle ölçülüyor — sekme arka plandayken de sayar.')
        : C('Bu sayaç sekme açıldığından beri işler. Bilgisayarın açık olduğu her anı ölçmek için Windows sürümünü kullan.');
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
    // VERİ TARAFI: bu rozet ancak seri oluşunca beliriyor. Temiz
    // bir tarayıcıda sınama koşunca DOM'da hiç yok ve dil taraması
    // geçiyordu.
    og.seriRozet.textContent = s > 0
      ? CS(`🔥 ${s} gün üst üste`,
           `🔥 ${s} ${s === 1 ? 'day' : 'days'} in a row`) : '';
    og.haftaGrafik.innerHTML = '';
    og.haftaGrafik.parentElement.querySelector('.hafta-not')?.remove();

    // Hiç mola yoksa yedi tane 3 piksellik kütük göstermek bozuk duruyor
    if (toplam === 0) {
      const bos = document.createElement('p');
      bos.className = 'hafta-bos';
      // Çalışma anında ekleniyor; `sayfayiCevir`in ona uğrayacağına
      // güvenmek yerine doğrudan aktif dilde kuruluyor.
      bos.textContent = CS(
        'Henüz mola yok. İlk molanı tamamladığında buraya günlük '
        + 'çubuğun düşecek.',
        'No breaks yet. Once you finish your first break, your daily '
        + 'bar will appear here.');
      og.haftaGrafik.appendChild(bos);
      og.haftaOzet.textContent = '';
      return;
    }

    // Kaç günde veri var? Tek günlük veriyle grafik teknik olarak
    // doğru ama görsel olarak bomboş duruyor: hedef 8, bugün 1 ise
    // çubuk %12 yükseklikte kalıyor ve kart 240 piksel boşluk oluyor.
    const doluGun = gunler.filter((g) => g.sayi > 0).length;
    if (doluGun <= 1) {
      og.haftaOzet.textContent = CS(
        `Bugün ${toplam} mola · geçmiş birikiyor`,
        `${toplam} breaks today · history is building up`);
    } else {
      const ortalama = Math.round((toplam / 7) * 10) / 10;
      og.haftaOzet.textContent = CS(
        `${toplam} mola · günde ortalama ${ortalama}`,
        `${toplam} breaks · ${ortalama} per day on average`);
    }

    const enb = Math.max(GUNLUK_HEDEF, ...gunler.map((g) => g.sayi));

    // Grafiğin tamamını ekran okuyucuya tek cümlede anlat
    og.haftaGrafik.setAttribute('role', 'img');
    // CS() ŞART: ekran okuyucu kullanan biri için BU metin grafiğin
    // kendisidir. Gözle görünmediği için hiçbir görsel tarama onu
    // yakalayamaz — İngilizce sayfada Türkçe okunuyordu.
    og.haftaGrafik.setAttribute('aria-label', CS(
      'Son yedi gün: ' + gunler.map((g) => `${g.bugunMu ? 'bugün' : g.ad} ${g.sayi}`).join(', ') +
        `. Toplam ${toplam} mola, günlük hedef ${GUNLUK_HEDEF}.`,
      'Last seven days: ' + gunler.map((g) => `${g.bugunMu ? 'today' : C(g.ad)} ${g.sayi}`).join(', ') +
        `. ${toplam} breaks in total, daily goal ${GUNLUK_HEDEF}.`));

    for (const g of gunler) {
      const hucre = document.createElement('div');
      hucre.className = 'gun'
        + (g.sayi >= GUNLUK_HEDEF ? ' hedefte' : '')
        + (g.bugunMu ? ' bugun' : '');
      // Fare üstüne gelince kesin sayı görünsün
      hucre.title = CS(`${g.bugunMu ? 'Bugün' : g.ad}: ${g.sayi} mola`,
                       `${g.bugunMu ? 'Today' : C(g.ad)}: ${g.sayi} breaks`)
                  + (g.sayi >= GUNLUK_HEDEF ? ' — hedef tamam' : '');

      const sayi = document.createElement('b');
      sayi.textContent = g.sayi || '';

      const alan = document.createElement('span');
      alan.className = 'cubuk-alan';
      const cubuk = document.createElement('i');
      cubuk.style.height = Math.max(3, Math.round((g.sayi / enb) * 100)) + '%';
      alan.appendChild(cubuk);

      const ad = document.createElement('span');
      ad.textContent = C(g.bugunMu ? 'Bugün' : g.ad);

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
      not.textContent = CS(
        'Grafik her gün biraz daha dolacak. '
          + `Kesikli çizgi günlük hedef: ${GUNLUK_HEDEF} mola.`,
        'The chart fills in a little more each day. '
          + `Dashed line is the daily goal: ${GUNLUK_HEDEF} breaks.`);
      og.haftaGrafik.after(not);
    }
  }

  /* ---------- Ana ekrandaki bilgi kartı ---------- */
  let bilgiSirasi = Math.floor(Math.random() * BILGILER.length);
  function bilgiGoster(hedefBaslik, hedefMetin, hedefKaynak, indeks) {
    // Dile göre kaynak dizi; İngilizce dosya yoksa Türkçeye düşer
    const dizi = (aktifDil() === 'en' && typeof BILGILER_EN !== 'undefined')
      ? BILGILER_EN : BILGILER;
    const b = dizi[indeks % dizi.length];
    hedefBaslik.textContent = b.baslik;
    hedefMetin.textContent = b.metin;
    hedefKaynak.textContent = CS(`Kaynak: ${b.kaynak}`, `Source: ${b.kaynak}`);
    return b;
  }
  bilgiGoster(og.anaBaslik, og.anaMetin, og.anaKaynak, bilgiSirasi);
  og.anaBilgiTiklama = $('anaBilgi');
  og.anaBilgiTiklama.style.cursor = 'pointer';
  og.anaBilgiTiklama.title = C('Başka bir bilgi göster');
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

    // C() ŞART: bu metinler `egzersiz.js` içinde sınıf sabiti ve
    // sayfa kurulduktan SONRA yazılıyor — `sayfayiCevir` onları
    // göremez. C()'siz hâlinde İngilizce sayfada Türkçe kalıyordu.
    og.molaBaslik.textContent = C(Sinif.ad);
    og.molaAlt.textContent = C(Sinif.yonerge);

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
        // Son üç saniyede haber ver: mola aniden bitince ekrana dönmek
        // sarsıcı oluyordu. Bakmadan da duyulsun diye metin değil,
        // ekranın kendisi hazırlık yapıyor.
        const kalanSn = motor.ayarlar.molaSuresi - gecen;
        const y = kalanSn <= 3 && kalanSn > 0
          ? C('Az kaldı — hazırlan')
          : egzersiz.anlikYonerge(gecen);
        if (y !== sonYonerge) { sonYonerge = y; og.molaAlt.textContent = y; }
        og.molaEkran.classList.toggle('bitmek-uzere', kalanSn <= 3);
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

  /* MOLADAN KAZAYLA ÇIKMAYI ÖNLEME.

     Kullanıcı "bi deyince çıkıyor" dedi; sebebi mola ekranının tam
     ekran olmaması: altta telefonun gezinti çubuğu duruyor ve geri
     tuşu bir dokunuş uzakta.

     KİLİTLEME DEĞİL. Esc her zaman tam ekrandan çıkarır — tarayıcı
     garantisi, engelleyemeyiz ve engellemeye çalışmıyoruz. Ana ekran
     tuşuna dokunmuyoruz. Ayar kapatılabiliyor. Amaç kazayı
     zorlaştırmak, çıkışı imkânsızlaştırmak değil. */
  let molaGecmisi = false;      // geçmişe giriş ekledik mi
  let molaKapaniyor = false;    // normal kapanış sırasında popstate'i yut
  let tamEkranBizden = false;   // tam ekranı biz mi açtık

  function molaCikisKorumasiKur() {
    if (!molaKilit) return;
    try {
      history.pushState({ gozMolasi: 1 }, '');
      molaGecmisi = true;
    } catch { molaGecmisi = false; }

    // Tam ekran: sistem çubukları gizlenince geri tuşu da kaybolur.
    // Kullanıcı hareketi olmadan reddedilebilir; REDDEDİLİRSE MOLA
    // YİNE ÇALIŞIR, kullanıcıya hata göstermiyoruz.
    try {
      const k = document.documentElement;
      if (k.requestFullscreen && !document.fullscreenElement) {
        k.requestFullscreen({ navigationUI: 'hide' })
          .then(() => { tamEkranBizden = true; })
          .catch(() => { tamEkranBizden = false; });
      }
    } catch { tamEkranBizden = false; }
  }

  function molaCikisKorumasiniKaldir() {
    if (tamEkranBizden && document.fullscreenElement) {
      document.exitFullscreen?.().catch(() => {});
    }
    tamEkranBizden = false;
    if (molaGecmisi) {
      // Eklediğimiz girişi geri al ki geri tuşu sonradan normal çalışsın.
      molaKapaniyor = true;
      molaGecmisi = false;
      try { history.back(); } catch { molaKapaniyor = false; }
      setTimeout(() => { molaKapaniyor = false; }, 400);
    }
  }

  window.addEventListener('popstate', () => {
    if (molaKapaniyor) { molaKapaniyor = false; return; }
    if (!molaAcik || !molaGecmisi) return;
    // Geri tuşuna basıldı ama mola sürüyor: girişi yeniden ekle.
    try { history.pushState({ gozMolasi: 1 }, ''); } catch {}
    molaIpucuGoster();
  });

  let ipucuZaman = 0;
  function molaIpucuGoster() {
    const e = $('molaIpucu');
    if (!e) return;
    e.textContent = motor.ayarlar.molaAtlanabilir
      ? CS('Mola sürüyor. Bitirmek için "Molayı atla"yı basılı tut.',
           'Break in progress. Hold “Skip break” to end it.')
      : CS('Mola sürüyor — birkaç saniye kaldı.',
           'Break in progress — a few seconds left.');
    e.hidden = false;
    clearTimeout(ipucuZaman);
    ipucuZaman = setTimeout(() => { e.hidden = true; }, 2500);
  }

  function molaEkraniAc() {
    molaAcik = true;
    molaCikisKorumasiKur();
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
      og.nedenKaynak.textContent = k.kaynak ? CS(`Kaynak: ${k.kaynak}`, `Source: ${k.kaynak}`) : '';
      og.nedenKart.dataset.tur = k.tur;
      og.nedenKart.classList.add('gorunur');

      // Ana ekrandaki kart göz bilgisi kalsın — orada hava durumu
      // göstermek sayfanın amacını bulanıklaştırıyor.
      if (k.tur === 'bilgi') {
        og.anaBaslik.textContent = k.baslik;
        og.anaMetin.textContent = k.metin;
        og.anaKaynak.textContent = k.kaynak ? CS(`Kaynak: ${k.kaynak}`, `Source: ${k.kaynak}`) : '';
      }
    }, nedenGecikme);

    // Atla düğmesi ayardan kapalıysa hiç gösterme
    og.atla.classList.toggle('gizli', !motor.ayarlar.molaAtlanabilir);

    og.okuyucu.textContent = CS(
      `Mola başladı. ${motor.ayarlar.molaSuresi} saniye boyunca uzağa bak.`,
      `Break started. Look away for ${motor.ayarlar.molaSuresi} seconds.`);
    calSes(660, 0.55);
    titret([120, 80, 120]);         // iki kısa: "dur"
    uyanikTut();
    bildirimGonder('Göz molası', 'Gözünü ekrandan ayır, 6 metre uzağa bak.');
    og.molaEkran.focus?.();
  }

  function molaEkraniKapat() {
    molaCikisKorumasiniKaldir();
    molaAcik = false;
    egzersiziDurdur();
    og.molaEkran.classList.remove('acik', 'bitmek-uzere');
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
    og.atla.textContent = C('Bırakma…');
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
  /* UZUN MOLA ÖNERİSİ
     Çekirdek iki saati aşan kesintisiz çalışmadan sonra
     `uzunMolaOnerisi` yayıyordu ve BUNU DİNLEYEN YOKTU. Ayar kutusu
     vardı, "Ders" kipi ayarı açıyordu, sayaç doğru sayıyordu — ama
     kullanıcıya hiçbir şey ulaşmıyordu. Bilgi üretilmiş, karar
     verilmemişti.

     ZORLAMA YOK: kart engellemez, sayaç arkada dönmeye devam eder.
     "Şimdi değil" denince bir süre bir daha sorulmaz — her mola
     sonunda tekrar sormak, öneriyi dırdıra çevirir ve kullanıcı
     kartı okumadan kapatmayı öğrenir. */
  let uzunMolaSessiz = 0;          // kaç öneri atlanacak
  function uzunMolaOner(kesintisizSn) {
    const kart = $('uzunMolaKarti');
    if (!kart) return;
    if (uzunMolaSessiz > 0) { uzunMolaSessiz--; return; }
    /* BURADA BIR KORUMA VARDI VE OZELLIGI TAMAMEN KAPATIYORDU.
       "Mola ekrani acikken kart gorunmesin" diye `durum === 'mola'`
       ise cikiyordum. Ama olay tam da mola BITERKEN yayiliyor ve o
       anda durum HALA 'mola' — cekirdek `_asamayaGec('calisiyor')`
       cagrisini olaydan SONRA yapiyor. Yani kart HIC cikmiyordu.
       Kendi sinamam yakaladi: uc kosul da saglandigi hâlde kart gizli.

       Makul gorunen bir koruma, ozelligi sessizce kapatabilir. */

    const dk = Math.round((+kesintisizSn || 0) / 60);
    const uzunDk = Math.round((motor.ayarlar.uzunMolaSuresi || 300) / 60);
    $('uzunMolaBaslik').textContent = CS('Uzun mola zamanı', 'Time for a long break');
    $('uzunMolaMetin').textContent = CS(
      `${dk} dakikadır aralıksız çalışıyorsun. ${uzunDk} dakikalık bir mola `
        + 'gözünü ve boynunu belirgin biçimde dinlendirir.',
      `You have been working for ${dk} minutes without a real rest. `
        + `A ${uzunDk}-minute break gives your eyes and neck a real recovery.`);
    $('uzunMolaEvet').textContent = CS('Uzun mola ver', 'Take a long break');
    $('uzunMolaSonra').textContent = CS('Şimdi değil', 'Not now');
    // Bir sonraki tike birak: mola ortusu kapansin, kart sonra gorunsun.
    setTimeout(() => { kart.hidden = false; }, 60);
  }

  function uzunMolaKapat() { const k = $('uzunMolaKarti'); if (k) k.hidden = true; }

  $('uzunMolaEvet')?.addEventListener('click', () => {
    uzunMolaKapat();
    try { motor.uzunMolayaGec(); } catch {}
  });
  $('uzunMolaSonra')?.addEventListener('click', () => {
    uzunMolaKapat();
    // Üç öneri boyunca sessiz: ~1 saat. Reddedilen öneriyi hemen
    // tekrarlamak, kullanıcıya saygısızlıktır.
    uzunMolaSessiz = 3;
  });

  let balonZaman = null;
  function balonGoster(saniye) {
    /* SÖZLÜKTEN DEĞİL `CS`TEN. Sözlük TAM eşleşme arıyor; içinde
       değişen bir sayı olan metin oraya konamaz. Nitekim konmuş:
       `'15 sn sonra göz molası'` diye tek bir değer vardı, yani
       yalnız 15'te çevriliyordu; 14'te Türkçeye dönüyordu. */
    const kalanSn = Math.ceil(saniye);
    og.balonMetin.textContent = CS(`${kalanSn} sn sonra göz molası`,
                                   `Eye break in ${kalanSn} s`);
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
      og.okuyucu.textContent = C('Mola bitti, devam edebilirsin.');

      if (tanitimMolasi) {
        // Örnek mola 6 saniyeydi; 20 saniyelik bir mola sayılmaz.
        tanitimMolasi = false;
        motor.istatistik.tamamlananMola =
          Math.max(0, (motor.istatistik.tamamlananMola | 0) - 1);
        kaydet();
        ekraniCiz(motor.anlikDurum());
        return;
      }

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
    .uzerine('uzunMolaOnerisi', (kesintisizSn) => uzunMolaOner(kesintisizSn))
    .uzerine('molaAtlandi', () => {
      molaEkraniKapat();
      og.okuyucu.textContent = C('Mola atlandı.');
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

  /* ============================================================
     BİLGİLER SEKMESİ

     Bilgiler dört ayrı dosyaya dağılmıştı ve yalnızca molalarda tek
     tek çıkıyorlardı; merak eden kişinin hepsini görebileceği bir yer
     yoktu. Burada tek listede toplanıyorlar.

     İçerik VERİDEN kuruluyor, HTML'e elle yazılmıyor. Elle yazmak aynı
     metnin ikinci kopyası demek; bugün bilgiler.py ile bilgiler.js'in
     tam bu yüzden ayrıştığını yakaladık.

     Rehber de kopyalanmıyor: rehber.html çalışma anında çekilip içeri
     konuyor. Tek kaynak, iki gösterim.
     ============================================================ */
  const kacis = (m) => String(m ?? '').replace(/[&<>"]/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function bilgiOgesi(baslik, metin, kaynak) {
    return '<div class="bilgi-oge"><b>' + kacis(baslik) + '</b><p>'
      + kacis(metin) + '</p>'
      + (kaynak ? '<span class="kaynak">' + kacis(kaynak) + '</span>' : '')
      + '</div>';
  }

  function bilgiBolumu(baslik, adet, not, ogeler) {
    return '<section class="bilgi-bolum"><h3>' + kacis(baslik)
      + ' <small>' + adet + '</small></h3>'
      + (not ? '<p class="bolum-not">' + kacis(not) + '</p>' : '')
      + ogeler.join('') + '</section>';
  }

  let bilgilerKuruldu = false;
  /* NELER DEĞİŞTİ listesi (K-44) — Bilgiler sekmesinde.
     Tek kaynak `degisiklikler.js`; şerit de aynı diziyi okuyor.
     İki yerde ayrı metin tutmak, ikisinin ayrışması demektir —
     bu projede `bilgiler.py`/`bilgiler.js` ikizinde yaşandı. */
  function degisiklikleriKur() {
    const kap = $('degisiklikListesi');
    if (!kap || typeof DEGISIKLIKLER === 'undefined') return;
    if (kap.dataset.kuruldu) return;
    kap.dataset.kuruldu = '1';
    kap.innerHTML =
      '<h2 class="kutu-baslik">' + CS('Neler değişti', 'What changed') + '</h2>' +
      DEGISIKLIKLER.map((d) =>
        '<div class="degisiklik-kayit">' +
        '<b>' + CS(d.tarih, d.tarihEn || d.tarih) + '</b>' +
        (d.ayarGozdenGecir
          ? '<p class="onemli-not">' + CS(
              'Aile kipi kullanıyorsan ayarlarını bir kez daha gözden geçir.',
              'If you use Family mode, review your settings once more.') + '</p>'
          : '') +
        '<ul>' + CS(d.maddeler, d.maddelerEn || d.maddeler)
          .map((m) => '<li>' + m + '</li>').join('') + '</ul>' +
        '</div>').join('');
    sayfayiCevir(kap);
  }

  async function bilgileriKur() {
    if (bilgilerKuruldu) return;
    bilgilerKuruldu = true;
    const kap = $('bilgilerIcerik');
    if (!kap) return;
    const parcalar = [];

    // 1) Göz sağlığı bilgileri
    try {
      const dizi = (aktifDil() === 'en' && typeof BILGILER_EN !== 'undefined')
        ? BILGILER_EN : BILGILER;
      parcalar.push(bilgiBolumu(
        C('Göz sağlığı'), dizi.length,
        C('Molalarda karşına çıkan kartlar. Kanıtı zayıf olanlarda bunu '
          + 'açıkça yazıyoruz — abartılı sağlık iddiası yok.'),
        dizi.map((b) => bilgiOgesi(b.baslik, b.metin, b.kaynak))));
    } catch {}

    // 2) Pratik ipuçları
    try {
      const ip = MolaIcerik.ipuclari();
      parcalar.push(bilgiBolumu(
        C('Pratik ipuçları'), ip.length,
        C('Molada ya da masa başında yapabileceğin küçük şeyler.'),
        ip.map((b) => bilgiOgesi(b.baslik, b.metin, b.kaynak))));
    } catch {}

    // 3) Egzersizler
    try {
      parcalar.push(bilgiBolumu(
        C('Molalardaki egzersizler'), TUM_EGZERSIZLER.length,
        C('Mola ekranında sırayla çıkarlar. "Uzağa bak" asıl olan; '
          + 'diğerleri ekranın ezberlenip görünmez olmasını önlüyor.'),
        TUM_EGZERSIZLER.map((E) => bilgiOgesi(E.ad, E.yonerge, ''))));
    } catch {}

    // 4) Dünyadan — İngilizcede henüz yok
    try {
      if (typeof DUNYA !== 'undefined' && DUNYA.length && aktifDil() !== 'en') {
        parcalar.push(bilgiBolumu(
          'Dünyadan', DUNYA.length,
          'Göz sağlığıyla ilgisi yok. Molada birkaç saniyeliğine merak '
          + 'edilecek bir şey olsun diye.',
          DUNYA.map((b) => bilgiOgesi(b.baslik, b.metin, b.kaynak))));
      }
    } catch {}

    kap.innerHTML = parcalar.join('')
      + '<section class="bilgi-bolum"><h3>' + kacis(C('Ayrıntılı rehber'))
      + '</h3><div class="rehber-govde" id="rehberGovde">'
      + '<p class="rehber-yukleniyor">' + kacis(C('Yükleniyor…'))
      + '</p></div></section>';

    /* Rehberi ÇEKİP koyuyoruz, kopyalamıyoruz. rehber.html hem arama
       motorları için ayrı bir sayfa olarak duruyor hem de burada
       görünüyor — tek kaynak. Çevrimdışıyken servis işçisinin
       önbelleğinden geliyor; o da yoksa bağlantı bırakıyoruz. */
    const govde = $('rehberGovde');
    try {
      const adres = aktifDil() === 'en' ? 'guide.html' : 'rehber.html';
      const yanit = await fetch(adres);
      if (!yanit.ok) throw new Error(yanit.status);
      const belge = new DOMParser().parseFromString(await yanit.text(), 'text/html');
      const yazi = belge.querySelector('main.yazi');
      if (!yazi) throw new Error('govde yok');
      yazi.querySelectorAll('script, .reklam-alani, nav.icindekiler')
        .forEach((o) => o.remove());
      govde.innerHTML = yazi.innerHTML;
    } catch {
      const adres = aktifDil() === 'en' ? 'guide.html' : 'rehber.html';
      govde.innerHTML = '<p class="rehber-yukleniyor">'
        + kacis(C('Rehber şu an yüklenemedi.')) + ' <a href="' + adres
        + '">' + kacis(C('Ayrı sayfada aç')) + '</a></p>';
    }
    try { sayfayiCevir(kap); } catch {}
    // Şeritteki "Neler değişti?" bağlantısı buraya kaydırıyor.
    try { degisiklikleriKur(); } catch {}
  }

  /* ---------- Sekme değiştirme ---------- */
  const sekmeler = [
    { dugme: $('sekmeDugmeSayac'), panel: $('sekmeSayac') },
    { dugme: $('sekmeDugmeBilgiler'), panel: $('sekmeBilgiler') },
  ];
  function sekmeSec(ad) {
    sekmeler.forEach((s) => {
      const secili = s.panel && s.panel.id === ad;
      if (!s.dugme || !s.panel) return;
      s.dugme.classList.toggle('secili', secili);
      s.dugme.setAttribute('aria-selected', secili ? 'true' : 'false');
      s.panel.hidden = !secili;
    });
    if (ad === 'sekmeBilgiler') bilgileriKur();
  }
  sekmeler.forEach((s) => s.dugme?.addEventListener(
    'click', () => sekmeSec(s.panel.id)));

  /* ---------- KISAYOLLAR ----------
     Boşluk ve M zaten vardı ama hiçbir yerde yazmıyordu. Kimsenin
     bilmediği kısayol kısayol değil. Liste "?" ile ya da alttaki
     bağlantıyla açılıyor.

     Mola ekranı açıkken HİÇBİRİ çalışmaz: 20 saniye tek tuşla
     geçilebilseydi mola olmazdı. */
  const kisayolPencere = $('kisayolPencere');
  function kisayollariGoster() {
    try { kisayolPencere?.showModal(); } catch {}
  }
  $('kisayolKapat')?.addEventListener('click', () => kisayolPencere?.close());
  $('kisayolAc')?.addEventListener('click', (e) => {
    e.preventDefault();
    kisayollariGoster();
  });

  document.addEventListener('keydown', (e) => {
    // e.target her zaman bir Element olmayabilir (document olabilir)
    if (e.target instanceof Element && e.target.matches('input, select, textarea')) return;
    if (e.ctrlKey || e.altKey || e.metaKey) return;   // tarayıcı kısayollarına dokunma
    if (kisayolPencere?.open) {
      if (e.key === 'Escape') kisayolPencere.close();
      return;
    }
    if (og.pencere.open || og.sifrePencere.open) return;
    if (molaAcik) return;                             // mola sırasında kısayol yok

    if (e.key === ' ') { e.preventDefault(); og.baslat.click(); return; }
    const t = e.key.toLowerCase();
    if (t === 'm') { og.mola.click(); return; }
    if (t === 'a') { e.preventDefault(); og.ayarAc.click(); return; }
    if (t === 't') { og.tema.click(); return; }
    if (t === 'r') { og.sifirla.click(); return; }
    if (t === 'b') { sekmeSec('sekmeBilgiler'); return; }
    if (t === 's') { sekmeSec('sekmeSayac'); return; }
    if (e.key === '?' || (e.key === '/' && e.shiftKey)) {
      e.preventDefault();
      kisayollariGoster();
    }
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
    { id: 'beyaz',    ad: 'Beyaz',          zemin: '#ffffff', a: '#0f8c78', b: '#9a6410' },
    { id: 'otomatik', ad: C('Sistemle aynı'), zemin: '#141130', a: '#7ee0d2', b: '#ffc46b' },
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
    { id: 'gokyuzu',  ad: 'Gökyüzü',        zemin: '#f6faff', a: '#1668a8', b: '#96590d' },
    { id: 'kum',      ad: 'Kum',            zemin: '#fbf7f0', a: '#8f5d0c', b: '#8a5a1c' },
    { id: 'zeytin',   ad: 'Zeytin',         zemin: '#f7f8f1', a: '#436b20', b: '#8d6410' },
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
        ? CS(`${ad} (%${yuzde}) — yazı okunaklılığı değişmez, sadece renklerin doygunluğu`,
             `${ad} (${yuzde}%) — only colour saturation changes; text legibility does not`)
        : C('Bu tarayıcı canlılık ayarını desteklemiyor; tema renkleri olduğu gibi kullanılıyor.');
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
  /* CEKINCE, KARARIN VERILDIGI YERDE DURMALI.
     Ikinci secenegin etiketi once "2023 calismasi bunu oneriyor"
     idi. Ilgili bilgi karti dogru yazilmis: "KUCUK bir calismada"
     diyor ve kaynagi veriyor (Johnson & Rosenfield, Optom Vis Sci,
     2023). Ama kullanici sureyi bu DUGMEDEN seciyor; karti hic
     acmayabilir. Cekince kartta kalirsa, kararin verildigi yerde
     yok demektir -- kucuk bir calismanin bulgusu, bir oneri gibi
     okunur. Wishnofsky ornegindeki ile ayni sinif: aktarilirken
     cekince dusuyor. */
  const SURE_SECENEKLERI = [
    { dk: 20, sn: 20, ad: '20 dk · 20 sn', not: 'Klasik 20-20-20 kuralı' },
    { dk: 10, sn: 20, ad: '10 dk · 20 sn', not: 'Küçük bir çalışmada daha iyi' },
    { dk: 30, sn: 30, ad: '30 dk · 30 sn', not: 'Daha seyrek, daha uzun' },
    { dk: 45, sn: 60, ad: '45 dk · 1 dk', not: 'Odak bloğu sevenler için' },
  ];

  function hazirSureleriKur() {
    og.hazirSureler.innerHTML = SURE_SECENEKLERI.map((s, i) => `
      <button type="button" class="sure-sec" data-i="${i}" aria-pressed="false">
        <b>${C(s.ad)}</b><span>${C(s.not)}</span>
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

    og.ayCalismaDeger.textContent = `${dk}` + CS(' dk', ' min');
    og.ayMolaDeger.textContent = sn >= 60
      ? (sn % 60 === 0 ? `${sn / 60}` + CS(' dk', ' min')
                       : `${Math.floor(sn / 60)}` + CS(' dk ', ' min ') + `${sn % 60}` + CS(' sn', ' s'))
      : `${sn}` + CS(' sn', ' s');
    og.ayUyariDeger.textContent = uy === 0 ? CS('kapalı', 'off')
                                           : `${uy}` + CS(' sn', ' s');

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
      not = '<span class="uyari-notu">' + CS(
        '⚠ 30 dakikadan seyrek molanın faydası azalıyor. '
          + 'Amerikan Optometri Birliği 20 dakika öneriyor.',
        '⚠ Breaks less often than every 30 minutes lose much of their benefit. '
          + 'The American Optometric Association suggests 20 minutes.') + '</span>';
    } else if (sn < 15) {
      not = '<span class="uyari-notu">' + CS(
        '⚠ 15 saniyeden kısa mola gözün odak kasının gevşemesine yetmeyebilir.',
        '⚠ A break shorter than 15 seconds may not let the focusing muscle relax.')
        + '</span>';
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
    og.ayUzunSureDeger.textContent = `${dk}` + CS(' dk', ' min');
    og.uzunMolaNe.textContent = CS(
      `2 saat kesintisiz çalışınca ${dk} dakikalık uzun mola önerilir. Zorlama yok, sorar.`,
      `After 2 hours of unbroken work it offers a ${dk}-minute long break. It asks, never forces.`);
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
              aria-checked="${t.id === tema}" title="${C(t.ad)}" aria-label="${C(t.ad)}"
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
    og.temaAdi.textContent = s ? s.ad
      : CS('Seçince hemen uygulanır', 'Applies immediately');
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
    og.ayUzakSifirla.checked = uzakSifirla;
    og.ayMolaKilit.checked = molaKilit;
    og.ayOtomatik.checked = otomatikBasla;
    og.ayTitresim.checked = titresimAcik;
    og.ayArkaPlan.checked = arkaPlanAcik;
    // Desteklenmiyorsa boşuna umut verme
    if (!navigator.vibrate) {
      og.ayTitresim.disabled = true;
      og.ayTitresim.closest('.satir').querySelector('small').textContent =
        C('Bu cihaz titreşimi desteklemiyor');
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
    uzakSifirla = og.ayUzakSifirla.checked;
    molaKilit = og.ayMolaKilit.checked;
    motor.ayarlar.uzakKalincaSifirla = uzakSifirla;
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

    og.aciklama.textContent = aciklamaMetni(dk, ml);

    if (motor.durum !== 'hazir') motor.sifirla();
    kaydet();
    kipleriTazele();
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
      og.hepsiniSil.textContent = C('Emin misin? Tekrar bas');
      og.sifirlamaDurum.textContent = C('Bu işlem geri alınamaz.');
      clearTimeout(silmeZaman);
      silmeZaman = setTimeout(() => {
        silmeOnayi = false;
        og.hepsiniSil.textContent = C('Sıfırla');
        og.sifirlamaDurum.textContent = C('Ayarlar, sayaçlar ve şifre silinir');
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

  /* DİKKAT — buraya alan EKLEMEK kolay, alan KORUMAK değil.
     Aşağıdaki nesne her seferinde SIFIRDAN kuruluyor. Listede
     olmayan hiçbir alan hayatta kalmaz: 15 saniyede bir ve her
     sayfa kapanışında silinir. Başka bir yerde `localStorage`a
     yazdığın bir alan varsa ya buraya ekle ya da AYRI anahtar
     kullan. "Neler değişti" işareti tam bu yüzden ayrı anahtarda
     (`goz-molasi-gorulen`) duruyor — buraya konduğunda ölçüldü:
     kullanıcı şeridi kapatıyor, 15 saniye sonra işaret siliniyor,
     bir dahaki açılışta şerit yine çıkıyordu. */
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
        uzakSifirla,
        molaKilit,
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
     SEKMELER ARASI EŞİTLEME

     Uygulama iki sekmede açıksa her sekmenin kendi sayacı işliyor ve
     ikisi aynı kaydı ezmeye çalışıyordu. Ölçtüm: bir sekme 36:20
     gösterirken yeni açılan sekme 36:56 gösteriyordu.

     storage olayı YALNIZCA diğer sekmelerde tetiklenir; kendi
     yazdığımızda gelmez. Yani başka bir sekme kaydettiğinde sayacı
     ondan eşitliyoruz — son yazan kazanıyor ve hepsi aynı şeyi
     gösteriyor.

     Mola sırasında eşitleme yapmıyoruz: mola ekranı açıkken sayacı
     dışarıdan oynatmak molayı bozar.
     ============================================================ */
  window.addEventListener('storage', (e) => {
    if (e.key !== KAYIT_ANAHTARI || !e.newValue) return;
    if (motor.durum === 'mola' || molaAcik) return;
    let veri = null;
    try { veri = JSON.parse(e.newValue); } catch { return; }
    if (!veri) return;
    if (motor.sayaciGeriYukle(veri)) {
      ekraniCiz(motor.anlikDurum());
    }
  });

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
        // Ekran kilitlendiyse kişi gerçekten uzaklaşmıştır; sayacın
        // sıfırlanması ancak bu durumda (ya da çok uzun bir aradan
        // sonra) doğru olur.
        if (d.screenState === 'locked') motor.ekranKilitlendiBildir();
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
  og.aciklama.textContent = aciklamaMetni(
    Math.round(motor.ayarlar.calismaSuresi / 60), motor.ayarlar.molaSuresi);

  ekraniCiz(motor.anlikDurum());
  tekSekmeyiKur();
  kipleriKur();
  tanitimiKurGerekirse();

  /* ---- Dil ----
     Sözlük Türkçe metnin kendisini anahtar alıyor, o yüzden HTML'e
     hiç dokunmadan çeviriyoruz: sayfa kurulduktan SONRA metin
     düğümleri geziliyor. Dinamik olarak yazılan metinler (kip adları,
     bilgi kartları) kendi yerlerinde C() ile geçiyor. */
  // İngilizce kipte rehber bağlantıları İngilizce rehbere gitsin
  if (aktifDil() === 'en') {
    document.querySelectorAll('a[href="rehber.html"]')
      .forEach((a) => { a.href = 'guide.html'; });
  }

  try {
    og.ayDil.value = aktifDil();
    og.ayDil.addEventListener('change', () => diliDegistir(og.ayDil.value));
    sayfayiCevir();
  } catch {}
  bildirimDurumunuGoster();
  kilitDurumunuGoster();
  temaSeciciyiKur();
  hazirSureleriKur();

  /* Açılışta kendiliğinden başla — AMA sayaç kayıttan geri
     yüklenmediyse. Eskiden koşulsuz çağrılıyordu ve geri yüklenen
     hedefi eziyordu: sayfayı yenilemek 36 dakikalık ilerlemeyi
     sıfırlıyordu. Ölçtüm, 13 saniye sonra yenilenen sayfa yine
     36:58 gösteriyordu.

     "Cihaza bakılmaya başlandığında başlasın" isteği burada
     iki parçayla karşılanıyor:
       1) Uygulama açılır açılmaz sayaç döner (bu satır),
       2) Kimse dokunmuyorsa 90 sn sonra sayaç kendini durdurur ve
          ilk dokunuşta yeniden başlar (motor.hareketVar).
     Yani bilgisayar açıkken sen yokken sayaç boşa dönmez. */
  const oncedenCalisiyordu =
    kayit.durum === 'calisiyor' || kayit.durum === 'uyari' || kayit.durum === 'mola';
  if (!motor.geriYuklendi && (otomatikBasla || oncedenCalisiyordu)) motor.basla();

  // Hata ayıklama / test için: konsoldan molaMotoru.ayarlar ile oynayabilirsin
  window.molaMotoru = motor;

  /* KÖPRÜ — Windows sürümü açıksa sayaç ORADAN devralınır.

     Sorun buydu: iki sürüm iki ayrı yere yazıyor. Kullanıcı Windows
     sürümünde 8 dakikadayken tarayıcıyı açınca 20:00 görüyor ve
     "süre başa sardı" diyordu. İki sayaç değil, tek sayaç olmalı.

     NEDEN WINDOWS KAZANIYOR: o sürüm sürekli açık ve sekme kapalıyken
     de ölçebiliyor. Tarayıcı kapalıyken hiçbir şey ölçemez. Hangisi
     daha çok şey biliyorsa doğru olan odur.

     Köprü yoksa (Windows sürümü kapalı, ya da tarayıcı yerel adrese
     izin vermiyor) burası SESSİZCE geçilir — olmayan bir şeyin
     eksikliği hata değildir. */
  (function kopruyuBagla() {
    if (!window.Kopru) return;

    // Kullanıcının içinde bulunduğu anı bozmayalım: mola ekranı
    // açıkken sayacı değiştirmek, gözünü ekrandan ayırmış birinin
    // molasını yarıda kesmek demek.
    const devralinabilir = () =>
      motor.durum === 'calisiyor' || motor.durum === 'uyari'
      || motor.durum === 'hazir' || motor.durum === 'bosta';

    let bildirildi = false;

    const uygula = (veri) => {
      if (!veri || !devralinabilir()) return;

      /* WINDOWS SAYMIYORSA SAYACA DOKUNMA.
         Bu satır bir hata düzeltmesidir, incelik değil. Eskiden bu
         denetim YOKTU: Windows boşta/duraklamış/çalışma saati dışında
         iken köprü sıfıra inen bir sayı gönderiyordu ve tarayıcı 25
         saniyede bir SAHTE MOLA veriyordu. Bir öğle molasında ~50
         sahte mola üretiyor, hepsi istatistiğe kalıcı yazılıyordu.

         Yani köprü, önlemek için yazıldığı şeyi — "süre başa sardı"
         hissini — kendisi üretiyordu.

         `sayiyor` alanı pakette VARDI ama okunmuyordu. Veri
         gönderilmiş, karar verilmemişti. */
      if (veri.sayiyor === false) return;

      const kalan = Math.max(0, Math.round(+veri.kalan_sn));

      // Zaten aynıysa dokunma. Her 5 saniyede sayacı yeniden kurmak
      // ekranda titreme ve ilerleme çubuğunda geri sıçrama yapar.
      if (Math.abs(motor.kalanSaniye() - kalan) < 3) return;

      // sayaciGeriYukle DEĞİL: o yol "sekme kapalıydı" durumu için ve
      // içindeki iki tahmin kuralı canlı veride zarar veriyor.
      // Gerekçesi cekirdek.js/kopruyuBenimse başında yazılı.
      const uyduMu = motor.kopruyuBenimse(kalan);
      if (!uyduMu) return;

      // Devraldıysak "uygulama X dakika kapalıydı" notu artık yanlış:
      // süre kaybolmadı, Windows sürümü saymaya devam etmişti.
      const eskiNot = $('durumNotu');
      if (eskiNot) eskiNot.hidden = true;

      if (!bildirildi) {
        bildirildi = true;
        const dk = Math.floor(kalan / 60);
        const sn = kalan % 60;
        const kalanYazi = `${dk}:${String(sn).padStart(2, '0')}`;
        const not = $('durumNotu');
        if (not) {
          const b = $('durumNotuBaslik');
          if (b) b.textContent = CS('Windows sürümüyle eşitlendi',
                                    'Synced with the Windows version');
          $('durumNotuMetin').textContent = CS(
            `Bu bilgisayarda Göz Molası açık. Sayaç baştan başlamadı, `
            + `oradan devraldı: ${kalanYazi} kaldı.`,
            `Eye Break is running on this computer. The timer did not `
            + `restart — it continued from there: ${kalanYazi} left.`);
          not.hidden = false;
          $('durumNotuKapat')?.addEventListener(
            'click', () => { not.hidden = true; });
        }
      }
    };

    window.Kopru.ilkDurum().then(uygula);
    window.Kopru.dinle(uygula);
  })();

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
    not.textContent = CS(
      'Telefonda: uygulama açıkken hatırlatır. Ekran kilitliyken '
        + 'tarayıcılar sayacı dondurur — bu bir telefon sınırı, uygulama hatası değil. '
        + 'Ayarlardan “Arka planda çalışmaya devam et” bunu büyük ölçüde çözer.',
      'On a phone it reminds you while the app is open. When the screen is '
        + 'locked, browsers freeze the timer — that is a phone limitation, not '
        + 'an app bug. “Keep running in the background” in Settings largely '
        + 'solves it.');
    document.querySelector('.alt-bilgi')?.appendChild(not);
  }

  // Reklam alanı — numaralar girilmemişse kendini tamamen kaldırır
  try { tumReklamlariKur(); } catch {}

  /* SAYAÇ NEDEN SIFIRLANDI?

     Motor, uzun süre kapalı kalındığı için sayacı sıfırladıysa sebebi
     kaydediyor. Burada bir kez gösteriyoruz.

     Neden gerekli: kullanıcı uygulamayı açıp 20:00 görünce "saymamış,
     bozuk" diye düşünüyor. Oysa tarayıcı, sekmesi kapalıyken hiçbir
     şey ölçemez — bu bir hata değil, teknik bir sınır. Söylemek,
     sessiz kalmaktan iyi. */
  (function sifirlanmaNotu() {
    const sebep = motor.sifirlanmaSebebi;
    const gec = motor.gecikmisMola;

    /* Üç ayrı şey söylenebilir ve üçü de söyleniyor. Eskiden yalnız
       'uzun-kapali' anlatılıyordu; mola ekranı açıkken kapanma yolu
       sebebi hiç kurmadığı için kullanıcı SESSİZ bir sıfırlama
       görüyordu — telefonda en sık yaşanan yol tam buydu. */
    const not = $('durumNotu');
    if (!not) return;

    let metin = null;
    if (gec) {
      const g = Math.max(1, gec.dakika | 0);
      metin = CS(
        `Mola sen uzaktayken geldi (${g} dakika). Sayaç sıfırlanmadı — `
        + `molan birazdan başlıyor.`,
        `Your break came due while you were away (${g} min). The timer was `
        + `not reset — your break starts shortly.`);
    } else if (sebep && sebep.tur === 'mola-sirasinda') {
      const d = Math.max(1, sebep.dakika | 0);
      metin = CS(
        `Mola ekranı açıkken ${d} dakika ayrılmışsın. O molayı verilmiş `
        + `saydık ve sayaç yeniden başladı.`,
        `You left for ${d} minutes while the break screen was open. We `
        + `counted that break as taken and the timer restarted.`);
    } else if (sebep && sebep.tur === 'uzun-kapali') {
      const dk = Math.max(1, sebep.dakika | 0);
      metin = CS(
        `Uygulama ${dk} dakika kapalıydı, o yüzden sayaç yeniden başladı — `
        + `o kadar süre ekrandan uzaktaysan gözlerin zaten dinlendi. `
        + `Tarayıcı, sekmesi kapalıyken hiçbir şey ölçemez; bu bir ayar `
        + `değil, teknik bir sınır. Bilgisayarında kapalıyken de ölçmesi `
        + `için Windows sürümünü kullanabilirsin.`,
        `The app was closed for ${dk} minutes, so the timer restarted — `
        + `if you were away from the screen that long, your eyes already `
        + `rested. A browser cannot measure anything while its tab is `
        + `closed; that is a technical limit, not a setting. On a `
        + `computer, the Windows version keeps measuring.`);
    }
    if (!metin) return;
    $('durumNotuMetin').textContent = metin;
    not.hidden = false;
    $('durumNotuKapat')?.addEventListener('click', () => { not.hidden = true; });
  })();

  /* NE DEĞİŞTİ (K-44) — güncellendikten SONRA bir kez.

     Bugüne kadar sessizce yayınladık: şerit "Yeni sürüm hazır"
     diyordu, doğru ama bilgisiz. Aile kipinde bu daha ağır — bir
     ebeveyn korumanın çalıştığını sanarak kurmuş olabilir ve
     düzelttiğimiz açıklar tam o sınıftı.

     Sürüm yüklü damgadan okunuyor. Ayrı bir sabit tutmak ikinci bir
     elle yazılan sayı olurdu; bugün masaüstünde tam bu yüzden
     bildirim hiç çıkmıyordu. */
  function yenilikNotunuGoster() {
    if (typeof DEGISIKLIKLER === 'undefined') return;
    const b = document.querySelector('script[src*="arayuz.js"]');
    const m = b && (b.getAttribute('src') || '').match(/[?&]s=v(\d+)/);
    const damga = m ? parseInt(m[1], 10) : null;
    if (!damga) return;

    // İlk ziyarette çıkmaz: yeni kullanıcı hiçbirini görmemiş.
    const onceki = gorulenSurumOku();
    if (!onceki) { gorulenSurumYaz(damga); return; }

    /* Damgaya EŞİT kayıt aramıyoruz — bilerek.
       Damga her yayında artıyor (bir yazım düzeltmesi bile artırıyor),
       kayıt ise yalnızca anlatılacak bir şey olunca yazılıyor. İkisi
       kaçınılmaz olarak ayrışır ve eşitlik arayan kod SESSİZCE hiç
       çıkmaz. Ölçüldü: damga v94, kayıt 93, şerit yok. Sayıları elle
       hizalamak çözüm değil; aynı tuzağı bir sonraki yayına erteler. */
    const yeniler = DEGISIKLIKLER.filter((d) => d.surum > onceki);
    gorulenSurumYaz(damga);
    if (!yeniler.length) return;
    const kayit = yeniler[0];

    const not = $('yenilikNotu');
    if (!not) return;
    $('yenilikBaslik').textContent = CS('Uygulama güncellendi',
                                        'The app was updated');
    // Kayit iki dilli; CS zaten aktif dile gore seciyor.
    let metin = CS(kayit.ozet, kayit.ozetEn || kayit.ozet);
    if (kayit.ayarGozdenGecir) {
      metin += CS(' Aile kipi kullanıyorsan ayarlarını bir kez daha gözden geçir.',
                  ' If you use Family mode, review your settings once more.');
    }
    $('yenilikMetin').textContent = metin;
    not.hidden = false;
    $('yenilikAyrinti')?.addEventListener('click', () => {
      not.hidden = true;
      gorulenSurumYaz(damga);
      sekmeSec('sekmeBilgiler');
      setTimeout(() => {
        document.getElementById('degisiklikListesi')
          ?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 400);
    });
    $('yenilikKapat')?.addEventListener('click', () => {
      not.hidden = true;
      gorulenSurumYaz(damga);
    });
  }

  /* AYRI ANAHTAR — bilerek, ayarların içinde değil.
     `kaydet()` ayar nesnesini alan alan YENİDEN KURUYOR; o listede
     olmayan her alan 15 saniyede bir siliniyor. Bu işaret oraya
     konduğunda ölçtüm: yazıldı, sonraki kayıtta kayboldu. Sonucu
     kullanıcı için şuydu — şeridi kapat, 15 saniye sonra işaret
     silinsin, bir dahaki açılışta şerit yine çıksın. Sonsuza kadar. */
  const GORULEN_ANAHTARI = 'goz-molasi-gorulen';
  function gorulenSurumOku() {
    try { return parseInt(localStorage.getItem(GORULEN_ANAHTARI), 10) || null; }
    catch { return null; }
  }
  function gorulenSurumYaz(s) {
    try { localStorage.setItem(GORULEN_ANAHTARI, String(s)); } catch { }
  }

  /* SERVİS İŞÇİSİ + "yeni sürüm hazır" bildirimi

     Sorun: servis işçisi yeni dosyaları indirip önbelleğe alıyor ama
     AÇIK OLAN sayfa eski sürümde çalışmaya devam ediyor. Kullanıcı
     düzelttiğimiz hatayı görmeye devam ediyor ve bunu bilmiyor.
     Geliştirme sırasında bizim de başımıza geldi: dosyayı ekledik,
     sunucuda vardı, sayfada yoktu.

     Sayfayı KENDİ KENDİNE yenilemiyoruz. Kullanıcı 19. dakikada
     olabilir; habersiz yenileme sayacı görünürde sıfırlar ve
     "uygulama bozuldu" izlenimi verir. Şeridi gösterip kararı
     kullanıcıya bırakıyoruz. */
  function guncellemeSeridiniGoster() {
    const serit = $('guncellemeSerit');
    if (!serit || serit.dataset.gosterildi) return;
    serit.dataset.gosterildi = '1';
    serit.hidden = false;
    // requestAnimationFrame DEGIL: sekme arka plandayken rAF
    // calismiyor ve serit gorunur ama ekranin disinda kaliyor.
    // Olctum: hidden kalkti, .acik sinifi hic eklenmedi.
    setTimeout(() => serit.classList.add('acik'), 20);
    $('guncelleYenile')?.addEventListener('click', () => {
      location.reload();
    });
    $('guncelleKapat')?.addEventListener('click', () => {
      serit.classList.remove('acik');
      setTimeout(() => { serit.hidden = true; }, 400);
    });
  }

  try { yenilikNotunuGoster(); } catch (e) { }

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    navigator.serviceWorker.register('sw.js').then((kayit) => {
      // Zaten bekleyen bir sürüm varsa (kullanıcı bu sekmeyi açık
      // bırakmışsa) hemen söyle
      if (kayit.waiting && navigator.serviceWorker.controller) {
        guncellemeSeridiniGoster();
      }
      kayit.addEventListener('updatefound', () => {
        const yeni = kayit.installing;
        if (!yeni) return;
        yeni.addEventListener('statechange', () => {
          // controller varsa bu bir GÜNCELLEME; yoksa ilk kurulum
          if (yeni.state === 'installed' && navigator.serviceWorker.controller) {
            guncellemeSeridiniGoster();
          }
        });
      });
    }).catch(() => {});
  }
})();
