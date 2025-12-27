from django.contrib import admin
from .models import IoTDevice, IoTReading


@admin.register(IoTDevice)
class IoTDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'device_id', 'supplier', 'device_type', 'is_active', 'last_seen']
    list_filter = ['is_active', 'device_type']
    search_fields = ['device_id', 'device_name', 'supplier__name']
    readonly_fields = ['api_key', 'installed_date', 'last_seen']


@admin.register(IoTReading)
class IoTReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'timestamp', 'energy_kwh', 'estimated_emissions_kg']
    list_filter = ['timestamp', 'device']
    search_fields = ['device__device_name', 'device__device_id']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'



