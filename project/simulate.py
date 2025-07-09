from skyfield.api import load, EarthSatellite
from routing import build_satellite_network
from collision_check import check_collision
from comms import send_message, receive_alerts, handle_sending
from logger import log_event
import threading
import time
import datetime

# Load timescale
ts = load.timescale()

# Load TLEs
with open("C:/Users/thusa.THUSA/Downloads/New folder (3)/tle_data.txt") as f:
    lines = f.read().splitlines()

satellites = {}
for i in range(0, len(lines), 3):
    name = lines[i].strip()
    tle1 = lines[i + 1].strip()
    tle2 = lines[i + 2].strip()
    sat = EarthSatellite(tle1, tle2, name, ts)
    satellites[name] = sat

sat_ports = {}
base_port = 5000
for i, name in enumerate(satellites.keys()):
    sat_ports[name] = base_port + i

# Start comms
for name, port in sat_ports.items():
    threading.Thread(target=receive_alerts, args=(port,), daemon=True).start()

threading.Thread(target=handle_sending, daemon=True).start()

print("🛰️ Satellite Simulation (Pause One, Resume Both When Safe) Started")

paused = {}  # e.g., { "SAT-A": paused_until_time }
frozen_positions = {}
active_alerts = set()  # (SAT-A, SAT-B)

threshold_km = 10

while True:
    now = datetime.datetime.utcnow()
    t = ts.now()
    names = list(satellites.keys())

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name1 = names[i]
            name2 = names[j]
            sat1 = satellites[name1]
            sat2 = satellites[name2]
            pair_key = tuple(sorted([name1, name2]))

            # Determine paused states
            is_paused1 = name1 in paused and now < paused[name1]
            is_paused2 = name2 in paused and now < paused[name2]

            # Get positions with frozen logic
            if is_paused1:
                pos1 = frozen_positions.get(name1)
                log_event("Paused", name1, f"Holding position")
            else:
                pos1 = sat1.at(t).position.km
                frozen_positions[name1] = pos1

            if is_paused2:
                pos2 = frozen_positions.get(name2)
                log_event("Paused", name2, f"Holding position")
            else:
                pos2 = sat2.at(t).position.km
                frozen_positions[name2] = pos2

            if pos1 is None or pos2 is None:
                continue

            # Collision check
            risk, distance = check_collision(pos1, pos2, threshold_km)

            if risk:
                if pair_key not in active_alerts:
                    msg = f"⚠️ COLLISION RISK! {name1} ↔ {name2} | Distance = {distance:.2f} km"
                    send_message(1, msg, "127.0.0.1", sat_ports[name2])
                    log_event("Alert", name1, msg)

                    # 🔧 Pause only one satellite (the one with the "lower" name)
                    pause_sat = min(name1, name2)
                    paused[pause_sat] = now + datetime.timedelta(seconds=20)
                    log_event("Action", pause_sat, "Paused due to collision risk")

                    active_alerts.add(pair_key)

            else:
                if pair_key in active_alerts:
                    # If they were previously paused due to collision and now safe
                    log_event("Resume", name1, f"Safe distance with {name2} = {distance:.2f} km")
                    log_event("Resume", name2, f"Safe distance with {name1} = {distance:.2f} km")
                    active_alerts.remove(pair_key)

                    # Remove pause if still active
                    for name in [name1, name2]:
                        if name in paused:
                            del paused[name]

                # Send telemetry
                telemetry1 = f"Telemetry {name1}: {pos1.round(2)}"
                telemetry2 = f"Telemetry {name2}: {pos2.round(2)}"
                send_message(2, telemetry1, "127.0.0.1", sat_ports[name2])
                send_message(2, telemetry2, "127.0.0.1", sat_ports[name1])
                log_event("Telemetry", name1, telemetry1)
                log_event("Telemetry", name2, telemetry2)

    time.sleep(5)
