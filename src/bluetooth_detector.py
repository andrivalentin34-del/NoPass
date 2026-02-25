#!/usr/bin/env python3
import time
import json
import os
from grace_period import GracePeriodManager, SystemState
from screen_lock import ScreenLockManager
# trying to import the actual library
try:
    import bluetooth
    USING_MOCK = False
    print("✅ Modul Bluetooth REAL detectat")
except ImportError:
    print("⚠️  Bluetooth indisponibil - folosesc modul SIMULARE")
    USING_MOCK = True

# ============================================
# CONFIGURATION
# ============================================

# for simulation only
MOCK_STATE_FILE = "mock_bluetooth_state.json"

# your own configuration of the key
TARGET_DEVICE_ADDRESS = "AA:BB:CC:DD:EE:FF"  # change with your address
TARGET_DEVICE_NAME = "MY PHONE"


# needs to be connected with the GRACE_PERIOD located in grace_period.py
CHECK_INTERVAL = 2


# FUNCTION FOR SIMULATION(MOCK)

def init_mock_state():
    if os.path.exists(MOCK_STATE_FILE):
        print(f"Fisier de stare gasit: {MOCK_STATE_FILE}")
        return

 # Fișierul nu există - îl creăm cu starea inițială
    print(f"📝 Creez fisier de stare: {MOCK_STATE_FILE}")

    initial_state = {
            "device_connected": False,
            "device_name": TARGET_DEVICE_NAME,
            "device_address": TARGET_DEVICE_ADDRESS,
            "last_update": time.strftime("%Y-%m-%d %H:%M:%S")
        }


    with open(MOCK_STATE_FILE, 'w') as f:
        json.dump(initial_state, f, indent=4)

    print("✅ succesfully created file")
    print(f"   Initial Status: Disconnected")


def read_mock_state():

    if not os.path.exists(MOCK_STATE_FILE):
        return None


    try:
        with open(MOCK_STATE_FILE, 'r') as f:
            state = json.load(f)
        return state
    except Exception as e:
        print(f"❌ Error when reading the file {e}")
        return None


def is_device_nearby_mock(target_address):

    state = read_mock_state()

    if state is None:
        return False

    return state.get("device_connected", False)


def is_device_nearby_real(target_address):

    try:

        result = bluetooth.lookup_name(target_address, timeout=5)


        if result is not None:
            return True
        else:
            return False

    except Exception as e:

        print(f"⚠️ Eroare Bluetooth: {e}")
        return False


def is_device_nearby_real(target_address):

    try:

        result = bluetooth.lookup_name(target_address, timeout=5)


        if result is not None:
            return True
        else:
            return False

    except Exception as e:

        print(f"⚠️ Eroare Bluetooth: {e}")
        return False


def is_device_nearby(target_address):

    if USING_MOCK:

        return is_device_nearby_mock(target_address)
    else:

        return is_device_nearby_real(target_address)


def main():
    """
    Main function
    Continuously monitors Bluetooth device presence
    """
    print("\n" + "=" * 60)
    print("🔵 BLUETOOTH PROXIMITY DETECTOR")
    print("=" * 60)

    # Check which mode we're using
    if USING_MOCK:
        print("🎭 MODE: SIMULATION (Mock)")
        print("   Control file:", MOCK_STATE_FILE)
        print()

        # Initialize state file if it doesn't exist
        init_mock_state()
    else:
        print("📡 MODE: REAL BLUETOOTH")
        print("   Bluetooth adapter must be functional")
        print()

    # Display configuration
    print("⚙️  CONFIGURATION:")
    print(f"   Target device: {TARGET_DEVICE_NAME}")
    print(f"   MAC Address: {TARGET_DEVICE_ADDRESS}")
    print(f"   Check interval: {CHECK_INTERVAL} seconds")
    print()

    # Instructions for simulation control
    if USING_MOCK:
        print("💡 SIMULATION CONTROL:")
        print("   To simulate connection/disconnection:")
        print()
        print("   1. Open the file:", MOCK_STATE_FILE)
        print("   2. Change 'device_connected' to:")
        print("      • true  = phone connected")
        print("      • false = phone disconnected")
        print("   3. Save the file")
        print()

    print("=" * 60)
    print("🔍 MONITORING ACTIVE")
    print("   Press Ctrl+C to stop")
    print("=" * 60)
    print()

    # Variable to track previous state
    manager = GracePeriodManager()
    lock_manager = ScreenLockManager()



    # Main loop - runs infinitely
    try:
        while True:
            # Display check timestamp
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] Checking presence...", end=" ")

            # Check if device is nearby
            device_present = is_device_nearby(TARGET_DEVICE_ADDRESS)

            # Detect state transitions
            manager.update(device_present)
            print(manager.get_status_display())

            if manager.state == SystemState.LOCKED:
                lock_manager.lock()
                # Verify if the user put the password
                if not lock_manager.is_system_locked():
                    manager.state = SystemState.UNLOCKED
                    lock_manager.unlock()
            else:
                lock_manager.unlock()

            remaining = manager.get_time_remaining()
            if remaining is not None:
                print(f"   ⏳ Time remaining: {remaining:.0f}s")

            # Wait before next check
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\n")
        print("=" * 60)
        print("⛔ Stopped by user")
        print("=" * 60)
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
