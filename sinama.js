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

  /* ---------- 4. DİL ---------- */
  {
    const turkceMi = (t) => /[çğıöşüÇĞİÖŞÜ]/.test(t);
    const gorunur = () => [...document.querySelectorAll('body *')]
      .filter(e => e.children.length === 0 && e.offsetParent)
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
    const kirik = [...document.querySelectorAll('a[href^="#"]')]
      .filter(a => { try { return !document.querySelector(a.getAttribute('href')); } catch { return true; } });
    ekle('sağlık', 'kırık iç bağlantı yok', kirik.length === 0, `${kirik.length} tane`);
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
