import csv
from traffic.Database.SQL import get_connection


def load_locations_csv(csv_path):
    """Loads static location assets from a CSV file into the locations table."""
    conn = get_connection()
    cursor = conn.cursor()

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                           INSERT
                           OR IGNORE INTO locations (road_name, road_type, latitude, longitude)
                VALUES (?, ?, ?, ?);
                           """, (row['road_name'], row['road_type'], float(row['latitude']), float(row['longitude'])))

    conn.commit()
    conn.close()
    print(f"Successfully loaded locations from {csv_path}")


def load_incidents_csv(csv_path):
    """Loads historical crash and road incident records from a CSV file."""
    conn = get_connection()
    cursor = conn.cursor()

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                           INSERT INTO incidents (incident_type, severity_level, vehicles_involved,
                                                  lane_blockage, timestamp_reported, response_time_mins,
                                                  weather_condition, location_id, clearance_time_mins)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                           """, (row['incident_type'], row['severity_level'], int(row['vehicles_involved']),
                                 row['lane_blockage'], row['timestamp_reported'], int(row['response_time_mins']),
                                 row['weather_condition'], int(row['location_id']), int(row['clearance_time_mins'])))

    conn.commit()
    conn.close()
    print(f"Successfully loaded incidents from {csv_path}")