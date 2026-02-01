from django.contrib import admin
from .models import Car, CarImage
from django.utils.html import mark_safe

# ตัวจัดการรูปภาพแบบ Inline (ซ้อนอยู่ในหน้ารถ)
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1  # แสดงช่องว่าง 1 ช่อง (กดเพิ่มเองได้)
    readonly_fields = ['show_image'] # โชว์รูปตัวอย่าง

    def show_image(self, obj):
        if obj.image:
            # แสดงรูปตัวอย่างขนาดเล็ก
            return mark_safe(f'<img src="{obj.image.url}" style="height: 100px; border-radius: 8px;">')
        return "-"
    show_image.short_description = "ตัวอย่าง"

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]
    
    # แก้บรรทัดนี้: เอา 'status' ใส่เข้าไป เพื่อให้มัน edit ได้
    list_display = ['brand', 'model_name', 'year', 'show_price', 'installment', 'status']
    
    list_filter = ['status', 'brand', 'gear']
    search_fields = ['model_name', 'brand']
    
    # บรรทัดนี้ถูกต้องแล้ว (ทำให้มี Dropdown เลือกสถานะได้เลยหน้าแรก)
    list_editable = ['status'] 

    def show_price(self, obj):
        return f"{obj.price:,} บาท"
    show_price.short_description = "ราคา"