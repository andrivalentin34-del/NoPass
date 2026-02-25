"""
Handles desktop notifications
"""

import subprocess

class Notifier:

    def __init__(self):
        self.last_notification = None

    def notify(self,title,message,urgency ="normal"):
        if self.last_notification == message:
            return

        try:
            subprocess.run([
                "notify-send",
                "--urgency", urgency,
                title,
                message
            ])
            self.last_notification = message

        except Exception as e:
            print(f"❌ Notification failed: {e}")