from django.contrib import admin
from django.urls import path

from . import views
app_name = 'engineeringOrder'

urlpatterns = [
    path('tidakDisetujui/', views.tidakDisetujui, name='tidakDisetujui'),
    path('disetujui/', views.disetujui, name='disetujui'),
    path('belumDisetujui/', views.belumDisetujui, name='belumDisetujui'),
    path('tidakSetujuEngineeringOrder/<str:tidakSetuju_id>', views.tidakSetuju, name='tidakSetujuEO'),
    path('setujuEngineeringOrder/prosesEO/prosesBaruEO/<str:setuju_id>', views.prosesBaruEO, name='prosesBaruEO'),
    path('setujuEngineeringOrder/prosesLamaBerlakuEO/prosesEO/prosesBaruEO/<str:setuju_id>', views.prosesBaruEO, name='prosesBaruEO'),
    path('setujuEngineeringOrder/prosesLamaTidakBerlakuEO/prosesEO/prosesBaruEO/<str:setuju_id>', views.prosesBaruEO, name='prosesBaruEO'),
    path('setujuEngineeringOrder/prosesLamaBerlakuEO/<str:setuju_id>', views.prosesLamaBerlakuEO, name='prosesLamaBerlakuEO'),
    path('setujuEngineeringOrder/prosesLamaTidakBerlakuEO/<str:setuju_id>', views.prosesLamaTidakBerlakuEO, name='prosesLamaTidakBerlakuEO'),
    path('setujuEngineeringOrder/prosesBerlakuEO/<str:setuju_id>', views.prosesBerlakuEO, name='prosesBerlakuEO'),
    path('setujuEngineeringOrder/prosesLamaEO/<str:setuju_id>', views.prosesLamaEO, name='prosesLamaEO'),
    path('setujuEngineeringOrder/prosesEO/<str:setuju_id>', views.prosesEO, name='prosesEO'),
    path('setujuEngineeringOrder/<str:setuju_id>', views.setuju, name='setujuEO'),
    path('deleteEngineeringOrder/<str:delete_id>', views.deleteEO, name='deleteEO'),
    path('newEngineeringOrder/', views.newEO, name='newEO'),
    path('', views.index, name='index'),
]