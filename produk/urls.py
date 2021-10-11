from django.contrib import admin
from django.urls import path

from . import views, viewsMaterial
app_name = 'produk'

urlpatterns = [
    path('riwayatMaterial/<str:idRiwayatMaterial>', viewsMaterial.riwayat, name='riwayatMaterial'),
    path('updateMaterial/<str:update_id>', viewsMaterial.updateMaterial, name='updateMaterial'),
    path('deleteMaterial/<str:delete_id>', viewsMaterial.deleteMaterial, name='deleteMaterial'),
    path('newMaterial/', viewsMaterial.newMaterial, name='newMaterial'),
    path('updateVarian/<str:update_id>', views.updateVarian, name='updateVarian'),
    path('deleteVarian/<str:delete_id>', views.deleteVarian, name='deleteVarian'),
    path('newVarian/', views.newVarian, name='newVarian'),
    path('<str:idVarianInput>/', viewsMaterial.billOfMaterial, name='billOfMaterial'),
    path('', views.index, name='index'),
]