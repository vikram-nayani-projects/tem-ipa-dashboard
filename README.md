# Fisherman First - Analytics Demo Platforms

This repository contains demonstration platforms for Fisherman First LLC's analytics proposals supporting Alaska fisheries management.

## 📁 Repository Structure

```
ff-planning/
├── tem-ipa/              # TEM IPA Manager Dashboard Demo
│   ├── src/
│   ├── requirements.txt
│   └── Procfile
│
├── rockfish/             # CGOA Rockfish Program Demo
│   ├── src/
│   ├── requirements.txt
│   └── Procfile
│
└── [RFP PDFs and documentation]
```

---

## 🐟 1. TEM IPA Manager Dashboard

**2026 A Season - Vessel Trip Limit Support System**

Demo platform for the GOA TEM Incentive Plan Agreement Manager proposal.

### Features

- ✅ Real-time 4-trip rolling average monitoring
- ✅ Color-coded compliance status (Green/Yellow/Red)
- ✅ **Next Trip Calculator** - Proactive vessel support
- ✅ Violation detection (Trip Limit + Egregious + MRA)
- ✅ Fleet overview dashboard
- ✅ Individual vessel detail pages
- ✅ Trip history charts with 4-trip averages
- ✅ Violation reports

### Demo Data

8 vessels showing various compliance scenarios:
- **Pacific Hunter** - Compliant (safe operations)
- **Northern Star** - Warning (trending high) ⭐
- **Sea Wolf** - Trip Limit Violation
- **Arctic King** - Egregious Violation (>335k single trip)
- **Ocean Voyager** - Roller Coaster (status changes)
- **Blue Horizon** - New Vessel (insufficient data)
- **Silver Fin** - MRA Compliant
- **Golden Catch** - MRA Violation

### Local Development

```bash
cd tem-ipa
pip install -r requirements.txt
streamlit run src/app.py
```

Open browser to `http://localhost:8501`

---

## 🎣 2. CGOA Rockfish Program Dashboard

**Analytics and Quota Management Platform**

Demo platform for the CGOA Rockfish Program Intercooperative & Cooperative Manager proposal.

### Features

- ✅ **Dashboard** - Fleet overview with quota status, PSC caps, active alerts
- ✅ **Vessel Performance** - Detailed vessel-level tracking across 4 cooperatives
- ✅ **Board Summary Report** - Comprehensive analytics with charts for board meetings
- ✅ **Transfer Management** - Record and track quota transfers between vessels
- ✅ Multi-cooperative structure (4 cooperatives, 22 vessels)
- ✅ Chinook (1,200 cap) and Halibut PSC monitoring
- ✅ Overage detection and forfeiture tracking
- ✅ A Season (Apr-Jun) and B Season (Oct-Nov) analytics

### Demo Data

Realistic 2026 season data:
- **4 Cooperatives:** North Pacific, OBSI, Silver Bay Seafoods, Star of Kodiak
- **22 Active Vessels** distributed across cooperatives
- **25,000 mt Total Quota** with 72% harvested
- **840 / 1,200 Chinook PSC** (70% of cap)
- **Weekly harvest data** showing PSC trends and hotspots
- **10 quota transfers** between vessels

### Local Development

```bash
cd rockfish
pip install -r requirements.txt
streamlit run src/app.py
```

Open browser to `http://localhost:8501`

---

## 🚂 Railway Deployment

Both demos are deployed separately on Railway.

### Deploy TEM IPA

1. Create new Railway project from this GitHub repo
2. Settings → Set **Root Directory** to `tem-ipa`
3. Railway auto-detects `Procfile` and `requirements.txt`
4. Deploy

### Deploy Rockfish

1. Create new Railway project from this GitHub repo
2. Settings → Set **Root Directory** to `rockfish`
3. Railway auto-detects `Procfile` and `requirements.txt`
4. Deploy

Each gets its own unique Railway URL.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Data Processing:** pandas, numpy
- **Visualization:** Plotly
- **Deployment:** Railway
- **Version Control:** Git

---

## 📋 Production Features (Not in Demo)

Production versions will include:

- 🔒 Secure authentication
- 🗄️ PostgreSQL database persistence
- 📊 Live eLandings data integration via API
- 📧 eFish quota transfer reconciliation
- 💰 Automated overage/penalty calculations
- 📱 Email/SMS alerts for critical events
- 📈 Multi-year historical analytics
- 📄 PDF/Excel report exports
- 👥 Role-based access (Manager, Vessels, Board)

---

## 📄 Related Documents

- `Fisherman_First_Proposal_GOA_TEM_IPA_Manager_Analytics_Support_2025 (2) (1).pdf` - TEM IPA Proposal
- `Fisherman_First_Proposal_CGOA_Rockfish_Manager_Analytics_Support_2025 (2) (1).pdf` - Rockfish Proposal
- `RFP_GOA TEM IPA MANAGER_Final (1).pdf` - TEM IPA RFP
- `RFP_CGOA RP Intercooperative and Cooperative Manager_Final (1).pdf` - Rockfish RFP

---

## 📞 Contact

**Fisherman First LLC**
Vikram Nayani, Principal
Seattle, WA

---

*Demo Platforms - Test Data Only*
*Generated for proposal demonstration purposes*
