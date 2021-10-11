from django.contrib import admin

# Register your models here.
from .models import JadwalLiniProduksi

class JadwalLiniProduksiAdmin(admin.ModelAdmin):
    pass


admin.site.register(JadwalLiniProduksi, JadwalLiniProduksiAdmin)