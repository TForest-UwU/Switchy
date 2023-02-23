import pexpect
import pygatt
import re

class Bot(object):
    """Switchbot class to control the bot."""

    def __init__(self, bot_id: int, mac: str, name: str):

        if not re.match(r"[0-9A-F]{2}(?:[-:][0-9A-F]{2}){5}$", mac):
            raise ValueError("Illegal Mac Address: ", mac)

        self.bot_id = bot_id
        self.mac = mac
        self.name = name

        self.adapter = pygatt.GATTToolBackend()
        self.device = None
        self.password = None
        self.notification_activated = False
        print(f"Successfully created {self.name} at {self.mac} with Id {self.bot_id}")

    def trigger(device):
        [mac, dev_type, act] = device
        
        con = pexpect.spawn('gatttool -b ' + mac + ' -t random -I')
        con.expect('\[LE\]>')
        print('Preparing to connect.')

    def press(self):
        con = pexpect.spawn('gatttool -b ' + self.mac + ' -t random -I')
        print('Preparing to connect.')
        retry = 3
        index = 0
        while retry > 0 and 0 == index:
            con.sendline('connect')
            index = con.expect(
                ['Error', '\[CON\]', 'Connection successful.*\[LE\]>'])
            retry -= 1
            if 0 == index:
                print('Connection error')
                return
            print(f"Connected to {self.name} at {self.mac}")