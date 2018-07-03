import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
from dbconnect import DBHelper
import sqlite3
"""
After **inserting token** in the source code, run it:
```
$ python2.7 diceyclock.py
```
[Here is a tutorial](http://www.instructables.com/id/Set-up-Telegram-Bot-on-Raspberry-Pi/)
teaching you how to setup a bot on Raspberry Pi. This simple bot does nothing
but accepts two commands:
- `/roll` - reply with a random integer between 1 and 6, like rolling a dice.
- `/time` - reply with the current time, like a clock.
"""

bot = telepot.Bot('575789532:AAFQ569xvZzwtqCogSBU8-4ZL0DvlveddVA')
def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    with sqlite3.connect("todo.sqlite") as con:
        db = DBHelper()
        print('Got command: %s' % command)
        if command:
            items = db.get_items()
            if str(chat_id) in items:
                print("Old one")
            else:
                db.add_item(str(chat_id))
                print("new one")


if __name__ == '__main__':


    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

    while 1:
        time.sleep(10)