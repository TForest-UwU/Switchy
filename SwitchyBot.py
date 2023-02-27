from termcolor import cprint

import binascii
import pexpect
import pygatt
import queue
import copy
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

            cmd = b'\x57\x01' # Command for no password
            self.write(handle=0x16, cmd=cmd)

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
            cprint("If action was succesfull ignore this message", "orange")

        return
    
class Scanner(object):
    def Scan(self):
        service_uuid = 'cba20d00-224d-11e6-9fb8-0002a5d5c51b'
        company_id = '6909'  # actually 0x0969
        
        param_list = []
        dev_list = []
        bot_list = []

        self.con = pexpect.spawn('hciconfig')
        pnum = self.con.expect(['hci0', pexpect.EOF, pexpect.TIMEOUT])
        if pnum == 0:
            self.con = pexpect.spawn('hcitool lescan')

            scanner = Scanner().withDelegate(Scanner())
            devices = scanner.scan(10.0)
            cprint("Scanning...", "cyan")

        else:
            raise ConnectionError("No bluetooth connection")
        
        for dev in devices:
            mac = 0
            param_list[:] = []
            for (adtype, desc, value) in dev.getScanData():
                if desc == "Local name":
                    if value == "WoHand":
                        mac = dev.addr
                        dev_type = b'H'

            if mac != 0:
                dev_list.append([mac, dev_type, copy.deepcopy(param_list)])

        for (mac, dev_type, params) in dev_list:
            if dev_type == b'H':
                if int(binascii.b2a_hex(params[0]), 16) > 127:
                    bot_list.append([mac, 'Bot', 'Turn On'])
                    bot_list.append([mac, 'Bot', 'Turn Off'])
                    bot_list.append([mac, 'Bot', 'Up'])
                    bot_list.append([mac, 'Bot', 'Down'])
                else:
                    bot_list.append([mac, 'Bot', 'Press'])