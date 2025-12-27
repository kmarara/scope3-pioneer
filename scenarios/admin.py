from django.contrib import admin
from .models import Scenario, ScenarioSupplier


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['name', 'scenario_type', 'baseline_emissions', 'projected_emissions', 'reduction_percentage', 'created_at']
    list_filter = ['scenario_type', 'created_at']
    search_fields = ['name', 'description']


@admin.register(ScenarioSupplier)
class ScenarioSupplierAdmin(admin.ModelAdmin):
    list_display = ['scenario', 'supplier', 'baseline_emissions', 'projected_emissions', 'reduction_percentage']
    list_filter = ['scenario']
    search_fields = ['supplier__name', 'scenario__name']



