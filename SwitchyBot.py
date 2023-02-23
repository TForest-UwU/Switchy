from termcolor import cprint

import pexpect
import pygatt
import re

class Bot(object):
    """Switchbot class to control the bot."""

    def __init__(self, bot_id: int, mac: str, name: str):

        if not re.match(r"[0-9A-F]{2}(?:[-:][0-9A-F]{2}){5}$", mac):
            raise ValueError(f"Illegal Mac Address: ", mac)

        self.bot_id = bot_id
        self.mac = mac
        self.name = name

        self.adapter = pygatt.GATTToolBackend()
        self.device = None
        self.password = None
        self.notification_activated = False
        cprint(f"Succesfully created {self.name} at {self.mac} with id {self.bot_id}", "cyan")

    def connect(self):
        con = pexpect.spawn('gatttool -b ' + self.mac + ' -t random -I')
        print('Preparing to connect')
        retry = 3
        index = 0
        while retry > 0 and 0 == index:
            con.sendline('connect')
            index = con.expect(
                ['Error', '\[CON\]', 'Connection successful.*\[LE\]>'])
            retry -= 1
            if 0 == index:
                cprint("Connection error", "red")
                return
            cprint(f"Connected to {self.name} at {self.mac}", "cyan")

    def press(self):
        try:
            self.adapter.start()
            self._connect()

            cmd = b'\x57\x01'
            value = self.write(handle=0x16, cmd=cmd)

        finally:
            self.adapter.stop()

    def _connect(self):
        try:
            self.device = self.adapter.connect(self.mac, address_type=pygatt.BLEAddressType.random)
            cprint(f"Succesfully reconnected to {self.name} at {self.mac}", "cyan")
        except pygatt.BLEError:
            raise ConnectionRefusedError(f"Failed to connect to {self.name} at {self.mac}")

    def write(self, handle, cmd):
        try:
            self.device.char_write_handle(handle = handle, value = cmd)
            cprint(f"Succesfully send {cmd} to {self.name} using handle {handle}")
 
        except pygatt.BLEError:
            raise ConnectionRefusedError(f"Failed to write {cmd} to {self.name} at {self.mac}")