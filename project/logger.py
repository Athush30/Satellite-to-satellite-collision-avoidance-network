import csv
from datetime import datetime, UTC

def log_event(event_type, sat_name, message):
    """
    Log an event to a CSV file.
    Args:
        event_type: Type of event (e.g., Alert, Action, Telemetry)
        sat_name: Name of the satellite
        message: Event description
    """
    try:
        with open('C:/Users/thusa.THUSA/Downloads/New folder (3)/log.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now(UTC), sat_name, event_type, message])
    except UnicodeEncodeError as e:
        print(f"Error writing to log.csv: {e}")
