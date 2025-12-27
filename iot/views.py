"""
IoT views for device management and data ingestion
"""
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from iot.models import IoTDevice, IoTReading
from iot.services import IoTDataProcessor
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def ingest_iot_data(request):
    """Endpoint for IoT devices to submit readings"""
    try:
        data = json.loads(request.body)
        device_id = data.get('device_id')
        api_key = data.get('api_key')
        
        # Authenticate device
        device = get_object_or_404(IoTDevice, device_id=device_id, api_key=api_key, is_active=True)
        
        # Update last seen
        from django.utils import timezone
        device.last_seen = timezone.now()
        device.save()
        
        # Create reading
        reading = IoTReading.objects.create(
            device=device,
            energy_kwh=Decimal(str(data.get('energy_kwh', 0))),
            power_kw=Decimal(str(data.get('power_kw', 0))) if data.get('power_kw') else None,
            voltage=Decimal(str(data.get('voltage', 0))) if data.get('voltage') else None,
            current=Decimal(str(data.get('current', 0))) if data.get('current') else None,
            temperature=Decimal(str(data.get('temperature', 0))) if data.get('temperature') else None,
            metadata=data.get('metadata', {}),
        )
        
        # Process reading
        emissions_tons = IoTDataProcessor.process_reading(reading)
        
        return JsonResponse({
            'status': 'success',
            'reading_id': reading.id,
            'estimated_emissions_tons': float(emissions_tons),
        })
    
    except Exception as e:
        logger.error(f"Error ingesting IoT data: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



