// sw-admin.js สำหรับ Django Admin (แบบ Bypass 100% เพื่อความเสถียร)

const CACHE_NAME = 'admin-secure-v4'; // อัปเดตเวอร์ชัน
const STATIC_ASSETS = [
  '/manifest-admin.json'
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
  // ควบคุมทุกแท็บที่เปิดอยู่ทันที
  event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
  // กฎเหล็ก: ปล่อยให้ทุกคำขอ (Request) วิ่งผ่านอินเทอร์เน็ตปกติ 
  // ไม่ต้องเข้าไปยุ่งหรือแก้ไขอะไรทั้งสิ้น เพื่อให้หน้า Django Admin ทำงานได้ 100%
  // ไม่ต้องมี event.respondWith(...) ในหน้านี้
  return; 
});