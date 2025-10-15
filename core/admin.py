from django.contrib import admin
from .models import Supplier, EmissionEntry


# Register your models here.
#ckue
# We start with Supplier Admin

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_code', 'name', 'region', 'industry', 'active', 'contact_email')
    search_fields = ('supplier_code', 'name', 'region', 'industry')


# EmissionEntry admin registry
@admin.register(EmissionEntry)
class EmissionEntryAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'date_reported', 'scope3_emissions', 'verified')
    list_filter = ('verified', 'date_reported', 'supplier')