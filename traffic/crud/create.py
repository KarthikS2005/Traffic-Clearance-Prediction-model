from traffic.Database.SQL import get_connection

def insert_location(road_name, road_type, latitude, longitude):
    """Inserts a new static road catalog location."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO locations (road_name, road_type, latitude, longitude)
            VALUES (?, ?, ?, ?);
        """, (road_name, road_type, latitude, longitude))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error inserting location: {e}")
        return None
    finally:
        conn.close()

def log_incident(incident_type, severity_level, vehicles_involved, lane_blockage,
                 timestamp_reported, response_time_mins, weather_condition, location_id):
    """Logs a new active traffic incident (clearance_time remains NULL until cleared)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO incidents (
                incident_type, severity_level, vehicles_involved, lane_blockage, 
                timestamp_reported, response_time_mins, weather_condition, location_id, clearance_time_mins
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL);
        """, (incident_type, severity_level, vehicles_involved, lane_blockage,
              timestamp_reported, response_time_mins, weather_condition, location_id))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error logging incident: {e}")
        return None
    finally:
        conn.close()

def log_traffic_history(location_id, timestamp, public_event_type='None',
                        expected_event_attendance=0, active_incident_flag=0, congestion_level=0):
    """Logs a metric snapshot for traffic volume and public events."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO traffic_history (
                location_id, timestamp, public_event_type, expected_event_attendance, 
                active_incident_flag, congestion_level
            ) VALUES (?, ?, ?, ?, ?, ?);
        """, (location_id, timestamp, public_event_type, expected_event_attendance,
              active_incident_flag, congestion_level))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error logging traffic history: {e}")
        return None
    finally:
        conn.close()


