// sw-admin.js สำหรับ Django Admin (แบบปลอดภัยจาก CSRF)
const CACHE_NAME = 'admin-secure-v1';
const STATIC_ASSETS = [
  '/manifest-admin.json',
  // เพิ่ม path รูปภาพแอดมิน ถ้าต้องการ
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  // ลบแคชเก่าๆ ทิ้งเมื่อมีการอัปเดตเวอร์ชัน
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
    ))
  );
});

self.addEventListener('fetch', (event) => {
  // 1. ถ้าไม่ใช่คำขอ GET (เช่น การกด Save, Login, หรือ POST ข้อมูล) ให้ข้ามไปเลย! ต้องต่อเน็ตเท่านั้น
  if (event.request.method !== 'GET') {
    return;
  }

  // 2. ถ้าเป็นการขอหน้าเว็บ HTML (Navigation) ให้ไปดึงจากเน็ตใหม่ทุกครั้ง (ป้องกัน CSRF Error)
  if (event.request.mode === 'navigate') {
    event.respondWith(fetch(event.request));
    return;
  }

  // 3. สำหรับไฟล์อื่นๆ (เช่น รูป, CSS) ให้ลองหาในแคชก่อน ถ้าไม่มีค่อยไปโหลดจากเน็ต
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});