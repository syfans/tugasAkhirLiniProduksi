from django.contrib import admin

# Register your models here.
from .models import LiniProduksi, StasiunKerja, KebutuhanMaterial, Proses, PeralatanProduksi, Operator, ProduksiHarian, PengirimanMaterial, Gangguan, WaktuIstirahat, TargetHarian, TargetMingguan, TargetBulanan, TargetTahunan

class LiniProduksiAdmin(admin.ModelAdmin):
    pass


class StasiunKerjaAdmin(admin.ModelAdmin):
    readonly_fields = [
        'liniProduksi',
    ]


class KebutuhanMaterialAdmin(admin.ModelAdmin):
    readonly_fields = [
        'stasiunKerja',
    ]


class ProsesAdmin(admin.ModelAdmin):
    readonly_fields = [
        'stasiunKerja',
    ]


class PeralatanProduksiAdmin(admin.ModelAdmin):
    readonly_fields = [
        'proses',
    ]


class OperatorAdmin(admin.ModelAdmin):
    pass


class ProduksiHarianAdmin(admin.ModelAdmin):
    pass


admin.site.register(WaktuIstirahat)
admin.site.register(ProduksiHarian, ProduksiHarianAdmin)
admin.site.register(LiniProduksi, LiniProduksiAdmin)
admin.site.register(StasiunKerja, StasiunKerjaAdmin)
admin.site.register(KebutuhanMaterial, KebutuhanMaterialAdmin)
admin.site.register(Proses, ProsesAdmin)
admin.site.register(PeralatanProduksi,PeralatanProduksiAdmin)
admin.site.register(Operator,OperatorAdmin)
admin.site.register(PengirimanMaterial)
admin.site.register(Gangguan)
admin.site.register(TargetHarian)
admin.site.register(TargetMingguan)
admin.site.register(TargetBulanan)
admin.site.register(TargetTahunan)