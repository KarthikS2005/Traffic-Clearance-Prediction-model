import csv
from traffic.Database.SQL import get_connection


def export_clearance_ml_dataset(output_path):
    """Generates the clean dataset CSV for training the Clearance Time Prediction Model."""
    conn = get_connection()
    cursor = conn.cursor()

    # Executes the joined query, stripping out variables that cause data leakage
    cursor.execute("""
                   SELECT i.incident_type,
                          i.severity_level,
                          i.vehicles_involved,
                          i.lane_blockage,
                          i.timestamp_reported,
                          i.response_time_mins,
                          i.weather_condition,
                          l.road_type,
                          l.latitude,
                          l.longitude,
                          i.clearance_time_mins
                   FROM incidents i
                            JOIN locations l ON i.location_id = l.location_id
                   WHERE i.clearance_time_mins IS NOT NULL;
                   """)

    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    conn.close()
    print(f"ML clearance training dataset exported to: {output_path}")


def export_congestion_ml_dataset(output_path):
    """Generates the clean dataset CSV for training the Congestion Level Model."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT th.timestamp,
                          th.public_event_type,
                          th.expected_event_attendance,
                          th.active_incident_flag,
                          l.road_type,
                          l.latitude,
                          l.longitude,
                          th.congestion_level
                   FROM traffic_history th
                            JOIN locations l ON th.location_id = l.location_id;
                   """)

    rows = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    conn.close()
    print(f"ML congestion training dataset exported to: {output_path}")