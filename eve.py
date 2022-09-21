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

# Server酱推送
sckey = os.environ["SCKEY"]

# 微信公众号 模板id
template_id = os.environ["TEMPLATE_ID_EVE"]

# 用户ID
user_id_1 = os.environ["USER_ID_1"]
user_id_2 = os.environ["USER_ID_2"]

# 用户列表 也可通过接口获取，但是接口获取的只有用户id没有用户昵称，不方便部分数据展示，如果有新增人员，对应添加一个user对象即可
'''
    user_id: 微信公众号的 openid
       name: 昵称
       date: 相识日期
   birthday: 生日
       city: 城市编码，api接口文档处查询
'''
user_id_list = [
    {'user_id': user_id_1, "name": 'Orange', "date": "2021-04-02", "birthday": "05-28",
     'city': '110108'},{'user_id': user_id_2, "name": 'Orange', "date": "2021-04-02", "birthday": "05-28",
     'city': '110108'}
]

def push():
    #text为推送的title,desp为推送的描述
    url = 'https://sc.ftqq.com/%s.send?text=自动推送完成'%sckey
    requests.get(url)


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


# 高德天气信息
def get_weather(city):
    url = "https://restapi.amap.com/v3/weather/weatherInfo?output=JSON&key=" + key + "&city=" + city
    res = requests.get(url).json()
    print(res)
    weather = res["lives"][0]
    return weather['weather'], weather['temperature'], weather['winddirection'], weather['province'] + weather[
        'city']


# 总天数
def get_count(start_date):
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


# 计算生日天数
def get_birthday(birthday):
    print(birthday)
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


# 发送消息 支持批量用户
def send_message():
    for user in user_id_list:
        user_id = user.get('user_id')
        name = user.get('name')
        birthday = user.get('birthday')
        start_date = user.get('date')
        city = user.get('city')
        get_count(start_date)
        get_birthday(birthday)
        print(user_id)

        wea, temperature, winddirection, cityName = get_weather(city)

        client = WeChatClient(app_id, app_secret)

        wm = WeChatMessage(client)
        # 获取今天日期
        # Date=today.strftime("%Y-%m-%d")
        data = {
            # "Time": {"value": today.strftime("%Y-%m-%d"), "color": get_random_color()},
            "name": {"value": name, "color": get_random_color()},
            "weather": {"value": wea, "color": get_random_color()},
            "temperature": {"value": temperature + "℃", "color": get_random_color()},
            "cityname": {"value": cityName, "color": get_random_color()},
            "winddirection": {"value": winddirection, "color": get_random_color()},
            "love_days": {"value": get_count(start_date), "color": get_random_color()},
            "birthday_left": {"value": get_birthday(birthday), "color": get_random_color()},
            "words": {"value": get_words(), "color": get_random_color()}
        }
        res = wm.send_template(user_id, template_id, data)
        print(res)


send_message()
push()
