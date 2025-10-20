# TEM IPA Manager Dashboard - Implementation Action Plan

**Goal:** Build Phase 1 (In-Season Vessel Support) by January 20, 2026
**Tech Stack:** PostgreSQL + Python + pandas + Streamlit
**Hosting:** Railway or Render
**Domain:** fishermenfirst.org

---

## Phase 0: Foundation (Week 1-2) - Complete by Nov 25, 2025

### Step 1: Local Development Setup
**Time: 2-3 hours**

1. Install PostgreSQL locally
   - Download: https://www.postgresql.org/download/
   - Create database: `tem_ipa`
   - Note credentials for later

2. Install Python dependencies
   ```bash
   cd C:\Users\vikra\Git\ff-planning
   pip install streamlit pandas psycopg2-binary sqlalchemy openpyxl
   ```

3. Verify Streamlit works
   ```bash
   streamlit hello
   ```
   - Should open browser with demo app
   - If working, you're ready

**Deliverable:** Local environment runs Streamlit demo

---

### Step 2: Create Database Schema
**Time: 2 hours**

1. Create `database/schema.sql` file with tables:
   - `vessels` (vessel_id, vessel_name, active)
   - `trips` (trip_id, vessel_id, delivery_date, pollock_lbs, season, fishing_year, data_source)
   - `trip_species` (trip_id, species_code, species_lbs)
   - `violations` (violation_id, trip_id, violation_type, calculated_value, penalty_amount)

2. Run schema in PostgreSQL
   ```bash
   psql -U postgres -d tem_ipa -f database/schema.sql
   ```

3. Insert test data (3-4 vessels, 10-15 trips each)
   - Manually write INSERT statements
   - Include mix of compliant and violation trips
   - Test data lets you build UI without real data

**Deliverable:** Database with schema + test data

---

### Step 3: Database Connection Module
**Time: 1 hour**

1. Create `src/database.py`
   - Function: `get_connection()` - connects to PostgreSQL
   - Function: `test_connection()` - verifies database works

2. Create `.streamlit/secrets.toml`
   - Store database credentials
   - Store IPA Manager password

3. Test connection
   ```bash
   python src/database.py
   ```

**Deliverable:** Working database connection from Python

---

## Phase 1: Core Business Logic (Week 3-4) - Complete by Dec 9, 2025

### Step 4: Trip Limit Calculator
**Time: 4-6 hours**

1. Create `src/calculators/trip_limits.py`

2. Implement functions:
   ```python
   def get_vessel_trips(vessel_id, season, year)
   # Returns: DataFrame of trips for vessel in season

   def calculate_rolling_average(vessel_id, season, year)
   # Returns: 4-trip rolling average

   def check_trip_limit_status(vessel_id, season, year)
   # Returns: {'status': 'COMPLIANT'|'WARNING'|'VIOLATION',
   #           'avg': float, 'trips': [...]}

   def check_egregious_violation(trip_id)
   # Returns: True if single trip > 335,000 lbs
   ```

3. Test with your test data in PostgreSQL
   - Write test script: `tests/test_trip_limits.py`
   - Verify calculations match Excel/manual math

**Deliverable:** Trip limit calculator working with test data

---

### Step 5: Data Ingestion Module
**Time: 3-4 hours**

**NOTE:** You'll need sample eLandings CSV from current IPA Manager first

1. Create `src/ingestion/elandings_parser.py`

2. Implement functions:
   ```python
   def parse_elandings_csv(file_path)
   # Returns: DataFrame with standardized columns

   def validate_trip_data(df)
   # Returns: List of validation errors/warnings

   def import_trips_to_db(df, connection)
   # Inserts validated trips into database
   ```

3. Handle edge cases:
   - Missing vessel IDs
   - Invalid dates
   - Negative or zero pounds
   - Duplicate trips

**Deliverable:** CSV upload → Database pipeline working

---

### Step 6: MRA Compliance Checker
**Time: 4-5 hours**

**NOTE:** Need CFR Table 10 percentages from IPA Manager

1. Create `src/calculators/mra_checker.py`

2. Create `src/data/cfr_table10.py`
   - Hardcode MRA percentages by species
   ```python
   MRA_LIMITS = {
       'POLLOCK': {
           'PCOD': 20,  # 20% Pacific Cod allowed
           'OTHER': 2   # 2% other species
       }
   }
   ```

3. Implement functions:
   ```python
   def calculate_mra_compliance(trip_id)
   # Returns: Dict of species with compliance status

   def get_mra_violations(trip_id)
   # Returns: List of violated species with overages
   ```

**Deliverable:** MRA calculator working with test data

---

## Phase 2: Streamlit UI (Week 5-6) - Complete by Dec 23, 2025

### Step 7: Authentication System
**Time: 2 hours**

1. Create `src/auth.py` (password check, logout)

2. Update `src/app.py` to require authentication

3. Test login/logout flow

**Deliverable:** Password-protected app

---

### Step 8: Vessel Status Dashboard
**Time: 6-8 hours**

1. Create `src/pages/vessel_status.py`

2. Build UI components:
   - Dropdown to select vessel
   - Display 4-trip rolling average
   - Color-coded status (Green/Yellow/Red)
   - Table of recent trips
   - Line chart of trip history
   - MRA compliance summary

3. Add real-time calculations
   - Updates when new data uploaded

**Deliverable:** Working vessel status page

---

### Step 9: Data Upload Page
**Time: 4-5 hours**

1. Create `src/pages/upload_data.py`

2. Build UI:
   - File uploader (CSV/Excel)
   - Preview uploaded data (first 10 rows)
   - Validation warnings display
   - Confirm and import button
   - Success/error messages

3. Wire up ingestion module from Step 5

**Deliverable:** Working data upload page

---

### Step 10: Violation Reports Page
**Time: 4-5 hours**

1. Create `src/pages/violation_reports.py`

2. Build UI:
   - Date range filter
   - Violation type filter (Trip Limit, Egregious, MRA)
   - Table of all violations
   - Export to CSV button
   - Summary statistics (total violations, total penalty)

3. Implement report generation:
   ```python
   def generate_violation_report(start_date, end_date, violation_types)
   # Returns: DataFrame of violations with details
   ```

**Deliverable:** Working violation reports page

---

## Phase 3: Deployment (Week 7) - Complete by Dec 30, 2025

### Step 11: Deploy to Railway
**Time: 3-4 hours**

1. Create Railway account (https://railway.app)

2. Create new project
   - Add PostgreSQL database
   - Add Streamlit app service

3. Connect GitHub repo
   - Push code to GitHub
   - Railway auto-deploys on push

4. Set environment variables (database credentials, password)

5. Migrate schema to production database

**Deliverable:** App running on Railway at temporary URL

---

### Step 12: Configure Custom Domain
**Time: 2-3 hours**

1. In Railway project settings:
   - Add custom domain: `tem-ipa.fishermenfirst.org`
   - Get Railway's DNS target (CNAME)

2. In your domain registrar (GoDaddy, Namecheap, etc.):
   - Add DNS record:
     - Type: CNAME
     - Host: tem-ipa
     - Points to: [Railway's target]
     - TTL: 3600

3. Wait for DNS propagation (5-60 minutes)

4. Verify HTTPS works automatically

**Deliverable:** App accessible at tem-ipa.fishermenfirst.org

---

## Phase 4: Testing & Polish (Week 8-9) - Complete by Jan 13, 2026

### Step 13: Get Real Sample Data
**Time: Depends on IPA Manager response**

1. Email current IPA Manager (Chelsae Radell)
   ```
   Subject: Sample Data Request for TEM IPA Dashboard Development

   Hi Chelsae,

   I'm building the data analytics platform for the 2026 TEM IPA season
   and need sample data to finalize the system.

   Could you provide:
   1. Sample eLandings export (CSV/Excel) - 1-2 weeks of data
   2. NMFS post-season database format (from previous year)
   3. CFR Table 10 MRA percentages you currently use
   4. Current penalty calculation spreadsheet (if available)

   This will ensure my system matches your current workflow.

   Thanks,
   [Your name]
   ```

2. Wait for response (1-3 days)

3. Load sample data into system

**Deliverable:** Real data format understood and ingested

---

### Step 14: Test with Real Data
**Time: 4-6 hours**

1. Import sample data via upload page

2. Verify calculations match IPA Manager's expected results
   - Trip limit averages
   - Egregious violations
   - MRA compliance

3. Fix any discrepancies

4. Get IPA Manager to review and approve

**Deliverable:** Verified accurate calculations

---

### Step 15: Polish UI and Documentation
**Time: 3-4 hours**

1. Customize Streamlit theme colors
   - Update `.streamlit/config.toml`
   - Match fishermenfirst.org branding

2. Add help text and tooltips
   - Explain what each metric means
   - Link to relevant CFR sections

3. Write user guide (1-2 pages)
   - How to upload data
   - How to read vessel status
   - How to generate reports

**Deliverable:** Production-ready app with documentation

---

## Phase 5: Go-Live (Week 10) - Jan 20, 2026

### Step 16: IPA Manager Training
**Time: 1-2 hours**

1. Schedule Zoom call with IPA Manager

2. Walk through:
   - Login
   - Upload first week of 2026 A season data
   - Review vessel status
   - Generate violation report

3. Answer questions

4. Provide contact info for support

**Deliverable:** IPA Manager can use system independently

---

### Step 17: Monitor First Week
**Time: Ongoing**

1. Check in with IPA Manager daily (Jan 20-27)

2. Fix any bugs or issues immediately

3. Verify data uploads working smoothly

**Deliverable:** Stable system in production use

---

## Summary Timeline

| Phase | Dates | Duration | Key Deliverable |
|-------|-------|----------|-----------------|
| Phase 0: Foundation | Nov 11-25 | 2 weeks | Database + dev environment |
| Phase 1: Business Logic | Nov 26 - Dec 9 | 2 weeks | Trip limit + MRA calculators |
| Phase 2: UI | Dec 10-23 | 2 weeks | Working dashboard |
| Phase 3: Deployment | Dec 24-30 | 1 week | Live on fishermenfirst.org |
| Phase 4: Testing | Dec 31 - Jan 13 | 2 weeks | Validated with real data |
| Phase 5: Go-Live | Jan 14-20 | 1 week | In production use |

**Total: 10 weeks (Nov 11 - Jan 20)**

---

## Critical Path Items

**These are blockers - prioritize first:**

1. ✅ PostgreSQL installed locally
2. ✅ Streamlit running locally
3. ✅ Database schema created
4. ⚠️ Sample eLandings CSV from IPA Manager (NEEDED ASAP)
5. ⚠️ CFR Table 10 MRA percentages (NEEDED by Dec 9)
6. ✅ Trip limit calculator working
7. ✅ Data upload working
8. ✅ Vessel status dashboard working
9. ✅ Deployed to production
10. ✅ IPA Manager trained

---

## Next Immediate Steps (This Week)

**Tuesday Nov 19:**
1. Install PostgreSQL (1 hour)
2. Install Python packages (30 min)
3. Verify Streamlit works (30 min)

**Wednesday Nov 20:**
4. Create database schema (2 hours)
5. Insert test data (1 hour)

**Thursday Nov 21:**
6. Build database connection module (1 hour)
7. Start trip limit calculator (2 hours)

**Friday Nov 22:**
8. Finish trip limit calculator (2 hours)
9. Test with test data (1 hour)

**Weekend:**
10. **Email IPA Manager for sample data** (CRITICAL)

---

## Questions to Answer Before You Start

1. Do you have PostgreSQL already installed?
2. Do you have Python 3.8+ installed?
3. Do you have a GitHub account (needed for deployment)?
4. Do you have the current IPA Manager's contact info?
5. Do you control DNS for fishermenfirst.org?

Let me know answers and we can start Step 1 immediately.
