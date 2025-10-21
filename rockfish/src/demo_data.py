"""
Demo data generator for CGOA Rockfish Program Analytics Dashboard
Based on real program structure from RFP
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducible demo data
np.random.seed(42)

# Real cooperative names from RFP
COOPERATIVES = [
    "North Pacific Rockfish Cooperative",
    "OBSI Rockfish Cooperative",
    "Silver Bay Seafoods Rockfish Cooperative",
    "Star of Kodiak Rockfish Cooperative"
]

# Vessel names (realistic Alaska fishing vessel names)
VESSEL_NAMES = [
    "Pacific Storm", "Kodiak Queen", "Northern Star", "Ocean Harvester", "Sea Wolf",
    "Arctic Prowler", "Golden Tide", "Blue Horizon", "Midnight Sun", "Silver Bay",
    "Thunder Bay", "Ocean Pride", "Alaska Spirit", "Neptune's Bounty", "Sea Hawk",
    "Pacific Challenger", "Bering Star", "Kodiak Explorer", "Ocean Venture", "Sea Lion",
    "North Wind", "Pacific Triumph"
]

def generate_cooperatives():
    """Generate cooperative data"""
    return pd.DataFrame({
        'cooperative_id': [f'COOP-{i+1}' for i in range(4)],
        'cooperative_name': COOPERATIVES,
        'processor': ['Processor A', 'Processor B', 'Processor C', 'Processor D'],
        'total_allocation_mt': [6500, 7200, 5800, 5500],  # Sums to 25,000 mt
        'member_count': [6, 7, 5, 4]  # Sums to 22 vessels
    })

def generate_vessels():
    """Generate vessel data with allocations"""
    vessels = []
    vessel_idx = 0

    # Distribute vessels across cooperatives
    coop_vessel_counts = [6, 7, 5, 4]
    coop_allocations = [6500, 7200, 5800, 5500]

    for coop_idx, (coop_name, vessel_count, total_allocation) in enumerate(
        zip(COOPERATIVES, coop_vessel_counts, coop_allocations)
    ):
        coop_id = f'COOP-{coop_idx+1}'

        # Generate random allocations that sum to cooperative total
        allocations = np.random.dirichlet(np.ones(vessel_count)) * total_allocation

        for v_idx in range(vessel_count):
            allocation = allocations[v_idx]

            # Harvest between 60-105% of allocation (some overages)
            harvest_pct = np.random.uniform(0.60, 1.05)
            harvest = allocation * harvest_pct

            # Chinook PSC - roughly proportional to harvest with some variation
            chinook_rate = np.random.uniform(28, 50)  # Chinook per 1000mt
            chinook_psc = int((harvest / 1000) * chinook_rate)

            # Halibut PSC - roughly proportional to harvest
            halibut_rate = np.random.uniform(15, 35)  # Halibut per 1000mt
            halibut_psc = int((harvest / 1000) * halibut_rate)

            # Determine status
            if harvest > allocation:
                status = "Overage"
            elif harvest > allocation * 0.95:
                status = "Near Overage"
            else:
                status = "In Compliance"

            vessels.append({
                'vessel_id': f'V-{vessel_idx+1:03d}',
                'vessel_name': VESSEL_NAMES[vessel_idx],
                'cooperative_id': coop_id,
                'cooperative_name': coop_name,
                'cq_allocation_mt': round(allocation, 1),
                'harvest_to_date_mt': round(harvest, 1),
                'quota_balance_mt': round(allocation - harvest, 1),
                'chinook_psc_count': chinook_psc,
                'halibut_psc_count': halibut_psc,
                'status': status
            })

            vessel_idx += 1

    return pd.DataFrame(vessels)

def generate_weekly_harvest():
    """Generate weekly harvest data for A season (Apr-Jun) + some B season (Oct-Nov)"""
    vessels_df = generate_vessels()

    # A Season: April 1 - June 30 (13 weeks)
    a_season_start = datetime(2026, 4, 1)
    a_season_weeks = 13

    # B Season: October 15 - November 15 (5 weeks)
    b_season_start = datetime(2026, 10, 15)
    b_season_weeks = 5

    harvest_data = []

    for _, vessel in vessels_df.iterrows():
        total_harvest = vessel['harvest_to_date_mt']
        total_chinook = vessel['chinook_psc_count']
        total_halibut = vessel['halibut_psc_count']

        # Split 80% in A season, 20% in B season
        a_season_harvest = total_harvest * 0.80
        b_season_harvest = total_harvest * 0.20

        # Generate A season weekly harvests (ramp up pattern)
        a_weekly_harvests = generate_seasonal_pattern(a_season_harvest, a_season_weeks, 'ramp_up')
        a_weekly_chinook = generate_seasonal_pattern(total_chinook * 0.80, a_season_weeks, 'ramp_up')
        a_weekly_halibut = generate_seasonal_pattern(total_halibut * 0.80, a_season_weeks, 'ramp_up')

        for week in range(a_season_weeks):
            week_date = a_season_start + timedelta(weeks=week)
            harvest_data.append({
                'vessel_id': vessel['vessel_id'],
                'vessel_name': vessel['vessel_name'],
                'cooperative_name': vessel['cooperative_name'],
                'week_ending': week_date,
                'season': 'A',
                'harvest_mt': round(a_weekly_harvests[week], 1),
                'chinook_psc': int(a_weekly_chinook[week]),
                'halibut_psc': int(a_weekly_halibut[week])
            })

        # Generate B season weekly harvests (declining pattern)
        b_weekly_harvests = generate_seasonal_pattern(b_season_harvest, b_season_weeks, 'decline')
        b_weekly_chinook = generate_seasonal_pattern(total_chinook * 0.20, b_season_weeks, 'decline')
        b_weekly_halibut = generate_seasonal_pattern(total_halibut * 0.20, b_season_weeks, 'decline')

        for week in range(b_season_weeks):
            week_date = b_season_start + timedelta(weeks=week)
            harvest_data.append({
                'vessel_id': vessel['vessel_id'],
                'vessel_name': vessel['vessel_name'],
                'cooperative_name': vessel['cooperative_name'],
                'week_ending': week_date,
                'season': 'B',
                'harvest_mt': round(b_weekly_harvests[week], 1),
                'chinook_psc': int(b_weekly_chinook[week]),
                'halibut_psc': int(b_weekly_halibut[week])
            })

    return pd.DataFrame(harvest_data)

def generate_seasonal_pattern(total, weeks, pattern='ramp_up'):
    """Generate weekly distribution with specific patterns"""
    if pattern == 'ramp_up':
        # Slow start, ramp up, then stabilize
        weights = np.array([0.5, 0.7, 0.9, 1.0, 1.1, 1.2, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.6][:weeks])
    elif pattern == 'decline':
        # Start strong, decline
        weights = np.array([1.3, 1.1, 0.9, 0.7, 0.5][:weeks])
    else:
        weights = np.ones(weeks)

    # Normalize to sum to total
    weights = weights / weights.sum() * total

    # Add some random variation (+/- 15%)
    variation = np.random.uniform(0.85, 1.15, weeks)
    weekly_values = weights * variation

    # Adjust to match total exactly
    weekly_values = weekly_values / weekly_values.sum() * total

    return weekly_values

def generate_transfers():
    """Generate quota transfer history"""
    vessels_df = generate_vessels()

    transfers = []
    transfer_dates = [
        datetime(2026, 3, 15),
        datetime(2026, 4, 5),
        datetime(2026, 4, 12),
        datetime(2026, 4, 20),
        datetime(2026, 5, 3),
        datetime(2026, 5, 15),
        datetime(2026, 5, 28),
        datetime(2026, 6, 10),
        datetime(2026, 10, 18),
        datetime(2026, 10, 25),
    ]

    for i, transfer_date in enumerate(transfer_dates):
        # Random from/to vessels
        from_vessel = vessels_df.sample(1).iloc[0]
        to_vessel = vessels_df[vessels_df['vessel_id'] != from_vessel['vessel_id']].sample(1).iloc[0]

        # Transfer amount (50-300 mt)
        amount = round(np.random.uniform(50, 300), 1)

        transfers.append({
            'transfer_id': f'T-{i+1:03d}',
            'transfer_date': transfer_date,
            'from_vessel_id': from_vessel['vessel_id'],
            'from_vessel_name': from_vessel['vessel_name'],
            'from_cooperative': from_vessel['cooperative_name'],
            'to_vessel_id': to_vessel['vessel_id'],
            'to_vessel_name': to_vessel['vessel_name'],
            'to_cooperative': to_vessel['cooperative_name'],
            'amount_mt': amount,
            'notes': 'Pre-season quota optimization' if transfer_date < datetime(2026, 4, 1) else 'In-season transfer'
        })

    return pd.DataFrame(transfers)

def generate_alerts():
    """Generate active alerts"""
    vessels_df = generate_vessels()

    alerts = []

    # Find vessels with overages
    overage_vessels = vessels_df[vessels_df['status'] == 'Overage']
    for _, vessel in overage_vessels.head(1).iterrows():
        alerts.append({
            'alert_id': 'A-001',
            'alert_type': 'Overage',
            'severity': 'high',
            'vessel_name': vessel['vessel_name'],
            'message': f"{vessel['vessel_name']}: {abs(vessel['quota_balance_mt']):.1f} mt overage (Pacific cod)",
            'badge_color': 'red'
        })

    # Near overage
    near_vessels = vessels_df[vessels_df['status'] == 'Near Overage']
    for _, vessel in near_vessels.head(1).iterrows():
        alerts.append({
            'alert_id': 'A-002',
            'alert_type': 'At Risk',
            'severity': 'medium',
            'vessel_name': vessel['vessel_name'],
            'message': f"{vessel['vessel_name']}: Quota overage risk (Pacific cod)",
            'badge_color': 'orange'
        })

    # Late processor submission
    alerts.append({
        'alert_id': 'A-003',
        'alert_type': 'Pending',
        'severity': 'low',
        'vessel_name': 'Processor X',
        'message': 'Processor X: Late fish ticket submission',
        'badge_color': 'yellow'
    })

    return pd.DataFrame(alerts)

# Generate all data
def load_demo_data():
    """Load all demo data"""
    return {
        'cooperatives': generate_cooperatives(),
        'vessels': generate_vessels(),
        'weekly_harvest': generate_weekly_harvest(),
        'transfers': generate_transfers(),
        'alerts': generate_alerts()
    }

if __name__ == "__main__":
    # Test data generation
    data = load_demo_data()

    print("Cooperatives:")
    print(data['cooperatives'])
    print("\nVessels:")
    print(data['vessels'].head())
    print("\nWeekly Harvest:")
    print(data['weekly_harvest'].head())
    print("\nTransfers:")
    print(data['transfers'].head())
    print("\nAlerts:")
    print(data['alerts'])
