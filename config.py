##-----------------------CONFIG------------------------##
# This is the config file for SwitchyBot.py
# BLE CONFIG is useless unless you call restartblue()
# Try not to change BOT CONFIG


##---------------------FILE CONFIG---------------------##
packagepath = "/usr/lib/python3/dist-packages"

##------------------FUNCTIONS CONFIG-------------------##
terminalcmd =   "lxterminal -e"

tryconnect  =   3

##---------------------BLE CONFIG----------------------##
startcmd    =   "sudo bluetoothctl power on"
stopcmd     =   "sudo bluetoothctl power off"
agentcmd    =   "sudo bluetoothctl agent on"
stagentcmd  =   "sudo bluetoothctl agent off"
scancmd     =   "sudo bluetoothctl scan on"
stscancmd   =   "sudo bluetoothctl scan off"
resetcmd    =   "sudo systemctl restart bluetooth"
rfkillcmd   =   "rfkill unblock bluetooth"

##---------------------BOT CONFIG----------------------##
notifuuid   =   "cba20003-224d-11e6-9fb8-0002a5d5c51b"
botuuid     =   "cba20002-224d-11e6-9fb8-0002a5d5c51b"

presscode   =   "570100"
oncode      =   "570101"
offcode     =   "570102"