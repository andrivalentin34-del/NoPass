import random
import time

class MockBluetoothDevice:

    def __init__(self,name,address):
        self.name = name
        self.address = address
        self.is_connected = False
        self.rssi = -100

    def connect(self):
        self.is_connected = True
        self.rssi = random.randint(-50,-10)
        print(f" {self.name} Connected!    RSSi: {self.rssi} ")


    def disconnect(self):
        self.is_connected = False
        self.rssi = -100
        print(f"{self.name}  DISCONNECTED!!!")


    def get_status(self):
        return {
            'name' : self.name,
            'adress': self.address,
            'connected': self.is_connected,
            'rssi': self.rssi
        }

    class MockBluetoothScanner:
        def __init__ (self):
            self.devices = []
            self.scan_count = 0

    def add_device(self,name,address):
        device = MockBluetoothDevice(name,address)
        self.devices.append(device)
        print(f"Adaugat dispozitiv mock: {name} {address} ")
        return device

    def scan(self):
        self.scan_count += 1
        print(f"\n Scan {self.scan_count}")
        connected = [d for d in self.devices if d.is_connected]

        print(f"  Gasite: {len(connected)} dispozitive ")
        return connected

    def find_device(self, address):
        for device in self.devices:
            if device.address == address:
                return device

            return None


    def is_device_nearby(self, address):
        device = self.find_device(address)
        if device is None:
            return False

        return device.is_connected

