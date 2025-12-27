# Quick Start Guide

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

## 📍 Key URLs

- **Admin Panel**: http://localhost:8000/admin/
- **Dashboard**: http://localhost:8000/dashboard/
- **API Root**: http://localhost:8000/api/
- **IoT Ingest**: http://localhost:8000/iot/ingest/

## 🔑 Quick API Test

### Get API Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -d "username=your_username&password=your_password"
```

### List Suppliers
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/suppliers/
```

## 📊 Create Your First Scenario

1. Go to Admin → Scenarios → Add Scenario
2. Fill in:
   - Name: "Renewable Energy Plan"
   - Scenario Type: "Renewable Energy Adoption"
   - Select suppliers
3. Click "Calculate" to see reduction projections

## 🔌 Connect IoT Device

1. Create supplier in admin
2. Go to IoT Devices → Add Device
3. Copy the API key
4. Send test reading:
```bash
curl -X POST http://localhost:8000/iot/ingest/ \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "TEST_001",
    "api_key": "your-api-key",
    "energy_kwh": 100.5
  }'
```

## 🤖 Run ML Prediction

In Django shell:
```python
from core.models import Supplier
from ml_services.services import MLPredictionService

supplier = Supplier.objects.first()
prediction = MLPredictionService.create_prediction(supplier)
print(f"Hotspot: {prediction.is_hotspot}, Confidence: {prediction.confidence_score}")
```

## ✅ Next Steps

1. Add suppliers and emission entries
2. Connect IoT devices
3. Train ML models with historical data
4. Create scenarios for reduction planning
5. Set up blockchain verification
6. Configure multi-tenant SaaS

For detailed documentation, see `README_UPGRADE.md`



