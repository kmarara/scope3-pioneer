"""
REST API views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import timedelta

from core.models import Supplier, EmissionEntry
from iot.models import IoTDevice, IoTReading
from iot.services import IoTDataProcessor
from ml_services.models import MLPrediction, SpendBasedEstimate
from ml_services.services import MLPredictionService, SpendBasedEstimator, HotspotPredictor
from blockchain.services import BlockchainService
from scenarios.models import Scenario, ScenarioSupplier
from .serializers import (
    SupplierSerializer, EmissionEntrySerializer,
    IoTDeviceSerializer, IoTReadingSerializer,
    MLPredictionSerializer, SpendBasedEstimateSerializer,
    ScenarioSerializer, ScenarioSupplierSerializer,
)


class SupplierViewSet(viewsets.ModelViewSet):
    """Supplier API endpoints"""
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter by tenant if using SaaS
        user = self.request.user
        if hasattr(user, 'tenant_membership'):
            return Supplier.objects.filter(tenant=user.tenant_membership.tenant)
        return Supplier.objects.all()
    
    @action(detail=True, methods=['get'])
    def emissions(self, request, pk=None):
        """Get emissions for a supplier"""
        supplier = self.get_object()
        entries = EmissionEntry.objects.filter(supplier=supplier)
        serializer = EmissionEntrySerializer(entries, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def predict_hotspot(self, request, pk=None):
        """Predict if supplier is a hotspot"""
        supplier = self.get_object()
        prediction = MLPredictionService.create_prediction(supplier, model_type='hotspot')
        serializer = MLPredictionSerializer(prediction)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def estimate_from_spend(self, request, pk=None):
        """Estimate emissions from spend"""
        supplier = self.get_object()
        spend_amount = request.data.get('spend_amount')
        period_start = request.data.get('period_start')
        period_end = request.data.get('period_end')
        
        if not spend_amount:
            return Response({'error': 'spend_amount required'}, status=status.HTTP_400_BAD_REQUEST)
        
        estimate = SpendBasedEstimator.estimate_emissions(
            supplier, spend_amount, period_start, period_end
        )
        serializer = SpendBasedEstimateSerializer(estimate)
        return Response(serializer.data)


class EmissionEntryViewSet(viewsets.ModelViewSet):
    """Emission entry API endpoints"""
    serializer_class = EmissionEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'tenant_membership'):
            return EmissionEntry.objects.filter(supplier__tenant=user.tenant_membership.tenant)
        return EmissionEntry.objects.all()
    
    @action(detail=True, methods=['post'])
    def verify_blockchain(self, request, pk=None):
        """Verify emission entry on blockchain"""
        entry = self.get_object()
        blockchain_service = BlockchainService()
        verification = blockchain_service.verify_emission_entry(entry)
        return Response({
            'transaction_hash': verification.transaction_hash,
            'status': verification.verification_status,
        })


class IoTDeviceViewSet(viewsets.ModelViewSet):
    """IoT device API endpoints"""
    serializer_class = IoTDeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'tenant_membership'):
            return IoTDevice.objects.filter(supplier__tenant=user.tenant_membership.tenant)
        return IoTDevice.objects.all()
    
    @action(detail=True, methods=['post'])
    def readings(self, request, pk=None):
        """Submit IoT reading"""
        device = self.get_object()
        
        # Verify API key matches device
        api_key = request.META.get('HTTP_X_API_KEY') or request.GET.get('api_key')
        if api_key != device.api_key:
            return Response({'error': 'Invalid API key for device'}, status=status.HTTP_401_UNAUTHORIZED)
        
        reading = IoTReading.objects.create(
            device=device,
            energy_kwh=request.data.get('energy_kwh'),
            power_kw=request.data.get('power_kw'),
            voltage=request.data.get('voltage'),
            current=request.data.get('current'),
            temperature=request.data.get('temperature'),
            metadata=request.data.get('metadata', {}),
        )
        
        # Process reading
        IoTDataProcessor.process_reading(reading)
        
        serializer = IoTReadingSerializer(reading)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def recent_readings(self, request, pk=None):
        """Get recent readings for device"""
        device = self.get_object()
        hours = int(request.query_params.get('hours', 24))
        since = timezone.now() - timedelta(hours=hours)
        
        readings = IoTReading.objects.filter(device=device, timestamp__gte=since)
        serializer = IoTReadingSerializer(readings, many=True)
        return Response(serializer.data)


class MLPredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """ML prediction API endpoints"""
    serializer_class = MLPredictionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'tenant_membership'):
            return MLPrediction.objects.filter(supplier__tenant=user.tenant_membership.tenant)
        return MLPrediction.objects.all()
    
    @action(detail=False, methods=['get'])
    def hotspots(self, request):
        """Get all hotspot predictions"""
        hotspots = self.get_queryset().filter(is_hotspot=True)
        serializer = self.get_serializer(hotspots, many=True)
        return Response(serializer.data)


class ScenarioViewSet(viewsets.ModelViewSet):
    """Scenario modeling API endpoints"""
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'tenant_membership'):
            return Scenario.objects.filter(tenant=user.tenant_membership.tenant)
        return Scenario.objects.all()
    
    @action(detail=True, methods=['post'])
    def calculate(self, request, pk=None):
        """Calculate scenario reduction"""
        from scenarios.services import ScenarioService
        scenario = self.get_object()
        result = ScenarioService.calculate_scenario(scenario)
        return Response(result)
