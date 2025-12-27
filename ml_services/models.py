from django.db import models
from core.models import Supplier, EmissionEntry
from decimal import Decimal


class MLModel(models.Model):
    """Tracks ML models used for predictions"""
    MODEL_TYPE_CHOICES = [
        ('hotspot', 'Hotspot Prediction'),
        ('spend_estimate', 'Spend-Based Estimation'),
        ('anomaly', 'Anomaly Detection'),
        ('forecast', 'Emission Forecasting'),
    ]
    name = models.CharField(max_length=255)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPE_CHOICES)
    version = models.CharField(max_length=50, default='1.0')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    model_path = models.CharField(max_length=500, blank=True, help_text="Path to saved model file")
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    training_data_size = models.IntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.name} v{self.version} ({self.model_type})"


class MLPrediction(models.Model):
    """Stores ML predictions for emissions and hotspots"""
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='ml_predictions')
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE, related_name='predictions')
    predicted_emissions = models.DecimalField(max_digits=12, decimal_places=2, help_text="Predicted emissions in tCO2e")
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, help_text="Confidence score (0-1)")
    is_hotspot = models.BooleanField(default=False, help_text="Flagged as emission hotspot")
    hotspot_reason = models.TextField(blank=True, help_text="Explanation for hotspot classification")
    prediction_date = models.DateTimeField(auto_now_add=True)
    period_start = models.DateField(help_text="Start of prediction period")
    period_end = models.DateField(help_text="End of prediction period")
    input_features = models.JSONField(default=dict, help_text="Features used for prediction")
    # Link to actual emission entry if prediction was validated
    validated_entry = models.ForeignKey(EmissionEntry, on_delete=models.SET_NULL, null=True, blank=True, related_name='validated_predictions')
    
    class Meta:
        ordering = ['-prediction_date']
    
    def __str__(self):
        return f"Prediction for {self.supplier.name}: {self.predicted_emissions} tCO2e (confidence: {self.confidence_score})"


class SpendBasedEstimate(models.Model):
    """Spend-based emission estimates using industry emission factors"""
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='spend_estimates')
    period_start = models.DateField()
    period_end = models.DateField()
    spend_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Spend in USD")
    emission_factor = models.DecimalField(max_digits=10, decimal_places=4, help_text="Emission factor (tCO2e/$)")
    estimated_emissions = models.DecimalField(max_digits=12, decimal_places=2, help_text="Estimated emissions in tCO2e")
    industry_category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Link to actual entry if validated
    validated_entry = models.ForeignKey(EmissionEntry, on_delete=models.SET_NULL, null=True, blank=True, related_name='spend_estimates')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Estimate for {self.supplier.name}: {self.estimated_emissions} tCO2e from ${self.spend_amount}"



