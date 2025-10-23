"""
CGOA Rockfish Program Analytics Dashboard
Demo platform for Fisherman First LLC proposal
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import demo_data

# Page config
st.set_page_config(
    page_title="CGOA Rockfish Analytics",
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
    st.title("🐟 CGOA Rockfish Analytics Dashboard")
    st.markdown("**2026 Rockfish Program Manager**")
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

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #0E7490;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #0E7490;
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
    }
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        opacity: 0.9;
    }
    .metric-value {
        font-size: 1.875rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    .alert-card {
        padding: 1rem;
        border-radius: 0.375rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid;
    }
    .alert-red {
        background-color: #FEE2E2;
        border-color: #DC2626;
    }
    .alert-orange {
        background-color: #FED7AA;
        border-color: #EA580C;
    }
    .alert-yellow {
        background-color: #FEF3C7;
        border-color: #CA8A04;
    }
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        display: inline-block;
    }
    .badge-green {
        background-color: #D1FAE5;
        color: #065F46;
    }
    .badge-orange {
        background-color: #FED7AA;
        color: #9A3412;
    }
    .badge-red {
        background-color: #FEE2E2;
        color: #991B1B;
    }
    </style>
""", unsafe_allow_html=True)

# Load demo data
@st.cache_data
def get_data():
    return demo_data.load_demo_data()

data = get_data()

# Sidebar navigation
st.sidebar.markdown(f"### Welcome, {st.session_state.user_name}!")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    logout()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🐟 CGOA Rockfish Analytics")
st.sidebar.markdown("*Demo Platform*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "🚢 Vessels", "🏛️ Board Report", "🔄 Transfers"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**2026 Rockfish Program Overview**")
st.sidebar.markdown("**Season:** April 1 - November 15")
st.sidebar.markdown("**Cooperatives:** 4")
st.sidebar.markdown("**Active Vessels:** 22")

# Demo banner
st.markdown("""
<div style="background-color: #fff4e6; padding: 15px; border-radius: 5px; border-left: 5px solid #ff9800; margin-bottom: 20px;">
    <strong>⚠️ DEMONSTRATION VERSION</strong><br/>
    This is a proof-of-concept with test data. Production system will include live eLandings integration,
    secure authentication, database persistence, and complete quota management features.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
if page == "📊 Dashboard":
    st.markdown('<div class="main-header">Rockfish Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">2026 Rockfish Program Overview</div>', unsafe_allow_html=True)

    # Calculate metrics
    vessels_df = data['vessels']
    coops_df = data['cooperatives']
    weekly_df = data['weekly_harvest']

    total_allocated = vessels_df['cq_allocation_mt'].sum()
    total_harvested = vessels_df['harvest_to_date_mt'].sum()
    harvest_pct = (total_harvested / total_allocated) * 100

    total_chinook = vessels_df['chinook_psc_count'].sum()
    chinook_cap = 1200
    chinook_pct = (total_chinook / chinook_cap) * 100

    total_halibut = vessels_df['halibut_psc_count'].sum()
    # Halibut cap not specified in RFP, using 650 as example
    halibut_cap = 650
    halibut_pct = (total_halibut / halibut_cap) * 100

    # Top metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Cooperative Quota (Allocated / Harvested)</div>
            <div class="metric-value">100% / {harvest_pct:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Chinook PSC Cap (PSC)</div>
            <div class="metric-value">{total_chinook:,} / {chinook_cap:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Halibut PSC Used</div>
            <div class="metric-value">{halibut_pct:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Active Alerts
    st.subheader("Active Alerts")
    alerts_df = data['alerts']

    for _, alert in alerts_df.iterrows():
        alert_class = f"alert-{alert['badge_color']}"
        st.markdown(f"""
        <div class="alert-card {alert_class}">
            <strong>{alert['vessel_name']}</strong><br>
            {alert['message'].split(':')[1] if ':' in alert['message'] else alert['message']}
            <span class="status-badge badge-{alert['badge_color']}" style="float: right;">{alert['alert_type']}</span>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# VESSELS PAGE
# ============================================================================
elif page == "🚢 Vessels":
    st.markdown('<div class="main-header">Vessel Performance Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">2026 Rockfish Program Vessel Analytics</div>', unsafe_allow_html=True)

    vessels_df = data['vessels']

    # Filters
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_coop = st.multiselect(
            "Filter by Cooperative",
            options=vessels_df['cooperative_name'].unique(),
            default=vessels_df['cooperative_name'].unique()
        )
    with col2:
        status_filter = st.multiselect(
            "Filter by Status",
            options=vessels_df['status'].unique(),
            default=vessels_df['status'].unique()
        )

    # Filter data
    filtered_df = vessels_df[
        (vessels_df['cooperative_name'].isin(selected_coop)) &
        (vessels_df['status'].isin(status_filter))
    ]

    st.markdown("### Fleet Performance Summary")

    # Format the dataframe for display
    display_df = filtered_df[['vessel_name', 'cooperative_name', 'cq_allocation_mt',
                               'harvest_to_date_mt', 'quota_balance_mt', 'chinook_psc_count',
                               'halibut_psc_count', 'status']].copy()

    display_df.columns = ['Vessel', 'Cooperative', 'CQ Allocation', 'Harvest-to-Date',
                          'Quota Balance', 'Chinook PSC', 'Halibut PSC', 'Status']

    # Style the dataframe
    def style_status(val):
        if val == 'Overage':
            return 'background-color: #FEE2E2; color: #991B1B; font-weight: 600'
        elif val == 'Near Overage':
            return 'background-color: #FED7AA; color: #9A3412; font-weight: 600'
        else:
            return 'background-color: #D1FAE5; color: #065F46; font-weight: 600'

    def style_balance(val):
        if val < 0:
            return 'color: #DC2626; font-weight: 600'
        return ''

    styled_df = display_df.style.applymap(style_status, subset=['Status']) \
                                  .applymap(style_balance, subset=['Quota Balance'])

    st.dataframe(styled_df, use_container_width=True, height=600)

    # Summary stats
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Vessels", len(filtered_df))
    with col2:
        in_compliance = len(filtered_df[filtered_df['status'] == 'In Compliance'])
        st.metric("In Compliance", in_compliance)
    with col3:
        with_overage = len(filtered_df[filtered_df['status'] == 'Overage'])
        st.metric("With Overages", with_overage)
    with col4:
        total_chinook = filtered_df['chinook_psc_count'].sum()
        st.metric("Total Chinook PSC", f"{total_chinook:,}")

# ============================================================================
# BOARD REPORT PAGE
# ============================================================================
elif page == "🏛️ Board Report":
    st.markdown('<div class="main-header">Board Summary Report – 2026 Rockfish Program</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprehensive fleet performance and program analytics</div>', unsafe_allow_html=True)

    vessels_df = data['vessels']
    coops_df = data['cooperatives']
    weekly_df = data['weekly_harvest']

    # Calculate metrics
    total_vessels = len(vessels_df)
    total_quota = vessels_df['cq_allocation_mt'].sum()
    total_harvested = vessels_df['harvest_to_date_mt'].sum()
    fleet_harvested_pct = (total_harvested / total_quota) * 100

    # Calculate total forfeitures (overages)
    overages = vessels_df[vessels_df['quota_balance_mt'] < 0]['quota_balance_mt'].abs().sum()
    forfeit_value = overages * 1.0  # $1/lb = ~$2000/mt, simplified to $18,500 for demo
    total_forfeitures = 18500

    total_chinook = vessels_df['chinook_psc_count'].sum()
    chinook_cap = 1200
    chinook_pct = (total_chinook / chinook_cap) * 100

    total_halibut = vessels_df['halibut_psc_count'].sum()
    halibut_cap = 650
    halibut_pct = (total_halibut / halibut_cap) * 100

    fleet_psc_rate = (total_chinook / total_harvested) * 1000  # Chinook per 1000mt

    vessels_in_compliance = len(vessels_df[vessels_df['status'] == 'In Compliance'])
    vessels_with_overages = len(vessels_df[vessels_df['status'] == 'Overage'])
    settlement_rate = (vessels_in_compliance / total_vessels) * 100

    # Top KPI cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Vessels</div>
            <div class="metric-value">{total_vessels}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Quota</div>
            <div class="metric-value">{total_quota:,.0f} mt</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Fleet Harvested</div>
            <div class="metric-value">{fleet_harvested_pct:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Forfeitures</div>
            <div class="metric-value">${total_forfeitures:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # PSC Summary and Program Compliance
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### PSC Summary")
        psc_data = pd.DataFrame({
            'Metric': ['Chinook PSC Used:', 'Halibut PSC Used:', 'Fleet PSC Rate:'],
            'Value': [
                f'{total_chinook:,} / {chinook_cap:,} ({chinook_pct:.0f}%)',
                f'{total_halibut:,} / {halibut_cap:,} ({halibut_pct:.0f}%)',
                f'{fleet_psc_rate:.1f}%'
            ]
        })
        st.dataframe(psc_data, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("### Program Compliance")
        compliance_data = pd.DataFrame({
            'Metric': ['Vessels in Compliance:', 'Vessels with Overages:', 'Settlement Rate:'],
            'Value': [
                f'{vessels_in_compliance} / {total_vessels}',
                f'{vessels_with_overages}',
                f'{settlement_rate:.1f}%'
            ]
        })
        st.dataframe(compliance_data, hide_index=True, use_container_width=True)

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Quota Usage by Cooperative (%)")

        # Calculate quota usage by cooperative
        coop_usage = vessels_df.groupby('cooperative_name').agg({
            'harvest_to_date_mt': 'sum',
            'cq_allocation_mt': 'sum'
        }).reset_index()
        coop_usage['usage_pct'] = (coop_usage['harvest_to_date_mt'] / coop_usage['cq_allocation_mt']) * 100

        fig_coop = go.Figure(data=[
            go.Bar(
                x=coop_usage['cooperative_name'],
                y=coop_usage['usage_pct'],
                marker_color='#0E7490',
                text=coop_usage['usage_pct'].round(0).astype(str) + '%',
                textposition='outside'
            )
        ])
        fig_coop.update_layout(
            xaxis_title="",
            yaxis_title="Usage %",
            showlegend=False,
            height=300,
            margin=dict(t=20, b=20),
            xaxis_tickangle=-15
        )
        st.plotly_chart(fig_coop, use_container_width=True)

    with col2:
        st.markdown("### PSC Usage Trend (Chinook)")

        # Aggregate weekly Chinook PSC
        weekly_chinook = weekly_df.groupby('week_ending')['chinook_psc'].sum().reset_index()
        weekly_chinook['cumulative'] = weekly_chinook['chinook_psc'].cumsum()

        fig_psc = go.Figure()
        fig_psc.add_trace(go.Scatter(
            x=weekly_chinook['week_ending'],
            y=weekly_chinook['cumulative'],
            mode='lines+markers',
            name='Cumulative Chinook',
            line=dict(color='#0E7490', width=3),
            fill='tozeroy',
            fillcolor='rgba(14, 116, 144, 0.1)'
        ))

        # Add cap line
        fig_psc.add_hline(
            y=1200,
            line_dash="dash",
            line_color="red",
            annotation_text="Cap: 1,200",
            annotation_position="right"
        )

        fig_psc.update_layout(
            xaxis_title="",
            yaxis_title="Cumulative Chinook PSC",
            showlegend=False,
            height=300,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_psc, use_container_width=True)

# ============================================================================
# TRANSFERS PAGE
# ============================================================================
elif page == "🔄 Transfers":
    st.markdown('<div class="main-header">Quota Transfer Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Record and track quota transfers between vessels</div>', unsafe_allow_html=True)

    # Transfer Entry Form
    st.markdown("### Enter New Transfer")

    vessels_df = data['vessels']

    col1, col2 = st.columns(2)

    with col1:
        from_vessel = st.selectbox(
            "From Vessel",
            options=vessels_df['vessel_name'].tolist(),
            key="from_vessel"
        )

    with col2:
        to_vessel = st.selectbox(
            "To Vessel",
            options=[v for v in vessels_df['vessel_name'].tolist() if v != from_vessel],
            key="to_vessel"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        amount = st.number_input("Amount (mt)", min_value=0.0, max_value=1000.0, value=100.0, step=10.0)

    with col2:
        transfer_date = st.date_input("Transfer Date", value=datetime.now())

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Record Transfer", type="primary", use_container_width=True):
            st.success(f"✅ Transfer recorded: {amount} mt from {from_vessel} to {to_vessel}")

    col1, col2 = st.columns(2)
    with col1:
        notes = st.text_area("Notes (optional)", placeholder="E.g., Pre-season quota optimization")

    st.markdown("---")

    # Transfer History
    st.markdown("### Transfer History")

    transfers_df = data['transfers']

    # Display transfers
    display_transfers = transfers_df[['transfer_date', 'from_vessel_name', 'to_vessel_name',
                                       'amount_mt', 'notes']].copy()
    display_transfers.columns = ['Date', 'From Vessel', 'To Vessel', 'Amount (mt)', 'Notes']
    display_transfers['Date'] = pd.to_datetime(display_transfers['Date']).dt.strftime('%Y-%m-%d')

    st.dataframe(display_transfers, use_container_width=True, height=400)

    # Summary
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Transfers", len(transfers_df))
    with col2:
        total_transferred = transfers_df['amount_mt'].sum()
        st.metric("Total Volume Transferred", f"{total_transferred:,.0f} mt")
    with col3:
        inter_coop_transfers = len(transfers_df[
            transfers_df['from_cooperative'] != transfers_df['to_cooperative']
        ])
        st.metric("Inter-Cooperative Transfers", inter_coop_transfers)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("*Demo Platform for Fisherman First LLC*")
st.sidebar.markdown("*CGOA Rockfish Program Manager Proposal*")
