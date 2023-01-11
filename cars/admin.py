from django.contrib import admin

from .models import Car, Refuel, Service


# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'reg_plate', 'mileage', 'last_service_mileage', 'slug')
    prepopulated_fields = {"slug": ("brand", "model")}


class RefuelAdmin(admin.ModelAdmin):
    list_display = ("car", "mileage", "liters", "city", "date")


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("car", "service_type", "mileage", "description", "date_reported", "date_fixed", "is_active")


admin.site.register(Car, CarAdmin)
admin.site.register(Refuel, RefuelAdmin)
admin.site.register(Service, ServiceAdmin)
