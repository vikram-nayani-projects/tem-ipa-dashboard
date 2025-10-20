"""
Test data for TEM IPA Manager Dashboard Demo
8 realistic vessels with different compliance scenarios
"""

import pandas as pd
from datetime import datetime, timedelta

# 8 test vessels with realistic Alaska fishing vessel names
VESSELS = [
    {'vessel_id': 'AK-7721', 'vessel_name': 'Pacific Hunter', 'active': True},
    {'vessel_id': 'AK-8832', 'vessel_name': 'Northern Star', 'active': True},
    {'vessel_id': 'AK-6543', 'vessel_name': 'Sea Wolf', 'active': True},
    {'vessel_id': 'AK-9214', 'vessel_name': 'Arctic King', 'active': True},
    {'vessel_id': 'AK-5678', 'vessel_name': 'Ocean Voyager', 'active': True},
    {'vessel_id': 'AK-4421', 'vessel_name': 'Blue Horizon', 'active': True},
    {'vessel_id': 'AK-7893', 'vessel_name': 'Silver Fin', 'active': True},
    {'vessel_id': 'AK-3156', 'vessel_name': 'Golden Catch', 'active': True},
]


def generate_test_trips():
    """
    Generate realistic trip data for 8 vessels with different scenarios:

    1. Pacific Hunter - Compliant (safe, green)
    2. Northern Star - Warning (trending high, yellow) ⭐ HERO SCENARIO
    3. Sea Wolf - Trip Limit Violation (over 300k avg, red)
    4. Arctic King - Egregious Violation (single trip >335k)
    5. Ocean Voyager - Roller Coaster (was violation, now compliant)
    6. Blue Horizon - New Vessel (only 2 trips, incomplete data)
    7. Silver Fin - MRA Compliant
    8. Golden Catch - MRA Violation (but trip limit OK)
    """

    trips = []
    trip_counter = 1
    start_date = datetime(2026, 1, 20)  # Real 2026 A Season start

    # Vessel 1: Pacific Hunter - The Perfect Operator (Compliant)
    vessel = VESSELS[0]
    trip_dates = [start_date + timedelta(days=i*3) for i in range(10)]
    catches = [240000, 255000, 248000, 252000, 245000, 258000, 250000, 246000, 253000, 249000]

    for date, pollock in zip(trip_dates, catches):
        pcod = int(pollock * 0.15)  # 15% Pacific Cod (under 20% limit)
        other = int(pollock * 0.01)  # 1% other (under 2% limit)
        trips.append({
            'trip_id': f'T{trip_counter:03d}',
            'vessel_id': vessel['vessel_id'],
            'vessel_name': vessel['vessel_name'],
            'delivery_date': date,
            'pollock_lbs': pollock,
            'pcod_lbs': pcod,
            'other_lbs': other,
            'season': 'A',
            'fishing_year': 2026
        })
        trip_counter += 1

    # Vessel 2: Northern Star - The Creeper (Warning - trending high) ⭐
    vessel = VESSELS[1]
    trip_dates = [start_date + timedelta(days=i*3) for i in range(10)]
    catches = [260000, 270000, 275000, 280000, 285000, 288000, 290000, 292000, 295000, 293000]

    for date, pollock in zip(trip_dates, catches):
        pcod = int(pollock * 0.14)
        other = int(pollock * 0.01)
        trips.append({
            'trip_id': f'T{trip_counter:03d}',
            'vessel_id': vessel['vessel_id'],
            'vessel_name': vessel['vessel_name'],
            'delivery_date': date,
            'pollock_lbs': pollock,
            'pcod_lbs': pcod,
            'other_lbs': other,
            'season': 'A',
            'fishing_year': 2026
        })
        trip_counter += 1

    # Vessel 3: Sea Wolf - The Violator (Over 300k avg)
    vessel = VESSELS[2]
    trip_dates = [start_date + timedelta(days=i*3) for i in range(10)]
    catches = [295000, 305000, 310000, 298000, 308000, 315000, 312000, 305000, 318000, 310000]

    for date, pollock in zip(trip_dates, catches):
        pcod = int(pollock * 0.16)
        other = int(pollock * 0.015)
        trips.append({
            'trip_id': f'T{trip_counter:03d}',
            'vessel_id': vessel['vessel_id'],
            'vessel_name': vessel['vessel_name'],
            'delivery_date': date,
            'pollock_lbs': pollock,
            'pcod_lbs': pcod,
            'other_lbs': other,
            'season': 'A',
            'fishing_year': 2026
        })
        trip_counter += 1

    # Vessel 4: Arctic King - The Egregious Offender (Single trip >335k)
    vessel = VESSELS[3]
    trip_dates = [start_date + timedelta(days=i*3) for i in range(10)]
    catches = [270000, 280000, 275000, 268000, 340000, 265000, 270000, 272000, 268000, 275000]

    for date, pollock in zip(trip_dates, catches):
        pcod = int(pollock * 0.13)
        other = int(pollock * 0.01)
        trips.append({
            'trip_id': f'T{trip_counter:03d}',
            'vessel_id': vessel['vessel_id'],
            'vessel_name': vessel['vessel_name'],
            'delivery_date': date,
            'pollock_lbs': pollock,
            'pcod_lbs': pcod,
            'other_lbs': other,
            'season': 'A',
            'fishing_year': 2026
        })
        trip_counter += 1

    # Vessel 5: Ocean Voyager - The Roller Coaster (Was violation, now compliant)
    vessel = VESSELS[4]
    trip_dates = [start_date + timedelta(days=i*3) for i in range(10)]
    catches = [310000, 295000, 305000, 285000, 315000, 270000, 265000, 275000, 260000, 268000]

    for date, pollock in zip(trip_dates, catches):
        pcod = int(pollock * 0.12)
        other = int(pollock * 0.01)
        trips.append({
            'trip_id': f'T{trip_counter:03d}',
            'vessel_id': vessel['vessel_id'],
            'vessel_name': vessel['vessel_name'],
            'delivery_date': date,
            'pollock_lbs': pollock,
            'pcod_lbs': pcod,
            'other_lbs': other,
            'season': 'A',
            'fishing_year': 2026
        })
        trip_counter += 1

    # Vessel 6: Blue Horizon - The New Arrival (Only 2 trips)
    vessel = VESSELS[5]
    trip_dates = [start_date + timedelta(days=i*4) for i in range(2)]
    catches = [280000, 290000]

    for date, pollock in zip(trip_dates, catches):
        pcod = int(pollock * 0.14)
        other = int(pollock * 0.01)
        trips.append({
            'trip_id': f'T{trip_counter:03d}',
            'vessel_id': vessel['vessel_id'],
            'vessel_name': vessel['vessel_name'],
            'delivery_date': date,
            'pollock_lbs': pollock,
            'pcod_lbs': pcod,
            'other_lbs': other,
            'season': 'A',
            'fishing_year': 2026
        })
        trip_counter += 1

    # Vessel 7: Silver Fin - MRA Compliant (Good species mix)
    vessel = VESSELS[6]
    trip_dates = [start_date + timedelta(days=i*3) for i in range(8)]
    catches = [265000, 270000, 268000, 272000, 275000, 269000, 271000, 267000]

    for date, pollock in zip(trip_dates, catches):
        pcod = int(pollock * 0.16)  # 16% Pacific Cod (under 20%)
        other = int(pollock * 0.012)  # 1.2% other (under 2%)
        trips.append({
            'trip_id': f'T{trip_counter:03d}',
            'vessel_id': vessel['vessel_id'],
            'vessel_name': vessel['vessel_name'],
            'delivery_date': date,
            'pollock_lbs': pollock,
            'pcod_lbs': pcod,
            'other_lbs': other,
            'season': 'A',
            'fishing_year': 2026
        })
        trip_counter += 1

    # Vessel 8: Golden Catch - MRA Violation (Too much Pacific Cod, but trip limit OK)
    vessel = VESSELS[7]
    trip_dates = [start_date + timedelta(days=i*3) for i in range(8)]
    catches = [270000, 275000, 268000, 272000, 280000, 271000, 269000, 273000]

    for date, pollock in zip(trip_dates, catches):
        pcod = int(pollock * 0.24)  # 24% Pacific Cod (OVER 20% limit!)
        other = int(pollock * 0.01)  # 1% other (under 2%)
        trips.append({
            'trip_id': f'T{trip_counter:03d}',
            'vessel_id': vessel['vessel_id'],
            'vessel_name': vessel['vessel_name'],
            'delivery_date': date,
            'pollock_lbs': pollock,
            'pcod_lbs': pcod,
            'other_lbs': other,
            'season': 'A',
            'fishing_year': 2026
        })
        trip_counter += 1

    return pd.DataFrame(trips)


# Pre-generate all test data
TRIPS_DF = generate_test_trips()


def get_vessel_trips(vessel_id):
    """Get all trips for a vessel, sorted by date"""
    return TRIPS_DF[TRIPS_DF['vessel_id'] == vessel_id].sort_values('delivery_date').copy()


def calculate_trip_limit_status(vessel_id):
    """
    Calculate 4-trip rolling average and compliance status

    Returns:
        dict with keys: status, color, avg, trips, all_trips, trips_needed
    """
    trips = get_vessel_trips(vessel_id)

    if len(trips) < 4:
        return {
            'status': 'INSUFFICIENT_DATA',
            'color': 'gray',
            'trips_needed': 4 - len(trips),
            'avg': None,
            'trips': trips.to_dict('records'),
            'all_trips': trips.to_dict('records')
        }

    # Last 4 trips (rolling window)
    last_4 = trips.tail(4)
    avg = last_4['pollock_lbs'].mean()

    # Determine status
    if avg > 300000:
        status = 'VIOLATION'
        color = 'red'
    elif avg > 285000:  # Within 15k of limit (5% buffer)
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


def calculate_next_trip_projection(vessel_id, next_trip_amounts=None):
    """
    Calculate what the new average would be for different next trip amounts

    Args:
        vessel_id: Vessel to calculate for
        next_trip_amounts: List of amounts to test (default: [250k, 280k, 300k, 320k])

    Returns:
        List of dicts with: amount, new_avg, status, color
    """
    if next_trip_amounts is None:
        next_trip_amounts = [250000, 280000, 300000, 320000]

    trips = get_vessel_trips(vessel_id)

    if len(trips) < 3:
        return []  # Need at least 3 trips to project

    # Get last 3 trips (next trip will make 4th)
    if len(trips) >= 4:
        last_3 = trips.tail(3)
    else:
        last_3 = trips

    projections = []
    for amount in next_trip_amounts:
        # Calculate new average with this hypothetical trip
        total = last_3['pollock_lbs'].sum() + amount
        new_avg = total / 4

        # Determine status
        if new_avg > 300000:
            status = 'VIOLATION'
            color = 'red'
        elif new_avg > 285000:
            status = 'WARNING'
            color = 'orange'
        else:
            status = 'COMPLIANT'
            color = 'green'

        projections.append({
            'amount': amount,
            'new_avg': new_avg,
            'status': status,
            'color': color
        })

    return projections


def check_egregious_violations():
    """Find all trips > 335k lbs (egregious threshold)"""
    return TRIPS_DF[TRIPS_DF['pollock_lbs'] > 335000].copy()


def calculate_mra_compliance(trip_id):
    """
    Check MRA (Maximum Retainable Amounts) compliance for a trip
    Based on CFR Table 10 percentages

    Returns:
        dict with: compliant (bool), violations (list)
    """
    trip = TRIPS_DF[TRIPS_DF['trip_id'] == trip_id].iloc[0]

    total_catch = trip['pollock_lbs'] + trip['pcod_lbs'] + trip['other_lbs']
    pcod_pct = (trip['pcod_lbs'] / total_catch) * 100
    other_pct = (trip['other_lbs'] / total_catch) * 100

    violations = []

    # CFR Table 10 limits
    if pcod_pct > 20:
        violations.append({
            'species': 'Pacific Cod',
            'actual_pct': pcod_pct,
            'limit_pct': 20,
            'overage_pct': pcod_pct - 20,
            'actual_lbs': trip['pcod_lbs'],
            'allowed_lbs': int(total_catch * 0.20)
        })

    if other_pct > 2:
        violations.append({
            'species': 'Other Species',
            'actual_pct': other_pct,
            'limit_pct': 2,
            'overage_pct': other_pct - 2,
            'actual_lbs': trip['other_lbs'],
            'allowed_lbs': int(total_catch * 0.02)
        })

    return {
        'compliant': len(violations) == 0,
        'violations': violations,
        'pcod_pct': pcod_pct,
        'other_pct': other_pct
    }


def get_all_mra_violations():
    """Get all trips with MRA violations"""
    mra_violations = []

    for _, trip in TRIPS_DF.iterrows():
        compliance = calculate_mra_compliance(trip['trip_id'])
        if not compliance['compliant']:
            for violation in compliance['violations']:
                mra_violations.append({
                    'trip_id': trip['trip_id'],
                    'vessel_name': trip['vessel_name'],
                    'delivery_date': trip['delivery_date'],
                    'species': violation['species'],
                    'actual_pct': violation['actual_pct'],
                    'limit_pct': violation['limit_pct'],
                    'overage_lbs': violation['actual_lbs'] - violation['allowed_lbs']
                })

    return pd.DataFrame(mra_violations) if mra_violations else pd.DataFrame()


# Summary statistics
def get_summary_stats():
    """Get overall fleet statistics"""
    total_vessels = len(VESSELS)
    total_trips = len(TRIPS_DF)

    # Count by status
    compliant = 0
    warning = 0
    violation = 0
    insufficient = 0

    for vessel in VESSELS:
        status = calculate_trip_limit_status(vessel['vessel_id'])
        if status['status'] == 'COMPLIANT':
            compliant += 1
        elif status['status'] == 'WARNING':
            warning += 1
        elif status['status'] == 'VIOLATION':
            violation += 1
        else:
            insufficient += 1

    egregious = len(check_egregious_violations())
    mra_violations = len(get_all_mra_violations())

    return {
        'total_vessels': total_vessels,
        'total_trips': total_trips,
        'compliant': compliant,
        'warning': warning,
        'violation': violation,
        'insufficient_data': insufficient,
        'egregious_violations': egregious,
        'mra_violations': mra_violations
    }
