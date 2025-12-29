# 🌍 Scope 3 Carbon Data Platform

A full-stack energy data platform empowering businesses to track, verify, and report Scope 3 carbon emissions, built with **Python (Django)** and **Java (Spring Boot)** expertise.

---

![Scope 3 Carbon Platform Dashboard](https://via.placeholder.com/700x220.png?text=Live+Carbon+Dashboard)

## 🚀 Vision

Businesses struggle to capture reliable supply chain carbon data. This platform solves that by giving suppliers an easy portal, automating audit trails, and using ML to flag anomalies—making *Scope 3 reporting* accessible and actionable.

---

## 🛠️ Tech Stack

- **Backend:** Python (Django), Java (Spring Boot)
- **Frontend:** React (planned), Bootstrap UI
- **Database:** PostgreSQL, Django ORM
- **Cloud:** Heroku (dev), AWS microservices for Spring (prod)
- **ML Tools:** scikit-learn (prototyping anomaly detection)

---

## 📈 Features

- Supplier portal for seamless carbon data input
- Automated verification with ML-based anomaly detection
- Audit logs for robust governance and trust
- Real-time dashboards and downloadable compliance reports
- Enterprise-ready integrations (ERP, procurement, benchmarking tools)

---

## 🤖 AI/ML Features

- **Emission Forecasting**: Time-series prediction using Linear Regression
- **Anomaly Detection**: ML-powered hotspot identification  
- **Spend-Based Estimation**: Automated emission calculations from procurement data
- **Supplier Scoring**: Risk assessment and benchmarking

### Training ML Models

```bash
# Train emission forecasting model
python manage.py train_emission_model

# Models are saved in ml_models/ directory
# View trained models in admin panel under ML Services
```

---

## 🗂️ Work Breakdown Structure

| Phase             | Deliverable                     | Status |
|-------------------|---------------------------------|--------|
| Vision & MVP      | Problem, features list          | ✅      |
| Scaffold Project  | Code repo, framework setup      | ✅      |
| Models            | Data models, migrations, ERD    | ✅      |
| Intake            | Portal, login, API              | ✅      |
| Verification      | Manual review, ML flags         | ✅      |
| Dashboards        | Interactive/UI, reports export  | ✅      |
| Integration & Scale| Spring Boot services, APIs     | ⏳      |
| Deploy & Feedback | Cloud deploy, feedback results  | ⏳      |

> See detailed WBS in `/docs/WBS.md` for ongoing progress.

---

## 👩‍💻 Who Am I?

- **Full-stack Developer:** Python and Java expert, passionate about meaningful data engineering and sustainability.
- **Builder:** From MVP to production, skilled in architecting robust, scalable cloud deployments.
- **Learner & Team Player:** Always seeking new challenges, invested in clean code and collaborative growth.

---

## � Deployment

### Free Deployment Options

This app can be deployed for free using:

1. **Railway** (Recommended)
   - Connect your GitHub repo
   - Automatic builds and deploys
   - Free tier: 512MB RAM, 1GB storage
   - Custom domain included

2. **Render**
   - Use `render.yaml` for configuration
   - Free tier: 750 hours/month
   - Automatic SSL

3. **Heroku**
   - Free tier available
   - Easy Django deployment

### Local Development

```bash
# Clone the repo
git clone <your-repo>
cd scope3_tracker

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Populate sample data
python manage.py populate_sample_data

# Train ML model (requires sample data first)
python manage.py train_emission_model

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Demo Account
After running `populate_sample_data`, you can login with:
- **Username:** demo_user
- **Password:** demo123

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

---

## �👔 Why Work With Me?

- **Dual-stack fluency:** Python *and* Java for versatile problem solving
- **Mission-driven:** Motivated by climate impact, not just code quality
- **End-to-end ownership:** From idea and prototype to deployment and iteration
- **Professional:** Clean documentation, pragmatic solutioning, open to feedback

---

## 📫 Contact

- **Email:** kudakwashe.d.marara@gmail.com
- **LinkedIn:** [My LinkedIn](www.linkedin.com/in/kudakwashe-marara)
- **Portfolio:** [My Portfolio](https://github.com/kmarara)

> *Let’s build a more transparent, sustainable future—together.*

---

![Collaboration Visual](https://via.placeholder.com/400x120.png?text=Collaboration+and+Sustainability)

