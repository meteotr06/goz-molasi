/* Servis iÅŸÃ§isi â€” uygulamanÄ±n Ã§evrimdÄ±ÅŸÄ± Ã§alÄ±ÅŸmasÄ±nÄ± saÄŸlar.
   SÃ¼rÃ¼mÃ¼ deÄŸiÅŸtirirsen tarayÄ±cÄ± eski dosyalarÄ± atar. */
const SURUM = 'goz-molasi-v5';

const DOSYALAR = [
  './',
  './index.html',
  './stil.css',
  './cekirdek.js',
  './arayuz.js',
  './bilgiler.js',
  './egzersiz.js',
  './manifest.json',
  './ikon-192.png',
  './ikon-512.png',
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(SURUM)
      .then((c) => c.addAll(DOSYALAR))
      .catch(() => null)          // bir dosya eksikse kurulum Ã§Ã¶kmesin
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

/* "Ã–nce aÄŸ, Ã¶nbellek yedek" yÃ¶ntemi.

   Neden bÃ¶yle? Ã–nce Ã¶nbellekten servis edersek, dosyalarÄ± gÃ¼ncelledikten
   sonra kullanÄ±cÄ± eski sÃ¼rÃ¼mde takÄ±lÄ± kalÄ±yor. Bu yÃ¶ntemde:
   - Ä°nternet varsa her zaman en gÃ¼ncel dosya gelir ve Ã¶nbelleÄŸe yazÄ±lÄ±r.
   - Ä°nternet yoksa son Ã§alÄ±ÅŸan sÃ¼rÃ¼m Ã¶nbellekten aÃ§Ä±lÄ±r.
   Uygulama bir kez aÃ§Ä±lÄ±p saatlerce aÃ§Ä±k kaldÄ±ÄŸÄ± iÃ§in ilk aÃ§Ä±lÄ±ÅŸtaki
   birkaÃ§ yÃ¼z milisaniyelik fark Ã¶nemsiz. */
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  if (new URL(e.request.url).origin !== location.origin) return;

  e.respondWith((async () => {
    const onbellek = await caches.open(SURUM);
    try {
      // no-cache: tarayÄ±cÄ±nÄ±n kendi Ã¶nbelleÄŸini de atlayÄ±p sunucuya sorar
      const cevap = await fetch(e.request, { cache: 'no-cache' });
      if (cevap && cevap.ok) onbellek.put(e.request, cevap.clone());
      return cevap;
    } catch {
      return (await onbellek.match(e.request))
        || (await onbellek.match('./index.html'))
        || new Response('Ã‡evrimdÄ±ÅŸÄ±', { status: 503 });
    }
  })());
});

/* Sayfa "mola vakti" derse bildirimi servis iÅŸÃ§isi gÃ¶sterir.
   Sebebi: sekme arka plandayken new Notification() gÃ¼venilir deÄŸil,
   registration.showNotification() ise Ã§alÄ±ÅŸÄ±r. */
self.addEventListener('message', (e) => {
  const veri = e.data || {};
  if (veri.tur === 'bildirim') {
    self.registration.showNotification(veri.baslik || 'GÃ¶z MolasÄ±', {
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
