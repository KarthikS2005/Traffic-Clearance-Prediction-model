import os
import sys

# Ensure the root directory is in the system path so internal package imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from traffic.Database import SQL
from traffic.crud import create, read, update, delete
from traffic.Conversion import csv_to_db, db_to_csv


def main():
    # Automatically check and build tables on application start
    SQL.create_tables()

    while True:
        print("\n=====================================")
        print("    TRAFFIC SYSTEM MANAGEMENT MENU    ")
        print("=====================================")
        print("1. Log New Location (Manual Entry)")
        print("2. Log New Incident (Manual Entry)")
        print("3. Bulk Import Datasets (CSV -> Database)")
        print("4. Export ML Ready Features (Database -> CSV)")
        print("5. Mark Active Incident as Cleared")
        print("6. Exit")
        print("=====================================")

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            print("\n--- Add Location ---")
            road = input("Road Name: ")
            rtype = input("Road Type (Highway/Urban/Residential): ")
            try:
                lat = float(input("Latitude: "))
                lon = float(input("Longitude: "))
                loc_id = create.insert_location(road, rtype, lat, lon)
                print(f"Success! Location ID assigned: {loc_id}")
            except ValueError:
                print("Error: Latitude and Longitude must be numeric values.")

        elif choice == "2":
            print("\n--- Log Incident ---")
            itype = input("Type (Accident/Construction/Hazard/Stall): ")
            sev = input("Severity (Low/Medium/High): ")
            try:
                vehicles = int(input("Vehicles Involved: "))
                block = input("Lane Blockage (None/Partial/Full): ")
                time_rep = input("Timestamp (YYYY-MM-DD HH:MM:SS): ")
                resp = int(input("Response Time (mins): "))
                weather = input("Weather Condition: ")
                loc_id = int(input("Location ID: "))

                inc_id = create.log_incident(itype, sev, vehicles, block, time_rep, resp, weather, loc_id)
                print(f"Success! Incident logged under ID: {inc_id}")
            except ValueError:
                print("Error: Count, time, and IDs must be integers.")

        elif choice == "3":
            print("\n--- Bulk Import Pipeline ---")
            print("Place your source CSV data files inside your project folder.")
            loc_csv = input("Enter path to Locations CSV (or press Enter to skip): ").strip()
            if loc_csv:
                try:
                    csv_to_db.load_locations_csv(loc_csv)
                except Exception as e:
                    print(f"Import failed: {e}")

            inc_csv = input("Enter path to Incidents CSV (or press Enter to skip): ").strip()
            if inc_csv:
                try:
                    csv_to_db.load_incidents_csv(inc_csv)
                except Exception as e:
                    print(f"Import failed: {e}")

        elif choice == "4":
            print("\n--- ML Feature Export Pipeline ---")
            clearance_out = input("Filename for Clearance Model data (e.g., clearance_train.csv): ").strip()
            if clearance_out:
                db_to_csv.export_clearance_ml_dataset(clearance_out)

            congestion_out = input("Filename for Congestion Model data (e.g., congestion_train.csv): ").strip()
            if congestion_out:
                db_to_csv.export_congestion_ml_dataset(congestion_out)

        elif choice == "5":
            print("\n--- Resolve Active Incident ---")
            try:
                inc_id = int(input("Enter Incident ID to clear: "))
                c_time = int(input("Enter target clearance duration (in minutes): "))
                if update.clear_incident(inc_id, c_time):
                    print("Incident resolved. Target attribute logged for ML training.")
                else:
                    print("Incident ID matching that record could not be found.")
            except ValueError:
                print("Error: IDs and durations must be numeric.")

        elif choice == "6":
            print("\nSystem shutting down.")
            break
        else:
            print("\nInvalid choice. Please select an option between 1 and 6.")


if __name__ == "__main__":
    # Create tables first
     print("Starting data ingestion stream...")
        
     main()
