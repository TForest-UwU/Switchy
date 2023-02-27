from termcolor import cprint

import pexpect
import pygatt
import queue
import sys
import re

notification_queue = queue.Queue()

def handle_notification(handle: int, value: bytes):
    notification_queue.put((handle, value))

class Bot(object):
    "Switchbot class to control the bot"

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
        connect = pexpect.spawn('hciconfig')

        pnum = connect.expect(["hci0", pexpect.EOF, pexpect.TIMEOUT])
        if pnum != 0:
            print('No bluetooth hardware, exit now')
            sys.exit()
        connect = pexpect.spawn('hciconfig hci0 up')

        con = pexpect.spawn('gatttool -b ' + self.mac + ' -t random -I')
        con.expect('\[LE\]>')
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

        con.sendline('char-desc')
        con.expect(['\[CON\]', 'cba20002-224d-11e6-9fb8-0002a5d5c51b'])
        cmd_handle = con.before.decode('utf-8').split('\n')[-1].split()[2].strip(',')

        con.sendline('char-write-cmd ' + cmd_handle + ' 570100')

    def press(self):
        try:
            self.adapter.start()
            self._connect()
            self._activate_notifications()

            if self.password:
                cmd = b'\x57\x11' + self.password
            else:
                cmd = b'\x57\x01'
            
            self.write(handle=0x16, cmd=cmd)

        finally:
            self.adapter.stop()

    def switch(self, state: bool):
        try:
            self.adapter.start()
            self._connect()
            self._activate_notifications()

            if self.password:
                cmd = b'\x57\x11' + self.password
            else:
                cmd = b'\x57\x01'
            
            if state:
                cmd += b'\x01'
            else:
                cmd += b'\x02'

            self.write(handle=0x16, cmd=cmd)

        finally:
            self.adapter.stop()
    
    def setmode(self, dual_state: bool, inverse: bool):
        try:
            self.adapter.start()
            self._connect()
            self._activate_notifications()

            if self.password:
                cmd_base = b'\x57\x13' + self.password
            else:
                cmd_base = b'\x57\x03'

            cmd = cmd_base + b'\x64'

            config = 0
            if dual_state:
                config += 16
            if inverse:
                config += 1

            cmd += config.to_bytes(1, byteorder='big')

            self._write_cmd_and_wait_for_notification(handle=0x16, cmd=cmd)

        finally:
            self.adapter.stop()


    def _connect(self):
        self.device = self.adapter.connect(self.mac, address_type=pygatt.BLEAddressType.random)


    def _activate_notifications(self):
        uuid = "cba20003-224d-11e6-9fb8-0002a5d5c51b"
        try:
            self.device.subscribe(uuid, callback=handle_notification)
            self.notification_activated = True
        except pygatt.BLEError:
            raise ConnectionError(message="communication with ble device failed")


    def write(self, handle, cmd):
        print("Attempting to send command")
        try:
            self.device.char_write_handle(handle = handle, value = cmd)

            cprint(f"Succesfully sent {cmd} to {self.name} using handle {handle}") # Does not print for some reason
 
        except pygatt.BLEError:
            cprint(f"Failed to send {cmd} to {self.name} at {self.mac}", "red")
            cprint("If action was succesfull ignore this message", "yellow")

        return