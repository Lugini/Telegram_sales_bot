import time
import sqlite3

import telepot
from telepot.loop import MessageLoop
import praw

from configs import bot
from dbconnect import DBHelper
from reddit_deamon import main_deamon


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    with sqlite3.connect("todo.sqlite"):
        db = DBHelper()
        print('Got command: %s' % command)
        if command:
            items = db.get_items()
            if str(chat_id) in items:
                print("Old one")
            else:
                db.add_item(str(chat_id))
                main_deamon(user_id=chat_id)
                print("new one")


if __name__ == '__main__':


    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

    while 1:
        time.sleep(10)