from traffic.Database.SQL import get_connection

def clear_incident(incident_id, clearance_time_mins):
    """Updates an incident record with its final clearance duration target value."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE incidents 
            SET clearance_time_mins = ? 
            WHERE incident_id = ?;
        """, (clearance_time_mins, incident_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating incident status: {e}")
        return False
    finally:
        conn.close()

def update_congestion_level(traffic_log_id, new_congestion_level):
    """Updates the congestion level scoring for a historical record snapshot."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE traffic_history 
            SET congestion_level = ? 
            WHERE traffic_log_id = ?;
        """, (new_congestion_level, traffic_log_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating congestion level: {e}")
        return False
    finally:
        conn.close()