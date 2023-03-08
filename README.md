# Switchy - Python API to control switchbots
This project makes it easier to connect to the switchbot services by combining 2 API's that for me only seemed to work together, yet not alone
This project is focused on the raspberry pi, syscmds therefore only work on that unless you change them in the config file

## DISCLAIMER
I did not fully make this myself, i heavily relied on these 2 existing programs to write this

Python-Host <br/>
Made by: OpenWonderLabs <br/>
https://github.com/OpenWonderLabs/python-host <br/>

Switchbotpy <br/>
Made by: nicolas-kuechler <br/>
https://github.com/RoButton/switchbotpy <br/>

## USAGE
Firstly import Bot from SwitchyBot <br/>
`from SwitchyBot import Bot` <br/>

Then you have to create a Bot instance to control, you can create one by running this command <br/>
`[Name of instance] = Bot(bot_id = [id you want], mac = [mac adress], name = [name of the bot])` <br/>
For example <br />
`Bot1 = Bot(bot_id = 1, mac = "A1:B2:C3:D4:E5:F6", name = "LightBot1")` <br/>

When we have the Bot instance we can call press() to press the bot, if the bot is in dual state mode it will switch between ON/OFF <br/>
`[Name of instance].press()` or `Bot1.press()` <br/>

We can also call the switch() function if we have a bot in dual state mode, state is 0 for OFF and 1 for ON <br/>
`[Name of instance].switch(state)` or `Bot1.switch(0)` <br/>

## SYSCMD
This is a class for the system commands, to use them import SysCmd <br/>
`from SwitchyBot import SysCmd` <br/>

To start bluetooth on demand run startblue() <br/>
`SysCmd.startblue()` <br/>

If you cant connect to bluetooth run restartblue() to restart bluetooth <br/>
`SysCmd.restartblue()` <br/>

## EXAMPLES
This is an example where you input your variables and it activates the bot
```
from SwitchyBot import Bot

Name = input("Instance name: ")                   # Pick a name
ID = input("ID: ")                                # An ID
Mac = input("Mac adress: ")                       # And the adress

Bot0 = Bot(bot_id = ID, mac = Mac, name = Name)   # Create the bot
Bot0.press()                                      # And press
```

## KNOWN ISSUES
After running a succesfull script you will get a warning that states <br/>
`Failed to send b'W\x01' to [Instance name] at [Mac adress]` <br/>

It did not fail, it just thinks it did <br/>

When trying to run the script you get a ModuleNotFoundError <br/>
`ModuleNotFoundError: No module named 'SwitchyBot'` <br/>

To fix this import sys and use sys.path.append or put the script in the same directory as the repository <br/>
```
import sys
sys.path.append([Your path to SwitchyBot.py])
from SwitchyBot import Bot
```

If you encounter any other errors or problems feel free to make an issue, however do keep in mind that im not a professional and can only do so much
