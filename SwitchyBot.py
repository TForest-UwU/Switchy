from termcolor import colored, cprint

import pexpect
import pygatt
import os
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
        cprint("Succesfully connected to ", "green")
        cprint(f"{self.name}", "on_cyan")

    def connect(self):
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