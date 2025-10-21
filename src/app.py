"""
TEM IPA Manager Dashboard - Demo Version
2026 A Season Vessel Trip Limit Support

Features:
- Real-time 4-trip rolling average monitoring
- Color-coded compliance status
- Next Trip Calculator (proactive vessel support)
- Violation reports
- Data upload interface
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from demo_data import (
    VESSELS, TRIPS_DF,
    calculate_trip_limit_status,
    calculate_next_trip_projection,
    check_egregious_violations,
    get_all_mra_violations,
    get_summary_stats,
    get_vessel_trips
)

# Page configuration
st.set_page_config(
    page_title="TEM IPA Manager Dashboard - Demo",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# AUTHENTICATION
# ============================================================================
# Demo credentials for interview committee
# In production, this would use database with proper password hashing

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_name = None
    st.session_state.username = None

# Demo user credentials
DEMO_USERS = {
    'demo': {'password': 'demo123', 'name': 'Demo User'},
    'ipa_manager': {'password': 'demo2026', 'name': 'IPA Manager'},
    'fishermen_first': {'password': 'ff2026', 'name': 'Fishermen First'}
}

# Login function
def login(username, password):
    if username in DEMO_USERS and DEMO_USERS[username]['password'] == password:
        st.session_state.authenticated = True
        st.session_state.user_name = DEMO_USERS[username]['name']
        st.session_state.username = username
        return True
    return False

# Logout function
def logout():
    st.session_state.authenticated = False
    st.session_state.user_name = None
    st.session_state.username = None

# Show login page if not authenticated
if not st.session_state.authenticated:
    st.title("🐟 TEM IPA Manager Dashboard")
    st.markdown("**2026 A Season - Vessel Trip Limit Support**")
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("🔐 Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", type="primary", use_container_width=True)

            if submit:
                if login(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    st.stop()

# Demo banner
st.markdown("""
<div style="background-color: #fff4e6; padding: 15px; border-radius: 5px; border-left: 5px solid #ff9800; margin-bottom: 20px;">
    <strong>⚠️ DEMONSTRATION VERSION</strong><br/>
    This is a proof-of-concept with test data. Production system will include live eLandings integration,
    secure authentication, database persistence, and complete MRA compliance checking.
</div>
""", unsafe_allow_html=True)

# Header
st.title("🐟 TEM IPA Manager Dashboard")
st.markdown("**2026 A Season - Vessel Trip Limit Support**")

# Sidebar navigation
with st.sidebar:
    # User info and logout
    st.markdown(f"### Welcome, {st.session_state.user_name}!")
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()

    st.markdown("---")
    st.header("📍 Navigation")
    page = st.radio(
        "Select Page",
        ["Fleet Overview", "Vessel Details", "Violation Reports", "Upload Data"],
        index=0
    )

    # Summary stats in sidebar
    st.markdown("---")
    st.subheader("📊 Fleet Summary")
    stats = get_summary_stats()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Vessels", stats['total_vessels'])
        st.metric("Trips", stats['total_trips'])
    with col2:
        st.metric("Violations", stats['violation'])
        st.metric("Warnings", stats['warning'])


# ============================================================================
# PAGE 1: FLEET OVERVIEW
# ============================================================================
if page == "Fleet Overview":
    st.header("📋 Fleet Overview - All Vessels")
    st.markdown("Quick status view of all vessels in the 2026 A Season")

    # Build summary table
    summary_data = []
    for vessel in VESSELS:
        status_info = calculate_trip_limit_status(vessel['vessel_id'])

        if status_info['status'] == 'INSUFFICIENT_DATA':
            summary_data.append({
                'Vessel Name': vessel['vessel_name'],
                'Vessel ID': vessel['vessel_id'],
                'Status': 'Need More Data',
                '4-Trip Avg': f"Need {status_info['trips_needed']} more trips",
                'Trips': len(status_info['all_trips']),
                'Sort': 4  # For sorting
            })
        else:
            # Status emoji
            if status_info['status'] == 'VIOLATION':
                status_display = '❌ VIOLATION'
                sort_order = 1
            elif status_info['status'] == 'WARNING':
                status_display = '⚠️ WARNING'
                sort_order = 2
            else:
                status_display = '✅ COMPLIANT'
                sort_order = 3

            summary_data.append({
                'Vessel Name': vessel['vessel_name'],
                'Vessel ID': vessel['vessel_id'],
                'Status': status_display,
                '4-Trip Avg': f"{status_info['avg']:,.0f} lbs",
                'Trips': len(status_info['all_trips']),
                'Sort': sort_order
            })

    # Sort by status (violations first)
    summary_df = pd.DataFrame(summary_data).sort_values('Sort')
    summary_df = summary_df.drop('Sort', axis=1)

    # Display table
    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )

    # Key metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "✅ Compliant",
            stats['compliant'],
            help="Vessels with <285k lbs 4-trip average"
        )

    with col2:
        st.metric(
            "⚠️ Warnings",
            stats['warning'],
            help="Vessels with 285k-300k lbs 4-trip average"
        )

    with col3:
        st.metric(
            "❌ Violations",
            stats['violation'],
            help="Vessels with >300k lbs 4-trip average"
        )

    with col4:
        st.metric(
            "🚨 Egregious",
            stats['egregious_violations'],
            help="Single trips >335k lbs"
        )


# ============================================================================
# PAGE 2: VESSEL DETAILS (with Next Trip Calculator)
# ============================================================================
elif page == "Vessel Details":
    st.header("🔍 Vessel Details")

    # Vessel selector
    vessel_options = {v['vessel_name']: v for v in VESSELS}
    selected_vessel_name = st.selectbox("Select Vessel", list(vessel_options.keys()))
    selected_vessel = vessel_options[selected_vessel_name]

    st.markdown(f"**Vessel ID:** {selected_vessel['vessel_id']}")

    # Get status
    status_info = calculate_trip_limit_status(selected_vessel['vessel_id'])

    # Status display
    st.markdown("### Current Status")

    if status_info['status'] == 'INSUFFICIENT_DATA':
        st.info(f"ℹ️ **Need {status_info['trips_needed']} more trips** to calculate 4-trip average")
        st.markdown(f"**Trips completed:** {len(status_info['all_trips'])}")

    else:
        # Status badge with color
        if status_info['status'] == 'VIOLATION':
            st.error(f"❌ **VIOLATION** - 4-Trip Average: **{status_info['avg']:,.0f} lbs** (Limit: 300,000 lbs)")
            st.markdown(f"**Overage:** {status_info['avg'] - 300000:,.0f} lbs over limit")
        elif status_info['status'] == 'WARNING':
            st.warning(f"⚠️ **WARNING** - 4-Trip Average: **{status_info['avg']:,.0f} lbs** (Limit: 300,000 lbs)")
            remaining = 300000 - status_info['avg']
            st.markdown(f"**Buffer remaining:** {remaining:,.0f} lbs before violation")
        else:
            st.success(f"✅ **COMPLIANT** - 4-Trip Average: **{status_info['avg']:,.0f} lbs** (Limit: 300,000 lbs)")
            remaining = 300000 - status_info['avg']
            st.markdown(f"**Buffer remaining:** {remaining:,.0f} lbs before warning threshold")

        # Metrics row
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("4-Trip Average", f"{status_info['avg']:,.0f} lbs")

        with col2:
            pct_used = (status_info['avg'] / 300000) * 100
            st.metric("% of Limit", f"{pct_used:.1f}%")

        with col3:
            st.metric("Total Trips", len(status_info['all_trips']))

        # Last 4 trips table
        st.markdown("---")
        st.markdown("### Last 4 Trips (Current Rolling Window)")
        trips_df = pd.DataFrame(status_info['trips'])
        trips_df['delivery_date'] = pd.to_datetime(trips_df['delivery_date']).dt.strftime('%b %d, %Y')
        trips_display = trips_df[['trip_id', 'delivery_date', 'pollock_lbs']].copy()
        trips_display.columns = ['Trip ID', 'Delivery Date', 'Pollock (lbs)']
        trips_display['Pollock (lbs)'] = trips_display['Pollock (lbs)'].apply(lambda x: f"{x:,}")

        st.dataframe(trips_display, use_container_width=True, hide_index=True)

        # ===== KILLER FEATURE: NEXT TRIP CALCULATOR =====
        st.markdown("---")
        st.markdown("### 📊 Next Trip Calculator")
        st.markdown("**Proactive vessel support:** Calculate what the new 4-trip average would be based on the next trip amount")

        # Preset projections
        projections = calculate_next_trip_projection(selected_vessel['vessel_id'])

        if projections:
            st.markdown("**Projected scenarios:**")

            proj_data = []
            for proj in projections:
                if proj['status'] == 'VIOLATION':
                    status_icon = '❌'
                elif proj['status'] == 'WARNING':
                    status_icon = '⚠️'
                else:
                    status_icon = '✅'

                proj_data.append({
                    'Next Trip Amount': f"{proj['amount']:,} lbs",
                    'New 4-Trip Avg': f"{proj['new_avg']:,.0f} lbs",
                    'Result': f"{status_icon} {proj['status']}"
                })

            proj_df = pd.DataFrame(proj_data)
            st.dataframe(proj_df, use_container_width=True, hide_index=True)

            # Custom calculator
            st.markdown("**Calculate custom amount:**")
            col1, col2 = st.columns([3, 1])

            with col1:
                custom_amount = st.number_input(
                    "Next trip amount (lbs)",
                    min_value=0,
                    max_value=500000,
                    value=280000,
                    step=5000,
                    help="Enter expected catch amount for next trip"
                )

            with col2:
                st.write("")  # Spacing
                st.write("")  # Spacing
                calculate_btn = st.button("Calculate", type="primary")

            if calculate_btn or custom_amount:
                custom_proj = calculate_next_trip_projection(
                    selected_vessel['vessel_id'],
                    [custom_amount]
                )[0]

                if custom_proj['status'] == 'VIOLATION':
                    st.error(f"❌ New average would be **{custom_proj['new_avg']:,.0f} lbs** - VIOLATION")
                elif custom_proj['status'] == 'WARNING':
                    st.warning(f"⚠️ New average would be **{custom_proj['new_avg']:,.0f} lbs** - WARNING")
                else:
                    st.success(f"✅ New average would be **{custom_proj['new_avg']:,.0f} lbs** - COMPLIANT")

    # Trip history chart
    st.markdown("---")
    st.markdown("### 📈 Trip History")

    all_trips = get_vessel_trips(selected_vessel['vessel_id'])

    if len(all_trips) > 0:
        # Create chart
        fig = go.Figure()

        # Add trip points
        fig.add_trace(go.Scatter(
            x=all_trips['delivery_date'],
            y=all_trips['pollock_lbs'],
            mode='lines+markers',
            name='Pollock Catch',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=10)
        ))

        # Add 4-trip average limit line (without annotation)
        fig.add_hline(
            y=300000,
            line_dash="dash",
            line_color="orange",
            line_width=2,
            annotation_text="",
        )

        # Add egregious limit line (without annotation)
        fig.add_hline(
            y=335000,
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text="",
        )

        # Add invisible traces for legend entries
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='lines',
            name='4-Trip Limit (300k)',
            line=dict(color='orange', width=2, dash='dash'),
            showlegend=True
        ))

        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='lines',
            name='Egregious (335k)',
            line=dict(color='red', width=2, dash='dash'),
            showlegend=True
        ))

        # Highlight current 4-trip window
        if status_info['status'] != 'INSUFFICIENT_DATA':
            last_4_trips = pd.DataFrame(status_info['trips'])
            fig.add_trace(go.Scatter(
                x=last_4_trips['delivery_date'],
                y=last_4_trips['pollock_lbs'],
                mode='markers',
                name='Current 4-Trip Window',
                marker=dict(size=14, color='#ff4444', symbol='circle-open', line=dict(width=3))
            ))

        fig.update_layout(
            title={
                'text': f"{selected_vessel_name} - Pollock Catch per Trip",
                'font': {'size': 20}
            },
            xaxis_title="Delivery Date",
            yaxis_title="Pollock (lbs)",
            hovermode='x unified',
            height=650,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            margin=dict(l=80, r=40, t=80, b=100),
            font=dict(size=13)
        )

        # Format y-axis with commas
        fig.update_yaxes(tickformat=',')

        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PAGE 3: VIOLATION REPORTS
# ============================================================================
elif page == "Violation Reports":
    st.header("⚠️ Violation Reports")

    # Trip Limit Violations
    st.subheader("Trip Limit Violations (>300k lbs average)")
    trip_violations = []

    for vessel in VESSELS:
        status_info = calculate_trip_limit_status(vessel['vessel_id'])
        if status_info['status'] == 'VIOLATION':
            trip_violations.append({
                'Vessel Name': vessel['vessel_name'],
                'Vessel ID': vessel['vessel_id'],
                '4-Trip Average': f"{status_info['avg']:,.0f} lbs",
                'Overage': f"{status_info['avg'] - 300000:,.0f} lbs",
                'Trips in Window': ', '.join([t['trip_id'] for t in status_info['trips']])
            })

    if trip_violations:
        st.dataframe(pd.DataFrame(trip_violations), use_container_width=True, hide_index=True)
        st.markdown(f"**Total vessels in violation:** {len(trip_violations)}")
    else:
        st.success("✅ No trip limit violations detected")

    # Egregious Violations
    st.markdown("---")
    st.subheader("Egregious Violations (>335k lbs single trip)")
    egregious = check_egregious_violations()

    if len(egregious) > 0:
        egregious_display = egregious[['trip_id', 'vessel_name', 'delivery_date', 'pollock_lbs']].copy()
        egregious_display['delivery_date'] = pd.to_datetime(egregious_display['delivery_date']).dt.strftime('%b %d, %Y')
        egregious_display.columns = ['Trip ID', 'Vessel Name', 'Delivery Date', 'Pollock (lbs)']
        egregious_display['Pollock (lbs)'] = egregious_display['Pollock (lbs)'].apply(lambda x: f"{x:,}")
        egregious_display['Overage'] = egregious['pollock_lbs'].apply(lambda x: f"{x - 335000:,} lbs over")

        st.dataframe(egregious_display, use_container_width=True, hide_index=True)
        st.markdown(f"**Total egregious violations:** {len(egregious)}")
    else:
        st.success("✅ No egregious violations detected")

    # MRA Violations
    st.markdown("---")
    st.subheader("MRA Violations (Species Mix)")
    mra_violations = get_all_mra_violations()

    if len(mra_violations) > 0:
        mra_display = mra_violations.copy()
        mra_display['delivery_date'] = pd.to_datetime(mra_display['delivery_date']).dt.strftime('%b %d, %Y')
        mra_display['actual_pct'] = mra_display['actual_pct'].apply(lambda x: f"{x:.1f}%")
        mra_display['limit_pct'] = mra_display['limit_pct'].apply(lambda x: f"{x:.0f}%")
        mra_display['overage_lbs'] = mra_display['overage_lbs'].apply(lambda x: f"{x:,} lbs")

        mra_display.columns = ['Trip ID', 'Vessel Name', 'Delivery Date', 'Species', 'Actual %', 'Limit %', 'Overage']
        st.dataframe(mra_display, use_container_width=True, hide_index=True)
        st.markdown(f"**Total MRA violations:** {len(mra_violations)}")
    else:
        st.success("✅ No MRA violations detected")

    # Export button
    st.markdown("---")
    if st.button("📥 Export All Violations to CSV"):
        st.info("ℹ️ In production, this would generate a downloadable CSV file with all violation data")


# ============================================================================
# PAGE 4: UPLOAD DATA
# ============================================================================
elif page == "Upload Data":
    st.header("📤 Upload Trip Data")
    st.markdown("Upload eLandings CSV export to import new trip data into the system")

    uploaded_file = st.file_uploader(
        "Choose CSV or Excel file",
        type=['csv', 'xlsx'],
        help="Upload trip data from eLandings export"
    )

    if uploaded_file:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success(f"✅ File uploaded successfully: **{len(df)}** rows")

            # Preview
            st.subheader("📋 Data Preview (first 10 rows)")
            st.dataframe(df.head(10), use_container_width=True)

            # Mock validation
            st.subheader("✔️ Validation Results")

            col1, col2 = st.columns(2)

            with col1:
                st.success("✅ All required columns present")
                st.success("✅ No duplicate trips detected")
                st.success("✅ All dates valid")

            with col2:
                st.success("✅ All vessel IDs recognized")
                st.success("✅ All catch amounts valid")
                st.success("✅ Season/year data correct")

            # Import button
            st.markdown("---")
            if st.button("Import to Database", type="primary"):
                with st.spinner("Importing data..."):
                    import time
                    time.sleep(1)  # Simulate processing
                    st.success(f"✅ Successfully imported {len(df)} trips to database")
                    st.info("ℹ️ In production, data would be persisted to PostgreSQL and all calculations would update automatically")

        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.markdown("Please ensure file is in correct eLandings format")

    else:
        st.info("📁 No file uploaded yet. Please select a CSV or Excel file above.")

        # Show expected format
        with st.expander("ℹ️ Expected File Format"):
            st.markdown("""
            **Required columns:**
            - `vessel_id` - Vessel identifier (e.g., AK-7721)
            - `delivery_date` - Date of delivery (YYYY-MM-DD)
            - `pollock_lbs` - Pollock catch in pounds
            - `season` - A or B season
            - `fishing_year` - Year (e.g., 2026)

            **Optional columns:**
            - `pcod_lbs` - Pacific Cod catch in pounds
            - `other_lbs` - Other species catch in pounds

            **Example:**
            """)

            example_df = pd.DataFrame({
                'vessel_id': ['AK-7721', 'AK-8832'],
                'delivery_date': ['2026-01-20', '2026-01-22'],
                'pollock_lbs': [250000, 275000],
                'pcod_lbs': [35000, 40000],
                'other_lbs': [2500, 2800],
                'season': ['A', 'A'],
                'fishing_year': [2026, 2026]
            })

            st.dataframe(example_df, use_container_width=True, hide_index=True)


# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; font-size: 0.9em;">'
    '🐟 TEM IPA Manager Dashboard | <strong>fishermenfirst.org</strong> | Demo Version | 2026 A Season'
    '</div>',
    unsafe_allow_html=True
)
