user_data = []
urls = {
    'main': "https://onlyfans.com",
    'notif_subs': "https://onlyfans.com/my/notifications/subscribed"
}

timesleep = 120
timedelay_restart = 5

xpath = {
    'btnAuth': "//button[@type='submit']",
    'nickSubs': '//a[@class="b-username"]',
    'dateSubs': './../../../..//span[contains(@class, "g-date")]',
    'chatBtn': "//a[@class='g-btn m-rounded m-border m-icon m-icon-only m-colored has-tooltip']",
    'chatInput': "//textarea[@id='new_post_text_input']",
    'chatSendMsg': '//button[@at-attr="send_btn" and not(@disabled)]',
    'chatTimeMsg': "./span[@class='b-chat__message__time']/span",
    'chatMessage': "//div[@at-attr='chat_message']",
    'chatTimeLine': "//div[@class='b-chat__messages__time']",
    'btnSubscribe': '//div[@class="m-rounded m-flex m-space-between g-btn"]'
}

driver = None

status_users = {
    'not_send': 0,
    'send_msg': 1,
    'paid_subs': 2,
    'not_find_chatBtn': 3
}
