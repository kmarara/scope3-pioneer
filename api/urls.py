"""
API URL configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    SupplierViewSet, EmissionEntryViewSet,
    IoTDeviceViewSet, MLPredictionViewSet,
    ScenarioViewSet,
)

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r'emissions', EmissionEntryViewSet, basename='emission')
router.register(r'iot/devices', IoTDeviceViewSet, basename='iot-device')
router.register(r'ml/predictions', MLPredictionViewSet, basename='ml-prediction')
router.register(r'scenarios', ScenarioViewSet, basename='scenario')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
]



