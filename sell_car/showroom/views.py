from django.shortcuts import render, get_object_or_404
from .models import Car

# ในไฟล์ showroom/views.py

from django.db.models import Q # เพิ่มบรรทัดนี้ด้านบนสุด

# ในไฟล์ showroom/views.py

def car_list(request):
    query = request.GET.get('q')
    gear_filter = request.GET.get('gear')
    
    # 1. ดึงรถทั้งหมดมาก่อน
    all_cars = Car.objects.all().order_by('-created_at')

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
    # exclude('SOLD') = เอาทุกสถานะ ยกเว้น 'SOLD'
    available_cars = all_cars.exclude(status='SOLD')
    
    # filter('SOLD') = เอาเฉพาะ 'SOLD'
    sold_cars = all_cars.filter(status='SOLD')
    
    context = {
        'available_cars': available_cars,
        'sold_cars': sold_cars,
    }
    
    return render(request, 'showroom/car_list.html', context)
def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    # แก้บรรทัดนี้ด้วย: เปลี่ยน 'garage/...' เป็น 'showroom/...'
    return render(request, 'showroom/car_detail.html', {'car': car})