import os
import random
from datetime import date, datetime

import requests
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage

# 当前日期
today = datetime.now()

# 微信公众号 ID
app_id = os.environ["APP_ID"]

# 微信公众号 app_secret
app_secret = os.environ["APP_SECRET"]

# 高德天气接口密钥 key
key = os.environ["KEY"]

# 微信公众号 模板id
template_id = os.environ["TEMPLATE_ID_EVE"]

# 用户ID
user_id_1 = os.environ["USER_ID_1"]
user_id_2 = os.environ["USER_ID_2"]

user_id_list = [
    {'user_id': user_id_1, "name": 'Orange', "date": "2021-04-02", "birthday": "05-28",
     'city': '110108'}, {'user_id': user_id_2, "name": 'Orange', "date": "2021-04-02", "birthday": "05-28",
                         'city': '110108'}
]


# 好听的情话 API
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    result = words.json()['data']['text']
    print(result)
    return result


# 随机文字颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


# 发送消息 支持批量用户
def wx_push():
    for user in user_id_list:
        user_id = user.get('user_id')
        print(user_id)

        client = WeChatClient(app_id, app_secret)

        wm = WeChatMessage(client)
        data = {
            "words": {"value": get_words(), "color": get_random_color()}
        }
        res = wm.send_template(user_id, template_id, data)
        print(res)


wx_push()
