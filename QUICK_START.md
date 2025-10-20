# Quick Start Checklist

**Target:** Phase 1 live by Jan 20, 2026

---

## This Week (Nov 18-24)

### Day 1: Environment Setup
- [ ] Install PostgreSQL
- [ ] Install Python packages: `pip install streamlit pandas psycopg2-binary sqlalchemy openpyxl`
- [ ] Run `streamlit hello` to verify working
- [ ] Create database: `tem_ipa`

### Day 2: Database
- [ ] Create `database/schema.sql`
- [ ] Run schema in PostgreSQL
- [ ] Insert 3-4 test vessels
- [ ] Insert 10-15 test trips (mix of compliant/violations)

### Day 3: Connection
- [ ] Create `src/database.py` with connection function
- [ ] Create `.streamlit/secrets.toml` with credentials
- [ ] Test connection works

### Day 4-5: Trip Calculator
- [ ] Create `src/calculators/trip_limits.py`
- [ ] Implement `get_vessel_trips()`
- [ ] Implement `calculate_rolling_average()`
- [ ] Implement `check_trip_limit_status()`
- [ ] Test with test data

### Weekend: Critical Action
- [ ] **EMAIL CURRENT IPA MANAGER FOR SAMPLE DATA**

---

## Week 2 (Nov 25 - Dec 1)

- [ ] Build CSV ingestion module
- [ ] Start MRA compliance checker
- [ ] Get CFR Table 10 percentages

---

## Week 3-4 (Dec 2-15)

- [ ] Build authentication system
- [ ] Build vessel status dashboard
- [ ] Build data upload page
- [ ] Build violation reports page

---

## Week 5 (Dec 16-22)

- [ ] Deploy to Railway
- [ ] Configure fishermenfirst.org domain
- [ ] Load test data into production

---

## Week 6-7 (Dec 23 - Jan 5)

- [ ] Get real sample data from IPA Manager
- [ ] Test with real data
- [ ] Fix calculation discrepancies
- [ ] Polish UI

---

## Week 8-9 (Jan 6-19)

- [ ] IPA Manager training session
- [ ] Documentation
- [ ] Final testing
- [ ] Buffer for issues

---

## Week 10 (Jan 20)

- [ ] **GO LIVE - 2026 A Season starts**

---

## Critical Dependencies

**MUST HAVE by Dec 1:**
- Sample eLandings CSV format
- CFR Table 10 MRA percentages

**MUST HAVE by Jan 13:**
- Test data from IPA Manager
- Validated calculations

---

## Contact Info Needed

- Current IPA Manager: Chelsae Radell (email?)
- fishermenfirst.org domain registrar login
- GitHub account for deployment

---

## Support Resources

**Streamlit Documentation:**
- https://docs.streamlit.io/

**PostgreSQL Tutorials:**
- https://www.postgresqltutorial.com/

**Railway Deployment:**
- https://docs.railway.app/

**Questions?**
- Refer to ACTION_PLAN.md for detailed steps
