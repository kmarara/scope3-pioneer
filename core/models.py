from django.db import models

# Create your models here.

# Starting with the supplier model
class Supplier(models.Model):
    supplier_code = models.CharField(max_length=50, unique=True, default="TEMP_CODE")
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(unique=True)
    industry = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    # Related emission entries will be linked from EmissionEntry

    def __str__(self):
        return f"{self.name} ({self.region})"


# Now we move to the Emissions Entry class/model
class EmissionEntry(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='emission_entries')
    date_reported = models.DateTimeField()
    scope3_emissions = models.DecimalField(max_digits=12, decimal_places=2) # Flexible for larger numbers
    evidence_file = models.FileField(upload_to='evidence/', blank=True, null=True)
    notes = models.TextField(blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.supplier.name} emmision on {self.date_reported}: {self.scope3_emissions} tons"