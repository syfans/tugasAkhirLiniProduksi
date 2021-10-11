from django.contrib import admin

from .models import EngineeringOrder
# Register your models here.

class EngineeringOrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(EngineeringOrder, EngineeringOrderAdmin)