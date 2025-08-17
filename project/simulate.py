from skyfield.api import load, EarthSatellite
from routing import build_satellite_network
from collision_check import check_collision
from comms import send_message, receive_alerts, handle_sending
from logger import log_event
import threading
import time
import datetime
import numpy as np
from datetime import UTC

# Load timescale
ts = load.timescale()

# Load and validate TLEs
with open("C:/Users/thusa.THUSA/Downloads/New folder (6)/tle_data.txt") as f:
    lines = f.read().splitlines()


def text_to_bits(text):
        return ''.join(format(ord(c), '08b') for c in text)


satellites = {}
original_states = {}  # Store original velocity and orbital elements
maneuver_states = {}  # Track maneuvers: {name: {'start_time': Time, 'dv': np.array, 'duration': float, 'pos_start': np.array, 'vel_start': np.array}}
for i in range(0, len(lines), 3):
    if i + 2 >= len(lines):
        print(f"Warning: Incomplete TLE data at line {i}")
        continue
    name = lines[i].strip()
    tle1 = lines[i + 1].strip()
    tle2 = lines[i + 2].strip()
    try:
        sat = EarthSatellite(tle1, tle2, name, ts)
        satellites[name] = sat
        t = ts.now()
        original_states[name] = {
            'velocity': sat.at(t).velocity.m_per_s,  # Original velocity vector (m/s)
            'mean_motion': sat.model.no,  # Original mean motion (rad/s)
            'tle1': tle1,  # Store TLE lines
            'tle2': tle2
        }
        print(f"Loaded satellite: {name} with TLE: {tle1}, {tle2}")
    except Exception as e:
        print(f"Error loading TLE for {name}: {e}")
        continue

if len(satellites) < 2:
    print(f"Error: Need at least 2 satellites, loaded {len(satellites)}")
    exit(1)

# Validate satellite names against routing
G = build_satellite_network(list(satellites.keys()))
for name in satellites:
    if name not in G.nodes:
        print(f"Warning: Satellite {name} not in network graph")

# Assign unique ports
sat_ports = {}
base_port = 9000  # Use higher ports to avoid reserved ranges
for i, name in enumerate(satellites.keys()):
    sat_ports[name] = base_port + i * 1000  # Wider port spacing
print(f"Assigned ports: {sat_ports}")

# Start comms
for name, port in sat_ports.items():
    print(f"Starting receive thread for {name} on port {port}")
    threading.Thread(target=receive_alerts, args=(port, name), daemon=True).start()

threading.Thread(target=handle_sending, daemon=True).start()

print("Satellite Simulation (Maneuver-Based Collision Avoidance with Velocity Restoration) Started")

active_alerts = set()  # (SAT-A, SAT-B)
threshold_km = 1000  # Reverted to realistic threshold
maneuver_duration = 20  # Seconds for maneuver effect
names = list(satellites.keys())
while True:
    t = ts.now()
    current_pos = {}
    current_vel = {}
    for name in satellites.keys():
        if name in maneuver_states:
            maneuver = maneuver_states[name]
            time_since_start = (t - maneuver['start_time'])
            if time_since_start < maneuver['duration']:
                # Kinematic approximation during maneuver
                pos = maneuver['pos_start'] + (maneuver['vel_start'] + maneuver['dv'] / 1000) * time_since_start
                vel = maneuver['vel_start'] + maneuver['dv'] / 1000
            else:
                # End of maneuver, revert to original TLE
                pos = satellites[name].at(t).position.km
                vel = satellites[name].at(t).velocity.km_per_s
                log_event("Action", name, f"Ended maneuver, restored to original orbit")
                del maneuver_states[name]
        else:
            pos = satellites[name].at(t).position.km
            vel = satellites[name].at(t).velocity.km_per_s
        current_pos[name] = pos
        current_vel[name] = vel

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name1 = names[i]
            name2 = names[j]
            pos1 = current_pos[name1]
            pos2 = current_pos[name2]
            pair_key = tuple(sorted([name1, name2]))

            # Collision check
            risk, distance = check_collision(pos1, pos2, name1, name2, threshold_km)

            if risk:
                if pair_key not in active_alerts:
                    msg = f"WARNING: COLLISION RISK! {name1} <-> {name2} | Distance = {distance:.2f} km"
                    send_message(1, msg, "127.0.0.1", sat_ports[name2])
                    log_event("Alert", name1, msg)

                    alert_bits = text_to_bits(msg)
                    print(msg)
                    print(alert_bits)
                    with open('C:/Users/thusa.THUSA/Downloads/New folder (6)/alert_bits.txt', 'w') as f:
                        f.write(alert_bits)
                    print('WRITTEN ON ALERT_BITTS.....................................................')

                    # Apply maneuver to one satellite (lower name)
                    maneuver_sat = min(name1, name2)
                    rel_pos = pos2 - pos1 if maneuver_sat == name1 else pos1 - pos2
                    dv_direction = rel_pos / np.linalg.norm(rel_pos)
                    dv = 0.01 * dv_direction  # 1 cm/s in m/s
                    t_start = t
                    pos_start = satellites[maneuver_sat].at(t_start).position.km
                    vel_start = satellites[maneuver_sat].at(t_start).velocity.km_per_s
                    maneuver_states[maneuver_sat] = {
                        'start_time': t_start,
                        'dv': dv,
                        'duration': maneuver_duration,
                        'pos_start': pos_start,
                        'vel_start': vel_start
                    }
                    log_event("Action", maneuver_sat, f"Applied Δv: {dv.round(3)} m/s")

                    active_alerts.add(pair_key)

            else:
                if pair_key in active_alerts:
                    # Check if safe to restore orbit
                    alert_bits = text_to_bits("Safe")
                    with open('C:/Users/thusa.THUSA/Downloads/New folder (6)/alert_bits.txt', 'w') as f:
                        f.write(alert_bits)
                    print('WRITTEN ON ALERT_BITTS.....................................................')
                    log_event("Safe", name1, f"Safe distance with {name2} = {distance:.2f} km")
                    log_event("Safe", name2, f"Safe distance with {name1} = {distance:.2f} km")
                    active_alerts.remove(pair_key)

    # Send telemetry for all pairs
    
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name1 = names[i]
            name2 = names[j]
            telemetry1 = f"Telemetry {name1}: {current_pos[name1].round(2)}"
            telemetry2 = f"Telemetry {name2}: {current_pos[name2].round(2)}"
            send_message(2, telemetry1, "127.0.0.1", sat_ports[name2])
            send_message(2, telemetry2, "127.0.0.1", sat_ports[name1])
            log_event("Telemetry", name1, telemetry1)
            log_event("Telemetry", name2, telemetry2)

    time.sleep(5)
