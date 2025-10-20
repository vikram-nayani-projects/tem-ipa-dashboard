# TEM IPA Manager Dashboard - Demo

**2026 A Season - Vessel Trip Limit Support System**

This is a proof-of-concept demonstration of a data analytics platform for Alaska TEM IPA cooperative management.

## Features

- ✅ Real-time 4-trip rolling average monitoring
- ✅ Color-coded compliance status (Green/Yellow/Red)
- ✅ **Next Trip Calculator** - Proactive vessel support
- ✅ Violation detection (Trip Limit + Egregious + MRA)
- ✅ Fleet overview dashboard
- ✅ Individual vessel detail pages
- ✅ Data upload interface
- ✅ Violation reports

## Tech Stack

- **Frontend:** Streamlit
- **Data Processing:** pandas
- **Visualization:** Plotly
- **Deployment:** Railway (planned)

## Local Development

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run src/app.py
```

3. Open browser to `http://localhost:8501`

## Demo Data

This demo uses realistic test data for 8 vessels showing various compliance scenarios:

1. **Pacific Hunter** - Compliant (safe operations)
2. **Northern Star** - Warning (trending high) ⭐
3. **Sea Wolf** - Trip Limit Violation
4. **Arctic King** - Egregious Violation (>335k single trip)
5. **Ocean Voyager** - Roller Coaster (status changes)
6. **Blue Horizon** - New Vessel (insufficient data)
7. **Silver Fin** - MRA Compliant
8. **Golden Catch** - MRA Violation

## Production Version

The production system will include:

- 🔒 Secure authentication (IPA Manager only)
- 🗄️ PostgreSQL database persistence
- 📊 Live eLandings data integration
- 📧 NMFS post-season reconciliation
- 💰 Automated penalty calculations
- 📱 Email notifications
- 📈 Historical analytics

## Contact

**Fishermen First**
fishermenfirst.org

---

*Demo Version - Test Data Only*
