# Retool AI Assistant Prompts - TEM IPA Manager Dashboard

Complete guide to building the TEM IPA Manager Dashboard in Retool using AI prompts.

**Estimated build time:** 3-4 hours
**Cost:** Free tier (up to 5 users) or $10/user/month for paid tier

---

## Prerequisites

1. **Retool account** - Sign up at https://retool.com
2. **Google Sheet with test data** - See "Data Preparation" section below
3. **Basic Retool familiarity** - Know how to create apps, add components, create queries

---

## Architecture Overview

### **Pages (4 total):**
1. Fleet Overview - Summary table + metrics
2. Vessel Details - Individual vessel with Next Trip Calculator
3. Violation Reports - All violations by type
4. Upload Data - CSV import interface

### **Data Source:**
- Google Sheets (3 tabs: vessels, trips, violations)
- Connect as Resource in Retool

### **Key Components:**
- Tables (vessel lists, trip history)
- Charts (Plotly line charts for trip history)
- Select dropdowns (vessel selector)
- Number inputs (Next Trip Calculator)
- Statistic cards (fleet metrics)
- Buttons (calculate, export, import)

---

## Step 1: Data Preparation (30 minutes)

### **Create Google Sheet: "TEM IPA Demo Data"**

#### **Tab 1: vessels_summary**

| id | name | status | avg_lbs | total_trips | last_4_trips |
|----|------|--------|---------|-------------|--------------|
| AK-7721 | Pacific Hunter | COMPLIANT | 248750 | 10 | T007,T008,T009,T010 |
| AK-8832 | Northern Star | WARNING | 292500 | 10 | T017,T018,T019,T020 |
| AK-6543 | Sea Wolf | VIOLATION | 307500 | 10 | T027,T028,T029,T030 |
| AK-9214 | Arctic King | VIOLATION | 271250 | 10 | T037,T038,T039,T040 |
| AK-5678 | Ocean Voyager | COMPLIANT | 267500 | 10 | T047,T048,T049,T050 |
| AK-4421 | Blue Horizon | INCOMPLETE | 0 | 2 | T051,T052 |
| AK-7893 | Silver Fin | COMPLIANT | 270250 | 8 | T061,T062,T063,T064 |
| AK-3156 | Golden Catch | COMPLIANT | 272625 | 8 | T069,T070,T071,T072 |

#### **Tab 2: trips**

| trip_id | vessel_id | vessel_name | delivery_date | pollock_lbs | pcod_lbs | other_lbs | season | year |
|---------|-----------|-------------|---------------|-------------|----------|-----------|--------|------|
| T001 | AK-7721 | Pacific Hunter | 2026-01-20 | 240000 | 36000 | 2400 | A | 2026 |
| T002 | AK-7721 | Pacific Hunter | 2026-01-23 | 255000 | 38250 | 2550 | A | 2026 |
| T003 | AK-7721 | Pacific Hunter | 2026-01-26 | 248000 | 37200 | 2480 | A | 2026 |
| T004 | AK-7721 | Pacific Hunter | 2026-01-29 | 252000 | 37800 | 2520 | A | 2026 |
| T005 | AK-7721 | Pacific Hunter | 2026-02-01 | 245000 | 36750 | 2450 | A | 2026 |
| T006 | AK-7721 | Pacific Hunter | 2026-02-04 | 258000 | 38700 | 2580 | A | 2026 |
| T007 | AK-7721 | Pacific Hunter | 2026-02-07 | 250000 | 37500 | 2500 | A | 2026 |
| T008 | AK-7721 | Pacific Hunter | 2026-02-10 | 246000 | 36900 | 2460 | A | 2026 |
| T009 | AK-7721 | Pacific Hunter | 2026-02-13 | 253000 | 37950 | 2530 | A | 2026 |
| T010 | AK-7721 | Pacific Hunter | 2026-02-16 | 249000 | 37350 | 2490 | A | 2026 |
| T011 | AK-8832 | Northern Star | 2026-01-20 | 260000 | 36400 | 2600 | A | 2026 |
| T012 | AK-8832 | Northern Star | 2026-01-23 | 270000 | 37800 | 2700 | A | 2026 |
| T013 | AK-8832 | Northern Star | 2026-01-26 | 275000 | 38500 | 2750 | A | 2026 |
| T014 | AK-8832 | Northern Star | 2026-01-29 | 280000 | 39200 | 2800 | A | 2026 |
| T015 | AK-8832 | Northern Star | 2026-02-01 | 285000 | 39900 | 2850 | A | 2026 |
| T016 | AK-8832 | Northern Star | 2026-02-04 | 288000 | 40320 | 2880 | A | 2026 |
| T017 | AK-8832 | Northern Star | 2026-02-07 | 290000 | 40600 | 2900 | A | 2026 |
| T018 | AK-8832 | Northern Star | 2026-02-10 | 292000 | 40880 | 2920 | A | 2026 |
| T019 | AK-8832 | Northern Star | 2026-02-13 | 295000 | 41300 | 2950 | A | 2026 |
| T020 | AK-8832 | Northern Star | 2026-02-16 | 293000 | 41020 | 2930 | A | 2026 |

*Continue for all 8 vessels... (68 trips total)*

#### **Tab 3: violations**

| violation_id | vessel_id | vessel_name | violation_type | trip_ids | details | overage_lbs |
|--------------|-----------|-------------|----------------|----------|---------|-------------|
| V001 | AK-6543 | Sea Wolf | TRIP_LIMIT | T027,T028,T029,T030 | 4-trip avg: 307,500 lbs | 7500 |
| V002 | AK-9214 | Arctic King | EGREGIOUS | T035 | Single trip: 340,000 lbs | 5000 |
| V003 | AK-3156 | Golden Catch | MRA | T072 | Pacific Cod: 24% (limit 20%) | 4% over |

**Download CSV template:** I'll create this for you below.

---

## Step 2: Connect Google Sheet to Retool (10 minutes)

### **In Retool:**

1. Click **"Resources"** in left sidebar
2. Click **"Create New" → "Google Sheets"**
3. Authenticate with your Google account
4. Select the spreadsheet: **"TEM IPA Demo Data"**
5. Name the resource: **"TEM_IPA_Data"**
6. Click **"Create Resource"**

---

## Step 3: Create App and Navigation (15 minutes)

### **Create New App:**

1. In Retool, click **"Create New" → "App"**
2. Name: **"TEM IPA Manager Dashboard"**
3. Choose **"Multi-page app"**

### **Set Up Pages:**

1. Page 1: **"Fleet Overview"** (home page)
2. Page 2: **"Vessel Details"**
3. Page 3: **"Violation Reports"**
4. Page 4: **"Upload Data"**

### **Add Navigation (Sidebar):**

**Prompt for Retool AI:**
```
Add a sidebar navigation container with:
- App title "TEM IPA Manager Dashboard" at top
- Subtitle "2026 A Season - Vessel Support"
- Navigation buttons for all 4 pages (Fleet Overview, Vessel Details, Violation Reports, Upload Data)
- Fleet summary statistics at bottom showing:
  * Total Vessels
  * Violations
  * Warnings
  * Total Trips

Style with blue primary color (#0066CC)
```

---

## Step 4: Page 1 - Fleet Overview (45 minutes)

### **Prompt 1: Create Data Query**

```
Create a new query named "getVesselsSummary" that:
- Type: Google Sheets
- Resource: TEM_IPA_Data
- Sheet: vessels_summary
- Action: Read spreadsheet
- Range: A:F (all columns)
```

### **Prompt 2: Create Summary Stats**

```
Add 4 Statistic components in a row at the top of the page:

1. Compliant Vessels
   - Value: {{ getVesselsSummary.data.filter(v => v.status === 'COMPLIANT').length }}
   - Icon: checkCircle
   - Color: green

2. Warnings
   - Value: {{ getVesselsSummary.data.filter(v => v.status === 'WARNING').length }}
   - Icon: alert
   - Color: orange

3. Violations
   - Value: {{ getVesselsSummary.data.filter(v => v.status === 'VIOLATION').length }}
   - Icon: xCircle
   - Color: red

4. Total Trips
   - Value: {{ getVesselsSummary.data.reduce((sum, v) => sum + v.total_trips, 0) }}
   - Icon: trendingUp
   - Color: blue
```

### **Prompt 3: Create Vessels Table**

```
Add a Table component named "vesselTable" that displays all vessels with:

Data source: {{ getVesselsSummary.data }}

Columns:
1. Vessel Name (text)
2. Vessel ID (text)
3. Status (text with conditional formatting):
   - Background color:
     - Green (#d4f4dd) if status === 'COMPLIANT'
     - Orange (#fff4cc) if status === 'WARNING'
     - Red (#ffdddd) if status === 'VIOLATION'
     - Gray (#f0f0f0) if status === 'INCOMPLETE'
   - Add emoji prefix:
     - ✅ for COMPLIANT
     - ⚠️ for WARNING
     - ❌ for VIOLATION
     - ℹ️ for INCOMPLETE

4. 4-Trip Average (number):
   - Format: {{ currentRow.avg_lbs.toLocaleString() }} lbs
   - Hidden if status === 'INCOMPLETE'

5. Total Trips (number)

Sorting:
- Default sort by status priority (VIOLATION → WARNING → COMPLIANT → INCOMPLETE)

Height: Fill remaining page space
```

### **Prompt 4: Add Demo Banner**

```
Add a Banner component at the very top of the page:
- Type: warning
- Title: "DEMONSTRATION VERSION"
- Message: "This is a proof-of-concept with test data. Production system will include live eLandings integration, secure authentication, and database persistence."
- Dismissible: false
```

---

## Step 5: Page 2 - Vessel Details (90 minutes - THE MOST IMPORTANT PAGE)

### **Prompt 1: Create Vessel Selector**

```
Add a Select component named "vesselSelector" at the top:
- Label: "Select Vessel"
- Data source: {{ getVesselsSummary.data }}
- Option labels: {{ item.name }}
- Option values: {{ item.id }}
- Default value: AK-8832 (Northern Star - the warning vessel)
- Full width: true
```

### **Prompt 2: Get Vessel Trips Query**

```
Create a new query named "getVesselTrips" that:
- Type: Google Sheets
- Resource: TEM_IPA_Data
- Sheet: trips
- Action: Read spreadsheet
- Range: A:I (all columns)
- Additional JavaScript transformation:

return data.filter(trip => trip.vessel_id === vesselSelector.value)
           .sort((a, b) => new Date(a.delivery_date) - new Date(b.delivery_date))
```

### **Prompt 3: Status Banner**

```
Create a Container component named "statusBanner" that displays the current vessel status:

Use conditional formatting based on vessel status:

If status === 'VIOLATION':
- Background: #ffdddd (light red)
- Border: 2px solid #ff4444
- Text: ❌ VIOLATION - 4-Trip Average: {{ currentAvg.toLocaleString() }} lbs (Limit: 300,000 lbs)
- Show overage: {{ (currentAvg - 300000).toLocaleString() }} lbs over limit

If status === 'WARNING':
- Background: #fff4cc (light orange)
- Border: 2px solid #ff9800
- Text: ⚠️ WARNING - 4-Trip Average: {{ currentAvg.toLocaleString() }} lbs (Limit: 300,000 lbs)
- Show buffer: {{ (300000 - currentAvg).toLocaleString() }} lbs remaining

If status === 'COMPLIANT':
- Background: #d4f4dd (light green)
- Border: 2px solid #4caf50
- Text: ✅ COMPLIANT - 4-Trip Average: {{ currentAvg.toLocaleString() }} lbs (Limit: 300,000 lbs)
- Show buffer: {{ (300000 - currentAvg).toLocaleString() }} lbs buffer

If status === 'INCOMPLETE':
- Background: #f0f0f0 (gray)
- Text: ℹ️ Need {{ 4 - totalTrips }} more trips to calculate average

Padding: 20px
Border radius: 8px
Font size: 18px
```

### **Prompt 4: Metrics Row**

```
Add 3 Statistic components in a row below the status banner:

1. 4-Trip Average
   - Value: {{ currentAvg.toLocaleString() }} lbs
   - Hide if status === 'INCOMPLETE'

2. % of Limit Used
   - Value: {{ ((currentAvg / 300000) * 100).toFixed(1) }}%
   - Hide if status === 'INCOMPLETE'

3. Total Trips
   - Value: {{ getVesselTrips.data.length }}
```

### **Prompt 5: Last 4 Trips Table**

```
Create a Table component showing the most recent 4 trips:

Heading: "Last 4 Trips (Current Rolling Window)"

Data source: {{ getVesselTrips.data.slice(-4) }}

Columns:
1. Trip ID
2. Delivery Date (format: MMM DD, YYYY)
3. Pollock (lbs) - formatted with commas

Hide if vessel has fewer than 4 trips
```

### **Prompt 6: Next Trip Calculator (⭐ KILLER FEATURE)**

```
Create a section titled "📊 Next Trip Calculator" with:

Subtitle: "Proactive vessel support: Calculate what the new 4-trip average would be based on the next trip amount"

Component 1: Table showing preset scenarios
- Data source: JavaScript transformer named "calculatePresetProjections"
- Columns:
  * Next Trip Amount (formatted: 250,000 lbs, 280,000 lbs, 300,000 lbs, 320,000 lbs)
  * New 4-Trip Avg (calculated)
  * Result (status with emoji: ✅ COMPLIANT, ⚠️ WARNING, ❌ VIOLATION)

Component 2: Custom calculator
- NumberInput component named "customTripAmount"
  * Label: "Calculate custom amount"
  * Default value: 280000
  * Min: 0
  * Max: 500000
  * Step: 5000
  * Format: Show commas

- Button "Calculate" that triggers transformer

- Text component showing result:
  * If avg > 300000: ❌ New average would be XXX,XXX lbs - VIOLATION (red)
  * If avg > 285000: ⚠️ New average would be XXX,XXX lbs - WARNING (orange)
  * Else: ✅ New average would be XXX,XXX lbs - COMPLIANT (green)
```

### **JavaScript Transformer: calculatePresetProjections**

```javascript
// Get last 3 trips for selected vessel
const vesselTrips = getVesselTrips.data || [];
const last3 = vesselTrips.slice(-3);

if (last3.length < 3) {
  return [];
}

// Preset amounts to test
const presets = [250000, 280000, 300000, 320000];

return presets.map(amount => {
  const last3Total = last3.reduce((sum, t) => sum + t.pollock_lbs, 0);
  const newAvg = (last3Total + amount) / 4;

  let status, emoji;
  if (newAvg > 300000) {
    status = 'VIOLATION';
    emoji = '❌';
  } else if (newAvg > 285000) {
    status = 'WARNING';
    emoji = '⚠️';
  } else {
    status = 'COMPLIANT';
    emoji = '✅';
  }

  return {
    amount: amount.toLocaleString() + ' lbs',
    newAvg: newAvg.toLocaleString() + ' lbs',
    result: emoji + ' ' + status
  };
});
```

### **Prompt 7: Trip History Chart**

```
Add a Chart component (Plotly) showing trip history over time:

Title: "{{ vesselSelector.selectedItem.name }} - Pollock Catch per Trip"

Chart type: Line chart with markers

Data source: {{ getVesselTrips.data }}

X axis: delivery_date (formatted as dates)
Y axis: pollock_lbs

Additional elements:
- Horizontal reference line at 300,000 (dashed, orange, label: "4-Trip Avg Limit")
- Horizontal reference line at 335,000 (dashed, red, label: "Egregious Limit")
- Highlight last 4 trips with larger markers or different color

Height: 500px
```

---

## Step 6: Page 3 - Violation Reports (45 minutes)

### **Prompt 1: Get Violations Query**

```
Create query named "getViolations":
- Type: Google Sheets
- Resource: TEM_IPA_Data
- Sheet: violations
- Range: A:G (all columns)
```

### **Prompt 2: Trip Limit Violations Section**

```
Add section with heading "Trip Limit Violations (>300k lbs average)"

Table component showing trip limit violations:
- Data source: {{ getViolations.data.filter(v => v.violation_type === 'TRIP_LIMIT') }}
- Columns:
  * Vessel Name
  * Vessel ID
  * 4-Trip Average (from details field)
  * Overage (formatted with commas)
  * Trips in Window (trip_ids)

If no violations:
- Show green banner: "✅ No trip limit violations detected"
```

### **Prompt 3: Egregious Violations Section**

```
Add section with heading "Egregious Violations (>335k lbs single trip)"

Table component showing egregious violations:
- Data source: {{ getViolations.data.filter(v => v.violation_type === 'EGREGIOUS') }}
- Columns:
  * Vessel Name
  * Trip ID (from trip_ids)
  * Details (shows the catch amount)
  * Overage (overage_lbs)

If no violations:
- Show green banner: "✅ No egregious violations detected"
```

### **Prompt 4: MRA Violations Section**

```
Add section with heading "MRA Violations (Species Mix)"

Table component showing MRA violations:
- Data source: {{ getViolations.data.filter(v => v.violation_type === 'MRA') }}
- Columns:
  * Vessel Name
  * Trip ID
  * Species (extracted from details)
  * Actual % (from details)
  * Limit % (20% for Pacific Cod, 2% for Other)
  * Overage

If no violations:
- Show green banner: "✅ No MRA violations detected"
```

### **Prompt 5: Export Button**

```
Add button at bottom:
- Label: "📥 Export All Violations to CSV"
- Action: Download table data as CSV
- Filename: tem-ipa-violations-{{ new Date().toISOString().split('T')[0] }}.csv
```

---

## Step 7: Page 4 - Upload Data (30 minutes)

### **Prompt 1: File Upload Component**

```
Add FileInput component named "dataUpload":
- Label: "Upload Trip Data (CSV or Excel)"
- Accepted file types: .csv, .xlsx
- Max file size: 10MB
```

### **Prompt 2: Data Preview**

```
Add section that shows after file is uploaded:

Heading: "📋 Data Preview (first 10 rows)"

Table component:
- Data source: {{ dataUpload.parsedValue.slice(0, 10) }}
- Show all columns from uploaded file
- Height: 300px

Only visible when: {{ dataUpload.value.length > 0 }}
```

### **Prompt 3: Validation Checklist**

```
Add Container with heading "✔️ Validation Results"

Display checkmarks for:
✅ All required columns present (vessel_id, delivery_date, pollock_lbs, season, fishing_year)
✅ No duplicate trip IDs
✅ All dates valid
✅ All vessel IDs recognized
✅ All catch amounts are positive numbers
✅ Season/year data correct

Use JavaScript transformer to actually validate the data:

const data = dataUpload.parsedValue || [];
const requiredCols = ['vessel_id', 'delivery_date', 'pollock_lbs', 'season', 'fishing_year'];

const validations = {
  hasRequiredColumns: requiredCols.every(col => data[0]?.hasOwnProperty(col)),
  noDuplicates: new Set(data.map(r => r.trip_id)).size === data.length,
  validDates: data.every(r => !isNaN(Date.parse(r.delivery_date))),
  positiveAmounts: data.every(r => r.pollock_lbs > 0)
};

return validations;
```

### **Prompt 4: Import Button**

```
Add Button component:
- Label: "Import to Database"
- Type: Primary
- Disabled: {{ !allValidationsPassed }}
- Action: Show success notification (in demo, doesn't actually import)
- Success message: "✅ Successfully imported {{ dataUpload.parsedValue.length }} trips to database"

Add info text below:
"ℹ️ In production, data would be persisted to PostgreSQL and all calculations would update automatically"
```

### **Prompt 5: Expected Format Expandable**

```
Add Expandable container with:
- Title: "ℹ️ Expected File Format"
- Content: Table showing example format with columns:
  * vessel_id: AK-7721
  * delivery_date: 2026-01-20
  * pollock_lbs: 250000
  * pcod_lbs: 35000
  * other_lbs: 2500
  * season: A
  * fishing_year: 2026
```

---

## Step 8: Styling and Theme (20 minutes)

### **Global Theme Settings:**

1. Go to **App Settings** (gear icon)
2. Under **"Theme"**:
   - Primary color: `#0066CC` (blue)
   - Success color: `#4caf50` (green)
   - Warning color: `#ff9800` (orange)
   - Error color: `#ff4444` (red)
   - Font: Sans-serif

### **Add Custom CSS:**

```css
/* Custom styles */
.violation-row {
  background-color: #ffdddd !important;
}

.warning-row {
  background-color: #fff4cc !important;
}

.compliant-row {
  background-color: #d4f4dd !important;
}

/* Status badges */
.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-weight: 600;
  display: inline-block;
}

.status-compliant {
  background: #d4f4dd;
  color: #2d7738;
}

.status-warning {
  background: #fff4cc;
  color: #b26a00;
}

.status-violation {
  background: #ffdddd;
  color: #c62828;
}
```

---

## Step 9: Authentication (10 minutes)

### **Enable Built-in Auth:**

1. Go to **App Settings** → **"Permissions"**
2. Toggle **"Require authentication"** ON
3. Add users:
   - Add your email
   - Add "IPA Manager" user (demo email)
4. Set permission level: **"Use"** (can use app but not edit)

---

## Step 10: Deploy and Share (5 minutes)

### **Get Shareable Link:**

1. Click **"Share"** button (top right)
2. Toggle **"Public access"** ON (for demo) or OFF (for auth-only)
3. Copy link: `https://your-org.retool.com/apps/tem-ipa-dashboard`

### **Optional: Custom Domain (Paid Plan Only)**

1. Go to **Organization Settings** → **"Custom Domain"**
2. Add: `tem-ipa-demo.fishermenfirst.org`
3. Configure DNS CNAME record
4. Wait for SSL certificate provisioning

---

## CSV Template for Google Sheets

Save this as `tem-ipa-demo-data.csv`:

```csv
vessel_id,vessel_name,status,avg_lbs,total_trips
AK-7721,Pacific Hunter,COMPLIANT,248750,10
AK-8832,Northern Star,WARNING,292500,10
AK-6543,Sea Wolf,VIOLATION,307500,10
AK-9214,Arctic King,VIOLATION,271250,10
AK-5678,Ocean Voyager,COMPLIANT,267500,10
AK-4421,Blue Horizon,INCOMPLETE,0,2
AK-7893,Silver Fin,COMPLIANT,270250,8
AK-3156,Golden Catch,COMPLIANT,272625,8
```

---

## Testing Checklist

After building, test:

- [ ] Fleet Overview loads with 8 vessels
- [ ] Status colors correct (green/yellow/red)
- [ ] Click vessel → goes to Vessel Details page
- [ ] Select "Northern Star" → shows WARNING status
- [ ] Next Trip Calculator shows 4 preset scenarios
- [ ] Custom amount calculator works (enter 250000, click Calculate)
- [ ] Trip history chart displays with reference lines
- [ ] Violation Reports shows violations by type
- [ ] Upload Data page accepts CSV file
- [ ] Data preview displays uploaded data
- [ ] Mobile responsive (test on phone/tablet)

---

## Retool-Specific Tips

### **Best Practices:**

1. **Name everything clearly** - Use descriptive names for queries, transformers, components
2. **Use transformers for calculations** - Don't put complex JavaScript in component values
3. **Test queries independently** - Use "Preview" button before connecting to components
4. **Save frequently** - Retool auto-saves, but manually save after major changes
5. **Use containers for layout** - Group related components in containers
6. **Comment your code** - Add notes to transformers explaining logic

### **Common Pitfalls:**

- ❌ Don't hardcode data in component values (use queries)
- ❌ Don't create circular dependencies (query A depends on query B depends on query A)
- ❌ Don't use synchronous queries unless necessary (makes app slow)
- ❌ Don't skip error handling (always check if data exists before accessing)

---

## AI Prompt Templates

### **General Component Creation:**

```
Create a [component type] that:
1. [Primary function]
2. [Data source/binding]
3. [Formatting requirements]
4. [Conditional logic if any]
5. [Styling preferences]

Connect to: [query/transformer name]
Show when: [conditional display logic]
```

### **Query Creation:**

```
Create a new query named "[name]" that:
- Type: [Google Sheets/REST API/Database]
- Resource: [resource name]
- Action: [Read/Write/Update]
- Filters: [any WHERE conditions]
- Transformations: [JavaScript if needed]
- Runs when: [trigger - page load, button click, etc]
```

### **Transformer Creation:**

```
Create a JavaScript transformer named "[name]" that:
- Inputs: [list of component values or query results]
- Logic: [describe the calculation/transformation]
- Output: [what it returns - array, object, number, etc]
- Error handling: [what to return if inputs invalid]
```

---

## Time Estimates by Section

| Section | Time |
|---------|------|
| Data Preparation (Google Sheets) | 30 min |
| Connect Resource | 10 min |
| App Setup & Navigation | 15 min |
| Fleet Overview Page | 45 min |
| Vessel Details Page | 90 min |
| Violation Reports Page | 45 min |
| Upload Data Page | 30 min |
| Styling & Theme | 20 min |
| Authentication Setup | 10 min |
| Testing & Refinement | 30 min |
| **Total** | **~5.5 hours** |

Realistically, with AI assistance and some Retool familiarity: **3-4 hours**

---

## Support Resources

- **Retool Docs:** https://docs.retool.com
- **Community Forum:** https://community.retool.com
- **AI Assistant:** Available in-app (bottom right corner)
- **Templates:** Check Retool template library for similar dashboards

---

## Comparison: Retool vs Streamlit

| Feature | Retool | Streamlit (Already Built) |
|---------|--------|---------------------------|
| Build Time | 3-4 hours | 30 min (code done) |
| Cost | $0-20/month | $0-10/month |
| UI Polish | ⭐⭐⭐⭐⭐ Professional | ⭐⭐⭐⭐ Good |
| Authentication | Built-in | Manual setup |
| Custom Domain | Requires paid plan | Easy on Railway |
| Deployment Time | Immediate | 5 minutes |
| Code Control | Limited | Full control |
| Maintenance | Retool handles | You handle |

**Recommendation:** Deploy Streamlit now (30 min), build Retool version if you win contract and client prefers it.

---

Good luck with your demo! 🐟
