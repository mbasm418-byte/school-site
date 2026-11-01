/* Service worker — الموقع يعمل كتطبيق بعد التثبيت */
const VERSION = 'v1';
const SHELL_CACHE = 'school-shell-' + VERSION;
const FONT_CACHE = 'school-fonts-' + VERSION;

const SHELL = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-512-maskable.png',
  './apple-touch-icon.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== SHELL_CACHE && key !== FONT_CACHE)
          .map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

const isFont = (url) =>
  url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // ملفات PDF كبيرة — تُجلب من الشبكة دائمًا ولا تُخزَّن مؤقتًا
  if (url.pathname.toLowerCase().endsWith('.pdf')) return;

  // الخطوط: من الكاش أولًا ثم الشبكة
  if (isFont(url)) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((response) => {
          const copy = response.clone();
          caches.open(FONT_CACHE).then((cache) => cache.put(request, copy));
          return response;
        }).catch(() => cached || Response.error());
      })
    );
    return;
  }

  // التنقل بين الصفحات: الشبكة أولًا مع الرجوع إلى النسخة المحفوظة
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(SHELL_CACHE).then((cache) => cache.put('./index.html', copy));
          return response;
        })
        .catch(() => caches.match('./index.html').then((cached) => cached || caches.match('./')))
    );
    return;
  }

  // بقية الملفات من نفس الموقع: الكاش أولًا
  if (url.origin === self.location.origin) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((response) => {
          if (response && response.status === 200) {
            const copy = response.clone();
            caches.open(SHELL_CACHE).then((cache) => cache.put(request, copy));
          }
          return response;
        });
      })
    );
  }
});
