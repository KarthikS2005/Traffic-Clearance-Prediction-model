import sqlite3
import os

# Define database file path relative to this file's directory
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "traffic.db")

# ==========================================
# PART 1: CONNECTION CODE
# ==========================================
def get_connection():
    """Establishes and returns a database connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ==========================================
# PART 2: SQL QUERY CODE
# ==========================================
def create_tables():
    """Executes SQL queries to initialize the 3 schema tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Query 1: Table 2 - Locations (Static Catalog)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        road_name TEXT NOT NULL,
        road_type TEXT CHECK(road_type IN ('Highway', 'Urban', 'Residential')) NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL
    );
    """)

    # Query 2: Table 1 - Incidents (Dynamic Event Log)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_type TEXT CHECK(incident_type IN ('Accident', 'Construction', 'Hazard', 'Stall')) NOT NULL,
        severity_level TEXT CHECK(severity_level IN ('Low', 'Medium', 'High')) NOT NULL,
        vehicles_involved INTEGER DEFAULT 0,
        lane_blockage TEXT CHECK(lane_blockage IN ('None', 'Partial', 'Full')) NOT NULL,
        timestamp_reported TEXT NOT NULL,          
        response_time_mins INTEGER,
        weather_condition TEXT NOT NULL,            
        location_id INTEGER,
        clearance_time_mins INTEGER,               
        FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
    );
    """)

    # Query 3: Table 3 - Traffic History & Events (Core Congestion Log)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic_history (
        traffic_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,
        timestamp TEXT NOT NULL,                   
        public_event_type TEXT DEFAULT 'None',     
        expected_event_attendance INTEGER DEFAULT 0,
        active_incident_flag INTEGER CHECK(active_incident_flag IN (0, 1)) DEFAULT 0,
        congestion_level INTEGER CHECK(congestion_level BETWEEN 0 AND 5), 
        FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at: {DB_PATH}")

if __name__ == "__main__":
    create_tables()