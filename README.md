# 🛰️ SatNet-CAN+: Satellite-to-Satellite Collision Alert Network (Python Simulation)

This project simulates a real-time **collision detection and alert system** for a constellation of satellites using **TLE orbital data**, priority-based inter-satellite communication, and routing over a dynamic network. It's built entirely in Python and designed to support any number of satellites. The updated version includes smart satellite response to collision risks, where one satellite pauses while the other continues moving, resuming when the risk is cleared.

---

## 🚀 Features

- ✅ Real-time orbit prediction using TLE data via Skyfield  
- ✅ Collision detection between all satellite pairs  
- ✅ Smart collision response:  
  - Pauses one satellite (lower name alphabetically) during collision risk  
  - Allows the other satellite to continue moving  
  - Resumes both when distance exceeds threshold  

- ✅ Priority-based UDP communication (alerts > telemetry)  
- ✅ Satellite-to-satellite alert broadcasting  
- ✅ Network routing simulation using networkx  
- ✅ Visualization of satellite communication topology  
- ✅ CSV logging of telemetry, alerts, pause, and resume events  

---

## 📂 Project Structure

```
satnet_can_plus/
├── tle_data.txt              # TLEs for all satellites
├── simulate.py       # Main simulation script with smart collision response
├── comms.py                  # UDP communication with priority queue
├── collision_check.py        # Collision detection logic
├── routing.py                # Network graph + routing path
├── logger.py                 # CSV logger
├── visualize_topology.py     # Visualize network using networkx
├── events_log.csv            # Logs all events (generated at runtime)
└── README.md
```

---

## 🛠️ Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```
skyfield
numpy
networkx
matplotlib
```

---

## 🛰️ Input: TLE Data

Your `tle_data.txt` must follow this format (repeat for N satellites):

```
SAT-A
1 <TLE line 1>
2 <TLE line 2>
SAT-B
1 <TLE line 1>
2 <TLE line 2>
...
```

✅ Use valid or custom TLEs to simulate collisions. A sample TLE file that triggers a collision is included.

---

## ▶️ How to Run

To start the simulation with smart collision response:

```bash
python simulate.py
```

---

## 🔁 Optional: Visualize Satellite Network

```bash
python visualize_topology.py
```

---

## 📈 Output Example

```
🛰️ Satellite Simulation (Pause One, Resume Both When Safe) Started
[ALERT] ⚠️ COLLISION RISK! SAT-A ↔ SAT-B | Distance = 3.2 km
[LOG] SAT-A paused due to collision risk
[LOG] SAT-B sending telemetry...
[LOG] SAT-A resumed — safe distance now 11.4 km
```

Also saved in:

- `events_log.csv` — timestamped log of telemetry, alerts, pause, and resume events

---

## 🔐 Concepts Demonstrated

- Orbital mechanics using TLEs  
- ECI coordinate simulation  
- Proximity detection and threat estimation  
- Smart collision avoidance (pause/resume logic)  
- UDP-based communication model  
- Message prioritization and custom routing  
- Realistic satellite networking behavior  

---

## 📚 References

- [Skyfield Documentation](https://rhodesmill.org/skyfield/)  
- [Celestrak TLE Sources](https://celestrak.com/NORAD/elements/)  
- NASA Space Debris & Collision Avoidance  

---
