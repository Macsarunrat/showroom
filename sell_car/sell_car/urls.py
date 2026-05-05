"""
URL configuration for sell_car project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from showroom import views # นำเข้า views ที่เราเพิ่งเขียน

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.car_list, name='car_list'), # หน้าแรก
    path('car/<int:pk>/', views.car_detail, name='car_detail'), # หน้ารายละเอียด
    
    # === PWA Files สำหรับลูกค้า (หน้าบ้าน) ===
    path('manifest.json', TemplateView.as_view(template_name='showroom/manifest.json', content_type='application/manifest+json')),
    path('sw.js', TemplateView.as_view(template_name='showroom/sw.js', content_type='application/javascript')),

    # === PWA Files สำหรับ Admin (หลังบ้าน) ===
    path('manifest-admin.json', TemplateView.as_view(template_name='showroom/manifest-admin.json', content_type='application/manifest+json')),
    path('sw-admin.js', TemplateView.as_view(template_name='showroom/sw-admin.js', content_type='application/javascript')),
]

# สำคัญมาก! บรรทัดนี้ทำให้โชว์รูปที่อัพโหลดได้ในโหมด DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)