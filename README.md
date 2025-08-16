# 🛰️ SatNet-CAN+: Satellite-to-Satellite Collision Alert Network

**SatNet-CAN+** is a Python-based real-time simulation system that models **inter-satellite communication for collision detection and avoidance** using **TLE data**, **orbital dynamics**, and **UDP-based message routing**.  

The project has been extended to include **ground-station communication using LoRa (MATLAB simulation)**, demonstrating how satellites can send collision alerts to Earth.  

---

## 🌟 Project Features  

- 🌍 **TLE-based Orbit Simulation** using Skyfield  
- 📡 **Inter-Satellite Communication** with UDP sockets and priority messaging  
- ⚠️ **Collision Detection** using real-time 3D position data  
- 🛡️ **Delta-V Maneuver Execution** for avoidance and orbit restoration  
- 🛰️ **Telemetry Exchange** between satellites  
- 🧠 **Graph-based Routing Engine** using NetworkX  
- 📓 **Logging System** for alerts, telemetry, and actions  
- 📡 **LoRa Ground Station Communication (MATLAB)** for transmitting collision alerts to Earth  

---

## 📂 Repository Structure  

```
sat-can+/project
│
├── simulate.py          # Main simulation runner
├── routing.py           # Network graph and routing logic
├── collision_check.py   # Collision detection logic
├── comms.py             # UDP-based communication system
├── logger.py            # Event logging utility
├── tle_data.txt         # Satellite TLE data
│
├── alert_bits.txt       # Collision alert bitstream (generated during simulation)
└── lora.m               # MATLAB LoRa script
```

---

## 🔧 How It Works  

### 1. Satellite-to-Satellite Simulation (Python)  
1. **Load TLEs** → Parses and initializes satellite orbits from `tle_data.txt`.  
2. **Construct Network** → Builds a full-mesh communication graph using NetworkX.  
3. **Detect Collisions** → Continuously checks distances between satellites.  
4. **Avoid Collisions** → Applies small velocity changes (Δv) to avoid collisions.  
5. **Communicate** → Satellites exchange warnings, telemetry, and status over UDP.  
6. **Restore Orbits** → Reverts to original TLEs after safe conditions are met.  

---

### 2. Ground Station Communication (LoRa Extension in MATLAB)  

1. **Alert Generation**  
   - Collision alerts are saved as **bitstreams** in `alert_bits.txt`.  

2. **LoRa Transmission** (`lora.m`)  
   - Reads `alert_bits.txt`  
   - Modulates the bits using **LoRa SF=7, BW=125 kHz**  
   - Transmits and receive the signal in MATLAB
   - Logs and displays the alert message   

---

## 📡 Satellite-to-Ground LoRa Communication Diagram  

```
      ┌───────────────┐
      │   SAT-1       │
      │ Collision     │
      │ Detection     │
      └─────┬─────────┘
            │ UDP Telemetry
            ▼
      ┌───────────────┐
      │   SAT-2       │
      │ Collision     │
      │ Detection     │
      └─────┬─────────┘
            │ UDP Telemetry
            ▼
      ┌───────────────────────┐
      │   Satellite Constellation
      │  (Collision Alerts)   │
      └─────┬─────────┬───────┘
            │ LoRa Transmission
            ▼
      ┌───────────────┐
      │ Ground Station│
      │  LoRa RX      │
      │ Demodulate &  │
      │ Display Alert │
      └───────────────┘
```

---

## 📌 Prerequisites  

- **Python 3.8+**  
```bash
pip install skyfield numpy networkx
```

- **MATLAB R2020a+** (for LoRa ground station simulation)  

---

## 🛠️ Running the Simulation  

### Run the Satellite Simulation  
```bash
python simulate.py
```

**Example Output:**  
```
Loaded satellite: SAT-1 with TLE: ...
Assigned ports: {'SAT-1': 9000, 'SAT-2': 10000, ...}
Collision check between SAT-1 and SAT-2: Distance = 0.95 km, Risk = True
[RECEIVED from ... for SAT-2]: WARNING: COLLISION RISK! SAT-1 <-> SAT-2 | Distance = 0.95 km
[Action] SAT-1: Applied Δv: [0.007 0.002 -0.001] m/s
[Alert Saved] -> alert_bits.txt
```

### Run LoRa Ground Station Simulation (MATLAB)  
```matlab
>> lora
```

---

## 📜 License  

This project is open-source and available under the **MIT License**.  

---

## 🌠 Future Work  

- Add orbital propagation using **SGP4/SGP8 integrators**  
- Integrate **machine learning** for intelligent maneuver planning  
- Extend LoRa simulation with **channel effects** (path loss, Doppler, noise)  
- Visualize orbits and LoRa link performance in **3D**  
- Multi-ground-station support with gateway selection
