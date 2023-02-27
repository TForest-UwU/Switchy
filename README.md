# Switchy - Python API to control switchbots
This project makes it easier to connect to the switchbot services by combining 2 API's that for me only seemed to work together, yet not alone

## DISCLAIMER
I did not fully make this myself, i heavily relied on these 2 existing programs to write this

Python-Host <br/>
Made by: OpenWonderLabs <br/>
https://github.com/OpenWonderLabs/python-host <br/>

Switchbotpy <br/>
Made by: nicolas-kuechler <br/>
https://github.com/RoButton/switchbotpy <br/>

## USAGE
Firstly you have to create a Bot instance to control, you can create one by running this command <br/>
`[Name of instance] = Bot(bot_id = [id you want], mac = [mac adress], name = [name of the bot])` <br/>
For example <br />
`Bot1 = Bot(bot_id = 1, mac = "A1:B2:C3:D4:E5:F6", name = "LightBot1")` <br/>

After we have our Bot instance we have to connect to it using the connect command <br/>
`[Name of instance].connect()` or `Bot1.connect()` <br/>

When we have connected the Bot instance we need to call a function, currently the only function is press() <br/>
`[Name of instance].press()` or `Bot1.press()` <br/>

## SPECIALS
Should you have the need to write a custom command to the bot you can use write() for it <br/>
`[Name of instance].write(handle, cmd)` for press this would be `Bot1.write(0x16, b'\x57\x01')` <br/>

## EXAMPLES
This is an example where you input a your variables and it activates the bot
```
from SwitchyBot import Bot

Name = input("Instance name: ")                   # Pick a name
ID = input("ID: ")                                # An ID
Mac = input("Mac adress: ")                       # And the adress

Bot0 = Bot(bot_id = ID, mac = Mac, name = Name)   # Create the bot
Bot0.connect()                                    # Connect to the bot
Bot0.press()                                      # And press
```

## KNOWN ISSUES
After running a succesfull script you will get a warning that states <br/>
`Failed to send b'W\x01' to [Instance name] at [Mac adress]` <br/>

It did not fail, it just thinks it did <br/>

When trying to run the script you get a ModuleNotFoundError <br/>
`ModuleNotFoundError: No module named 'SwitchyBot'` <br/>

To fix this import sys and use sys.path.append <br/>
```
import sys
sys.path.append([Your path to SwitchyBot.py])
from SwitchyBot import Bot
```

If you encounter any other errors or problems feel free to make an issue, however do keep in mind that im not a professional and can only do so much
