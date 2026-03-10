from django.shortcuts import render, get_object_or_404
from .models import Car
from django.db.models import Q, F

def car_list(request):
    query = request.GET.get('q')
    gear_filter = request.GET.get('gear')
    
    # 1. ดึงรถทั้งหมดมาก่อนพร้อมรูปภาพ (Prefetch เพื่อลด N+1 Query)
    all_cars = Car.objects.prefetch_related('images').all().order_by('-created_at')

    # 2. กรองตามคำค้นหา (ถ้ามี)
    if query:
        all_cars = all_cars.filter(
            Q(brand__icontains=query) | 
            Q(model_name__icontains=query) |
            Q(description__icontains=query)
        )
    
    if gear_filter:
        all_cars = all_cars.filter(gear=gear_filter)

    # 3. แยกกอง: รถพร้อมขาย/ติดจอง vs รถขายแล้ว
    available_cars = all_cars.exclude(status='SOLD')
    sold_cars = all_cars.filter(status='SOLD')
    
    context = {
        'available_cars': available_cars,
        'sold_cars': sold_cars,
    }
    
    return render(request, 'showroom/car_list.html', context)

def car_detail(request, pk):
    # ใช้ Prefetch กับหน้า Detail ด้วยเพื่อให้โหลดรูปสไลด์ได้เร็วขึ้น
    car = get_object_or_404(Car.objects.prefetch_related('images'), pk=pk)
    
    # ✅ ใช้ F() expression เพื่อบวกยอดวิวในระดับ Database (ป้องกัน Race Condition และประหยัดทรัพยากร)
    Car.objects.filter(pk=pk).update(views_count=F('views_count') + 1)
    
    # ดึงค่าที่อัปเดตแล้วกลับมาใส่ในตัวแปร car เพื่อแสดงผล
    car.refresh_from_db(fields=['views_count'])
    
    return render(request, 'showroom/car_detail.html', {'car': car})