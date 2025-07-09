import csv
from datetime import datetime

def log_event(event_type, sat_name, message):
    with open('C:/Users/thusa.THUSA/Downloads/New folder (3)/log.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.utcnow(), sat_name, event_type, message])
