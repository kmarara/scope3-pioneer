from django.contrib import admin
from .models import MLModel, MLPrediction, SpendBasedEstimate


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'version', 'is_active', 'accuracy_score']
    list_filter = ['model_type', 'is_active']
    search_fields = ['name']


@admin.register(MLPrediction)
class MLPredictionAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'model', 'predicted_emissions', 'is_hotspot', 'confidence_score', 'prediction_date']
    list_filter = ['is_hotspot', 'model', 'prediction_date']
    search_fields = ['supplier__name']


@admin.register(SpendBasedEstimate)
class SpendBasedEstimateAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'spend_amount', 'estimated_emissions', 'emission_factor', 'created_at']
    list_filter = ['created_at', 'industry_category']
    search_fields = ['supplier__name']



