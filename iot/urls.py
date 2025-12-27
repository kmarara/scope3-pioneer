"""
IoT URLs
"""
from django.urls import path
from .views import ingest_iot_data

urlpatterns = [
    path('ingest/', ingest_iot_data, name='iot_ingest'),
]



