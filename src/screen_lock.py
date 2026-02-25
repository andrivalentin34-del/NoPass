"""
Screen Lock Manager
-using system commands

"""

import subprocess

# Cinnamon: "cinnamon-screensaver-command --lock"
# MATE:     "mate-screensaver-command --lock"
# GNOME:    "loginctl lock-session"
# XFCE

LOCK_COMMAND = 'xflock4'

class ScreenLockManager:
    def __init__(self):
        self.is_locked = False

    def lock(self):
        if self.is_locked:
            return

        try:
            subprocess.run([LOCK_COMMAND], check=True)
            self.is_locked = True
            print("Screen locked - succes")
        except subprocess.CalledProcessError as e:
            print("Failed to lock the screen")

        except FileNotFoundError:
            print(f"Command not found {LOCK_COMMAND} make sure is the right distro or the command is installed")


    def unlock(self):
        self.is_locked = False
        print("Screen unlocked state")

