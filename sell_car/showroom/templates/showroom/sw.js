// Service Worker สำหรับ PWA
const CACHE_NAME = 'sellcar-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  // ข้ามคำขอที่ไม่ใช่ GET หรือเป็นข้าม Domain
  if (event.request.method !== 'GET' || !event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // 1. ถ้ามีใน Cache ให้ใช้จาก Cache ทันที (เพื่อความเร็ว)
      if (cachedResponse) {
        // อัปเดต Cache ในพื้นหลัง (Stale-while-revalidate)
        fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, networkResponse);
            });
          }
        }).catch(() => {});
        return cachedResponse;
      }

      // 2. ถ้าไม่มีใน Cache ให้โหลดจาก Network
      return fetch(event.request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }

        // เก็บลง Cache เฉพาะไฟล์ที่จำเป็น
        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return networkResponse;
      }).catch(() => {
        // 3. ถ้า Offline และหาใน Cache ไม่เจอ ให้ส่งหน้าแรกกลับไป
        if (event.request.mode === 'navigate') {
          return caches.match('/');
        }
      });
    })
  );
});
