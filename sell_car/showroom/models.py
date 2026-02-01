from django.db import models
from django.core.files import File
from PIL import Image # ตัวช่วยจัดการรูป
from io import BytesIO
import os

class Car(models.Model):
    # ... (Code ส่วน Car เหมือนเดิมทุกอย่าง ไม่ต้องแก้) ...
    STATUS_CHOICES = [
        ('AVAILABLE', '✅ ว่าง (พร้อมขาย)'),
        ('RESERVED', '🟡 ติดจอง'),
        ('SOLD', '🔴 ขายแล้ว'),
    ]
    
    GEAR_CHOICES = [
        ('AUTO', 'ออโต้'),
        ('MANUAL', 'ธรรมดา'),
    ]

    FUEL_CHOICES = [
        ('DIESEL', 'ดีเซล'),
        ('PETROL', 'เบนซิน'),
        ('HYBRID', 'ไฮบริด'),
        ('EV', 'ไฟฟ้า 100%'),
    ]

    brand = models.CharField("ยี่ห้อ", max_length=50)
    model_name = models.CharField("รุ่น", max_length=100)
    year = models.CharField("ปี (ค.ศ.)", max_length=4)
    price = models.IntegerField("ราคา (บาท)")
    installment = models.IntegerField("ผ่อนเริ่มต้น (บาท/เดือน)", blank=True, null=True, help_text="ใส่แค่ตัวเลข ถ้าไม่ใส่ ระบบจะไม่แสดง")
    gear = models.CharField("เกียร์", max_length=10, choices=GEAR_CHOICES, default='AUTO')
    color = models.CharField("สี", max_length=50, blank=True)
    mileage = models.CharField("เลขไมล์", max_length=50, blank=True, help_text="เช่น 45,xxx")
    description = models.TextField("รายละเอียดรถ", blank=True, help_text="เช่น รถมือเดียว น็อตไม่ขยับ")
    status = models.CharField("สถานะ", max_length=10, choices=STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)
    fuel_type = models.CharField("เชื้อเพลิง", max_length=10, choices=FUEL_CHOICES, default='DIESEL')

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.year})"

    class Meta:
        verbose_name = "รถยนต์"
        verbose_name_plural = "ข้อมูลรถยนต์ทั้งหมด"


# 👇 ส่วนที่เพิ่มระบบย่อรูป คือตรงนี้ครับ
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField("รูปภาพ", upload_to='cars/%Y/%m/')
    
    def save(self, *args, **kwargs):
        # ถ้ามีรูปภาพ (และเป็นรูปใหม่ที่เพิ่งอัพ)
        if self.image:
            self.compress_image()
        super().save(*args, **kwargs)

    def compress_image(self):
        # 1. เปิดรูปขึ้นมา
        img = Image.open(self.image)
        
        # 2. แปลงโหมดเป็น RGB (กันเหนียว เผื่อเจอไฟล์ PNG/RGBA)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # 3. ถ้ารูปใหญ่เกิน 1024px ให้ย่อลงมา (ดูบนมือถือชัดเหลือเฟือ)
        if img.width > 1024:
            output_size = (1024, 1024)
            img.thumbnail(output_size)
            
        # 4. เตรียมเซฟทับ
        im_io = BytesIO()
        # Quality=70 คือจุดสมดุล (ชัดแต่ไฟล์เล็ก)
        img.save(im_io, 'JPEG', quality=70, optimize=True) 
        
        # 5. สร้างไฟล์ใหม่ทับไฟล์เดิม
        new_image = File(im_io, name=self.image.name)
        self.image = new_image

    def __str__(self):
        return f"รูปของ {self.car.model_name}"