/* Servis işçisi — uygulamanın çevrimdışı çalışmasını sağlar.
   Sürümü değiştirirsen tarayıcı eski dosyaları atar. */
const SURUM = 'goz-molasi-v192';

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

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(SURUM)
      .then((c) => c.addAll(DOSYALAR))
      .catch(() => null)          // bir dosya eksikse kurulum çökmesin
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((adlar) => Promise.all(adlar.filter((a) => a !== SURUM).map((a) => caches.delete(a))))
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
      for (const c of liste) if ('focus' in c) return c.focus();
      if (self.clients.openWindow) return self.clients.openWindow('./index.html');
    })
  );
});
