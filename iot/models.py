from django.db import models
from core.models import Supplier
import secrets


class IoTDevice(models.Model):
    """IoT devices for real-time energy monitoring at supplier facilities"""
    device_id = models.CharField(max_length=100, unique=True, help_text="Unique device identifier")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='iot_devices')
    device_name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=100, help_text="e.g., Smart Meter, Energy Monitor, Sensor")
    location = models.CharField(max_length=255, blank=True, help_text="Physical location description")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    installed_date = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    api_key = models.CharField(max_length=255, unique=True, help_text="API key for device authentication")
    
    class Meta:
        verbose_name = "IoT Device"
        verbose_name_plural = "IoT Devices"
    
    def __str__(self):
        return f"{self.device_name} ({self.device_id}) - {self.supplier.name}"
    
    @staticmethod
    def generate_api_key():
        """Generate a secure API key for device authentication"""
        return secrets.token_urlsafe(48)
    
    def save(self, *args, **kwargs):
        """Auto-generate API key if not provided"""
        if not self.api_key:
            self.api_key = self.generate_api_key()
        super().save(*args, **kwargs)


class IoTReading(models.Model):
    """Real-time energy consumption readings from IoT devices"""
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    energy_kwh = models.DecimalField(max_digits=12, decimal_places=4, help_text="Energy consumption in kWh")
    power_kw = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Instantaneous power in kW")
    voltage = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    current = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    temperature = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Temperature in Celsius")
    # Calculated emissions (based on grid emission factor)
    estimated_emissions_kg = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Estimated CO2e in kg")
    metadata = models.JSONField(default=dict, blank=True, help_text="Additional device-specific data")
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.device.device_name} - {self.timestamp}: {self.energy_kwh} kWh"



