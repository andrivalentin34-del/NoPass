# 🔵 Bluetooth Proximity Authentication System for Linux

A Linux system that automatically locks your screen when your phone or Bluetooth device goes out of range, and unlocks it when you return — no password needed while your phone is nearby.

> **Status:** Work in progress — Phase 2 active  

> **Language:** Python 3

---

## 📋 Table of Contents

- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [State Machine Logic](#state-machine-logic)
- [Development Roadmap](#development-roadmap)
- [Contributing](#contributing)

---

## How It Works

The system continuously monitors the proximity of a paired Bluetooth device (phone, smartwatch, etc.). Based on whether the device is nearby or not, the system transitions between states and locks/unlocks the screen accordingly.

```
Phone nearby (0-2m)     →  PC stays unlocked
Phone gone (< timeout)  →  Grace period (warning countdown)
Phone gone (> timeout)  →  Screen locks automatically
Phone returns           →  Screen unlocks automatically
```

Password always remains available as a fallback — if you don't have your phone, you can still log in normally.

---

## Project Structure

```
bluetooth-unlock/
├── src/
│   ├── bluetooth_detector.py    # Main script - detection loop & entry point
│   ├── bluetooth_mock.py        # Mock module for testing without hardware
│   └── grace_period.py          # State machine & timeout logic
├── venv/                        # Python virtual environment (not tracked)
├── mock_bluetooth_state.json    # Simulation control file (auto-generated)
├── .gitignore
└── README.md
```

---

## Setup & Installation

### Requirements

- Linux (tested on Linux Mint)
- Python 3.8+
- Bluetooth adapter (optional — mock mode works without it)

### Installation

```bash
# Clone the repository
git clone https://github.com/USERNAME/bluetooth-unlock.git
cd bluetooth-unlock

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (real Bluetooth mode)
pip install pybluez
```

> **Note:** If PyBluez is unavailable or your adapter is not supported, the system automatically switches to **Mock Mode** for testing.

---

## Usage

```bash
# Activate virtual environment first
source venv/bin/activate

# Run the detector
python src/bluetooth_detector.py
```

### Mock Mode (no hardware required)

When PyBluez is not installed, the system runs in simulation mode. You can control the simulated device state by editing `mock_bluetooth_state.json`:

```json
{
    "device_connected": true,
    "device_name": "My Phone",
    "device_address": "AA:BB:CC:DD:EE:FF"
}
```

Change `device_connected` to `true` or `false` while the program is running to simulate phone arriving/leaving.

---

## Configuration

All configurable values are at the top of their respective files:

**`bluetooth_detector.py`**
```python
TARGET_DEVICE_ADDRESS = "AA:BB:CC:DD:EE:FF"  # Your device MAC address
TARGET_DEVICE_NAME    = "My Phone"            # Display name
CHECK_INTERVAL        = 2                     # Seconds between checks
```

**`grace_period.py`**
```python
GRACE_PERIOD = 30  # Seconds to wait before locking
```

---

## State Machine Logic

The system uses a 4-state machine to manage transitions safely:

```
         phone present              phone present
STARTUP ──────────────► UNLOCKED ◄──────────────── GRACE
   │                       │                          │
   │ phone absent           │ phone absent             │ timeout expires
   │                        ▼                          │
   └──────────────────► LOCKED ◄──────────────────────┘
```

| State | Description |
|-------|-------------|
| `STARTUP` | First check after program launch |
| `UNLOCKED` | Phone nearby, PC is accessible |
| `GRACE` | Phone gone, countdown before locking |
| `LOCKED` | Screen locked, password required to re-enter |

**Security note:** Once in `LOCKED` state, the phone alone cannot unlock the system. This prevents unauthorized access if both the phone and laptop are stolen together. Re-authentication always requires the system password.

---

## Development Roadmap

### ✅ Phase 1 — Basic Detection (Complete)
- [x] Python Bluetooth detection script
- [x] Mock mode for testing without hardware
- [x] Transition detection (device found/lost)
- [x] JSON configuration for simulation
- [x] Git repository & GitHub

### 🔄 Phase 2 — Grace Period & Screen Lock (In Progress)
- [x] Grace period timeout logic
- [x] 4-state state machine (STARTUP, UNLOCKED, GRACE, LOCKED)
- [ ] Integration with Linux screen lock commands (`loginctl`, `xdg-screensaver`)
- [ ] Desktop notifications (warn before locking)
- [ ] systemd daemon service

### 🔜 Phase 3 — System Integration (Planned)
- [ ] PAM module for authentication at boot
- [ ] Auto-detect paired devices (no manual MAC config)
- [ ] RSSI-based distance estimation (not just present/absent)
- [ ] Configuration file (instead of editing source code)
- [ ] GUI tray icon

---

## Contributing

This project is developed as a learning exercise and potential thesis project. Contributions and suggestions are welcome.

If you find a bug or have an idea, open an issue on GitHub.

---

## License

MIT License — free to use, modify, and distribute.