from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls','users')),
    path('liniProduksi/', include('liniProduksi.urls','liniProduksi')),
    path('produk/', include('produk.urls','produk')),
    path('jadwal/', include('jadwal.urls','jadwal')),
    path('engineeringOrder/', include('engineeringOrder.urls','engineeringOrder')),
    path('contributor/',views.contributor, name='contributor'),
    path('home/',views.home, name='home'),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)