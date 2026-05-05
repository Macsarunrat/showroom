// sw-admin.js สำหรับ Django Admin

const CACHE_NAME = 'admin-secure-v2'; // อัปเดตเวอร์ชันเป็น v2 เพื่อเคลียร์ของเก่า
const STATIC_ASSETS = [
  '/manifest-admin.json',
  '/static/showroom/icon-admin-192.png' // ใส่ path รูปของคุณ
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
    ))
  );
});

self.addEventListener('fetch', (event) => {
  // 1. ถ้าไม่ใช่ GET ให้ข้ามการแคชไปเลย
  if (event.request.method !== 'GET') {
    return;
  }

  // 2. ถ้าเป็นหน้าเว็บ HTML (รวมถึงหน้า /admin/)
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => {
        // ถ้าเน็ตหลุดตอนพยายามเข้าหน้า HTML ให้พยายามหาหน้าไหนก็ได้จาก Cache มาโชว์แก้ขัด (หรือหน้า Offline ถ้ามี)
        return caches.match(event.request);
      })
    );
    return;
  }

  // 3. สำหรับไฟล์อื่นๆ (รูป, CSS, JS) 
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // ถ้าเจอใน Cache ให้ใช้เลย
      if (cachedResponse) {
        return cachedResponse;
      }

      // ถ้าไม่เจอ ให้ดึงจาก Network และ "จับ Error" ไว้ ไม่ให้พังหน้าเว็บ
      return fetch(event.request).catch(err => {
        console.warn('Admin PWA: Fetch failed for', event.request.url, err);
        // สามารถคืนค่าว่างๆ หรือรูปภาพ default กลับไปได้เพื่อไม่ให้ระบบค้าง
        // return new Response('Offline resource not found', { status: 404 });
      });
    })
  );
});