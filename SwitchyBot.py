from termcolor import cprint
from enum import Enum

import pexpect
import pygatt
import queue
import re

handle_queue = queue.Queue

class ActionStatus(Enum):
    complete = 1
    device_busy = 3
    device_unreachable = 11
    device_encrypted  = 7
    device_unencrypted = 8
    wrong_password = 9

    unable_resp = 254
    unable_connect = 255

class Bot(object):
    "Switchbot class to control the bot."

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
            self.handle_notify(value=value)

        finally:
            self.adapter.stop()


    def _connect(self):
        print("Attempting reconnection")
        try:
            self.device = self.adapter.connect(self.mac, address_type = pygatt.BLEAddressType.random)
            cprint(f"Succesfully reconnected to {self.name} at {self.mac}", "cyan")
        except pygatt.BLEError:
            raise ConnectionError(f"Failed to connect to {self.name} at {self.mac}")


    def handle_notify(handle: int, value: bytes):
        handle_queue.put((handle, value))


    def notify(self):
        uuid = "cba20003-224d-11e6-9fb8-0002a5d5c51b"
        try:
            self.device.subscribe(uuid, callback=handle_notify)
            self.notification_activated = True
        except pygatt.BLEError:
            raise ConnectionError("Failed to activate notification")


    def write(self, handle, cmd, timeout = 5):
        print("Attempting to send command")
        try:
            self.device.char_write_handle(handle = handle, value = cmd)
            _, value = handle_queue.get(timeout=timeout)
            cprint(f"Succesfully sent {cmd} to {self.name} using handle {handle}")
 
        except pygatt.BLEError:
            raise ConnectionError(f"Failed to send {cmd} to {self.name} at {self.mac}")

    
    def _handle_switchbot_status_msg(self, value: bytearray):
        status = value[0]
        action_status = ActionStatus(status)

        if action_status is not ActionStatus.complete:
            raise ConnectionError(f"{self.name} failed to execute command")