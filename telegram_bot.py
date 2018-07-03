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
        if command == "/start":
            users = db.get_items()
            if str(chat_id)in users:
                bot.sendMessage(chat_id, "I'am glad to send you my deals. If you wanna stop receiving my messages "
                                         "use /stop command")
                print("Old one")
                return
            else:
                bot.sendMessage(chat_id, "Hi i'm Game Deals Bot, I will share with you some great offers to save your"
                                         " money. If you wanna stop receiving my messages use /stop command")
                db.add_item(str(chat_id))
                main_deamon(user_id=chat_id)
                print("New one")
        elif command == "/stop":
            if str(chat_id) in db.get_items():
                bot.sendMessage(chat_id, "Okay I will shut up if you want. Just let me know if you want to receive"
                                         " my messages again, use /start command")
                db.delete_item(chat_id)
        else:
            if str(chat_id) in db.get_items():
                bot.sendMessage(chat_id, "I'm not sure if I understand you. Wait for new offers and have a nice day :)")
            else:
                bot.sendMessage(chat_id, "It seems we are not familiar yet, use /start command and I will who I am")


if __name__ == '__main__':
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

    while 1:
        time.sleep(10)