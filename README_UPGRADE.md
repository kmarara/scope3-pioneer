# Scope 3 Tracker - AI-Powered Upgrade

## 🚀 New Features

### 1. **IoT Integration** 📡
- Real-time energy monitoring from IoT devices
- Automatic emission calculation from energy consumption
- Device management and API key authentication
- Endpoints: `/iot/ingest/` for device data ingestion

### 2. **Machine Learning Services** 🤖
- **Hotspot Prediction**: Identifies high-emission suppliers using Isolation Forest
- **Spend-Based Estimation**: Estimates emissions from procurement spend using industry factors
- **Anomaly Detection**: Flags unusual emission patterns
- Models stored in `ml_models/` directory

### 3. **Blockchain Verification** ⛓️
- Immutable verification of emission data
- Transaction hashing for data integrity
- Supports multiple blockchain networks (Ethereum, Polygon, etc.)
- Automatic verification on emission entry creation

### 4. **Scenario Modeling** 📊
- "What-if" analysis for emission reduction strategies
- Supports multiple scenario types:
  - Supplier switching
  - Renewable energy adoption
  - Energy efficiency improvements
  - Transport optimization
- Calculates baseline vs. projected emissions and reduction percentages

### 5. **SaaS Multi-Tenancy** 🏢
- Multi-tenant architecture for organizations
- Subscription tiers (Free, Starter, Professional, Enterprise)
- API key management for programmatic access
- User roles and permissions per tenant

### 6. **REST API** 🔌
- Full REST API using Django REST Framework
- Token and API key authentication
- Endpoints for all major features
- API documentation at `/api/`

### 7. **AWS Lambda Serverless** ☁️
- Serverless functions for scalable processing
- IoT data processing function
- Batch ML prediction function
- Deploy with Serverless Framework

## 📦 Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Create superuser:**
```bash
python manage.py createsuperuser
```

4. **Load initial data (optional):**
```bash
python manage.py loaddata initial_data.json
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file:
```
SECRET_KEY=your-secret-key
DEBUG=True
BLOCKCHAIN_NETWORK=ethereum
BLOCKCHAIN_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

### Database
Default is SQLite. For production, update `settings.py` to use PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'scope3_tracker',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Deployment

### AWS Lambda Deployment
1. Install Serverless Framework:
```bash
npm install -g serverless
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Deploy functions:
```bash
cd lambda_functions
serverless deploy
```

## 📊 Usage

### API Endpoints

#### Suppliers
- `GET /api/suppliers/` - List suppliers
- `POST /api/suppliers/` - Create supplier
- `GET /api/suppliers/{id}/emissions/` - Get supplier emissions
- `POST /api/suppliers/{id}/predict_hotspot/` - Predict hotspot
- `POST /api/suppliers/{id}/estimate_from_spend/` - Estimate from spend

#### Emissions
- `GET /api/emissions/` - List emissions
- `POST /api/emissions/` - Create emission entry
- `POST /api/emissions/{id}/verify_blockchain/` - Verify on blockchain

#### IoT
- `GET /api/iot/devices/` - List devices
- `POST /api/iot/devices/{id}/readings/` - Submit reading
- `GET /api/iot/devices/{id}/recent_readings/` - Get recent readings

#### ML
- `GET /api/ml/predictions/` - List predictions
- `GET /api/ml/predictions/hotspots/` - Get hotspots

#### Scenarios
- `GET /api/scenarios/` - List scenarios
- `POST /api/scenarios/` - Create scenario
- `POST /api/scenarios/{id}/calculate/` - Calculate scenario

### IoT Device Integration

1. Register device in admin or via API
2. Use device API key for authentication
3. Send readings to `/iot/ingest/`:
```json
{
  "device_id": "device_123",
  "api_key": "your-api-key",
  "energy_kwh": 150.5,
  "power_kw": 12.3,
  "voltage": 240.0,
  "current": 5.1,
  "temperature": 25.0
}
```

### ML Model Training

Train hotspot prediction model:
```python
from ml_services.services import HotspotPredictor

predictor = HotspotPredictor(model_version='1.0')
predictor.train()
```

### Scenario Modeling

Create a scenario:
```python
from scenarios.services import ScenarioService
from core.models import Supplier

suppliers = Supplier.objects.filter(region='Zimbabwe')
scenario = ScenarioService.create_scenario(
    name='Renewable Energy Adoption',
    scenario_type='renewable_energy',
    suppliers=suppliers,
    parameters={'reduction_percentage': 35}
)
```

## 📈 Dashboard

Access the enhanced dashboard at `/dashboard/` to see:
- Total emissions and trends
- ML hotspot predictions
- IoT device status
- Scenario modeling results
- Data source breakdown
- Verification statistics

## 🔐 Authentication

### API Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -d "username=your_username&password=your_password"
```

### API Key
```bash
curl -H "X-API-Key: your-api-key" \
  http://localhost:8000/api/suppliers/
```

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

## 📝 Next Steps

1. **Production Deployment:**
   - Set up PostgreSQL database
   - Configure AWS services (Lambda, S3, DynamoDB)
   - Set up CI/CD pipeline
   - Configure monitoring and logging

2. **ML Model Improvements:**
   - Collect more training data
   - Experiment with different algorithms
   - Add TensorFlow models for deep learning
   - Implement model versioning

3. **Blockchain Integration:**
   - Connect to actual blockchain network
   - Implement smart contracts for verification
   - Add gas fee management

4. **Frontend:**
   - Build React dashboard
   - Create supplier portal
   - Add data visualization charts

## 🤝 Contributing

This is an enterprise-grade Scope 3 tracking platform. Contributions welcome!

## 📄 License

Proprietary - All rights reserved



