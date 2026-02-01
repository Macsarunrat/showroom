from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from showroom import views # นำเข้า views ที่เราเพิ่งเขียน

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.car_list, name='car_list'), # หน้าแรก
    path('car/<int:pk>/', views.car_detail, name='car_detail'), # หน้ารายละเอียด
]

# สำคัญมาก! บรรทัดนี้ทำให้โชว์รูปที่อัพโหลดได้ในโหมด DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)