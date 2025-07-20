# 🛰️ SatNet-CAN+: Satellite-to-Satellite Collision Alert Network (Python Simulation)


**Sat-CAN+** is a Python-based real-time simulation system that models inter-satellite communication for **collision detection and avoidance** using Two-Line Element (TLE) data, orbital dynamics, and UDP-based message routing. It mimics how satellites in a constellation can autonomously avoid potential collisions by exchanging telemetry and applying delta-v maneuvers.

---

## 🚀 Project Features

- 🌍 **TLE-based Orbit Simulation** using [Skyfield](https://rhodesmill.org/skyfield/)
- 📡 **Inter-Satellite Communication** with UDP Sockets and Priority Messaging
- ⚠️ **Collision Detection** using real-time 3D position data
- 🛡️ **Delta-V Maneuver Execution** for avoidance and orbit restoration
- 🛰️ **Telemetry Exchange** between all satellites
- 🧠 **Graph-based Routing Engine** using NetworkX
- 📓 **Logging System** for alerts, telemetry, and actions

---

## 📂 Repository Structure

```
sat-can+/project
│
├── simulate.py              # Main simulation runner
├── routing.py               # Network graph and routing logic
├── collision_check.py       # Collision detection logic
├── comms.py                 # Communication system (UDP)
├── logger.py                # Event logging utility
└──tle_data.txt             # TLE data for satellites
 
```

---

## 🔧 How It Works

1. **Load TLEs**: Parses and initializes satellite orbits from `tle_data.txt`.
2. **Construct Network**: Builds a full-mesh communication graph using `NetworkX`.
3. **Detect Collisions**: Continuously checks distances between satellites.
4. **Avoid Collisions**: Applies small velocity changes (Δv) to avoid collisions.
5. **Communicate**: Satellites send warnings, telemetry, and status over UDP.
6. **Restore Orbits**: Reverts to original TLEs after safe conditions are met.

---

## 📌 Prerequisites

- Python 3.8+
- Install dependencies:

```bash
pip install skyfield numpy networkx
```

---

## 🛠️ Running the Simulation

1. Place your TLE data in `tle_data.txt` with the format:
    ```
    SAT-1
    1 25544U 98067A   24190.12345678  .00001234  00000-0  12345-4 0  9991
    2 25544  51.6432 123.4567 0001234 123.4567 234.5678 15.54321098765432
    SAT-2
    ...
    ```

2. Run the main script:
```bash
python simulate.py
```

---

## 📊 Example Output

```
Loaded satellite: SAT-1 with TLE: ...
Assigned ports: {'SAT-1': 9000, 'SAT-2': 10000, ...}
Collision check between SAT-1 and SAT-2: Distance = 0.95 km, Risk = True
[RECEIVED from ... for SAT-2]: WARNING: COLLISION RISK! SAT-1 <-> SAT-2 | Distance = 0.95 km
[Action] SAT-1: Applied Δv: [0.007 0.002 -0.001] m/s
```

---

## 📁 Modules Explained

- **simulate.py**  
  Main simulation loop, orbit restoration, maneuver logic

- **routing.py**  
  Builds a graph of all satellite connections

- **collision_check.py**  
  Detects collision risks based on positions

- **comms.py**  
  Implements UDP communication between satellites

- **logger.py** *(optional)*  
  Can be extended to log to file or cloud

---

## 🧪 Test It Yourself

You can simulate multiple satellites by editing the `tle_data.txt` file with real or synthetic TLEs. The system automatically detects risk and executes maneuvers in real-time.

---

## 🔒 Security Note

This simulation uses local UDP communication and does not reflect space-grade encryption or actual satellite protocols. It is intended for educational and research purposes only.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).


---

## 🌠 Future Work

- Add orbital propagation using SGP4/SGP8 integrators  
- Integrate ML models for intelligent maneuver decisions  
- Visualize orbits and network using 3D plotting tools
