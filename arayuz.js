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
    hemenMola: $('hemenMolaDugme'),

    molaEkran: $('molaEkran'),
    molaBaslik: $('molaBaslik'),
    molaAlt: $('molaAlt'),
    uzunMolaNotu: $('uzunMolaNotu'),
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
    sureUyari: $('sureUyari'),
    ayHava: $('ayHava'),
    havaDurum: $('havaDurum'),
    havaKonumSatir: $('havaKonumSatir'),
    konumBulDugme: $('konumBulDugme'),
    konumNotu: $('konumNotu'),
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
    ayAile: $('ayAile'),
    aySinir: $('aySinir'),
    aySinirDeger: $('aySinirDeger'),
    aileSinirSatir: $('aileSinirSatir'),
    ayYasak: $('ayYasak'),
    aileYasakSatir: $('aileYasakSatir'),
    aileYasakSaat: $('aileYasakSaat'),
    ayYasakBas: $('ayYasakBas'),
    ayYasakBit: $('ayYasakBit'),
    engelEkran: $('engelEkran'),
    engelBaslik: $('engelBaslik'),
    engelAciklama: $('engelAciklama'),
    engelEbeveyn: $('engelEbeveyn'),
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

  /* ESKİ KULLANICI MI? Bu soruyu BURADA sormak zorundayız: birkaç
     satır aşağıda kilit sıfırlama bloğu kayda yazıyor ve o andan
     sonra herkes "kaydı var" görünüyor. `kayit` ise diskten
     okunmuş HAM hâli. */
  const eskiKullanici = Object.keys(kayit).length > 0;

  const motor = new MolaMotoru();

  /* SIRA ÖNEMLİ: `iceAktar` geri yükleme kararını BURADA veriyor.
     Ayarı ondan sonra vermek, kararın eski ayarla alınması demek.
     Ölçüldü: ayar kapalıyken ekran 20:00'a döndü AMA not "sayaç
     sıfırlanmadı" dedi — motor iki kez çağrılınca iki bayrak birden
     kalmıştı ve kullanıcı ekranla çelişen bir cümle okuyordu. */
  let bostaAcik = kayit.bostaAcik !== false;
  /* VARSAYILAN CİHAZA GÖRE — ve bu bilerek böyle.

     "5 dakikadan uzun uzaklaşma dinlenmedir" varsayımı BİLGİSAYAR
     varsayımıdır: orada sekme açık kalır, uzaklaşmak gerçekten
     ekrandan kalkmaktır.

     TELEFONDA BU YANLIŞ. Başka uygulamaya geçmek normal kullanımdır
     ve kişi hâlâ ekrana bakıyordur. Kullanıcı 10 dakika mesajlaşıp
     dönüyor ve sayacı sıfırlanmış buluyordu — aynı şikâyeti iki kez
     bildirdi. Yani düzelttiğimiz şey telefonda hâlâ her seferinde
     oluyordu, çünkü varsayımı değil yalnızca eşiği düzeltmiştik.

     `pointer: coarse` dokunmatik cihazı gösterir. Ekran genişliği
     KULLANILMIYOR: dar bir masaüstü penceresi telefon değildir.
     Kullanıcı ayarı bir kez elle değiştirirse seçimi korunur. */
  const dokunmatik = window.matchMedia
    && window.matchMedia('(pointer: coarse)').matches;
  let uzakSifirlaGocu = kayit.uzakSifirlaGocu === true;
  let uzakSifirla = (kayit.uzakSifirla === undefined)
    ? !dokunmatik
    : kayit.uzakSifirla !== false;
  let uzakSifirlaSecildi = kayit.uzakSifirlaSecildi === true;

  /* GÖÇ — telefon varsayılanı ESKİ kullanıcıya ulaşmıyordu.

     Bu ayar v104'te HERKES için açık varsayılanıyla eklendi ve
     `kaydet()` onu hemen kullanıcının deposuna yazdı. v112'de
     varsayılanı cihaza bağladım, ama varsayılan yalnızca "kayıtta
     hiç yoksa" işler — deposunda `true` yazan kullanıcı yeni
     davranışın DIŞINDA kaldı.

     Ölçüldü: dokunmatik + depoda `true` → ekran 20:00, sayaç
     sıfırlanıyor. Kullanıcı bunu dört kez bildirdi; düzeltmelerim
     yalnızca temiz kurulumu kapsıyordu.

     Kullanıcının BİLİNÇLİ seçimini ezmiyoruz — ama hiç dokunmadığı
     eski bir varsayılanı "seçim" saymıyoruz. Göçten sonra bayrak
     konuyor; bir daha dokunulmuyor. */
  if (dokunmatik && uzakSifirla && !uzakSifirlaSecildi
      && kayit.uzakSifirlaGocu !== true) {
    uzakSifirla = false;
    uzakSifirlaGocu = true;
  }
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
     Şifre konunca ŞİFREYİ DEĞİŞTİRMEK, ŞİFREYİ KALDIRMAK ve
     VERİLERİ SİLMEK şifre ister. Başka bir şey istemez.

     DÜZELTME (28.08.2026): burada eskiden "molayı atlamak,
     duraklatmak, sıfırlamak ve ayarları değiştirmek şifre ister"
     yazıyordu. Ölçüldü — istemiyor: `sifreSor()` yalnızca üç yerden
     çağrılıyor. Kullanıcıya gösterilen yazı DOĞRUYDU ("şifreyi
     değiştirme ve verileri silme korumalı"); yanlış olan yalnızca
     buradaki açıklamaydı. Bir sonraki geliştiriciyi yanıltırdı —
     nitekim bir süre beni yanılttı.

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

  /** Bu damga CANLI mı?

      `an` GELECEKTE ise saat oynanmış demektir: kullanıcı saati geri
      aldı, yaz saati değişti ya da NTP düzeltmesi geldi. O kayıt
      güvenilmez.

      Ölçüldü (31.08.2026): saat bir saat geri alınınca ölü bir liderin
      damgası "canlı" görünüyordu ve HİÇBİR sekme devralmıyordu —
      sayaç tamamen duruyordu, ekranda hiçbir uyarı olmadan. Mola hiç
      gelmiyordu; uygulamanın tek işi bu.
        KONTROL  temiz sayfa        : 19:58 -> 19:51  işliyor
        BOZMA    damga ileri tarihli: 20:00 -> 20:00  DURMUŞ

      GÜVENLİ YÖN devralmaktır: fazladan devralma zararsız (tek sekmede
      zaten lider olunur), devralmamak uygulamayı tümüyle durdurur. */
  function damgaCanli(l) {
    const fark = Date.now() - l.an;
    return fark >= 0 && fark < LIDER_OLU;
  }

  /** Başka bir sekme şu an canlı lider mi? */
  function baskaLiderVar() {
    const l = liderOku();
    return !!(l && l.kimlik !== SEKME_KIMLIGI && damgaCanli(l));
  }

  function lideriDevral() {
    liderMiyim = true;
    try { motor.askidanCikar(); } catch {}
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
    /* Sayaç bu sekmede işlemesin; ölçüm çift sayılmasın.
       Yalnızca kalp atışını durdurmak YETMİYORDU: `_asamayaGec()`
       her durum geçişinde onu yeniden başlatıyor. Ölçüldü — ikinci
       sekme kendini ikinci sekme gösterip yine sayıyordu, üstelik
       liderden farklı bir sayı. Artık motor askıya alınıyor. */
    try { motor.askiyaAl(); } catch {}
  }

  /** İki saniyede bir: liderim damgala, değilsem devralınabilir mi bak. */
  function liderNobeti() {
    if (liderMiyim) {
      const l = liderOku();
      // Başka sekme devraldıysa sessizce geri çekil
      if (l && l.kimlik !== SEKME_KIMLIGI && damgaCanli(l)) {
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
    og.tanitimMetin.textContent = CS(
      'İşte böyle görünüyor. Gerçeğinde 20 saniye sürecek ve '
      + 'kapatılamayacak.',
      'That is how it looks. The real one lasts 20 seconds and cannot '
      + 'be dismissed.');
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
      const seriYazi = seri >= Gecmis.saklananGun ? `${seri}+` : `${seri}`;
      parcalar.push(CS(`${seriYazi} gündür üst üste`,
                       `${seriYazi} ${seri === 1 ? 'day' : 'days'} in a row`));
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
      og.etkinlikDurum.textContent = CS(
        'Bu tarayıcı cihaz etkinliğini paylaşmıyor (Chrome ve Edge '
        + 'destekliyor). Sayaç yalnızca bu sekmedeki hareketi görüyor.',
        'This browser does not share device activity (Chrome and Edge do). '
        + 'The timer only sees movement in this tab.');
      return;
    }
    if (acik) {
      og.etkinlikDugme.textContent = C('Kapat');
      og.etkinlikDurum.textContent = CS(
        'Açık — sekme arka plandayken de cihazda hareket olup olmadığı '
        + 'görülüyor. Sadece "etkin mi, ekran kilitli mi" bilgisi; ne '
        + 'yaptığın değil.',
        'On — activity on the device is seen even while this tab is in the '
        + 'background. Only "active or not, screen locked or not"; never '
        + 'what you are doing.');
    } else if (d === 'denied') {
      og.etkinlikDugme.textContent = C('İzin ver');
      /* NE KAYBETTİĞİNİ DE SÖYLE.

         Bildirim izninde bu ders zaten öğrenilmişti ("ne kaybediyorsun"
         + "geri nasıl alırsın"), ama KARDEŞ izinde uygulanmamıştı:
         burada yalnızca geri alma yolu yazıyordu. Kullanıcı neyi
         kaçırdığını bilmeden "izin vereyim mi" diye karar veremez. */
      og.etkinlikDurum.textContent = CS(
        'İzin reddedilmiş. Ne kaybediyorsun: sekme arka plandayken '
        + 'cihazda hareket olup olmadığı görülemiyor, başka pencerede '
        + 'çalışırken sayaç seni "boşta" sanıp durabilir. Geri vermek '
        + 'için: adres çubuğundaki kilit simgesinden açabilirsin.',
        'Permission was denied. What you lose: activity on the device '
        + 'cannot be seen while this tab is in the background, so while '
        + 'you work in another window the timer may think you are idle '
        + 'and pause. To allow it again: use the padlock icon in the '
        + 'address bar.');
    } else {
      og.etkinlikDugme.textContent = C('İzin ver');
      og.etkinlikDurum.textContent = CS(
        'Kapalı — sayaç yalnızca bu sekmedeki hareketi görüyor. '
        + 'Başka pencerede çalışırken "boşta" sanılabilir.',
        'Off — the timer only sees movement in this tab. While you work in '
        + 'another window it may think you are idle.');
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
    /* MESAJI BURADA ÇEVİRİYORUZ, ÇAĞIRANDA DEĞİL.

       Ölçüldü (28.08.2026): konum izni reddedilince İngilizce arayüzde
       Türkçe cümle çıkıyordu — "Konum izni verilmedi. Aşağıdan şehir
       arayabilirsin." Çünkü mesajlar çağıranlarda düz yazı olarak
       veriliyor ve buraya olduğu gibi yazılıyordu.

       Çeviriyi görüntüleyen işleve bağlamak, sınıfı da kapatıyor:
       çağıran kim olursa olsun metin sözlükten geçiyor ve eksik bir
       çeviri varsa `sinama_sozluk.py` onu kendiliğinden yakalıyor. */
    if (mesaj) { og.havaDurum.textContent = C(mesaj); return; }
    if (!og.ayHava.checked) {
      og.havaDurum.textContent = C('Kapalı — molalarda yalnızca göz bilgisi gösterilir');
    } else if (konum) {
      og.havaDurum.textContent = (konum.ad ? konum.ad + ' · ' : '') +
        C('her birkaç molada bir hava durumu gösterilir');
    } else {
      og.havaDurum.textContent = C('Açık — önce konum ver ya da şehir ara');
    }
  }

  og.ayHava.addEventListener('change', () => havaDurumunuGoster());

  /* Konumun nereye gittiğini BASMADAN ÖNCE yaz. Basıldıktan sonra
     söylemek, izni alındıktan sonra söylemek demek. */
  if (og.konumNotu) {
    og.konumNotu.textContent = CS(
      'Konumun hava durumu için open-meteo.com sunucusuna gönderilir. '
      + 'Yaklaşık konuma yuvarlanır (yaklaşık 100 metre); tam adresin '
      + 'gönderilmez. İstemezsen aşağıdan şehir arayabilirsin.',
      'Your location is sent to open-meteo.com to fetch the weather. '
      + 'It is rounded to about 100 metres; your exact position is not '
      + 'sent. If you prefer, search for a city below instead.');
  }

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
  /** Kurulu uygulamanin simgesine rozet koy/kaldir.

      Uygulama KAPALIYKEN "mola bekliyor" bilgisini gosterebilen tek
      yol bu. Bildirim kaydirilip gecilebilir, rozet ana ekranda durur.

      Desteklenmeyen tarayicida sessizce yok sayiliyor - `setAppBadge`
      yalnizca kurulu uygulamalarda ve bazi tarayicilarda var. Burada
      SESSIZ GECMEK dogru: rozet bir EK, kaybi bir sey bozmuyor. */
  function rozet(sayi) {
    try {
      if (sayi > 0) navigator.setAppBadge?.(sayi);
      else navigator.clearAppBadge?.();
    } catch {}
  }

  function bildirimGonder(baslik, metin) {
    rozet(1);
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
    /* DURUM BILDIRMEK YETMIYOR.
       Eskiden yalnizca "izin verilmedi" yaziyor ve dugmeyi
       kapatiyordu: cikmaz sokak. Kullanici NE KAYBETTIGINI ve
       GERI NASIL ALACAGINI bilmiyordu. Tarayici bir kez
       reddedildikten sonra tekrar sormamiza izin vermiyor, o yuzden
       yolu tarif etmek zorundayiz. */
    const not = $('bildirimSiniri');
    if (izin === 'granted') {
      og.bildirim.textContent = C('🔔 Bildirimler açık');
      og.bildirim.disabled = true;
      if (not) {
        not.textContent = CS(
          'Bildirimler açık. Yine de telefon kilitliyken ya da tarayıcı '
          + 'arka plandayken uyarı gelmeyebilir; bunun için verilerin bir '
          + 'sunucuya gitmesi gerekirdi, göndermiyoruz.',
          'Notifications are on. Even so, if your phone is locked or the '
          + 'browser is in the background the alert may not arrive — '
          + 'delivering it would mean sending your data to a server, and '
          + 'we do not.');
      }
    } else if (izin === 'denied') {
      og.bildirim.textContent = C('🔕 Bildirimlere izin verilmedi');
      og.bildirim.disabled = true;
      if (not) {
        // KISA TUTULUYOR: telefonda bu blok alti satir olup ana ekranin
        // en buyuk metni haline geliyordu - ustelik bir hata aciklamasi.
        // Uc bilgi de duruyor (ne kaybettin / sayac calisiyor / nasil
        // geri acilir), yalnizca tekrarlar atildi.
        not.textContent = CS(
          'İzin verilmedi: sekme önde değilken mola haberi gelmez. '
          + 'Sayaç çalışmaya devam eder, molan seni bekler. '
          + 'Geri açmak: adres çubuğundaki kilit simgesi → bu site '
          + 'için bildirim.',
          'Not allowed: you will not be told about a break while this '
          + 'tab is in the background. The timer keeps running and your '
          + 'break waits for you. To allow: padlock icon in the address '
          + 'bar → notifications for this site.');
      }
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
      /* GERİ DÜŞME YOLU, ASIL YOLDAN DAHA KIRILGAN OLMASIN.

         Eskiden burada `window.prompt` vardı. Pano izni yoksa ya da
         bağlam güvenli değilse oraya düşülüyordu — ama tarayıcılar
         `prompt`'u pek çok durumda ENGELLİYOR (sekme önde değilken,
         kullanıcı "bu sayfa bir daha pencere açmasın" dedikten sonra,
         gömülü bağlamlarda). Engellenince `prompt` hata atmaz, sessizce
         `null` döner: kullanıcı "Paylaş"a basar ve EKRANDA HİÇBİR ŞEY
         OLMAZ. Ne linki alır, ne neden alamadığını öğrenir.

         Kendi kutumuz tarayıcıya bağlı değil: link ekranda durur,
         kullanıcı seçip kopyalar. */
      linkiEkrandaGoster();
    }
  });

  /* Paylaşımın son çaresi: linki uygulamanın kendi notunda göster. */
  function linkiEkrandaGoster() {
    try {
      const not = $('durumNotu');
      if (!not) return;
      $('durumNotuBaslik').textContent = CS('Linki kopyala', 'Copy the link');
      const metin = $('durumNotuMetin');
      metin.textContent = PAYLASIM.url;
      metin.style.userSelect = 'all';
      not.hidden = false;
      // Bir dokunuşta seçili gelsin: kopyalamak tek adım kalsın.
      try {
        const aralik = document.createRange();
        aralik.selectNodeContents(metin);
        const secim = window.getSelection();
        secim.removeAllRanges();
        secim.addRange(aralik);
      } catch { }
      $('durumNotuKapat')?.addEventListener('click',
        () => { not.hidden = true; }, { once: true });
    } catch { }
  }

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

  /* "Şimdi değil" SONSUZA KADAR DEĞİL — 7 gün.

     Ölçüldü (30.08.2026): eskiden 'evet' yazılıyordu ve bir daha hiç
     silinmiyordu. Bir kez kapatan kullanıcı uygulamayı bir daha hiç
     kuramıyordu; Android'de düğme de gizli olduğu için başka yol da
     yoktu. Kullanıcının kendi sözü: "her ne olursa olsun telefonda
     indiri önersin".

     Eski 'evet' kaydı da süreye çevriliyor, yoksa bugüne kadar
     kapatmış olan herkes kalıcı olarak sessizde kalırdı. */
  const KAPATMA_SURESI = 7 * 24 * 3600 * 1000;

  function kurulumKapatildiMi() {
    try {
      const d = localStorage.getItem(KURULUM_KAPATILDI);
      if (!d) return false;
      if (d === 'evet') {                       // eski kayıt: süreye çevir
        localStorage.setItem(KURULUM_KAPATILDI, String(Date.now()));
        return true;
      }
      /* Fark negatif olamaz: damga gelecekteyse saat oynanmış demektir.
         Yoksa davet hak ettiğinden uzun susar. Aynı desen liderlik
         kaydında sayacı tümüyle durduruyordu (31.08.2026). */
      const fark = Date.now() - Number(d);
      return fark >= 0 && fark < KAPATMA_SURESI;
    } catch { return false; }
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
    if (kalici) {
      try { localStorage.setItem(KURULUM_KAPATILDI, String(Date.now())); } catch {}
    }
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
    // Tarayıcı kendi kurulum yolunu vermediyse tarifi biz veriyoruz.
    // Android'de adres çubuğunda ⊕ yok; oradaki tarif yanlış olurdu.
    $('kurulumAciklama').textContent = android
      ? C('Tarayıcı menüsünü aç (⋮), "Uygulamayı yükle" ya da "Ana ekrana ekle" de')
      : C('Adres çubuğunun sağındaki ⊕ / kurulum simgesine bas');
    $('kurulumAciklama').style.color = 'var(--vurgu)';
  });

  /* Android/Chrome/Edge: tarayıcı "bu kurulabilir" dediğinde */
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();               // kendi davetimizi gösteriyoruz
    kurulumOlayi = e;
    og.kur.classList.remove('gizli');
    seridiGoster(C('Uygulama olarak kur'),
                 C('Ana ekranına ekle, internetsiz de çalışsın'), C('Kur'));
  });

  window.addEventListener('appinstalled', () => {
    /* KURMAK "HAYIR" DEMEK DEĞİLDİR.

       Burada eskiden `seridiGizle(true)` vardı; o `true` diske
       "kullanıcı daveti kapattı" kaydı yazıyordu. Ama kullanıcı daveti
       kapatmamıştı — tam tersini yapmış, uygulamayı KURMUŞTU.

       Kullanıcı bildirdi (30.08.2026): "ben indirdiğim şeyi sildim,
       tekrar indiremedim". Zincir şuydu: kur → kayıt yazılır →
       uygulamayı sil → kayıt DURUR (localStorage silinmez) → davet bir
       daha çıkmaz. Eski sürümde bu kayıt kalıcıydı, yani geri dönüş
       yolu hiç yoktu.

       Artık: davet yalnızca BU OTURUM için gizleniyor ve varsa eski
       kayıt SİLİNİYOR — uygulamayı kuran biri daveti reddetmiş
       sayılamaz. Kaldırırsa davet kendiliğinden geri gelir. */
    og.kur.classList.add('gizli');
    kurulumOlayi = null;
    seridiGizle(false);
    try { localStorage.removeItem(KURULUM_KAPATILDI); } catch {}
  });

  og.kur.addEventListener('click', () => $('kurulumEvet').click());
  if (uygulamaKipi) {
    og.kur.classList.add('gizli');
    /* Uygulama kipinde açıldıysa kullanıcı onu KURMUŞ demektir; eski bir
       "şimdi değil" kaydı artık geçersiz. Silmezsek, uygulamayı kaldırıp
       tarayıcıya döndüğünde davet yine susardı. */
    try { localStorage.removeItem(KURULUM_KAPATILDI); } catch {}
  }

  /* iPhone'da beforeinstallprompt YOK — hiç tetiklenmez.
     Beklersek kullanıcı kurulabileceğini hiç öğrenemez. */
  if (iOS && !uygulamaKipi) {
    og.kur.textContent = C('⬇ Ana ekrana ekle');
    og.kur.classList.remove('gizli');
    seridiGoster(C('Ana ekrana ekle'),
                 C('Uygulama gibi açılsın, internetsiz de çalışsın'),
                 C('Nasıl?'));
  }

  /* ANDROID: `beforeinstallprompt` GELMEYEBİLİR.

     Kullanıcı bildirdi (30.08.2026): telefonda uygulama kurulu değil
     ama hiçbir kurulum teklifi çıkmıyor. Sebebi buydu — Android'in
     yedeği yoktu. iOS'un var (olay hiç gelmez, kod bunu biliyor),
     masaüstünün var (3 sn sonra yine göster), Android'in yoktu.
     Olay gelmiyorsa (Chrome dışı tarayıcı, uygulama içi tarayıcı,
     Chrome'un kendi koşulları) kullanıcı kurulabileceğini hiç
     öğrenemiyordu; `kurDugme` de HTML'de gizli başlayıp yalnız o
     olayın içinde açıldığı için başka yol da kalmıyordu. */
  if (android && !uygulamaKipi) {
    og.kur.classList.remove('gizli');          // düğme HER ZAMAN dursun
    setTimeout(() => {
      if (!kurulumOlayi && serit.classList.contains('gizli')) {
        seridiGoster(C('Uygulama olarak kur'),
                     C('Ana ekranına ekle, internetsiz de çalışsın'),
                     C('Nasıl?'));
      }
    }, 3000);
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

  /** Aile kipi engeli ekranda mı olmalı?

      Her çizimde soruluyor: sınır gün içinde dolabilir, yasak saat
      girebilir. Sayacı DURDURMUYORUZ — engel kalkınca kullanıcı
      kaldığı yerden devam etsin.

      Metin AYARDAN türüyor, sabit yazılmıyor: masaüstünde (30.08.2026)
      tam bu yüzden ekranda "2 saate yaklaşıyorsun" yazarken eşik 8
      saatti. */
  function engeliTazele() {
    const e = motor.engelDurumu();
    if (!e) { og.engelEkran.classList.add('gizli'); return; }
    let baslik, aciklama;
    if (e.sebep === 'sinir') {
      baslik = C('Bugünün ekran süresi doldu');
      aciklama = CS(
        `Bugün için ${motor.ayarlar.gunlukSinirDk} dakika ayarlanmış. `
        + 'Yarın sıfırlanır.',
        // "1 minutes" olmasin diye tekil/cogul kacinilmis bicim.
        `Today's limit is ${motor.ayarlar.gunlukSinirDk} min. `
        + 'It resets tomorrow.');
    } else if (e.sebep === 'yasak-bozuk') {
      // SESSİZ DÜŞME YOK: uydurma bir saat aralığı uygulamıyoruz ve
      // bunu gizlemiyoruz. Masaüstünde bu hata sessizdi ve yasak
      // penceresi 00:00'a kayıyordu.
      baslik = C('Yasak saat ayarı okunamıyor');
      aciklama = CS('Saat aralığı bozuk göründüğü için yasak uygulanmıyor. '
                    + 'Ayarlardan saatleri yeniden gir.',
                    'The time range looks broken, so the block is not '
                    + 'applied. Set the hours again in Settings.');
    } else {
      baslik = C('Şimdi bilgisayar zamanı değil');
      aciklama = CS(
        `Yasak saatler: ${motor.ayarlar.yasakBas} — ${motor.ayarlar.yasakBit}. `
        + `Kalan: ${saatYaz(e.kalanSn)}.`,
        `Blocked hours: ${motor.ayarlar.yasakBas} — ${motor.ayarlar.yasakBit}. `
        + `Left: ${saatYaz(e.kalanSn)}.`);
    }
    og.engelBaslik.textContent = baslik;
    og.engelAciklama.textContent = aciklama;
    og.engelEkran.classList.remove('gizli');
  }

  /* EBEVEYN ÇIKIŞI — bu OLMAZSA kullanıcı kendini kilitler.
     Sınırı kendi koyuyor, dolunca ayarlara giremiyor, geri alamıyor.
     Masaüstü sürümünde de aynı çıkış var. */
  og.engelEbeveyn.addEventListener('click', async () => {
    if (!(await sifreSor(C('Ek süre vermek için şifreni gir.')))) return;
    motor.ayarlar.ekSureBitis = Date.now() + 15 * 60 * 1000;
    motor.kaydet();
    engeliTazele();
  });

  function ekraniCiz(d) {
    engeliTazele();
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
        const ss = saatYaz(t);
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

    // Sayılar dilin yazımıyla: Türkçede 1000 -> "1.000".
    og.istMola.textContent = SAYI(d.istatistik.tamamlananMola);
    og.istAtlanan.textContent = SAYI(d.istatistik.atlananMola);
    og.istSure.textContent = SAYI(Math.floor(d.istatistik.ekranSuresi / 60))
                           + CS(' dk', ' min');
    // Etiket dürüst olsun: izin yoksa bu sayı cihazın değil, sekmenin süresi
    if (og.istSureEtiket) {
      // "takip edilen süre" yanıltıyordu: kullanıcı 4 saattir
      // bilgisayarda ama sekme 6 dakika önce açıldıysa 6 dk yazıyor
      // ve "saymamış" sanılıyor. Etiket ne ölçtüğünü açıkça söylüyor.
      og.istSureEtiket.textContent = C(etkinlikDedektoru
        ? 'cihaz başında süre' : 'bu sekmede geçen süre');
      /* DEĞİŞMEZ DENETİMİ (K-53) — ekranda canlı.

         Kullanıcının gördüğü: "3 tamamlanan mola · 9 dk". 20 dakikalık
         kipte üç mola en az ~60 dakika demek. İki sayı yan yana durup
         birbirini yalanlıyor.

         Ölçüldü, ikisi de KENDİ İÇİNDE doğru:
           • mola vadesi DUVAR SAATİNDEN gelir (`hedefZaman - simdi`),
             sekme kapalıyken de işler;
           • ekran süresi yalnız ÖN PLANDA işleyen tıklardan birikir
             (`ekranSuresi += 0.25`), sekme arka plandayken saymaz.

         Yan yana durdukları için yalan söylüyorlar. Etiket tek başına
         yetmedi — kullanıcı "bu sekmede geçen süre" yazısını GÖRÜP
         yine yanıldı. Bu yüzden fark büyüdüğünde sebebini açıkça
         yazıyoruz. Uyarı ipucunda (`title`) duramaz: telefonda hover
         yok, oradaki cümle kullanıcıya hiç ulaşmıyor. */
      if (og.sureUyari) {
        const molaSay = (d.istatistik.tamamlananMola || 0)
                      + (d.istatistik.atlananMola || 0);
        const beklenen = molaSay * (motor.ayarlar.calismaSuresi || 1200);
        const olculen = d.istatistik.ekranSuresi || 0;
        // Yarısından azını görmüşsek fark kullanıcıya çelişki gibi gelir.
        const celisik = molaSay >= 2 && olculen < beklenen * 0.5;
        og.sureUyari.hidden = !celisik;
        if (celisik) {
          og.sureUyari.textContent = CS(
            'Molalar saate göre geliyor, süre ise yalnız uygulama '
            + 'açıkken sayılıyor. Bu yüzden mola sayısı süreden fazla '
            + 'görünebilir — ikisi de doğru, aynı şeyi ölçmüyorlar.',
            'Breaks are timed by the clock, while the duration only '
            + 'counts while the app is open. That is why the break count '
            + 'can look larger than the time — both are correct, they '
            + 'measure different things.');
        }
      }
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
    /* Seri saklama penceresine dayandıysa gerçek değer daha büyük
       olabilir; "120" demek eksik bilgi vermek olurdu. */
    const sYazi = s >= Gecmis.saklananGun ? `${s}+` : `${s}`;
    og.seriRozet.textContent = s > 0
      ? CS(`🔥 ${sYazi} gün üst üste`,
           `🔥 ${sYazi} ${s === 1 ? 'day' : 'days'} in a row`) : '';
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
        // "1 breaks" olmasin: Turkcede sorun yok, Ingilizcede var.
        `${toplam} break${toplam === 1 ? '' : 's'} today`
        + ' · history is building up');
    } else {
      const ortalama = Math.round((toplam / 7) * 10) / 10;
      // Ondalık ayırıcı dile göre: Türkçe "6,7" · İngilizce "6.7"
      og.haftaOzet.textContent = CS(
        `${SAYI(toplam)} mola · günde ortalama ${SAYI(ortalama, 1)}`,
        `${SAYI(toplam)} breaks · ${SAYI(ortalama, 1)} per day on average`);
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

    /* UZUN MOLADA: ayağa kalkmaya DAVET.

       Bilerek iddiasız: eşik yok, kaynak adı yok, "gerekir" yok.
       Ölçüldü (29.08.2026) — NHS 30 dakikada bir kalkmayı öneriyor
       AMA aynı sayfada "sınır koyacak kadar kanıt yok" diyor; WHO
       hiç süre vermiyor. Sayıyı eşiğe çevirmek, AOA'da yaptığımız
       hatanın aynısı olurdu (v141). Kaynaklı cümle bilgi kartında.

       20 dakikalık molaya EKLENMEDİ: onun işi gözü dinlendirmek,
       ikinci amaç asıl işi zayıflatır. */
    try {
      const not = og.uzunMolaNotu;
      if (not) {
        const uzunMu = !!motor.uzunMoladaMi;
        not.textContent = uzunMu
          ? CS('Uzun moladasın — istersen ayağa kalk, biraz hareket et.',
               'This is a long break — if you like, stand up and move a little.')
          : '';
        not.hidden = !uzunMu;
      }
    } catch {}

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
          // C() SART: bu yol mola sirasinda saniyede birkac kez
          // yaziyor ve kullanicinin EN COK gordugu metin bu. Ustteki
          // statik yol (satir ~1624) zaten C()'den geciyordu; burasi
          // unutulmus ve Ingilizce arayuzde Turkce kaliyordu.
          : C(egzersiz.anlikYonerge(gecen));
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

  /* EKRAN OKUYUCUYA DUYUR.
     `#ekranOkuyucu` alanı vardı, `og.okuyucu` diye kayıtlıydı ve
     HİÇ YAZILMIYORDU — düzenek kurulmuş, bağlanmamış. Ekran okuyucu
     kullanan biri molanın başladığını hiç duymuyordu. Bu bir göz
     sağlığı uygulaması; az gören kullanıcı burada normalden fazla
     olabilir. */
  function okuyucuyaSoyle(metin) {
    if (!og.okuyucu) return;
    // Aynı metni üst üste yazmak duyurulmuyor; kısa bir boşluk şart.
    og.okuyucu.textContent = '';
    setTimeout(() => { og.okuyucu.textContent = metin; }, 60);
  }

  function molaEkraniAc() {
    molaAcik = true;
    molaCikisKorumasiKur();
    const sn = Math.round(motor.ayarlar.molaSuresi);
    okuyucuyaSoyle(CS(
      `Göz molası başladı. ${sn} saniye. Gözünü ekrandan ayır, ` +
      'yaklaşık 6 metre uzağa bak.',
      `Eye break started. ${sn} seconds. Look away from the screen, ` +
      'about 6 metres.'));
    og.molaEkran.classList.add('acik');
    // Mola ekrana geldi: rozetin isi bitti. Beklemeyi anlatan bir
    // isaret, bekleme bitince durmamali.
    rozet(0);
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
    /* ODAK, ÖGE GÖRÜNÜR OLDUKTAN SONRA.
       `.acik` sınıfı opacity/visibility geçişi başlatıyor; geçiş
       bitmeden `focus()` çağırmak SESSİZCE hiçbir şey yapmıyor —
       görünmez öge odak almaz. Ölçüldü: mola açıkken odak hâlâ
       BODY üzerindeydi, yani `aria-modal` bir pencere açılıyor ama
       ekran okuyucu kullanıcısı içine girmiyordu.

       Hem geçiş bitimini dinliyoruz hem de kısa bir yedek süre
       koyuyoruz: geçiş hiç çalışmazsa (hareket azaltma açıkken
       süre 0.001ms) `transitionend` gelmeyebilir. */
    const odakla = () => {
      if (!molaAcik) return;
      if (getComputedStyle(og.molaEkran).visibility === 'hidden') return;
      og.molaEkran.focus?.();
    };
    og.molaEkran.addEventListener('transitionend', odakla, { once: true });
    setTimeout(odakla, 80);
    setTimeout(odakla, 400);
  }

  function molaEkraniKapat() {
    molaCikisKorumasiniKaldir();
    if (molaAcik) {
      okuyucuyaSoyle(CS('Mola bitti. Sayaç yeniden başladı.',
                        'Break finished. The timer has restarted.'));
    }
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
    return CS('Atlamak için basılı tut', 'Press and hold to skip');
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
    /* NE OLACAĞINI SÖYLE. Eskiden "15 sn sonra göz molası" diyordu;
       ne olacağını bilmeyen biri için bu bir uyarı değil, bir etiket.
       Kullanıcının kendi cümlesi: "uyar sen, telefon kapanacak diye." */
    const molaSn = Math.round(motor.ayarlar.molaSuresi);
    og.balonMetin.textContent = CS(
      `${kalanSn} sn sonra ekran ${molaSn} saniye kararacak`,
      `The screen goes dark for ${molaSn} s in ${kalanSn} s`);
    og.balon.classList.add('acik');
    calSes(1100, 0.18);
    /* Bildirim metni SABİT TÜRKÇEYDİ — İngilizce kullanan biri
       Türkçe bildirim alıyordu. Ayrıca ne olacağını söylemiyordu. */
    bildirimGonder(
      CS('Ekran birazdan kararacak', 'The screen is about to go dark'),
      CS(`${Math.ceil(saniye)} saniye sonra ekran ${molaSn} saniye kararacak.`,
         `In ${Math.ceil(saniye)} s the screen goes dark for ${molaSn} s.`));
    // Uyarı anında da titret: telefonda 15 saniyelik bir balonu
    // kaçırmak kolay, cepteyken hiç görünmez.
    titret([40, 60, 40]);
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
  /* Balondaki "Şimdi molaya geç": kullanıcı beklemek yerine
     hemen halletmek isteyebilir. Sessizlik reddetme değil —
     hiçbir şey yapılmazsa mola normal başlar. */
  og.hemenMola?.addEventListener('click', () => {
    og.balon.classList.remove('acik');
    if (motor.durum === 'hazir') motor.basla();
    motor.molayaGec();
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
        C('Molalardaki egzersizler'), CIKAN_EGZERSIZLER.length,
        C('Mola ekranında sırayla çıkarlar. "Uzağa bak" asıl olan; '
          + 'diğerleri ekranın ezberlenip görünmez olmasını önlüyor.'),
        CIKAN_EGZERSIZLER.map((E) => bilgiOgesi(C(E.ad), C(E.yonerge), ''))));
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
    /* try ŞART. Bu işlev AÇILIŞTA, en üst düzeyde çağrılıyor; gizli
       sekmede ya da site verileri engelliyken `getItem` istisna atar
       ve o istisna bütün betiği düşürür — uygulama HİÇ açılmaz.
       En ağır başarısızlık bu: kullanıcı boş ekran görür.

       Hemen aşağıdaki `setItem` zaten sarılıydı; yazma korunmuş,
       okuma unutulmuştu. Aynı satırın iki yarısı farklı korunuyorsa
       bu bir gözden kaçmadır, tercih değil. */
    let d = NaN;
    try { d = parseInt(localStorage.getItem(CANLILIK_ANAHTAR) || '100', 10); }
    catch { return 100; }
    return Number.isFinite(d) ? Math.min(150, Math.max(60, d)) : 100;
  }

  function canlilikUygula(yuzde, kaydet = false) {
    document.documentElement.style.setProperty('--canlilik', (yuzde / 100).toFixed(2));
    if (kaydet) { try { localStorage.setItem(CANLILIK_ANAHTAR, String(yuzde)); } catch {} }
    if (og.canlilikDurum) {
      const ad = yuzde <= 75 ? CS('Sakin', 'Calm')
        : yuzde >= 130 ? CS('Canlı', 'Vivid') : CS('Dengeli', 'Balanced');
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
      ? `${Math.round(toplamSn / 60)} ` + CS('dakika', 'minutes')
      : `${toplamSn} ` + CS('saniye', 'seconds');

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
      /* Komsu iki dal `CS` kullaniyordu, bu dal kullanmiyordu. DOM
         karsilastirmasi bunu GOREMEDI cunku dal hic calismamisti:
         kosula bagli metin, ancak kosul saglanirsa olculur. */
      not = '<span class="uyari-notu">' + CS(
        'Sık mola: 2023 çalışması 10 dakikayı destekliyor, ama işini bölebilir.',
        'Frequent breaks: a 2023 study supports 10 minutes, but it may interrupt your work.')
        + '</span>';
    }

    /* CALISMA ANINDA URETILEN METIN SOZLUGE UGRAMAZ.
       `sayfayiCevir` sayfa yuklenirken bir kez geziyor; burasi sonradan
       yaziliyor. Sozluge eklemek yetmez, `CS` ile kurmak gerekir.
       Olculdu (test-dil.html): bu cumlenin bes parcasi Ingilizce kipte
       Turkce kaliyordu. */
    og.sureOzeti.innerHTML = CS(
      `8 saatlik bir günde <b>${molaSayisi} mola</b> · toplam <b>${toplam}</b> göz dinlenmesi`,
      `In an 8-hour day: <b>${molaSayisi} breaks</b> · <b>${toplam}</b> of eye rest in total`) + not;
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

  /* ---- AİLE KİPİ ---- */
  function aileyiTazele() {
    const acik = og.ayAile.checked;
    og.aileSinirSatir.classList.toggle('gizli', !acik);
    og.aileYasakSatir.classList.toggle('gizli', !acik);
    og.aileYasakSaat.classList.toggle('gizli', !acik || !og.ayYasak.checked);
    const dk = +og.aySinir.value || 0;
    og.aySinirDeger.textContent = dk ? saatYaz(dk * 60) : C('sınır yok');
  }
  og.aySinir.addEventListener('input', aileyiTazele);
  og.ayYasak.addEventListener('change', aileyiTazele);

  /* Şifre kapısı — iki yönlü.

     AÇARKEN şifre şart: şifresiz bir "aile kipi" çocuğun tek dokunuşla
     kapatabileceği bir şeydir, yani koruma değil süstür. Masaüstü sürümü
     de aynı kuralı uyguluyor.

     KAPATIRKEN de şifre şart: yoksa sınır dolduğunda çocuk ayarlara girip
     kipi kapatır ve sınır kalkar. */
  og.ayAile.addEventListener('change', async () => {
    if (og.ayAile.checked) {
      if (!kilitOzeti) {
        og.ayAile.checked = false;
        // Sessizce geri almiyoruz: kullanici anahtari acti, kapandigini
        // gormeli ve NEDEN kapandigini bilmeli.
        try {
          const not = $('durumNotu');
          if (not) {
            $('durumNotuBaslik').textContent = C('Aile kipi');
            $('durumNotuMetin').textContent =
              C('Aile kipi için önce bir şifre koy (Kilit bölümünden).');
            not.hidden = false;
            $('durumNotuKapat')?.addEventListener(
              'click', () => { not.hidden = true; });
          }
        } catch { }
      }
    } else if (motor.ayarlar.kip === 'aile') {
      if (!(await sifreSor(C('Aile kipini kapatmak için şifreni gir.')))) {
        og.ayAile.checked = true;
      }
    }
    aileyiTazele();
  });

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
    /* `C()` UNUTULMUSTU. Iki satir yukarida `title`/`aria-label` icin
       `C(t.ad)` yaziliyor ama gorunen etiket ham `s.ad` aliyordu: ekran
       okuyucu "White" derken ekranda "Beyaz" yaziyordu. Olculdu
       (test-dil.html): "Beyaz" sozlukte VARDI ama buraya ugramiyordu --
       sozluge eklemek yetmiyor, cagirmak da gerekiyor. */
    og.temaAdi.textContent = s ? C(s.ad)
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
    og.ayAile.checked = motor.ayarlar.kip === 'aile';
    og.aySinir.value = motor.ayarlar.gunlukSinirDk || 0;
    og.ayYasak.checked = !!motor.ayarlar.yasakAcik;
    og.ayYasakBas.value = motor.ayarlar.yasakBas || '21:00';
    og.ayYasakBit.value = motor.ayarlar.yasakBit || '07:00';
    aileyiTazele();
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
    /* UYARI ÇALIŞMADAN UZUN OLAMAZ — ama SIFIRLAMAK yanlış cevaptı.

       Ölçüldü (28.08.2026): çalışma 1 dakikaya, uyarı en yükseğe (60 sn)
       çekilince `60 >= 60` tutuyor ve uyarı **0** oluyordu. Kullanıcı
       "60 saniye önceden uyar" diyor, hiç uyarı almıyordu. Kaydırıcı o an
       hâlâ 60 gösteriyordu; ekranla depo birbirini yalanlıyordu.

       Kullanıcının istediği şey aslında "beni hemen uyar". Bunun doğru
       karşılığı sıfır değil, çalışma süresinin hemen altı. Sıfır yalnızca
       kullanıcı BİLEREK sıfır seçtiğinde ya da Toplantı/Film kipinde
       kalır — orada sıfır "uyarma" demektir ve doğrudur. */
    if (uy >= dk * 60) uy = Math.max(0, dk * 60 - 5);

    motor.ayarlar.calismaSuresi = dk * 60;
    motor.ayarlar.molaSuresi = ml;
    motor.ayarlar.uyariSuresi = uy;
    motor.ayarlar.molaAtlanabilir = og.ayAtla.checked;
    motor.ayarlar.sesAcik = og.aySes.checked;
    bostaAcik = og.ayBosta.checked;
    if (og.ayUzakSifirla.checked !== uzakSifirla) {
      // Kullanıcı bu ayara BİLEREK dokundu; bir daha ezmeyiz.
      uzakSifirlaSecildi = true;
    }
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
    motor.ayarlar.kip = og.ayAile.checked ? 'aile' : 'bireysel';
    motor.ayarlar.gunlukSinirDk = Math.max(0, +og.aySinir.value || 0);
    motor.ayarlar.yasakAcik = og.ayYasak.checked;
    motor.ayarlar.yasakBas = og.ayYasakBas.value || '21:00';
    motor.ayarlar.yasakBit = og.ayYasakBit.value || '07:00';
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
    /* TEK ANAHTAR DEĞİL, BÜTÜN VERİ.

       Eskiden yalnızca `KAYIT_ANAHTARI` siliniyordu. Ama kullanıcıya
       "Ayarlar, sayaçlar ve şifre silinir" diyoruz ve SAYAÇLAR ayrı
       bir anahtarta duruyor (`goz-molasi-gecmis` — 7 gün grafiği ve
       seri). Ölçüldü (28.08.2026): silme sonrası sayaç 0 gösteriyor
       ama ekranda hâlâ "8 mola bugün" yazıyor, grafikte çubuk duruyor
       ve seri rozeti "1 gün üst üste" diyor. Kullanıcı her şeyi
       sildiğini sanıyor; kullanım geçmişi cihazda kalıyor.

       Anahtarları TEK TEK saymıyoruz: bugün öğrendiğimiz gibi ad
       listesi, kendisinden sonra doğan anahtarı göremez. Önekle
       silmek kural yazmaktır — sonradan eklenen her `goz-molasi*`
       anahtarı kendiliğinden kapsanır. */
    try {
      const silinecek = [];
      for (let i = 0; i < localStorage.length; i++) {
        const a = localStorage.key(i);
        if (a && a.indexOf('goz-molasi') === 0) silinecek.push(a);
      }
      // Her anahtar AYRI korunuyor: biri istisna atarsa (gizli
      // sekme, kota) kalanlar yine silinsin. Yarim silme, hic
      // silmemekten iyidir.
      silinecek.forEach((a) => { try { localStorage.removeItem(a); } catch {} });
    } catch {}
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
      // NOT: `gunuIsle` kendi içinde de MAX alıyor; buradaki çağrı
      // motorun anlık değerini veriyor, orası küçüğü yazmaz.
      Gecmis.gunuIsle(motor.istatistik.gun || Gecmis.gunAdi(), motor.istatistik);
    } catch {}
    /* ESKİ SEKME YENİ SAYIYI EZMESİN.

       Ölçüldü: B sekmesinde 9 mola birikti; hâlâ 3'te olan eski A
       sekmesi kapanınca `pagehide` → `kaydet()` → kayıt 3'e döndü.
       Kapanan sekme, en son gördüğü dünyayı yazıyor.

       Çözüm: yazmadan ÖNCE depoyu yeniden oku ve yalnızca ARTAN
       sayaçlar için büyüğü al. `kesintisizSure` buna dahil DEĞİL —
       o gerçekten sıfırlanabilen bir değer, MAX almak onu asla
       sıfırlanmaz yapardı.

       GÜN DENETİMİ ŞART: farklı bir güne aitse birleştirme yok,
       yoksa dünün 9 molası bugünü 9'da tutardı. */
    const gonderilecek = { ...motor.disaAktar() };
    try {
      const depodaki = JSON.parse(localStorage.getItem(KAYIT_ANAHTARI) || '{}');
      const e = depodaki.istatistik;
      const y = gonderilecek.istatistik;
      if (e && y && e.gun && e.gun === y.gun) {
        const buyuk = (a, b) => Math.max(a | 0, b | 0);
        gonderilecek.istatistik = {
          ...y,
          tamamlananMola: buyuk(e.tamamlananMola, y.tamamlananMola),
          atlananMola: buyuk(e.atlananMola, y.atlananMola),
          ekranSuresi: buyuk(e.ekranSuresi, y.ekranSuresi),
          uzunMola: buyuk(e.uzunMola, y.uzunMola),
        };
      }
    } catch { }

    try {
      localStorage.setItem(KAYIT_ANAHTARI, JSON.stringify({
        ...gonderilecek,
        bostaAcik,
        uzakSifirla,
        uzakSifirlaSecildi,
        uzakSifirlaGocu,
        molaKilit,
        otomatikBasla,
        titresimAcik,
        arkaPlanAcik,
        tema,
        kilitOzeti,
        kilitTuz,
        kilitSifirlandi: KILIT_SIFIRLAMA_DAMGASI,
        // `disaAktar()` zaten `saatFarki` veriyor; burada tekrar
        // yazmıyoruz ama listeden DÜŞMESİN diye not: yayılan
        // nesne onu taşıyor.
        kayitAni: Date.now(),
      }));
      kayitHatasi = 0;
    } catch {
      /* KAYIT SESSİZCE BAŞARISIZ OLMASIN.

         Ölçüldü: depo kotası dolduğunda uygulama çalışmaya devam
         ediyor ama kullanıcıya hiçbir şey söylenmiyor. Molaları,
         serisi ve ayarları kaydedilmiyor; bir dahaki açılışta hepsi
         gitmiş oluyor ve sebebini bilmiyor.

         Tek seferlik hata için uyarmıyoruz — geçici bir kilit
         olabilir ve her seferinde uyarmak uyarıyı değersizleştirir.
         Üst üste üç başarısızlık gerçek bir sorundur. */
      kayitHatasi++;
      if (kayitHatasi === 3) kayitUyarisiniGoster();
    }
  }

  let kayitHatasi = 0;
  let kayitUyarisiVerildi = false;

  function kayitUyarisiniGoster() {
    if (kayitUyarisiVerildi) return;
    kayitUyarisiVerildi = true;
    try {
      const not = $('durumNotu');
      if (!not) return;
      $('durumNotuBaslik').textContent = CS('Kayıt yapılamıyor', 'Cannot save');
      $('durumNotuMetin').textContent = CS(
        'Cihazın depolama alanı dolu olabilir ya da tarayıcı site '
        + 'verilerini engelliyor. Sayaç çalışmaya devam eder, ama bugünün '
        + 'molaları, serin ve ayarların KAYDEDİLMİYOR — uygulamayı '
        + 'kapatırsan kaybolurlar. Tarayıcı ayarlarından yer açabilir ya da '
        + 'bu siteye veri saklama izni verebilirsin.',
        'Your device storage may be full, or the browser is blocking site '
        + 'data. The timer keeps running, but today\u2019s breaks, your '
        + 'streak and your settings are NOT being saved \u2014 they will be '
        + 'lost if you close the app. You can free up space or allow site '
        + 'data for this site in your browser settings.');
      not.hidden = false;
      $('durumNotuKapat')?.addEventListener('click', () => { not.hidden = true; });
    } catch { }
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
    if (e.key !== KAYIT_ANAHTARI) return;

    /* BASKA SEKME "HEPSINI SIL" DEDIYSE BIZ DE DURALIM.

       Olculdu (29.08.2026): iki sekme acikken birinde "hepsini sil"
       denince veri gercekten siliniyor, ama OTEKI SEKME bunu hic
       duymuyordu ve 15 saniyelik kaydinda kendi bellegindeki eski
       durumu GERI YAZIYORDU. Kullanicinin sayaclari ve butun ayarlari
       diriliyordu; silme, ikinci sekme yuzunden tutmuyordu.

       Eskiden bu satir `|| !e.newValue` ile silinmeyi YOK SAYIYORDU -
       yani tam da haber verilmesi gereken olayi eliyordu.

       `KAYIT_ANAHTARI` normal islerde silinmez; yalnizca "hepsini sil"
       siler. O yuzden silinmeyi "veri supuruldu" isareti saymak
       guvenli. `silindi` bayragi `kaydet()`i durduruyor, sonra sayfa
       yenilenip temiz basliyor - silen sekmenin yaptiginin aynisi. */
    if (!e.newValue) {
      silindi = true;
      try { motor._kalpAtisiDurdur(); } catch {}
      location.reload();
      return;
    }

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
      if (veri.sayiyor !== true) return;

      /* İKİNCİ KAPI (29.08.2026 ölçümü).
         Aile kipi engel ekranı açıkken Windows sürümü
         `sayiyor:true, kalan_sn:0` yolluyordu; üstteki denetim
         yalnız `=== false` baktığı için geçiyor ve hayalet mola
         geri geliyordu (ölçüldü: IdleDetector izni açıkken
         30 dakikada 71 sahte mola). Windows tarafı düzeltildi —
         burada iki kapı daha:
           • `!== true`: alan eksik ya da bozuk gelirse DEVRALMA.
             Eski bir Windows sürümünde alan hiç yoktu ve
             `undefined === false` YANLIŞ, yani geçiyordu.
           • `donmus`: sayaç donmuşsa gelen sayı ekranda yazan
             sayı değildir; ona bakarak mola kararı verilmez. */
      if (veri.donmus === true) return;

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
      /* BIR DAKIKANIN ALTINDA SURE SOYLEMIYORUZ.

         Olculdu (29.08.2026): `Math.max(1, ...)` tabani yuzunden
         4 SANIYELIK bir kesinti "1 dakika ayrilmissin" diye
         yaziliyordu. Sayfayi yenileyen kullanici hic ayrilmiyor;
         ona sure soylemek uydurma olur.

         Yanindaki "saat-degisti" dali da ayni gerekceyle sure
         soylemiyor: ne oldugunu biliyoruz, ne kadar surdugunu
         bilmiyoruz. */
      const d = sebep.dakika | 0;
      /* ESKİ METİN YALANDI. "O molayı verilmiş saydık" yazıyordu.

         Ölçüldü: `tamamlananMola` yalnızca TEK yerde artıyor
         (cekirdek.js, `tik()` içinde, mola ekranı ekranda süresini
         doldurunca). Bu yol oraya hiç uğramıyor — sebebi yazıp
         `return false` yapıyor. Yani mola SAYILMIYORDU; cümle
         sayıldığını söylüyordu.

         Kullanıcı sayılara zaten güvenmiyordu; sayı hakkında yanlış
         cümle kurmak, yanlış sayı kadar zararlı. */
      metin = (d >= 1)
        ? CS(
          `Mola ekranı açıkken ${d} dakika ayrılmışsın. Sayaç yeniden `
          + `başladı — o mola sayılmadı, çünkü ekranda geçmedi.`,
          `You left for ${d} minutes while the break screen was open. The `
          + `timer restarted — that break was not counted, because it did `
          + `not run on screen.`)
        : CS(
          'Mola ekranı kapandı. Sayaç yeniden başladı — o mola '
          + 'sayılmadı, çünkü ekranda geçmedi.',
          'The break screen closed. The timer restarted — that break was '
          + 'not counted, because it did not run on screen.');
    } else if (sebep && sebep.tur === 'saat-degisti') {
      /* "Kapalıydın" DEMİYORUZ: kullanıcı hiç ayrılmamış olabilir.
         Ölçüldü: saat 1 saat ileri alınınca uygulama "60 dakika
         kapalıydı" diyordu. Ne olduğunu bilmediğimizde, bilmediğimizi
         söylemek uydurmaktan iyidir. */
      metin = CS(
        'Cihazın saati değişmiş görünüyor (yaz saati ya da elle ayar). '
        + 'Geçen süreyi güvenilir ölçemediğimiz için sayaç yeniden '
        + 'başladı — kapalı kaldığın için değil.',
        'Your device clock appears to have changed (daylight saving or a '
        + 'manual adjustment). We cannot measure the elapsed time '
        + 'reliably, so the timer restarted — not because you were away.');
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
    let onceki = gorulenSurumOku();

    /* İŞARETİ YOK AMA YENİ DEĞİL.
       Ölçüldü: v90'dan gelen bir kullanıcı — 42 molalık geçmişi,
       teması, ayarları duruyor — işaret anahtarı bulunmadığı için
       "ilk ziyaret" sayılıyordu ve "neler değişti" şeridini HİÇ
       görmüyordu. Yani K-44, en çok gerektiği anda (geçişte) tam
       hedef kitlesini ıskalıyordu.

       Daha kötüsü: bugün eklenen "molada kazayla çıkmayı önle"
       ayarı onda AÇIK başlıyor. Yani davranışı değişiyor ve haberi
       olmuyor — sessiz değişikliğin ta kendisi.

       Kaydı olan ama işareti olmayan kişi ESKİ kullanıcıdır. */
    if (!onceki && eskiKullanici) onceki = 1;

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

  /* KLAVYE AÇILINCA PENCERE EKRAN DIŞINDA KALMASIN.

     `dvh` tarayıcı çubuklarını hesaba katar ama EKRAN KLAVYESİNİ
     KATMAZ. Telefonda şifre alanına dokununca pencere klavyenin
     altında kalabilir — ve buradaki pencere aile kipinin şifresini
     soruyor: ebeveyn kendi kilidini açamazsa özellik işe yaramaz.

     `visualViewport` gerçekten görünen alanı verir. Yoksa hiçbir şey
     değişmiyor, CSS `88dvh`e düşüyor.

     DÜRÜSTLÜK NOTU: bu ortamda ekran klavyesi üretilemedi, yani
     düzeltmenin İŞE YARADIĞI ölçülmedi — yalnızca bir şeyi
     bozmadığı ölçüldü. Telefonda bakılmalı. */
  if (window.visualViewport) {
    const gorunuruOlc = () => {
      document.documentElement.style.setProperty(
        '--gorunur-yukseklik', (visualViewport.height * 0.88) + 'px');
    };
    visualViewport.addEventListener('resize', gorunuruOlc);
    visualViewport.addEventListener('scroll', gorunuruOlc);
    /* `window.resize` de dinleniyor: ölçüldü ki bazı ortamlarda
       görünen alan değişirken `visualViewport.resize` hiç
       gelmiyor ve değişken bayat kalıyor. */
    window.addEventListener('resize', gorunuruOlc);
    window.addEventListener('orientationchange', gorunuruOlc);
    gorunuruOlc();
  }

  // Odaklanan alanı görünür alanın ortasına al.
  document.addEventListener('focusin', (e) => {
    const alan = e.target;
    if (!alan.closest || !alan.closest('dialog[open]')) return;
    setTimeout(() => {
      try { alan.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
      catch { }
    }, 150);
  });

  /* Sürüm numarası YÜKLÜ DAMGADAN okunuyor — ayrı bir sabit
     tutmak ikinci bir elle yazılan sayı olurdu ve bugün tam bu
     yüzden üç projede bildirim sessizce hiç çıkmamıştı. */
  try {
    const b = document.querySelector('script[src*="arayuz.js"]');
    const m = b && (b.getAttribute('src') || '').match(/[?&]s=v(\d+)/);
    const e = $('surumSatiri');
    if (e && m) e.textContent = CS('Sürüm ' + m[1], 'Version ' + m[1]);
  } catch (e) { }

  try { yenilikNotunuGoster(); } catch (e) { }

  if ('serviceWorker' in navigator && location.protocol !== 'file:') {
    /* GUNCELLEME DENETIMI — bunsuz kurulu uygulama ESKI kalir.

       Kullanici bildirdi (31.08.2026): telefondaki kurulu uygulama
       hicbir guncelleme almamis, logo bile eski. Olculdu: serit ve
       `skipWaiting` dogru calisiyordu, ama `update()` HIC
       cagrilmiyordu. Tarayici kurulu bir PWA'da sw.js'i kendiliginden
       cok seyrek denetler; sormazsak kullanici suresiz eski surumde
       kalir. Yayin dogru, teslimat yoktu. */
    const DENETIM_ARASI = 15 * 60 * 1000;
    let sonDenetim = 0;
    const denetle = (kayit) => {
      const simdi = Date.now();
      // Fark negatif olamaz: saat geri alinirsa bir daha hic
      // denetlemezdik (bu gece ayni desenden uc kusur cikti).
      if (sonDenetim && simdi - sonDenetim >= 0 &&
          simdi - sonDenetim < DENETIM_ARASI) return;
      sonDenetim = simdi;
      try { kayit.update(); } catch {}
    };

    navigator.serviceWorker.register('sw.js').then((kayit) => {
      denetle(kayit);
      document.addEventListener('visibilitychange', () => {
        if (!document.hidden) denetle(kayit);
      });
      /* Yeni denetleyici devraldiysa haber ver. OTOMATIK YENILEMIYORUZ:
         bu bir sayac uygulamasi, mola sirasinda kendiliginden yenilemek
         molayi keser. Karar kullanicinin; serit "Yenile" sunuyor.

         `denetleyiciVardi` SART: `controllerchange` ILK KURULUMDA da
         tetikleniyor (`clients.claim` sayfayi ilk kez sahipleniyor).
         Korumasiz birakinca uygulamayi yeni kuran kullaniciya "yeni
         surum hazir" diyordu - olctum, kendi duzeltmemin urettigi yeni
         bir hataydi. Ustteki `updatefound` dali ayni korumayi
         `navigator.serviceWorker.controller` ile zaten yapiyor. */
      const denetleyiciVardi = !!navigator.serviceWorker.controller;
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (denetleyiciVardi) guncellemeSeridiniGoster();
      });
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
