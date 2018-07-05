import sqlite3

import praw
import configs
from dbconnect import DBHelper, Sent


class URLAnalyzer(object):
    def __init__(self):
        self.replasers = {
            "amazon.com": self.amazon_ref_replace
        }
    @staticmethod
    def is_ref_link(url):
        is_ref = False
        for tag in configs.URL_TYPES.values():
            if tag in url:
                is_ref = True
                break
        return is_ref

    def ref_code_replace(self, url):

        for domain in configs.REF_CODES:
            if domain in url:
                return self.replasers[domain](url)

    @staticmethod
    def amazon_ref_replace(url):
        str_1 = url.split("ref=")
        str_2 = str_1[1].split("?")
        str_2[0] = configs.REF_CODES["amazon.com"]
        new_url = "{}ref={}".format(str_1[0], configs.REF_CODES["amazon.com"])
        if len(str_2) > 1:
            new_url += "?{}".format('?'.join(str_2[1:]))
        return new_url


def main_deamon(user_id = None):
    url_analyzer = URLAnalyzer()
    reddit = praw.Reddit(client_id='QGgquYDRm7jKqQ',
                         client_secret='kIU_Rxo4gfO1jKP-XXMMHQH6Mug', password='131199artur',
                         user_agent='PrawTut', username = 'Lugini')

    subreddit = reddit.subreddit('GameDeals')
    i=0
    not_sent = 0
    with sqlite3.connect("todo.sqlite") as con:
        sent_table = Sent()
        sent_table.setup()
        db = DBHelper()
        for submission_id in subreddit.stream.submissions():
            try:
                i += 1
                submission = reddit.submission(id=submission_id)
                if submission.ups >= configs.MIN_UPVOTES and url_analyzer.is_ref_link(submission.url):
                    not_sent += 1
                    new_url = url_analyzer.ref_code_replace(submission.url)
                    exists = sent_table.get_items()
                    if new_url in exists:
                        not_sent += 1
                        print('Post_{}_existing_not_sent {}'.format(i, not_sent))
                        continue
                    if user_id:
                        not_sent += 1
                        configs.bot.sendMessage(user_id, "{}\n{}".format(submission.title, new_url))
                    else:
                        print('Post_{}_ref_sent {}'.format(i, not_sent))
                        for user in db.get_items():
                            configs.bot.sendMessage(user, "{}\n{}".format(submission.title, new_url))
                        sent_table.add_item(new_url)
                elif i >= 100 and not_sent >= 15 and "reddit.com" not in submission.url:
                    not_sent = 0
                    sent_table.add_item(new_url)
                    for user in db.get_items():
                        configs.bot.sendMessage(user, "{}\n{}".format(submission.title, submission.url))
                    print('Post_{}_sent'.format(i))
                else:
                    not_sent += 1
                    print('Post_{}_not_sent {}'.format(i, not_sent))
                if user_id and i == 100:
                    return
                else:
                    continue
            except praw.exceptions.PRAWException as e:
                pass
            except Exception as e:
                print("Not sent error")
                continue



if __name__ == '__main__':
    main_deamon()