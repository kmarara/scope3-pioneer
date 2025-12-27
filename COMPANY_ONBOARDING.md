# 🏢 Company Onboarding Guide

## How Companies Can Use Scope 3 Tracker

### Overview

Scope 3 Tracker is an AI-powered platform that helps companies track, verify, and reduce their indirect supply chain emissions (Scope 3). Perfect for energy firms, manufacturing companies, and any organization committed to carbon transparency and reduction.

---

## Getting Started (5 Steps)

### Step 1: Register Your Organization

1. **Visit the registration page**: `/accounts/register/`
2. **Fill in your details**:
   - Organization/Company Name
   - Your name and email
   - Choose a username and password
3. **Submit** - Your organization account is automatically created!

**What happens**: 
- A tenant account is created for your company
- You become the organization owner
- You get access to the Free tier (up to 10 suppliers)

---

### Step 2: Add Your Suppliers

1. **Go to Admin Panel** → Suppliers → Add Supplier
2. **Enter supplier information**:
   - Supplier name and code
   - Contact email
   - Region and industry
   - Annual spend (for ML estimation)
   - Emission factor (if known)
3. **Save** - Repeat for all suppliers

**Tip**: You can also add suppliers via the API for bulk imports.

---

### Step 3: Start Tracking Emissions

#### Option A: Manual Entry
1. Go to **Submit Emission** page
2. Select supplier
3. Enter:
   - Date reported
   - CO₂ emissions (tons)
   - Upload evidence document (optional)
   - Add notes/context
4. Submit

#### Option B: IoT Integration
1. **Add IoT Device** (Admin → IoT Devices)
2. **Copy API Key** for the device
3. **Configure device** to send data to `/iot/ingest/`
4. **Automatic**: Readings are converted to emissions in real-time

#### Option C: API Integration
- Use REST API to programmatically submit emissions
- Generate API key in Admin → API Keys
- Integrate with your ERP/procurement systems

#### Option D: ML Estimates
- For suppliers without direct data, use spend-based estimation
- System automatically estimates emissions from procurement spend
- Uses industry-specific emission factors

---

### Step 4: Explore Insights

#### Dashboard Features:
- **Total Emissions**: See cumulative Scope 3 emissions
- **ML Hotspots**: Identify high-emission suppliers automatically
- **Top Suppliers**: Rank suppliers by emission impact
- **Data Sources**: Track where data comes from (manual, IoT, ML)
- **Verification Status**: Monitor data verification progress

#### Scenario Modeling:
1. Go to **Admin → Scenarios**
2. Create "what-if" scenarios:
   - Renewable energy adoption
   - Supplier switching
   - Energy efficiency improvements
   - Transport optimization
3. **View projections**: See potential emission reductions

---

### Step 5: Verify & Report

#### Blockchain Verification:
- Enable blockchain verification for critical entries
- Creates immutable audit trail
- Perfect for compliance reporting

#### Export & Reporting:
- Export data via API
- Generate compliance reports
- Share with stakeholders

---

## Use Cases by Company Type

### Energy Companies
- **Track**: Power purchase emissions, transmission losses, equipment suppliers
- **IoT**: Connect smart meters for real-time monitoring
- **Goal**: Achieve net-zero Scope 3 emissions

### Manufacturing Firms
- **Track**: Raw materials, component suppliers, logistics
- **ML**: Use spend-based estimation for thousands of suppliers
- **Goal**: Identify and reduce supply chain hotspots

### Service Companies
- **Track**: Cloud services, business travel, waste management
- **Focus**: Office suppliers, IT equipment, facilities
- **Goal**: Comprehensive Scope 3 coverage

### Retail/E-commerce
- **Track**: Product suppliers, packaging, logistics, delivery
- **Scale**: Handle hundreds of suppliers with ML estimates
- **Goal**: Transparent supply chain emissions

---

## Key Features for Companies

### 1. Multi-Tenant Architecture
- Each company has isolated data
- Complete privacy and security
- Custom branding (Enterprise tier)

### 2. Multiple Data Sources
- **Manual Entry**: Traditional reporting
- **IoT**: Real-time monitoring
- **ML Estimates**: Fill data gaps intelligently
- **Result**: 90%+ coverage

### 3. AI-Powered Insights
- **Hotspot Detection**: Automatically identify high-emission suppliers
- **Anomaly Detection**: Flag unusual patterns
- **Predictions**: Forecast future emissions

### 4. Scenario Planning
- Model different reduction strategies
- Compare baseline vs. projected emissions
- Calculate ROI on interventions

### 5. Verification & Compliance
- Blockchain verification for audit trails
- Compliance-ready reporting
- Data integrity guarantees

### 6. API Integration
- Connect with ERP systems
- Automate data collection
- Build custom integrations

---

## Subscription Tiers

### Free Tier
- Up to 10 suppliers
- Basic dashboard
- Manual entry only
- Community support

### Starter ($99/month)
- Up to 50 suppliers
- ML predictions
- API access
- Email support

### Professional ($499/month)
- Unlimited suppliers
- IoT integration
- Scenario modeling
- Priority support
- Custom integrations

### Enterprise (Custom)
- Everything in Professional
- Custom branding
- Dedicated support
- SLA guarantees
- On-premise option

---

## Integration Options

### 1. ERP Systems
- SAP, Oracle, Microsoft Dynamics
- Via REST API
- Automated emission tracking from procurement data

### 2. IoT Platforms
- AWS IoT, Azure IoT, Google Cloud IoT
- Connect sensors and meters
- Real-time emission calculation

### 3. Carbon Accounting Tools
- Export data for CDP reporting
- Integrate with carbon footprint calculators
- Support for GHG Protocol standards

### 4. Business Intelligence
- Export to Power BI, Tableau
- Custom dashboards
- Advanced analytics

---

## Training & Support

### Onboarding Support
- Guided setup session
- Best practices training
- Integration assistance

### Documentation
- API documentation
- User guides
- Video tutorials

### Community
- User forum
- Monthly webinars
- Case studies

---

## Success Metrics

Track your progress:
- **Coverage**: % of Scope 3 emissions tracked
- **Reduction**: Absolute and percentage reductions
- **Verification**: % of data verified
- **Hotspots**: Number identified and addressed

---

## Next Steps

1. **Register** your organization at `/accounts/register/`
2. **Explore** the dashboard and features
3. **Add** your first supplier and emission entry
4. **Connect** IoT devices (if applicable)
5. **Create** your first scenario
6. **Integrate** with your systems via API

---

## Support

- **Email**: support@scope3tracker.com
- **Documentation**: `/docs/`
- **API Docs**: `/api/`
- **Admin Panel**: `/admin/`

**Ready to get started?** Register your organization today! 🚀

