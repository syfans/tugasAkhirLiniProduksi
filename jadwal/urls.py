from django.contrib import admin
from django.urls import path

from . import views
app_name = 'jadwal'

urlpatterns = [
    path('belumKonfirmasi/<str:idStasiunKerjaInput>/', views.belumKonfirmasi_SK, name='belumKonfirmasi_SK'),
    path('belumKonfirmasi/', views.belumKonfirmasi, name='belumKonfirmasi'),
    path('sudahKonfirmasi/<str:idStasiunKerjaInput>/', views.sudahKonfirmasi_SK, name='sudahKonfirmasi_SK'),
    path('sudahKonfirmasi/', views.sudahKonfirmasi, name='sudahKonfirmasi'),
    path('konfirmasi/<str:konfirmasi_id>', views.newKonfirmasi, name='konfirmasi'),
    path('jadwalTersedia/', views.jadwalTersedia, name='jadwalTersedia'),
    path('permintaanMaterial/<str:pm_id>', views.permintaanMaterial, name='permintaanMaterial'),
    path('<str:idStasiunKerjaInput>/', views.index_SK, name='index_SK'),
    path('', views.index, name='index'),
]