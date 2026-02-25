"""
Grace Period Manager
Handles the timeout logic before locking the screen
when the Bluetooth device goes out of range.
"""

import time
from enum import Enum

class SystemState(Enum):
    UNLOCKED = "unlocked"
    GRACE = "grace"
    LOCKED = "locked"

GRACE_PERIOD = 30

class GracePeriodManager:

    def __init__(self):
        self.state = SystemState.UNLOCKED
        self.grace_start = None

    def update(self,device_present):
        if device_present:
            self.state = SystemState.UNLOCKED
            self.grace_start = None

        elif self.state == SystemState.UNLOCKED and not device_present:
            self.state = SystemState.GRACE
            self.grace_start = time.time()

        elif self.state == SystemState.GRACE:
            elapsed = time.time() - self.grace_start
            if elapsed > GRACE_PERIOD:
                self.state = SystemState.LOCKED

    def get_time_remaining(self):
        if self.state != SystemState.GRACE:
            return None
        elapsed = time.time() - self.grace_start
        remaining = GRACE_PERIOD - elapsed
        return max(0, remaining)

    def get_status_display(self):

        if self.state == SystemState.UNLOCKED:
            return "🟢 UNLOCKED - Phone nearby"

        elif self.state == SystemState.GRACE:
            remaining = self.get_time_remaining()
            return f"🟡 GRACE PERIOD - Locking in {remaining:.0f} seconds"

        elif self.state == SystemState.LOCKED:
            return "🔴 LOCKED - Phone out of range"