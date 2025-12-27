from django.db import models
from core.models import Supplier
from decimal import Decimal


class Scenario(models.Model):
    """What-if scenario modeling for emission reduction strategies"""
    SCENARIO_TYPE_CHOICES = [
        ('supplier_switch', 'Supplier Switch'),
        ('renewable_energy', 'Renewable Energy Adoption'),
        ('efficiency', 'Energy Efficiency Improvement'),
        ('transport_optimization', 'Transport Optimization'),
        ('custom', 'Custom Strategy'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scenario_type = models.CharField(max_length=50, choices=SCENARIO_TYPE_CHOICES)
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, null=True, blank=True, related_name='scenarios')
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    baseline_emissions = models.DecimalField(max_digits=12, decimal_places=2, help_text="Baseline emissions in tCO2e")
    projected_emissions = models.DecimalField(max_digits=12, decimal_places=2, help_text="Projected emissions in tCO2e")
    reduction_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage reduction")
    reduction_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Absolute reduction in tCO2e")
    implementation_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text="Estimated cost in USD")
    payback_period_years = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    parameters = models.JSONField(default=dict, help_text="Scenario-specific parameters")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.reduction_percentage}% reduction"
    
    def calculate_reduction(self):
        """Calculate reduction metrics"""
        if self.baseline_emissions and self.projected_emissions:
            self.reduction_amount = self.baseline_emissions - self.projected_emissions
            if self.baseline_emissions > 0:
                self.reduction_percentage = (self.reduction_amount / self.baseline_emissions) * 100
            self.save()


class ScenarioSupplier(models.Model):
    """Links suppliers to scenarios for targeted modeling"""
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='scenario_suppliers')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='scenario_participations')
    baseline_emissions = models.DecimalField(max_digits=12, decimal_places=2)
    projected_emissions = models.DecimalField(max_digits=12, decimal_places=2)
    reduction_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    intervention_details = models.TextField(blank=True, help_text="Specific intervention for this supplier")
    
    class Meta:
        unique_together = ['scenario', 'supplier']
    
    def __str__(self):
        return f"{self.scenario.name} - {self.supplier.name}"



