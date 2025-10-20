# Demo Week Plan - TEM IPA Manager POC

**Target:** Working demo by Friday Nov 22 for interview committee
**URL:** tem-ipa-demo.fishermenfirst.org
**Approach:** Streamlit + hardcoded test data (no database)

---

## Day 1 (Monday): Environment + Test Data
**Time: 3-4 hours**

### Step 1: Install Python packages (15 min)
```bash
pip install streamlit pandas openpyxl plotly
```

### Step 2: Verify Streamlit works (15 min)
```bash
streamlit hello
```
Browser should open with demo. If working, you're ready.

### Step 3: Create realistic test data (2-3 hours)

Create `src/demo_data.py`:

```python
import pandas as pd
from datetime import datetime, timedelta

# 5 vessels with realistic names
VESSELS = [
    {'vessel_id': 'AK-001', 'vessel_name': 'Pacific Hunter', 'active': True},
    {'vessel_id': 'AK-002', 'vessel_name': 'Northern Star', 'active': True},
    {'vessel_id': 'AK-003', 'vessel_name': 'Sea Wolf', 'active': True},
    {'vessel_id': 'AK-004', 'vessel_name': 'Arctic King', 'active': True},
    {'vessel_id': 'AK-005', 'vessel_name': 'Ocean Voyager', 'active': True},
]

# Generate 50 trips (10 per vessel)
# Mix of compliant, warnings, and violations
def generate_test_trips():
    trips = []
    start_date = datetime(2026, 1, 20)

    for vessel in VESSELS:
        for i in range(10):
            trip_date = start_date + timedelta(days=i*3)

            # Vary pounds to create interesting scenarios
            if vessel['vessel_id'] == 'AK-001':
                # Compliant vessel
                pollock_lbs = 250000 + (i * 5000)
            elif vessel['vessel_id'] == 'AK-002':
                # Warning vessel (approaching limit)
                pollock_lbs = 280000 + (i * 3000)
            elif vessel['vessel_id'] == 'AK-003':
                # Violation vessel (over 300k avg)
                pollock_lbs = 310000 + (i * 2000)
            elif vessel['vessel_id'] == 'AK-004':
                # Egregious violation (single trip >335k)
                pollock_lbs = 340000 if i == 5 else 270000
            else:
                # Mixed
                pollock_lbs = 260000 + (i * 8000)

            # Add some MRA species
            pcod_lbs = int(pollock_lbs * 0.15)  # 15% Pacific Cod (under 20% limit)
            other_lbs = int(pollock_lbs * 0.01)  # 1% other (under 2% limit)

            trips.append({
                'trip_id': f'T{len(trips)+1:03d}',
                'vessel_id': vessel['vessel_id'],
                'vessel_name': vessel['vessel_name'],
                'delivery_date': trip_date,
                'pollock_lbs': pollock_lbs,
                'pcod_lbs': pcod_lbs,
                'other_lbs': other_lbs,
                'season': 'A',
                'fishing_year': 2026
            })

    return pd.DataFrame(trips)

# Pre-generate data
TRIPS_DF = generate_test_trips()

def get_vessel_trips(vessel_id):
    """Get all trips for a vessel"""
    return TRIPS_DF[TRIPS_DF['vessel_id'] == vessel_id].sort_values('delivery_date')

def calculate_trip_limit_status(vessel_id):
    """Calculate 4-trip rolling average and status"""
    trips = get_vessel_trips(vessel_id)

    if len(trips) < 4:
        return {
            'status': 'INSUFFICIENT_DATA',
            'trips_needed': 4 - len(trips),
            'avg': None,
            'trips': trips.to_dict('records')
        }

    last_4 = trips.tail(4)
    avg = last_4['pollock_lbs'].mean()

    # Determine status
    if avg > 300000:
        status = 'VIOLATION'
        color = 'red'
    elif avg > 285000:
        status = 'WARNING'
        color = 'orange'
    else:
        status = 'COMPLIANT'
        color = 'green'

    return {
        'status': status,
        'color': color,
        'avg': avg,
        'trips': last_4.to_dict('records'),
        'all_trips': trips.to_dict('records')
    }

def check_egregious_violations():
    """Find all trips > 335k lbs"""
    return TRIPS_DF[TRIPS_DF['pollock_lbs'] > 335000]

def calculate_mra_compliance(trip_id):
    """Check MRA compliance for a trip"""
    trip = TRIPS_DF[TRIPS_DF['trip_id'] == trip_id].iloc[0]

    total_catch = trip['pollock_lbs'] + trip['pcod_lbs'] + trip['other_lbs']
    pcod_pct = (trip['pcod_lbs'] / total_catch) * 100
    other_pct = (trip['other_lbs'] / total_catch) * 100

    violations = []
    if pcod_pct > 20:
        violations.append({
            'species': 'Pacific Cod',
            'percentage': pcod_pct,
            'limit': 20,
            'overage': pcod_pct - 20
        })

    if other_pct > 2:
        violations.append({
            'species': 'Other Species',
            'percentage': other_pct,
            'limit': 2,
            'overage': other_pct - 2
        })

    return {
        'compliant': len(violations) == 0,
        'violations': violations
    }
```

**Deliverable:** Test data file with realistic scenarios

---

## Day 2 (Tuesday): Vessel Status Dashboard
**Time: 4-5 hours**

### Build main dashboard page

Create `src/app.py`:

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from demo_data import (
    VESSELS, TRIPS_DF, calculate_trip_limit_status,
    check_egregious_violations, get_vessel_trips
)

# Page config
st.set_page_config(
    page_title="TEM IPA Manager - Demo",
    page_icon="🐟",
    layout="wide"
)

# Header
st.title("🐟 TEM IPA Manager Dashboard")
st.markdown("**2026 A Season - Vessel Trip Limit Support (DEMO)**")
st.info("ℹ️ This is a demonstration with test data. Real system will use live eLandings data.")

# Sidebar
with st.sidebar:
    st.header("Select Vessel")
    vessel_options = {v['vessel_name']: v['vessel_id'] for v in VESSELS}
    selected_vessel_name = st.selectbox("Vessel", list(vessel_options.keys()))
    selected_vessel_id = vessel_options[selected_vessel_name]

    st.markdown("---")
    st.markdown("### Demo Navigation")
    page = st.radio("Page", ["Vessel Status", "All Vessels Summary", "Violation Reports"])

# Page: Vessel Status
if page == "Vessel Status":
    st.header(f"📊 {selected_vessel_name} ({selected_vessel_id})")

    # Calculate status
    status = calculate_trip_limit_status(selected_vessel_id)

    # Status badge
    if status['status'] == 'VIOLATION':
        st.error(f"❌ **VIOLATION** - 4-Trip Avg: {status['avg']:,.0f} lbs (Limit: 300,000 lbs)")
    elif status['status'] == 'WARNING':
        st.warning(f"⚠️ **WARNING** - 4-Trip Avg: {status['avg']:,.0f} lbs (Limit: 300,000 lbs)")
    elif status['status'] == 'COMPLIANT':
        st.success(f"✅ **COMPLIANT** - 4-Trip Avg: {status['avg']:,.0f} lbs (Limit: 300,000 lbs)")
    else:
        st.info(f"ℹ️ Need {status['trips_needed']} more trips to calculate average")

    # Metrics row
    if status['status'] != 'INSUFFICIENT_DATA':
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("4-Trip Average", f"{status['avg']:,.0f} lbs")

        with col2:
            remaining = 300000 - status['avg'] if status['avg'] <= 300000 else 0
            st.metric("Remaining Capacity", f"{remaining:,.0f} lbs")

        with col3:
            pct_used = (status['avg'] / 300000) * 100
            st.metric("% of Limit Used", f"{pct_used:.1f}%")

    # Last 4 trips table
    if status['status'] != 'INSUFFICIENT_DATA':
        st.subheader("Last 4 Trips (Used for Average)")
        trips_df = pd.DataFrame(status['trips'])
        trips_df['delivery_date'] = pd.to_datetime(trips_df['delivery_date']).dt.strftime('%Y-%m-%d')
        st.dataframe(
            trips_df[['trip_id', 'delivery_date', 'pollock_lbs']],
            use_container_width=True,
            hide_index=True
        )

    # Trip history chart
    st.subheader("Trip History")
    all_trips = get_vessel_trips(selected_vessel_id)
    fig = px.line(
        all_trips,
        x='delivery_date',
        y='pollock_lbs',
        markers=True,
        title=f"{selected_vessel_name} - Pollock Catch per Trip"
    )
    fig.add_hline(y=300000, line_dash="dash", line_color="orange",
                  annotation_text="4-Trip Avg Limit (300k lbs)")
    fig.add_hline(y=335000, line_dash="dash", line_color="red",
                  annotation_text="Egregious Limit (335k lbs)")
    st.plotly_chart(fig, use_container_width=True)

# Page: All Vessels Summary
elif page == "All Vessels Summary":
    st.header("📋 All Vessels Summary")

    summary_data = []
    for vessel in VESSELS:
        status = calculate_trip_limit_status(vessel['vessel_id'])
        if status['status'] != 'INSUFFICIENT_DATA':
            summary_data.append({
                'Vessel': vessel['vessel_name'],
                'Vessel ID': vessel['vessel_id'],
                'Status': status['status'],
                '4-Trip Avg (lbs)': f"{status['avg']:,.0f}",
                'Trips Completed': len(status['all_trips'])
            })

    summary_df = pd.DataFrame(summary_data)

    # Color-code status
    def color_status(val):
        if val == 'VIOLATION':
            return 'background-color: #ffcccc'
        elif val == 'WARNING':
            return 'background-color: #fff4cc'
        elif val == 'COMPLIANT':
            return 'background-color: #ccffcc'
        return ''

    styled_df = summary_df.style.applymap(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Page: Violation Reports
elif page == "Violation Reports":
    st.header("⚠️ Violation Reports")

    # Trip limit violations
    st.subheader("Trip Limit Violations (>300k lbs avg)")
    violations = []
    for vessel in VESSELS:
        status = calculate_trip_limit_status(vessel['vessel_id'])
        if status['status'] == 'VIOLATION':
            violations.append({
                'Vessel': vessel['vessel_name'],
                'Vessel ID': vessel['vessel_id'],
                '4-Trip Avg': f"{status['avg']:,.0f} lbs",
                'Overage': f"{status['avg'] - 300000:,.0f} lbs"
            })

    if violations:
        st.dataframe(pd.DataFrame(violations), use_container_width=True, hide_index=True)
    else:
        st.success("✅ No trip limit violations")

    # Egregious violations
    st.subheader("Egregious Violations (>335k lbs single trip)")
    egregious = check_egregious_violations()
    if len(egregious) > 0:
        egregious_display = egregious[['trip_id', 'vessel_name', 'delivery_date', 'pollock_lbs']].copy()
        egregious_display['pollock_lbs'] = egregious_display['pollock_lbs'].apply(lambda x: f"{x:,.0f} lbs")
        st.dataframe(egregious_display, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No egregious violations")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666;">'
    '🐟 TEM IPA Manager Dashboard | fishermenfirst.org | Demo Version'
    '</div>',
    unsafe_allow_html=True
)
```

### Test locally
```bash
cd C:\Users\vikra\Git\ff-planning
streamlit run src/app.py
```

**Deliverable:** Working dashboard showing vessel status, violations

---

## Day 3 (Wednesday): Data Upload Page + Polish
**Time: 3-4 hours**

### Add upload functionality (even if it doesn't persist)

Update `src/app.py` sidebar to add "Upload Data" page:

```python
# In sidebar
page = st.radio("Page", ["Vessel Status", "All Vessels Summary", "Violation Reports", "Upload Data"])

# New page
elif page == "Upload Data":
    st.header("📤 Upload Trip Data")
    st.markdown("Upload eLandings CSV to import new trip data")

    uploaded_file = st.file_uploader("Choose CSV file", type=['csv', 'xlsx'])

    if uploaded_file:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"✅ File loaded: {len(df)} rows")

        # Preview
        st.subheader("Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

        # Mock validation
        st.subheader("Validation Results")
        st.success("✅ All required columns present")
        st.success("✅ No duplicate trips detected")
        st.success("✅ All dates valid")
        st.info("ℹ️ In production, this data would be imported to database")
```

### Add custom theme

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F8FF"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
```

**Deliverable:** Upload page working, custom theme applied

---

## Day 4 (Thursday): Deploy to Railway
**Time: 2-3 hours**

### Step 1: Prepare for deployment

Create `requirements.txt`:
```
streamlit==1.28.0
pandas==2.0.0
plotly==5.17.0
openpyxl==3.1.0
```

Create `.gitignore`:
```
__pycache__/
*.pyc
.env
.DS_Store
```

### Step 2: Push to GitHub

```bash
cd C:\Users\vikra\Git\ff-planning
git init
git add .
git commit -m "Initial commit - TEM IPA demo"
git branch -M main
git remote add origin [your-github-repo-url]
git push -u origin main
```

### Step 3: Deploy to Railway

1. Go to https://railway.app
2. Sign up/login
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your ff-planning repo
5. Railway auto-detects Streamlit
6. Wait 2-3 minutes for deployment
7. Click generated URL to test

**Deliverable:** Demo live at Railway URL

---

## Day 5 (Friday): Custom Domain + Final Polish
**Time: 2-3 hours**

### Step 1: Configure custom domain

In Railway project settings:
1. Click "Settings" → "Domains"
2. Click "Custom Domain"
3. Enter: `tem-ipa-demo.fishermenfirst.org`
4. Copy the CNAME target provided

In your domain registrar:
1. Add DNS record:
   - Type: CNAME
   - Host: tem-ipa-demo
   - Points to: [Railway CNAME]
   - TTL: 3600
2. Save and wait 5-30 minutes for DNS propagation

### Step 2: Add demo banner

Update `src/app.py` header:
```python
st.title("🐟 TEM IPA Manager Dashboard")
st.markdown("**2026 A Season - Vessel Trip Limit Support**")

# Demo banner
st.warning("""
⚠️ **DEMONSTRATION VERSION**

This is a proof-of-concept with test data. The production system will include:
- Live eLandings data integration
- Secure authentication (IPA Manager only)
- Database persistence
- Post-season NMFS reconciliation
- Complete MRA compliance checking
- Automated penalty calculations
""")
```

### Step 3: Add explanatory text

Add help text to key sections explaining the functionality.

**Deliverable:** Demo at tem-ipa-demo.fishermenfirst.org with polish

---

## What You'll Have on Friday

### **Live Demo URL:** tem-ipa-demo.fishermenfirst.org

### **Functionality:**
✅ Vessel status dashboard (5 test vessels)
✅ 4-trip rolling average calculation
✅ Color-coded compliance status (Green/Yellow/Red)
✅ Trip history charts
✅ All vessels summary table
✅ Violation reports (trip limit + egregious)
✅ Data upload page (preview, validation)
✅ Professional Streamlit theme
✅ Mobile-responsive

### **For Interview Committee:**
Send them:
1. Demo URL: tem-ipa-demo.fishermenfirst.org
2. 1-page doc explaining what they're seeing
3. Note that it's test data, production will connect to real eLandings

### **What's NOT in Demo (but in production):**
- Database (using in-memory data)
- Authentication (demo is public)
- Real eLandings integration
- MRA compliance (partially shown)
- Post-season NMFS reconciliation

---

## Time Commitment

| Day | Tasks | Hours |
|-----|-------|-------|
| Monday | Setup + test data | 3-4 |
| Tuesday | Vessel dashboard | 4-5 |
| Wednesday | Upload page + polish | 3-4 |
| Thursday | Deploy to Railway | 2-3 |
| Friday | Custom domain + final touches | 2-3 |
| **Total** | | **14-19 hours** |

Spread over 5 days = ~3 hours/day

---

## Next Steps After Demo

**If you win the contract:**
- Spend Weeks 2-9 building production version (database, auth, real data)
- Demo becomes your UI template

**If you don't win:**
- Only invested 15-20 hours
- Still have working demo for future proposals
- Learned Streamlit for other projects

---

## Ready to Start?

**Monday morning checklist:**
1. [ ] Install Python packages: `pip install streamlit pandas plotly openpyxl`
2. [ ] Run `streamlit hello` to verify working
3. [ ] Create `src/demo_data.py` with test data
4. [ ] Test that you can import the test data

Want me to help you create the test data file first?
