from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
# Below are the data models I implemented for this project

# Starting with the supplier model
class Supplier(models.Model):
    supplier_code = models.CharField(max_length=50, unique=True, default="TEMP_CODE")
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(unique=True)
    industry = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    # SaaS: Link to tenant/organization
    tenant = models.ForeignKey('saas.Tenant', on_delete=models.CASCADE, null=True, blank=True, related_name='suppliers')
    # Additional fields for ML and spend-based estimation
    annual_spend = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text="Annual spend in USD")
    emission_factor = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Emission factor (tCO2e/$)")
    # Related emission entries will be linked from EmissionEntry

    def __str__(self):
        return f"{self.name} ({self.region})"
    
    def get_estimated_emissions_from_spend(self):
        """Calculate estimated emissions based on spend and emission factor"""
        if self.annual_spend and self.emission_factor:
            return self.annual_spend * self.emission_factor
        return None


# Now we move to the Emissions Entry class/model
class EmissionEntry(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='emission_entries')
    date_reported = models.DateTimeField()
    scope3_emissions = models.DecimalField(max_digits=12, decimal_places=2) # Flexible for larger numbers
    evidence_file = models.FileField(upload_to='evidence/', blank=True, null=True)
    notes = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    # Blockchain verification
    blockchain_hash = models.CharField(max_length=255, blank=True, null=True, help_text="Blockchain verification hash")
    blockchain_verified = models.BooleanField(default=False)
    # Data source tracking
    DATA_SOURCE_CHOICES = [
        ('manual', 'Manual Entry'),
        ('iot', 'IoT Device'),
        ('ml_estimate', 'ML Estimate'),
        ('spend_based', 'Spend-Based Estimate'),
    ]
    data_source = models.CharField(max_length=20, choices=DATA_SOURCE_CHOICES, default='manual')
    # ML confidence score
    ml_confidence = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True, help_text="ML model confidence (0-1)")

    def __str__(self):
        return f"{self.supplier.name} emission on {self.date_reported}: {self.scope3_emissions} tons"