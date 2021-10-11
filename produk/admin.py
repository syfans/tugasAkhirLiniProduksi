from django.contrib import admin

from .models import Brand, Model, Varian, Material
# Register your models here.

class BrandAdmin(admin.ModelAdmin):
    pass


class ModelAdmin(admin.ModelAdmin):
    pass

class VarianAdmin(admin.ModelAdmin):
    pass


class MaterialAdmin(admin.ModelAdmin):
    pass

admin.site.register(Brand, BrandAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Varian, VarianAdmin)
admin.site.register(Material, MaterialAdmin)