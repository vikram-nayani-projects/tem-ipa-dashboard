# Test Demo Locally - Quick Start

Before deploying to Railway, test everything works on your local machine.

**Time: 10 minutes**

---

## Step 1: Install Python Packages

Open Command Prompt or PowerShell:

```bash
cd C:\Users\vikra\Git\ff-planning

pip install streamlit pandas plotly openpyxl
```

**Expected output:**
```
Successfully installed streamlit-X.X.X pandas-X.X.X plotly-X.X.X openpyxl-X.X.X
```

**If you get an error:**
- Make sure Python 3.8+ is installed: `python --version`
- Try: `python -m pip install streamlit pandas plotly openpyxl`

---

## Step 2: Verify Streamlit Works

```bash
streamlit hello
```

**Expected:**
- Browser opens automatically
- Shows Streamlit "Welcome" demo with animations
- If working, press Ctrl+C to stop

**If browser doesn't open:**
- Manually go to: http://localhost:8501

---

## Step 3: Run Your Demo

```bash
streamlit run src/app.py
```

**Expected:**
- Browser opens to http://localhost:8501
- Shows TEM IPA Manager Dashboard
- Demo banner at top (orange warning box)
- Fleet Overview page loads with 8 vessels

---

## Step 4: Test Each Feature

### ✅ Fleet Overview Page

**What to check:**
- Table shows 8 vessels
- Status column has emojis (✅ ⚠️ ❌)
- Northern Star shows "⚠️ WARNING"
- Sea Wolf shows "❌ VIOLATION"
- Arctic King shows "❌ VIOLATION"
- Bottom metrics show: 3-4 compliant, 1-2 warnings, 2-3 violations

**If something's wrong:**
- Check browser console for errors (F12)
- Verify `src/demo_data.py` exists

---

### ✅ Vessel Details Page (THE KILLER FEATURE)

**What to check:**

1. Click "Vessel Details" in sidebar

2. Select "Northern Star" from dropdown

3. Verify you see:
   - ⚠️ WARNING status badge (orange/yellow)
   - Current 4-Trip Average: ~290,000 lbs
   - Last 4 trips table
   - **Next Trip Calculator** section ⭐
   - Projection table with 4 scenarios
   - Custom calculator with input box
   - Chart showing all trips with trend line

4. Test custom calculator:
   - Enter "250000" in the input
   - Click "Calculate"
   - Should show green ✅ message: "New average would be 281,250 lbs - COMPLIANT"

5. Try "Northern Star" then switch to "Sea Wolf":
   - Should show ❌ VIOLATION (red)
   - Should show current average >300k

**This is your demo centerpiece - make sure it works perfectly!**

---

### ✅ Violation Reports Page

**What to check:**

1. Click "Violation Reports" in sidebar

2. Verify three sections:
   - **Trip Limit Violations:** Shows Sea Wolf (and maybe Ocean Voyager)
   - **Egregious Violations:** Shows Arctic King with 340,000 lbs trip
   - **MRA Violations:** Shows Golden Catch with Pacific Cod overage

3. Check "Export All Violations to CSV" button exists (won't download in demo)

---

### ✅ Upload Data Page

**What to check:**

1. Click "Upload Data" in sidebar

2. See file uploader widget

3. Click "Expected File Format" expander:
   - Shows table with example data format
   - Has vessel_id, delivery_date, pollock_lbs columns

4. **Optional:** Create a test CSV to upload:
   - Create `test_upload.csv` with:
   ```csv
   vessel_id,delivery_date,pollock_lbs,season,fishing_year
   AK-9999,2026-03-01,280000,A,2026
   AK-9999,2026-03-04,290000,A,2026
   ```
   - Upload it
   - Should show "File uploaded successfully: 2 rows"
   - Should show data preview table
   - Should show green validation checkmarks

---

## Step 5: Visual Check

**Theme and Branding:**
- Primary color is blue (#0066CC)
- Clean, professional appearance
- Footer shows "fishermenfirst.org"
- Demo banner at top is orange
- Status colors work: Green ✅, Yellow/Orange ⚠️, Red ❌

**Charts:**
- Trip history chart has two dashed lines (300k and 335k limits)
- Points are connected with lines
- Current 4-trip window highlighted with red circles
- Hover shows trip details

---

## Step 6: Performance Check

**Test responsiveness:**
1. Switch between vessels quickly (dropdown)
2. Navigate between pages (sidebar)
3. Should feel fast (<1 second)

**If slow:**
- Normal for first load (Streamlit compiles)
- Subsequent actions should be fast
- This is test data - no database delays

---

## Common Issues

### Import Error: "No module named 'demo_data'"

**Fix:**
```bash
# Make sure you're in the right directory
cd C:\Users\vikra\Git\ff-planning

# Check structure
dir src
# Should show: app.py, demo_data.py

# Run from project root
streamlit run src/app.py
```

### Port Already in Use

**Fix:**
```bash
# Stop existing Streamlit process
# Press Ctrl+C in terminal

# Or specify different port
streamlit run src/app.py --server.port 8502
```

### Blank Page or Errors

**Fix:**
1. Check terminal for error messages
2. Common issues:
   - Missing dependency: `pip install [package]`
   - Python version too old: Need 3.8+
   - File path issues: Run from project root

---

## Success Criteria

✅ Demo loads without errors
✅ All 8 vessels appear in Fleet Overview
✅ Northern Star shows WARNING status
✅ Next Trip Calculator works (custom input)
✅ Charts display with proper formatting
✅ Upload page shows file uploader
✅ Theme colors are correct (blue primary)

---

## Ready to Deploy?

If all tests pass, you're ready for Railway deployment!

**Next:** See `DEPLOYMENT_GUIDE.md`

---

## Demo Tips

**For interview committee:**

1. **Start with Northern Star** (the warning vessel)
   - Shows proactive support
   - Use Next Trip Calculator
   - Say: "IPA Manager can call them right now and say 'Keep your next trip under 275k'"

2. **Show Arctic King** (egregious)
   - Point to chart spike
   - Shows you understand all the rules

3. **Mention production features**
   - "This is test data - production will connect to real eLandings"
   - "We'll add authentication so only IPA Manager can access"
   - "Database will persist all historical data"

4. **Keep it short**
   - 5-minute demo is perfect
   - Don't show every vessel
   - Focus on the value: proactive support vs. just reporting

Good luck! 🐟
