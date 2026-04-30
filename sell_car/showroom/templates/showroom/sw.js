// Service Worker สำหรับ PWA (Add to Home Screen)
const CACHE_NAME = 'sellcar-v1';

self.addEventListener('install', (event) => {
  // ติดตั้ง Service Worker
});

self.addEventListener('fetch', (event) => {
  // ทำหน้าที่เป็น Proxy กรองคำขอ
  // สามารถเพิ่มระบบ Cache ได้ที่นี่ในภายหลัง
});
