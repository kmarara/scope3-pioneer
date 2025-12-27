from django.db import models
from core.models import EmissionEntry
import hashlib
import json


class BlockchainVerification(models.Model):
    """Blockchain verification records for emission data integrity"""
    emission_entry = models.OneToOneField(EmissionEntry, on_delete=models.CASCADE, related_name='blockchain_verification')
    transaction_hash = models.CharField(max_length=255, unique=True, help_text="Blockchain transaction hash")
    block_number = models.BigIntegerField(null=True, blank=True)
    block_timestamp = models.DateTimeField(null=True, blank=True)
    network = models.CharField(max_length=50, default='ethereum', help_text="Blockchain network (ethereum, polygon, etc.)")
    verified_at = models.DateTimeField(auto_now_add=True)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    data_hash = models.CharField(max_length=255, help_text="Hash of the emission data")
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-verified_at']
    
    def __str__(self):
        return f"Verification for Entry {self.emission_entry.id}: {self.transaction_hash[:16]}..."
    
    @staticmethod
    def generate_data_hash(emission_entry):
        """Generate hash of emission entry data for blockchain verification"""
        data = {
            'supplier_id': emission_entry.supplier.id,
            'supplier_code': emission_entry.supplier.supplier_code,
            'date_reported': emission_entry.date_reported.isoformat(),
            'scope3_emissions': str(emission_entry.scope3_emissions),
            'notes': emission_entry.notes,
        }
        data_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()



