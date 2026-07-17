from traffic.Database.SQL import get_connection

def delete_incident(incident_id):
    """Deletes a specific incident record by its unique ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM incidents WHERE incident_id = ?;", (incident_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting incident: {e}")
        return False
    finally:
        conn.close()

def delete_location(location_id):
    """Deletes a location (Cascades to linked incidents and logs automatically)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM locations WHERE location_id = ?;", (location_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting location: {e}")
        return False
    finally:
        conn.close()