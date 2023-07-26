import time
import logging
import random
import traceback
from models.bdCreator import Session, db_create
from models.users import Users
from apiSelenium import Authorization
from apiSelenium import Subscriber
from apiSelenium import MessageManager
from apiSelenium import UserManager
from send import send_mail
import data

NAME_ROJECT = "OnlyFans bot"
VERSION = '1.4'

pause = False
restart = False
session = Session()
file_log = logging.FileHandler('logs.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out),
                    format=f'[%(asctime)s | %(levelname)s | {VERSION}]: %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)


def checkUserInBd(url):
    user = session.query(Users).filter(Users.url == url)
    return bool(user.count())


def addUserInBd(url, status):
    session.add(Users(url=url, status=status))
    session.commit()


def loadMSG():
    file = open("textMSG.txt", 'r')
    msgList = file.read().split('\n')
    file.close()
    if msgList[-1] == "":
        msgList.pop(-1)
    return msgList


def main(restart=False):

    if not restart:
        logging.info(f"Start bots")

        authManager = Authorization(data)
        authManager.auth(data.user_data)
        data.driver = authManager.driver

        logging.info("Authorizations...")

        while not authManager.authCheck:
            pass

        logging.info("Great authorization")

    else:
        logging.info(f"Great restart")

    subsManager = Subscriber(data.driver, data)
    msgManager = MessageManager(data.driver, data)
    userManager = UserManager(data.driver, data)

    logging.info("Loads all managers")

    msgList = loadMSG()

    logging.info("Loads messages from file textMSG.txt")

    while True:
        if not pause:

            subsManager.GetPageNewSubscribers(1)
            for i in subsManager.subs:

                if checkUserInBd(i):  # если юер в БД уже есть пропускаем итерацию
                    continue

                time.sleep(0.5)
                chatUrl = userManager.GetUserChatUrl(i)
                if chatUrl == data.status_users["paid_subs"]:
                    addUserInBd(i, data.status_users['paid_subs'])
                elif chatUrl is None:
                    addUserInBd(i, data.status_users['not_find_chatBtn'])
                else:
                    msg = random.choice(msgList).replace(
                        '<nick>', subsManager.subs[i][0])

                    res = msgManager.SendMessage(chatUrl, f"{msg}")
                    if res:
                        logging.info(f"{i} sended messge '{msg}'")
                        addUserInBd(i, data.status_users['send_msg'])
                    else:
                        addUserInBd(i, data.status_users['not_send'])

            logging.info(f"Waiting next step ({data.timesleep} s).")
            time.sleep(data.timesleep)


if __name__ == "__main__":
    db_create()
    while True:
        try:
            main(restart)
        except Exception as err:
            logging.error(err, exc_info=True)
            msg = f'Error:\n{traceback.format_exc()})'
            send_mail(title=f"{NAME_ROJECT} v{VERSION}", message=msg)

            time.sleep(data.timedelay_restart)
            restart = True

        while True:
            try:
                eval(input(">>>"))
            except Exception as e:
                print(f"Error {e}")
