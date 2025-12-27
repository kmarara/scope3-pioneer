# ⚡ QUICK RUN - Get Started Now!

## 🎯 Fastest Way to Start (Copy & Paste These Commands)

```bash
cd /home/recursivex/Energy_projects/project3/scope3_tracker

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Create migrations for all apps
python manage.py makemigrations

# Run migrations to create database tables
python manage.py migrate

# Create admin user (you'll be prompted)
python manage.py createsuperuser

# Start the server! 🚀
python manage.py runserver
```

**Then open in browser:**
- Admin: http://127.0.0.1:8000/admin/
- Dashboard: http://127.0.0.1:8000/dashboard/
- API: http://127.0.0.1:8000/api/

---

## 🐍 Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Or on Windows
# venv\Scripts\activate

# Then install dependencies
pip install -r requirements.txt

# Continue with setup commands above...
```

---

## 🎬 What You'll See

After running migrations, you'll have these apps ready:
- ✅ Core (Suppliers, Emissions)
- ✅ IoT (Devices, Readings)
- ✅ ML Services (Predictions, Estimates)
- ✅ Blockchain (Verifications)
- ✅ Scenarios (What-if Analysis)
- ✅ SaaS (Tenants, API Keys)

---

## 🧪 Test It Works

1. **Go to Admin**: http://127.0.0.1:8000/admin/
2. **Add a Supplier**:
   - Click "Suppliers" → "Add Supplier"
   - Fill in: Name, Email, Region, Industry
   - Save
3. **Add an Emission Entry**:
   - Click "Emission Entries" → "Add Emission Entry"
   - Select your supplier
   - Enter emissions (e.g., 100.5 tons)
   - Save
4. **View Dashboard**: http://127.0.0.1:8000/dashboard/
   - See your emissions!

---

## 🚨 Troubleshooting

### "No module named 'django'"
→ Install dependencies: `pip install -r requirements.txt`

### "App 'xxx' not found"
→ Check `INSTALLED_APPS` in `settings.py` (should be there already)

### Migration errors
→ Try: `python manage.py makemigrations --empty iot` (or app name)

### Port 8000 in use
→ Use different port: `python manage.py runserver 8001`

---

## 📚 Next Steps After Running

See `START_HERE.md` for:
- Creating sample data
- Testing ML predictions
- Testing IoT integration
- API usage examples

---

**Ready? Run the commands above and let's go! 🚀**

