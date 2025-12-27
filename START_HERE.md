# 🚀 START HERE - Get the App Running!

## Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
cd /home/recursivex/Energy_projects/project3/scope3_tracker
pip install -r requirements.txt
```

**Note**: If you don't have a virtual environment, create one first:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Create All Migrations
```bash
python manage.py makemigrations
```

This will create migrations for:
- core (enhanced models)
- iot
- ml_services
- blockchain
- scenarios
- saas
- api

### Step 3: Run Migrations
```bash
python manage.py migrate
```

### Step 4: Create Superuser (Admin Access)
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### Step 5: Start the Server! 🎉
```bash
python manage.py runserver
```

The app will be running at: **http://127.0.0.1:8000/**

---

## 🎯 What to Explore

### 1. Admin Panel
Go to: **http://127.0.0.1:8000/admin/**
- Login with your superuser credentials
- Explore all the new models:
  - **Core**: Suppliers, Emission Entries
  - **IoT**: Devices, Readings
  - **ML Services**: Models, Predictions, Estimates
  - **Blockchain**: Verifications
  - **Scenarios**: Scenarios, Scenario Suppliers
  - **SaaS**: Tenants, Users, API Keys, Subscriptions

### 2. Dashboard
Go to: **http://127.0.0.1:8000/dashboard/**
- View emissions overview
- See ML hotspot predictions
- Check IoT device status
- Explore scenarios

### 3. API Endpoints
- **API Root**: http://127.0.0.1:8000/api/
- **IoT Ingest**: http://127.0.0.1:8000/iot/ingest/

---

## 🧪 Quick Test - Create Sample Data

### Option 1: Using Django Admin
1. Go to http://127.0.0.1:8000/admin/
2. Add a Supplier
3. Add an Emission Entry for that supplier
4. View it in the dashboard!

### Option 2: Using Django Shell
```bash
python manage.py shell
```

Then run:
```python
from core.models import Supplier, EmissionEntry
from django.utils import timezone
from decimal import Decimal

# Create a supplier
supplier = Supplier.objects.create(
    name="Zimbabwe Energy Corp",
    supplier_code="ZEC001",
    region="Zimbabwe",
    contact_email="contact@zec.co.zw",
    industry="Energy",
    annual_spend=Decimal("500000"),
    emission_factor=Decimal("0.85")
)

# Create an emission entry
entry = EmissionEntry.objects.create(
    supplier=supplier,
    date_reported=timezone.now(),
    scope3_emissions=Decimal("125.5"),
    notes="Q1 2024 emissions",
    data_source="manual"
)

print(f"Created: {supplier.name} with {entry.scope3_emissions} tCO2e")
```

---

## 🎬 Next Steps

1. **Add Suppliers**: Create a few suppliers in the admin
2. **Add Emissions**: Add emission entries for different dates
3. **Test ML**: Run hotspot predictions (see QUICK_START.md)
4. **Test IoT**: Create an IoT device and send test readings
5. **Test Scenarios**: Create a scenario to see reduction projections
6. **Test API**: Try the REST API endpoints

---

## 🐛 Troubleshooting

### Import Errors?
Make sure all apps are in `INSTALLED_APPS` in `settings.py` ✅ (already done)

### Migration Errors?
```bash
python manage.py makemigrations --dry-run  # Check what would be created
python manage.py showmigrations  # See migration status
```

### Can't Access Admin?
- Make sure you created a superuser
- Check you're using the correct credentials
- Try: `python manage.py createsuperuser` again

### Port Already in Use?
```bash
python manage.py runserver 8001  # Use different port
```

---

## 📚 More Info

- **Detailed Setup**: See `README_UPGRADE.md`
- **API Guide**: See `QUICK_START.md`
- **Features**: See `UPGRADE_SUMMARY.md`

---

**Ready? Run these commands now:**

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Then open:** http://127.0.0.1:8000/admin/ 🎉

