from django.contrib import admin
from .models import Supplier, EmissionEntry


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier_code', 'region', 'industry', 'active', 'tenant']
    list_filter = ['active', 'region', 'industry', 'tenant']
    search_fields = ['name', 'supplier_code', 'contact_email']
    readonly_fields = ['added_on']


@admin.register(EmissionEntry)
class EmissionEntryAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'date_reported', 'scope3_emissions', 'data_source', 'verified', 'blockchain_verified']
    list_filter = ['verified', 'blockchain_verified', 'data_source', 'date_reported']
    search_fields = ['supplier__name', 'notes']
    readonly_fields = ['blockchain_hash']