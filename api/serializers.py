"""
REST API serializers
"""
from rest_framework import serializers
from core.models import Supplier, EmissionEntry
from iot.models import IoTDevice, IoTReading
from ml_services.models import MLPrediction, SpendBasedEstimate
from scenarios.models import Scenario, ScenarioSupplier
from saas.models import Tenant, APIKey


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class EmissionEntrySerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    
    class Meta:
        model = EmissionEntry
        fields = '__all__'


class IoTDeviceSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    
    class Meta:
        model = IoTDevice
        fields = '__all__'
        extra_kwargs = {'api_key': {'read_only': True}}


class IoTReadingSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.device_name', read_only=True)
    
    class Meta:
        model = IoTReading
        fields = '__all__'


class MLPredictionSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    
    class Meta:
        model = MLPrediction
        fields = '__all__'


class SpendBasedEstimateSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    
    class Meta:
        model = SpendBasedEstimate
        fields = '__all__'


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'


class ScenarioSupplierSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    scenario_name = serializers.CharField(source='scenario.name', read_only=True)
    
    class Meta:
        model = ScenarioSupplier
        fields = '__all__'



