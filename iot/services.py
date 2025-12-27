"""
IoT services for real-time data processing
"""
from iot.models import IoTDevice, IoTReading
from core.models import EmissionEntry, Supplier
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta, datetime
import logging

logger = logging.getLogger(__name__)

# Grid emission factors by region (kg CO2e per kWh)
GRID_EMISSION_FACTORS = {
    'zimbabwe': Decimal('0.85'),  # kg CO2e/kWh
    'south_africa': Decimal('0.95'),
    'kenya': Decimal('0.35'),
    'default': Decimal('0.50'),
}


class IoTDataProcessor:
    """Process IoT readings and convert to emissions"""
    
    @staticmethod
    def get_emission_factor(region=None):
        """Get grid emission factor for region"""
        if region:
            region_lower = region.lower().replace(' ', '_')
            return GRID_EMISSION_FACTORS.get(region_lower, GRID_EMISSION_FACTORS['default'])
        return GRID_EMISSION_FACTORS['default']
    
    @staticmethod
    def process_reading(reading):
        """Process IoT reading and calculate emissions"""
        # Get emission factor for supplier's region
        supplier = reading.device.supplier
        emission_factor = IoTDataProcessor.get_emission_factor(supplier.region)
        
        # Calculate emissions: kWh * factor = kg CO2e
        # Convert to tons: kg / 1000
        emissions_kg = reading.energy_kwh * emission_factor
        emissions_tons = emissions_kg / Decimal('1000')
        reading.estimated_emissions_kg = emissions_kg
        reading.save()
        
        return emissions_tons
    
    @staticmethod
    def aggregate_daily_emissions(device, date):
        """Aggregate daily emissions from IoT readings"""
        start = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time()))
        end = start + timedelta(days=1)
        
        readings = IoTReading.objects.filter(
            device=device,
            timestamp__gte=start,
            timestamp__lt=end
        )
        
        total_energy = sum([r.energy_kwh for r in readings])
        total_emissions_kg = sum([r.estimated_emissions_kg for r in readings if r.estimated_emissions_kg])
        total_emissions_tons = total_emissions_kg / Decimal('1000')
        
        return {
            'total_energy_kwh': total_energy,
            'total_emissions_tons': total_emissions_tons,
            'reading_count': readings.count(),
        }
    
    @staticmethod
    def create_emission_entry_from_iot(device, date, aggregated_data):
        """Create emission entry from aggregated IoT data"""
        entry = EmissionEntry.objects.create(
            supplier=device.supplier,
            date_reported=timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time())),
            scope3_emissions=aggregated_data['total_emissions_tons'],
            data_source='iot',
            notes=f"Auto-generated from IoT device {device.device_name} ({device.device_id})",
        )
        
        logger.info(f"Created emission entry {entry.id} from IoT device {device.device_id}")
        return entry
