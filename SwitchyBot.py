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

        raise ValueError("Mac: ", self.mac)

    def trigger(device):
        [mac, dev_type, act] = device
        raise ValueError("Mac: ", self.mac)
        con = pexpect.spawn('gatttool -b ' + mac + ' -t random -I')
        con.expect('\[LE\]>')
        print('Preparing to connect.')

    def press(self):
        _trigger
