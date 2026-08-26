/* Servis işçisi — uygulamanın çevrimdışı çalışmasını sağlar.
   Sürümü değiştirirsen tarayıcı eski dosyaları atar. */
const SURUM = 'goz-molasi-v46';

const DOSYALAR = [
  './',
  './index.html',
  './gizlilik.html',
  './rehber.html',
  './stil.css',
  './dil.js',
  './cekirdek.js',
  './mola_icerik.js',
  './arayuz.js',
  './bilgiler.js',
  './bilgiler_en.js',
  './egzersiz.js',
  './reklam.js',
  './manifest.json',
  './ikon-192.png',
  './ikon-512.png',
  './ikon-maskeli.png',
  './onizleme.png',
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
      if (cevap && cevap.ok) onbellek.put(e.request, cevap.clone());
      return cevap;
    } catch {
      return (await onbellek.match(e.request))
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
      requireInteraction: false,
      silent: false,
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
