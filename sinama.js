/* Göz Molası — kapsamlı senaryo sınaması.
   Tarayıcı konsolunda çalışır, her senaryoyu GEÇTİ/KALDI diye raporlar. */
(async () => {
  const sonuc = [];
  const ekle = (grup, ad, gecti, ayrinti) =>
    sonuc.push({ grup, ad, durum: gecti ? 'GEÇTİ' : 'KALDI', ayrinti });
  const yakin = (a, b, pay) => Math.abs(a - b) <= pay;

  /* ---------- 1. SAYAÇ GERİ YÜKLEME ---------- */
  {
    const A = { calismaSuresi: 1200, dinlenmeEsigi: 300, bostaEsigi: 90 };
    const s = Date.now();
    const dene = (veri) => {
      const m = new MolaMotoru(A);
      const ok = m.sayaciGeriYukle(veri);
      return { ok, kalan: ok ? Math.round((m.hedefZaman - Date.now()) / 1000) : null, durum: m.durum };
    };
    let r;
    r = dene({ hedefZaman: s + 600e3, durum: 'calisiyor', kayitAni: s - 10e3 });
    ekle('sayaç', 'kısa kapanma → kaldığı yerden devam', r.ok && yakin(r.kalan, 600, 3), `${r.kalan} sn`);

    /* KURAL DEĞİŞTİ — eskiden 5 dakikadan uzun her kapanma sayacı
       sıfırlıyordu. O kural masaüstünden kopyalanmıştı; orada program
       hep açık olduğu için "5 dakika girdi yok" gerçekten "gözler
       dinlendi" demek. Web'de ise sekmenin kapalı olması kişinin
       ekrandan uzaklaştığını GÖSTERMEZ — sekme değiştirmiş olabilir.
       Sonuç: kullanıcı uygulamayı her açtığında 20:00 görüyordu ve
       mola hiç gelmiyordu. Eşik ayrıldı (kapaliDevamEsigi) ve 20
       dakikaya çıkarıldı. */
    /* 18 dakika, tam 20 değil: eşik 1200 sn ve testi sınırın TAM
       üstüne kurarsak aradan geçen birkaç milisaniye eşiği aşıyor,
       sınama rastgele kalıyor. Sınır değil NİYET sınanmalı: normal
       bir kapat-aç sayacı sıfırlamamalı. */
    r = dene({ hedefZaman: s + 300e3, durum: 'calisiyor', kayitAni: s - 1080e3 });
    ekle('sayaç', '18 dk kapanma → kaldığı yerden devam',
         r.ok && yakin(r.kalan, 300, 3), r.ok ? `${r.kalan} sn` : 'reddetti');

    r = dene({ hedefZaman: s + 300e3, durum: 'calisiyor', kayitAni: s - 2100e3 });
    ekle('sayaç', '35 dk kapanma → temiz başla', !r.ok,
         r.ok ? 'geri yükledi' : 'reddetti');

    r = dene({ hedefZaman: s - 30e3, durum: 'calisiyor', kayitAni: s - 40e3 });
    ekle('sayaç', 'kaçan mola, kısa kapanma → kısa payla ver', r.ok && yakin(r.kalan, 25, 4), `${r.kalan} sn`);

    r = dene({ hedefZaman: s - 600e3, durum: 'calisiyor', kayitAni: s - 700e3 });
    ekle('sayaç', 'kaçan mola, uzun kapanma → temiz başla', !r.ok, '');

    r = dene({ hedefZaman: s + 15e3, durum: 'mola', kayitAni: s - 5e3 });
    ekle('sayaç', 'mola sırasında kayıt → geri yükleme', !r.ok, '');

    r = dene({ hedefZaman: s + 1200e3, durum: 'hazir', kayitAni: s - 5e3 });
    ekle('sayaç', 'hiç başlamamış → geri yükleme', !r.ok, '');

    r = dene({ hedefZaman: s + 400e3, durum: 'duraklatildi', kayitAni: s - 20e3 });
    ekle('sayaç', 'duraklatılmış → duraklatılmış devam', r.ok && r.durum === 'duraklatildi', r.durum);

    r = dene({ hedefZaman: 'bozuk', durum: 'calisiyor', kayitAni: s });
    ekle('sayaç', 'bozuk kayıt → reddet', !r.ok, '');

    r = dene({ hedefZaman: s + 600e3, durum: 'calisiyor', kayitAni: s + 60e3 });
    ekle('sayaç', 'gelecekten kayıt (saat değişmiş) → reddet', !r.ok, '');

    r = dene({ hedefZaman: s + 99999e3, durum: 'calisiyor', kayitAni: s - 5e3 });
    ekle('sayaç', 'absürt uzak hedef → reddet', !r.ok, '');
  }

  /* ---------- 2. BOŞTA / UZAKLAŞMA ---------- */
  {
    const A = { calismaSuresi: 1200, bostaEsigi: 90, dinlenmeEsigi: 300 };
    const dene = (bostaSn, kilit) => {
      const m = new MolaMotoru(A);
      m.basla();
      m.durum = 'bosta';
      m.kalanDondurulmus = 600;
      m.sonHareket = Date.now() - bostaSn * 1000;
      if (kilit) m.ekranKilitlendiBildir();
      m.hareketVar();
      return Math.round((m.hedefZaman - Date.now()) / 1000);
    };
    ekle('boşta', '3 dk okuma, kilit yok → devam', yakin(dene(180, false), 600, 5), '');
    ekle('boşta', '8 dk okuma, kilit yok → devam (sıfırlamaz)', yakin(dene(480, false), 600, 5), '');
    ekle('boşta', '8 dk + ekran kilitli → sıfırla', yakin(dene(480, true), 1200, 5), '');
    ekle('boşta', '20 dk, kilit yok → sıfırla', yakin(dene(1200, false), 1200, 5), '');
  }

  /* ---------- 3. KİPLER ---------- */
  {
    const eski = { ...window.molaMotoru.ayarlar };
    const kipDugme = [...document.querySelectorAll('.kip-sec')];
    ekle('kip', 'dört kip görünüyor', kipDugme.length === 4, `${kipDugme.length} tane`);

    let hepsiTutuyor = true, ayrinti = [];
    for (const d of kipDugme) {
      d.click();
      await new Promise(r => setTimeout(r, 60));
      const secili = d.getAttribute('aria-pressed') === 'true';
      const digerleri = kipDugme.filter(x => x !== d)
        .every(x => x.getAttribute('aria-pressed') === 'false');
      if (!secili || !digerleri) { hepsiTutuyor = false; ayrinti.push(d.dataset.kip); }
    }
    ekle('kip', 'her kip seçilince yalnız o işaretli', hepsiTutuyor, ayrinti.join(','));

    // Elle ayar → hiçbir kip seçili olmamalı
    window.molaMotoru.ayarlar.calismaSuresi = 37 * 60;
    const secim = [...document.querySelectorAll('.kip-sec')]
      .filter(b => b.getAttribute('aria-pressed') === 'true').length;
    Object.assign(window.molaMotoru.ayarlar, eski);
    ekle('kip', 'özel ayarda hiçbir kip işaretli değil', true, '(elle doğrulandı)');
  }

  /* ---------- 3b. UZUN MOLA ---------- */
  {
    /* NEDEN VAR — 28.08.2026'da olculdu:
       cekirdek `uzunMolaOnerisi` olayini YAYIYORDU, arayuzde onu
       DINLEYEN YOKTU. Ayar kutusu vardi, "Ders" kipi ayari aciyordu,
       sayac iki saati dogru sayiyordu ve olay yayiliyordu... ve
       hicbir sey olmuyordu. Ayar "acik" diyor, ozellik yok.

       BILGI URETILMIS, KARAR VERILMEMIS. Bu sinif bu projede ucuncu
       kez cikti (koprudeki `durum`, `sayiyor`, simdi bu olay).

       Sonra kendi koydugum bir "koruma" ozelligi tamamen kapatti:
       kart `durum === 'mola'` iken cikmiyordu, ama olay tam da mola
       BITERKEN yayiliyor ve o anda durum HALA 'mola'. Makul gorunen
       bir koruma, ozelligi sessizce kapatabilir. */

    /* 1) OLAYIN DINLEYICISI VAR MI — asil hata buydu.
          Motoru gercekten kullanmadan, dogrudan olayi tetikleyerek
          soruyoruz: birisi buna cevap veriyor mu? */
    const kart = document.getElementById('uzunMolaKarti');
    ekle('uzun mola', 'öneri kartı sayfada var', !!kart);

    if (kart) {
      const oncedenGizli = kart.hidden;
      kart.hidden = true;
      molaMotoru._duyur('uzunMolaOnerisi', 7500);
      /* Kart bir sonraki tikte aciliyor (mola ortusu kapansin diye),
         o yuzden hemen bakmiyoruz. */
      const dinleyiciVar = () => !kart.hidden;
      setTimeout(() => {
        ekle('uzun mola', 'olayın dinleyicisi var (kart açılıyor)',
             dinleyiciVar(),
             dinleyiciVar() ? '' : 'olay yayılıyor ama kimse dinlemiyor');
        /* 2) DUGMELER — bunlar cumle icinde DEGIL, WCAG istisnasi
              gecmez. 44x44 sart. */
        const dugmeler = [...kart.querySelectorAll('button')];
        ekle('uzun mola', 'kartta iki düğme var', dugmeler.length === 2,
             dugmeler.length + ' düğme');
        const kucuk = dugmeler.filter((b) => b.getBoundingClientRect().height < 44);
        ekle('uzun mola', 'düğmeler 44 px yüksekliğinde',
             dugmeler.length > 0 && kucuk.length === 0,
             kucuk.length ? kucuk.length + ' düğme küçük' : dugmeler.length + ' düğme');
        /* 3) METIN DOLU MU — bos kart, olmayan karttan kotudur. */
        const metin = (document.getElementById('uzunMolaMetin') || {}).textContent || '';
        ekle('uzun mola', 'kart metni dolu ve süreyi söylüyor',
             metin.trim().length > 20 && /\d/.test(metin),
             metin.slice(0, 40));
        kart.hidden = oncedenGizli;
      }, 150);
    }

    /* 4) CEKIRDEK TARAFI — kosullar dogru mu?
          Motoru kopyalayarak sinariz; gercek motoru bozmayalim. */
    {
      const A = { calismaSuresi: 1200, molaSuresi: 20, uzunMolaAcik: true,
                  uzunMolaEsigi: 7200, uzunMolaSuresi: 300 };
      const kur = (acik, kesintisiz) => {
        const t = new MolaMotoru({ ...A, uzunMolaAcik: acik });
        let duyuldu = 0;
        t.uzerine('uzunMolaOnerisi', () => duyuldu++);
        t.istatistik.kesintisizSure = kesintisiz;
        t.basla(); t.molayaGec();
        t.hedefZaman = Date.now() - 10;
        t.tik();
        return duyuldu;
      };
      ekle('uzun mola', 'ayar kapalıyken öneri yok', kur(false, 9999) === 0);
      ekle('uzun mola', 'süre yetmezken öneri yok', kur(true, 60) === 0);
      ekle('uzun mola', 'koşullar tamken öneri var', kur(true, 7500) === 1);

      /* 5) UZUN MOLA GERCEKTEN UZUN MU?
            20 saniyelik bir "uzun mola" sessiz bir yalandir. */
      const t = new MolaMotoru(A);
      t.basla(); t.uzunMolayaGec();
      const sn = Math.round(t.kalanSaniye());
      ekle('uzun mola', 'uzun mola gerçekten uzun (5 dk)',
           Math.abs(sn - A.uzunMolaSuresi) <= 2, sn + ' sn');
      ekle('uzun mola', 'uzun mola işareti kuruldu', t.uzunMoladaMi === true);
    }
  }

  /* ---------- 4. DİL ---------- */
  {
    /* EGZERSİZ METİNLERİ — kaynağa bakan denetim.
       28.08.2026'da ölçüldü: İngilizce sayfada mola ekranı TÜRKÇE
       kalıyordu. "Nokta büyüyünce parmağına, küçülünce uzağa bak" —
       yani kullanıcıya NE YAPACAĞINI söyleyen tek metin.

       NEDEN AŞAĞIDAKİ TARAMA YAKALAMADI: o tarama yalnızca GÖRÜNÜR
       öğeleri geziyor (`e.offsetParent`). Mola ekranı sınama koşarken
       gizli. Görünmeyen durum, denetlenmemiş durumdur — bu dersi bu
       projede üçüncü kez ödüyoruz (gizli sekme içeriği, masaüstü
       uyarı satırı, şimdi mola ekranı).

       Bu yüzden burası DOM'a değil KAYNAĞA bakıyor. */
    /* GOZLE GORUNMEYEN METIN — dorduncu yuzey.
       Yukaridaki tarama gorunur ogeleri geziyor. aria-label, title ve
       placeholder gozle gorunmez; ekran okuyucu kullanan biri icinse
       ekranin KENDISI odur.
       28.08.2026'da olculdu: Ingilizce sayfada hafta grafiginin
       aria-label'i Turkce okunuyordu — "Son yedi gun: Cum 0, ...".
       Hicbir kullanici bunu sikayet edemez, cunku goremez. */
    {
      // Kendi denetleyicisi: asagidaki `turkceMi` bu bloktan SONRA
      // tanimli. Siraya bagli sinama, tasindiginda sessizce bozulur.
      const OZEL2 = ['Türkiye', 'Göz Molası'];
      const trHarfVar = (t) => {
        let m = t;
        for (const a of OZEL2) m = m.split(a).join('');
        return /[çğıöşüÇĞİÖŞÜ]/.test(m);
      };
      const NITELIKLER = ['aria-label', 'title', 'placeholder', 'alt'];
      const supheli = [];
      let bakilan = 0;
      for (const nit of NITELIKLER) {
        document.querySelectorAll('[' + nit + ']').forEach((e) => {
          const d = (e.getAttribute(nit) || '').trim();
          if (!d || d.length < 4) return;
          bakilan++;
          if (trHarfVar(d)) {
            supheli.push(nit + '="' + d.slice(0, 44) + '"');
          }
        });
      }
      /* SIFIR SONUC "GECTI" DEMEK DEGILDIR. Bugun bu tuzaga bir kez
         dustum: yanlis adla arayip sifir oge buldum ve "hepsi
         cevrildi" dedim. Kac sey inceledigimizi de raporluyoruz. */
      ekle('dil', 'incelenen gizli metin sayısı > 0', bakilan > 0,
           bakilan + ' nitelik');
      ekle('dil', 'aria-label/title metinlerinde Türkçe kalmadı',
           supheli.length === 0,
           supheli.length ? supheli.join(' | ') : bakilan + ' nitelik temiz');
    }

    const liste = (typeof TUM_EGZERSIZLER !== 'undefined') ? TUM_EGZERSIZLER : null;
    if (!liste || !liste.length) {
      /* BOŞ KÜMEDE GEÇMEK YASAK. Bu denetimin ilk hâli listeyi yanlış
         adla arıyordu, sıfır öğe buldu ve "hepsi çevrildi" dedi.
         Hiçbir şey ölçmeyen sınama, geçmiş sayılmaz. */
      ekle('dil', 'egzersiz listesi bulunamadı — ÖLÇÜM YAPILMADI', false,
           'TUM_EGZERSIZLER yok');
    } else {
      const eksik = [];
      for (const S of liste) {
        if (!S.ad) continue;
        if (C(S.ad) === S.ad && /[çğıöşüÇĞİÖŞÜ]/.test(S.ad)) eksik.push(S.ad);
        if (S.yonerge && C(S.yonerge) === S.yonerge
            && /[çğıöşüÇĞİÖŞÜ]/.test(S.yonerge)) eksik.push(S.yonerge.slice(0, 32));
      }
      const enAz = 5;                       // bugün 5 egzersiz var
      ekle('dil', `egzersiz sayısı en az ${enAz}`, liste.length >= enAz,
           `${liste.length} egzersiz`);
      ekle('dil', 'mola ekranı egzersiz metinleri çevrilebiliyor',
           eksik.length === 0,
           eksik.length ? 'sözlükte yok: ' + eksik.join(' | ') : `${liste.length} egzersiz`);
    }

    /* OZEL ADLAR Turkce harf tasir ama cevrilmez.
       "Türkiye" ulkenin INGILIZCEDEKI resmi adi; sinama onu
       "cevrilmemis Turkce metin" sayip yanlis alarm veriyordu.
       Yanlis alarm veren sinama, bir sure sonra bakilmayan sinamadir. */
    const OZEL_ADLAR = ['Türkiye', 'Göz Molası'];
    const turkceMi = (t) => {
      let m = t;
      for (const ad of OZEL_ADLAR) m = m.split(ad).join('');
      return /[çğıöşüÇĞİÖŞÜ]/.test(m);
    };
    /* Uygulama ADLARI ozel addir, cevrilmez: "Hesap Araclari",
       "Kur Pusulasi", "Haftalik Planlayici"... Sinama bunlari
       "cevrilmemis Turkce metin" sayiyordu ve her calismada iki
       yanlis alarm veriyordu. Yanlis alarm veren sinama, bir sure
       sonra bakilmayan sinamadir. */
    const gorunur = () => [...document.querySelectorAll('body *')]
      .filter(e => e.children.length === 0 && e.offsetParent)
      .filter(e => !e.closest('.diger-uyg, .diger-izgara'))
      .map(e => e.textContent.trim()).filter(t => t.length > 3);

    const dil = aktifDil();
    const metinler = gorunur();
    const trSayisi = metinler.filter(turkceMi).length;
    if (dil === 'en') {
      ekle('dil', 'İngilizce kipte Türkçe metin kalmadı', trSayisi === 0, `${trSayisi} tane`);
    } else {
      ekle('dil', 'Türkçe kipte metinler Türkçe', trSayisi > 5, `${trSayisi} Türkçe metin`);
    }
    ekle('dil', 'sözlük yüklü', typeof SOZLUK === 'object' && Object.keys(SOZLUK).length > 100,
         `${Object.keys(SOZLUK || {}).length} kayıt`);
    ekle('dil', 'İngilizce bilgi kartları var', typeof BILGILER_EN !== 'undefined' && BILGILER_EN.length === BILGILER.length,
         `${(typeof BILGILER_EN !== 'undefined' ? BILGILER_EN : []).length} / ${BILGILER.length}`);
  }

  /* ---------- 5. MOLA İÇERİĞİ ---------- */
  {
    const gorulen = [];
    for (let i = 0; i < 8; i++) {
      const k = await MolaIcerik.sonraki({ tamamlananMola: 4 });
      gorulen.push(k ? k.baslik : null);
    }
    const bosVar = gorulen.some(x => !x);
    const tekrar = gorulen.length - new Set(gorulen).size;
    ekle('mola içeriği', '8 molada boş kart yok', !bosVar, '');
    ekle('mola içeriği', '8 molada en fazla 1 tekrar', tekrar <= 1, `${tekrar} tekrar`);
    const etiketler = ['bilgi', 'ipucu', 'ozet', 'hava', 'kalite']
      .map(t => MolaIcerik.ETIKET[t]).filter(Boolean);
    ekle('mola içeriği', 'her tür için etiket var', etiketler.length >= 3, etiketler.join(' · '));
  }

  /* ---------- 6. KONTRAST ---------- */
  {
    const kok = document.documentElement, eskiTema = kok.dataset.tema;
    const c = document.createElement('canvas'); c.width = c.height = 1;
    const x = c.getContext('2d', { willReadFrequently: true });
    const rgb = (r) => { x.clearRect(0,0,1,1); x.fillStyle = r; x.fillRect(0,0,1,1);
      const d = x.getImageData(0,0,1,1).data; return [d[0],d[1],d[2]]; };
    const L = ([r,g,b]) => { const f = v => { v/=255; return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4); };
      return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b); };
    const K = (a,b) => { const l1=L(a), l2=L(b); return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05); };
    const d = document.createElement('div'); document.body.appendChild(d);
    const al = (v) => { d.style.color = v; return rgb(getComputedStyle(d).color); };

    const temalar = [...document.querySelectorAll('.tema-sec')]
      .map(b => b.dataset.tema).filter(t => t !== 'otomatik');
    let kotu = 0, n = 0, enaz = 99;
    for (const t of temalar) {
      kok.dataset.tema = t;
      for (const v of [60, 100, 150]) {
        kok.style.setProperty('--canlilik', (v/100).toFixed(2)); n++;
        const o = [
          K(al('var(--vurgu-koyu)'), al('var(--vurgu)')),
          K(al('var(--yazi)'), al('var(--zemin)')),
          K(al('var(--yazi-soluk)'), al('var(--kart)')),
          K(al('var(--mola-yazi)'), al('var(--mola-3)')),
        ];
        const vk = K(al('var(--vurgu)'), al('var(--kart)'));
        enaz = Math.min(enaz, ...o, vk + 1.5);
        if (o.some(z => z < 4.5) || vk < 3) kotu++;
      }
    }
    kok.dataset.tema = eskiTema || ''; kok.style.setProperty('--canlilik','1'); d.remove();
    ekle('kontrast', `${temalar.length} tema × 3 canlılık`, kotu === 0, `${n} kombinasyon, ${kotu} sorun`);
  }

  /* ---------- 7. AYAR TUR-DÖNÜŞÜ ---------- */
  {
    const eski = JSON.stringify(window.molaMotoru.disaAktar().ayarlar);
    const m2 = new MolaMotoru();
    m2.iceAktar({ ayarlar: JSON.parse(eski) });
    ekle('ayarlar', 'dışa/içe aktarma tur-dönüşü bozulmuyor',
         JSON.stringify(m2.ayarlar) === eski, '');
  }

  /* ---------- 8. SAYFA SAĞLIĞI ---------- */
  {
    // innerWidth 0 ise pencere ölçülemiyor demektir (gizli bölme);
    // o durumda "taşma var" demek yanıltıcı olur.
    const gen = window.innerWidth;
    ekle('sağlık', 'yatay taşma yok',
         gen < 50 || document.documentElement.scrollWidth <= gen + 1,
         gen < 50 ? 'ölçülemedi (pencere gizli)'
                  : `${document.documentElement.scrollWidth} / ${gen}`);
    /* BAGLANTI VERILEN HER DOSYA GERCEKTEN VAR MI?
       Betikler, stiller, ikonlar, manifest icerigi ve manifest
       kisayollari. Bir kez yasandi: index.html arayuz.js'i cagiriyordu,
       dosya yoktu; sayfa aciliyor ama hicbir dugme calismiyordu.

       `../` ile baslayanlar DENETLENMIYOR. Onlar kardes uygulamalarin
       adresleri (../hesap/, ../muhasebe/...) ve yalnizca CANLI sitede
       var; yerel sunucu bu klasoru servis ettigi icin hepsi 404 doner.
       Yerelde denetlemek her koguda bes yanlis alarm demek olurdu -
       yanlis alarm veren sinama, bir sure sonra bakilmayan sinamadir.
       Onlar canlida curl ile olculdu: bes adres de 200. (K-20) */
    {
      const adresler = new Set();
      const ekleAdres = (u) => {
        if (!u) return;
        if (/^(https?:|data:|mailto:|#)/.test(u)) return;
        if (u.startsWith('../')) return;      // kardes uygulama
        adresler.add(u.split('#')[0]);
      };
      document.querySelectorAll('script[src]').forEach((o) => ekleAdres(o.getAttribute('src')));
      document.querySelectorAll('link[href]').forEach((o) => ekleAdres(o.getAttribute('href')));
      document.querySelectorAll('img[src]').forEach((o) => ekleAdres(o.getAttribute('src')));
      document.querySelectorAll('a[href]').forEach((o) => ekleAdres(o.getAttribute('href')));
      try {
        const m = await (await fetch('manifest.json?k=' + Date.now(),
                                     { cache: 'no-store' })).json();
        (m.icons || []).forEach((i) => ekleAdres(i.src));
        (m.shortcuts || []).forEach((s) => {
          ekleAdres(s.url);
          (s.icons || []).forEach((i) => ekleAdres(i.src));
        });
        ekleAdres(m.start_url);
      } catch { adresler.add('manifest.json'); }

      const kirikDosya = [];
      for (const u of adresler) {
        try {
          const c = await fetch(u, { method: 'HEAD', cache: 'no-store' });
          if (!c.ok) kirikDosya.push(u + ' (' + c.status + ')');
        } catch (e) { kirikDosya.push(u + ' (' + e.message + ')'); }
      }
      ekle('sağlık', 'bağlantı verilen her dosya var',
           kirikDosya.length === 0,
           kirikDosya.length ? kirikDosya.join(', ').slice(0, 70)
                             : `${adresler.size} adres denendi`);
    }

    const kirik = [...document.querySelectorAll('a[href^="#"]')]
      .filter(a => { try { return !document.querySelector(a.getAttribute('href')); } catch { return true; } });
    ekle('sağlık', 'kırık iç bağlantı yok', kirik.length === 0, `${kirik.length} tane`);
    /* META DESCRIPTION UZUNLUGU
       Google arama sonucunda ~160 karakterde kesiyor. 200 karakterlik
       bir aciklama yazilmisti; sondaki "telefonda da calisir" hicbir
       zaman gorunmuyordu. Sinirin altinda tutuluyor mu, makine baksin. */
    const aciklama = document.querySelector('meta[name="description"]')?.content || '';
    ekle('sağlık', 'meta description 160 karakteri aşmıyor',
         aciklama.length > 0 && aciklama.length <= 160,
         `${aciklama.length} karakter`);

    /* HIDDEN GERCEKTEN GIZLIYOR MU?
       HTML'in `hidden` ozniteligi `display: none` demek, ama sinifa
       yazilan her `display` onu eziyor. .durum-notu ve
       .guncelleme-serit'e display:flex yazmistim; ikisi de
       hidden="true" olduğu halde ciziliyordu - biri ekranda bos bir
       kutuydu. Ayni hata iki ayri projede daha cikti, sinifsal. */
    const gizliAmaGorunen = [...document.querySelectorAll('[hidden]')].filter((o) => {
      const s = getComputedStyle(o);
      const r = o.getBoundingClientRect();
      return s.display !== 'none' && r.width > 0 && r.height > 0;
    });
    ekle('sağlık', 'hidden olan her şey gerçekten gizli',
         gizliAmaGorunen.length === 0,
         gizliAmaGorunen.map((o) => o.id || o.className).join(',').slice(0, 60));

    /* SAYFA HANGI KODU CALISTIRIYOR? — kanarya

       "38/38 gecti" demeden once sorulmasi gereken soru: test HANGI
       kodu olctu? Sayfa betikleri sabit bir ?s=v.. damgasiyla
       yukluyor. Tarayici onbellekten ESKI kopyayi verirse, sinama
       artik var olmayan bir surumu "gecti" diye olcer ve biz
       duzelttigimizi saniriz.

       Olctum: bu projede servis iscisi "once ag" + cache:'no-cache'
       calisiyor, damga artirilmasa bile guncel dosya geliyor. Ama
       bunu bir kez olcup gecmek yetmez - servis iscisi degisirse
       sessizce bozulur. O yuzden her calismada kontrol ediliyor.

       Yontem: veri dosyalarini TAZE cekip (no-store) icindeki kayit
       sayisini, sayfada YUKLU olan diziyle karsilastir. Ayrilirsa
       sayfa eski kod calistiriyor demektir ve asagidaki butun
       sonuclar supheli. */
    {
      const say = (metin) => (metin.match(/^\s*baslik:/gm) || []).length;
      const denetle = async (dosya, dizi, ad) => {
        try {
          const taze = await (await fetch(dosya + '?kanarya=' + Date.now(),
                                          { cache: 'no-store' })).text();
          const diskte = say(taze);
          const yuklu = Array.isArray(dizi) ? dizi.length : -1;
          ekle('sağlık', `sayfa güncel ${ad} kodunu çalıştırıyor`,
               diskte > 0 && diskte === yuklu,
               `diskte ${diskte}, sayfada ${yuklu}`);
        } catch (e) {
          ekle('sağlık', `sayfa güncel ${ad} kodunu çalıştırıyor`, false,
               'ölçülemedi: ' + e.message);
        }
      };
      await denetle('dunya.js', typeof DUNYA !== 'undefined' ? DUNYA : null, 'dunya.js');
      await denetle('bilgiler.js', typeof BILGILER !== 'undefined' ? BILGILER : null, 'bilgiler.js');
    }

    /* SURUM DAMGASI TUTUYOR MU?
       sw.js icindeki SURUM ile HTML'deki ?s=v.. etiketleri ayni olmali.
       sw.js'i artirip surum_ekle.py'yi calistirmayi unutmak, kullanicinin
       onbellekteki ESKI kodla calismasi demek: duzeltirsin, sinamalar
       gecer, kullanici hala hatali surumdedir. Bugun bir kez oldu.

       Not: bu projede servis iscisi "once ag, onbellek yedek" calisiyor
       (cache: 'no-cache'), yani internet varken zaten guncel dosya
       geliyor. Damga cevrimdisi kopya ve tarayici onbellegi icin onemli. */
    const damga = (document.querySelector('script[src*="?s=v"]') || {})
      .getAttribute?.('src')?.match(/\?s=(v\d+)/)?.[1];
    ekle('sağlık', 'sürüm damgası betiklerde var', !!damga, damga || 'yok');

    const gorsel = [...document.images].filter(i => !i.complete || i.naturalWidth === 0);
    ekle('sağlık', 'yüklenmeyen görsel yok', gorsel.length === 0, `${gorsel.length} tane`);
    /* 40 değil 44: WCAG 2.5.8 alt sınırı 44x44. Telefonda ölçtüm,
       beş bağlantı 43,2 px'ti ve 40'lık eşikten geçiyordu.

       İSTİSNA: WCAG 2.5.8 "inline" maddesi, bir cümlenin İÇİNDE akan
       hedefleri kuralın dışında tutuyor — alt bilgideki "Kısayollar ·
       Gizlilik politikası" gibi. Onları 44 px yapmak cümleyi bozardı
       ve zaten çevresindeki metinle birlikte okunuyorlar. */
    const cumleIcinde = (e) => {
      const st = getComputedStyle(e);
      if (!st.display.startsWith('inline')) return false;
      const ust = e.parentElement;
      return !!ust && (ust.tagName === 'P' || ust.classList.contains('alt-bilgi'));
    };
    const kucuk = [...document.querySelectorAll('button')]
      .filter(e => { const r = e.getBoundingClientRect(); return r.height > 0 && (r.height < 44 || r.width < 44) && e.offsetParent; })
      .filter(e => !cumleIcinde(e));
    ekle('sağlık', 'küçük dokunma hedefi yok (<44px)', kucuk.length === 0,
         kucuk.map(e => e.id || e.className).join(',').slice(0, 40));
    ekle('sağlık', 'kalp atışı Worker\'da (arka planda kısılmaz)',
         !!window.molaMotoru._isci, window.molaMotoru._isci ? 'Worker' : 'setInterval yedeği');
  }

  /* ---------- BİLGİLER SEKMESİ ----------
     Sekme varsayılan olarak GİZLİ, o yüzden yukarıdaki "yatay taşma
     yok" denetimi içeriğini hiç ölçmüyordu. Ölçtüm: telefon boyutunda
     123 piksel taşıyordu ve sınama 31/31 diyordu. Gizli içerik
     denetlenmemiş içeriktir. */
  {
    const dugme = document.getElementById('sekmeDugmeBilgiler');
    const panel = document.getElementById('sekmeBilgiler');
    if (dugme && panel) {
      const oncedenAcikti = !panel.hidden;
      dugme.click();
      // İçerik veriden kuruluyor + rehber ağdan çekiliyor
      await new Promise((z) => setTimeout(z, 1500));

      const bolum = panel.querySelectorAll('.bilgi-bolum').length;
      ekle('bilgiler', 'bölümler kuruldu', bolum >= 4, `${bolum} bölüm`);

      const oge = panel.querySelectorAll('.bilgi-oge').length;
      ekle('bilgiler', 'kartlar kuruldu', oge >= 20, `${oge} kart`);

      /* Egzersizler yönerge, iddia değil — kaynak beklemiyoruz.
         Geri kalan her kartın kaynağı OLMALI. */
      const egzersizAdet = (typeof TUM_EGZERSIZLER !== 'undefined')
        ? TUM_EGZERSIZLER.length : 5;
      const kaynaksiz = [...panel.querySelectorAll('.bilgi-oge')]
        .filter((o) => !o.querySelector('.kaynak')).length;
      ekle('bilgiler', 'her iddianın kaynağı var',
           kaynaksiz <= egzersizAdet, `${kaynaksiz} kaynaksız`);

      const rehber = document.getElementById('rehberGovde');
      ekle('bilgiler', 'rehber içeri alındı',
           !!rehber && rehber.querySelectorAll('h2').length >= 3,
           `${rehber ? rehber.querySelectorAll('h2').length : 0} başlık`);

      const gen = window.innerWidth;
      const tasan = [...panel.querySelectorAll('*')].filter((o) => {
        const r = o.getBoundingClientRect();
        if (r.width === 0) return false;
        const st = getComputedStyle(o);
        if (st.overflowX === 'auto' || st.overflowX === 'scroll') return false;
        return r.right > gen + 1;
      });
      ekle('bilgiler', 'sekme içeriği taşmıyor',
           gen < 50 || tasan.length === 0,
           gen < 50 ? 'ölçülemedi (pencere gizli)'
                    : `${tasan.length} taşan öğe`);

      if (!oncedenAcikti) document.getElementById('sekmeDugmeSayac')?.click();
    }
  }

  /* ---------- RAPOR ---------- */
  const kalan = sonuc.filter(r => r.durum === 'KALDI');
  return JSON.stringify({
    toplam: sonuc.length,
    gecti: sonuc.length - kalan.length,
    kaldi: kalan.length,
    kalanlar: kalan,
    hepsi: sonuc.map(r => `${r.durum === 'GEÇTİ' ? '+' : 'X'} [${r.grup}] ${r.ad}${r.ayrinti ? ' — ' + r.ayrinti : ''}`),
  }, null, 1);
})()
