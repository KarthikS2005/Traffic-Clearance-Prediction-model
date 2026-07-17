from traffic.Database.SQL import get_connection

def get_all_locations():
    """Retrieves all registered road segments."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM locations;")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_active_incidents():
    """Retrieves incidents that have not yet been cleared (target is NULL)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents WHERE clearance_time_mins IS NULL;")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_clearance_training_data():
    """Fetches joined incident and location attributes for the Clearance Time Model."""
    conn = get_connection()
    cursor = conn.cursor()
    # Explicitly omitting timestamp_cleared to prevent data leakage as discussed
    cursor.execute("""
        SELECT i.incident_type, i.severity_level, i.vehicles_involved, i.lane_blockage, 
               i.timestamp_reported, i.response_time_mins, i.weather_condition,
               l.road_type, l.latitude, l.longitude, i.clearance_time_mins
        FROM incidents i
        JOIN locations l ON i.location_id = l.location_id
        WHERE i.clearance_time_mins IS NOT NULL;
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_congestion_training_data():
    """Fetches joined history data for the Traffic Congestion Level Model."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT th.timestamp, th.public_event_type, th.expected_event_attendance, 
               th.active_incident_flag, l.road_type, l.latitude, l.longitude, th.congestion_level
        FROM traffic_history th
        JOIN locations l ON th.location_id = l.location_id;
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows