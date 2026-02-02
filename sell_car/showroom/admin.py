from django.contrib import admin
from django import forms
from django.utils.html import mark_safe
from .models import Car, CarImage

class MultipleFileInput(forms.FileInput): # เปลี่ยนจาก ClearableFileInput เป็น FileInput (เหมาะกับการอัพเพิ่ม)
    allow_multiple_selected = True

# 1.2 สร้าง Field (ตัวรับข้อมูล) ที่ฉลาดพอจะอ่าน List ของไฟล์ได้ (แก้ปัญหา "ไม่ได้ส่งรูป")
class MultipleFileField(forms.FileField):
    def to_python(self, data):
        if not data:
            return None
        # ถ้าส่งมาเป็น List (หลายไฟล์) ก็คืนค่าเป็น List ไปเลย ไม่ต้อง Validate ทีละอัน
        if isinstance(data, list):
            return [super(MultipleFileField, self).to_python(f) for f in data]
        return data

    def clean(self, data, initial=None):
        # ข้ามการตรวจสอบแบบปกติ (เพราะแบบปกติมันรับได้แค่ไฟล์เดียว)
        return data

# 1. สร้างฟอร์มพิเศษสำหรับ "อัพโหลดหลายรูป"
class CarAdminForm(forms.ModelForm):
    photos = MultipleFileField(
        widget=MultipleFileInput(),
        label='📸 อัพโหลดรูปภาพเพิ่ม (เลือกได้หลายรูป)',
        required=False,
        help_text='กด Ctrl ค้างไว้เพื่อเลือกหลายรูป หรือลากรูปมาวางตรงนี้ได้เลย'
    )

    class Meta:
        model = Car
        fields = '__all__'

    # ✅ เคล็ดลับวิชาตัวเบา: แอบมาใส่ 'multiple' ตรงนี้แทน เพื่อหลบ Error
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photos'].widget.attrs.update({'multiple': True})

# 2. ตัวจัดการรูปภาพที่อัพไปแล้ว (โชว์รูปตัวอย่าง)
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    readonly_fields = ['show_image']

    def show_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="height: 100px; border-radius: 8px;">')
        return "-"
    show_image.short_description = "ตัวอย่าง"

# 3. หน้าจัดการรถ (รวมร่างฟีเจอร์เก่า + ใหม่)
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    form = CarAdminForm  # ใช้ฟอร์มใหม่ที่มีปุ่มอัพรัวๆ
    inlines = [CarImageInline]

    # ฟีเจอร์เดิม: โชว์ราคาแบบมีคอมม่า + แก้สถานะได้เลย
    list_display = ['brand', 'model_name', 'year', 'show_price', 'installment', 'status']
    list_editable = ['status']  # แก้สถานะหน้าแรกได้
    list_filter = ['status', 'brand', 'gear']
    search_fields = ['model_name', 'brand']

    def show_price(self, obj):
        return f"{obj.price:,} บาท"
    show_price.short_description = "ราคา"

    # ฟีเจอร์ใหม่: ระบบเซฟรูปทีเดียวหลายใบ
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        
        # ดึงไฟล์รูปทั้งหมดจากช่อง photos
        images = request.FILES.getlist('photos')
        
        # สร้าง Database รูปภาพทีละใบ
        for img in images:
            CarImage.objects.create(car=form.instance, image=img)