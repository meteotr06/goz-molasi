/* Servis işçisi — uygulamanın çevrimdışı çalışmasını sağlar.
   Sürümü değiştirirsen tarayıcı eski dosyaları atar. */
const SURUM = 'goz-molasi-v214';

const DOSYALAR = [
  './',
  './index.html',
  './gizlilik.html',
  './rehber.html',
  './guide.html',
  './stil.css',
  './dil.js',
  './cekirdek.js',
  './degisiklikler.js',
  './kopru.js',
  './mola_icerik.js',
  './arayuz.js',
  './bilgiler.js',
  './bilgiler_en.js',
  './dunya.js',
  './egzersiz.js',
  './reklam.js',
  './manifest.json',
  './yazi/fraunces-latin.woff2',
  './yazi/fraunces-latinext.woff2',
  './ikon-192.png',
  './ikon-512.png',
  './ikon-maskeli.png',
  './onizleme.png',
  './onizleme-en.png',
];

/* ÇEKİRDEK DOSYALAR — bunlar olmadan uygulama çevrimdışı AÇILMAZ.
   Ötekiler (ikonlar, yazı tipi, bilgi dosyaları) eksik olsa da uygulama
   çalışır; bir tanesi yüzünden güncellemeyi tümden durdurmak daha
   büyük zarar olurdu. */
const CEKIRDEK_DOSYALAR = [
  './', './index.html', './stil.css', './cekirdek.js', './arayuz.js', './dil.js',
];

self.addEventListener('install', (e) => {
  /* `addAll` HEP-YA-HİÇ: tek dosya düşerse hiçbiri eklenmiyordu ve
     `.catch(() => null)` bunu YUTUP `skipWaiting()`e geçiyordu. Sonra
     `activate` çalışan ESKİ önbelleği siliyordu — yani bir dosyanın
     eksikliği, çalışan çevrimdışı katmanı sessizce öldürebilirdi.

     DÜRÜST NOT: bu zararı ÜRETEMEDİM (03.09.2026, üç deneme). Ağ-önce
     yöntem önbelleği çalışırken yeniden dolduruyor, üstelik dosyayı
     diskten kaldırsam bile tarayıcının kendi HTTP önbelleği onu
     sunuyor — yani "404" kurulamadı. Kusuru GÖSTEREMEDİM; düzeltme
     kanıta değil, kodun şekline dayanıyor ve bunu saklamıyorum.

     Yeni davranış: dosyalar TEK TEK ekleniyor, biri düşse ötekiler
     duruyor. Yalnız ÇEKİRDEK bir dosya düşerse kurulum başarısız
     sayılıyor ve `skipWaiting` ÇAĞRILMIYOR — eski işçi görevde kalır,
     çalışan önbellek silinmez. Kullanıcı eski ama ÇALIŞAN sürümde
     kalır; bozuk bir sürümde kalmasından iyidir. */
  e.waitUntil((async () => {
    const c = await caches.open(SURUM);
    const dusenler = [];
    await Promise.all(DOSYALAR.map(async (d) => {
      try { await c.add(d); } catch { dusenler.push(d); }
    }));
    const cekirdekDustu = dusenler.some((d) => CEKIRDEK_DOSYALAR.includes(d));
    if (cekirdekDustu) {
      // Bilerek fırlatılıyor: kurulum başarısız olsun ki eski işçi kalsın.
      throw new Error('cekirdek dosya eksik: ' + dusenler.join(', '));
    }
    await self.skipWaiting();
  })());
});

/* ONBELLEK ADI ONEKI — YALNIZ KENDI ONBELLEKLERIMIZI SILIYORUZ.

   `caches` (CacheStorage) KOKEN basinadir, kapsam (scope) basina
   DEGIL. Eski temizlik "adi SURUM olmayan her onbellegi sil" diyordu
   ve `meteotr06.github.io` kokenindeki BUTUN kardes uygulamalarin
   onbellegini siliyordu: Hava Durumu portali, Hesap Araclari,
   Muhasebe, Kur Pusulasi, Planlayici.

   Kullanicinin gordugu sey: ucakta/metroda kurulu Hesap Araclari'ni
   aciyor, bos sayfa geliyor. Simetrik olarak onlar da bizim
   onbellegimizi siliyordu, yani Goz Molasi'nin kendi cevrimdisi
   yetenegi de surekli yok ediliyordu. Hicbir hata mesaji yok -
   cevrimiciyken her sey kusursuz calistigi icin sebebi bulunamiyor.

   Onek SURUM'den turetiliyor ki ikisi birbirinden ayrisamasin. */
const ONEK = SURUM.replace(/v\d+$/, '');

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((adlar) => Promise.all(adlar
        .filter((a) => a !== SURUM && a.startsWith(ONEK))
        .map((a) => caches.delete(a))))
      .then(() => self.clients.claim())
  );
});

/* "Önce ağ, önbellek yedek" yöntemi.

   Neden böyle? Önce önbellekten servis edersek, dosyaları güncelledikten
   sonra kullanıcı eski sürümde takılı kalıyor. Bu yöntemde:
   - İnternet varsa her zaman en güncel dosya gelir ve önbelleğe yazılır.
   - İnternet yoksa son çalışan sürüm önbellekten açılır.
   Uygulama bir kez açılıp saatlerce açık kaldığı için ilk açılıştaki
   birkaç yüz milisaniyelik fark önemsiz. */
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  if (new URL(e.request.url).origin !== location.origin) return;

  e.respondWith((async () => {
    const onbellek = await caches.open(SURUM);
    try {
      // no-cache: tarayıcının kendi önbelleğini de atlayıp sunucuya sorar
      const cevap = await fetch(e.request, { cache: 'no-cache' });
      /* ANAHTAR SORGUSUZ YAZILIR.

         Eskiden `onbellek.put(e.request, ...)` idi, yani anahtar TAM
         ADRESTI. Iki sonucu vardi (03.09.2026 olculdu: 6 sorgulu
         adres onbellegi 25 -> 43 girdiye cikardi):

         1. Her varlik IKI KEZ duruyordu: on yukleme `./stil.css`
            yaziyor, sayfa `stil.css?s=v174` istiyor, ag-once yontem
            de donen cevabi tam adresle yeniden yaziyordu.

         2. Disaridan gelen HER sorgu (`?utm_source=...` gibi) kalici
            yeni bir sayfa kopyasi aciyordu. Sayilari bizim elimizde
            degil.

         Kota dolunca tarayici yazmayi reddeder ve cevrimdisi katman
         SESSIZCE olur - ekranda hicbir sey degismez.

         Sorgu anahtardan cikarilabilir cunku onbellegin ADI zaten
         surumle damgali; surum degisince tamami siliniyor. Okuma
         tarafi da `ignoreSearch: true` kullaniyor. */
      if (cevap && cevap.ok) {
        const anahtar = new URL(e.request.url);
        anahtar.search = '';
        onbellek.put(anahtar.href, cevap.clone());
      }
      return cevap;
    } catch {
      // ignoreSearch: dosya adreslerinde ?s=<sürüm> etiketi var.
      // (Buraya örnek sürüm YAZILMIYOR: yayın nöbetçisi kaynak taramasında
      //  yorumdaki sayıyı gerçek damga sanıp yanlış alarm veriyordu.)
      // Tam eşleşme aransa çevrimdışı yedek hiç bulunamazdı.
      return (await onbellek.match(e.request, { ignoreSearch: true }))
        || (await onbellek.match('./index.html'))
        || new Response('Çevrimdışı', { status: 503 });
    }
  })());
});

/* Sayfa "mola vakti" derse bildirimi servis işçisi gösterir.
   Sebebi: sekme arka plandayken new Notification() güvenilir değil,
   registration.showNotification() ise çalışır. */
self.addEventListener('message', (e) => {
  const veri = e.data || {};
  if (veri.tur === 'bildirim') {
    self.registration.showNotification(veri.baslik || 'Göz Molası', {
      body: veri.metin || '',
      icon: './ikon-192.png',
      badge: './ikon-192.png',
      tag: 'goz-molasi',
      renotify: true,
      /* KAYBOLMASIN. Mola hatirlatmasi gorulmezse hicbir ise
         yaramaz; kullanici baska islerken kendiliginden silinen bir
         bildirim, hic gonderilmemis gibidir. Kullanici istedi
         (31.08.2026): "bildirimlerimizi yogunlastir". */
      requireInteraction: true,
      silent: false,
      /* Telefon sessizdeyken tek fark edilme yolu titresim. */
      vibrate: veri.titresim || [140, 70, 140],
    });
  }
});

self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  e.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((liste) => {
      /* YALNIZ KENDI PENCERELERIMIZ.

         `includeUncontrolled: true` ile `matchAll`, iscinin KAPSAMINI
         degil KOKENINI doner: ayni adresteki Hesap Araclari, Hava
         Durumu, Muhasebe pencereleri de listeye giriyor ve liste en
         son odaklanan pencereden basliyor. Mola bildirimine tiklayan
         kullanicinin karsisina Goz Molasi degil BASKA bir uygulama
         geliyordu.

         Kapsam `self.registration.scope` -- sabit yazmak, uygulama
         baska bir yola tasininca sessizce bozulurdu. */
      const kapsam = self.registration.scope;
      for (const c of liste) {
        if (c.url && c.url.startsWith(kapsam) && 'focus' in c) return c.focus();
      }
      if (self.clients.openWindow) return self.clients.openWindow('./index.html');
    })
  );
});
