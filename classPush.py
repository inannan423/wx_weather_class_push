import json  # json 解析
import random
import os
import requests  # http 请求库
import datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
########################
# 填写账号密码
########################

id = os.environ["STUDENT_ID"]  # 学号
pwd = os.environ["PASSWORD"]  # 密码
# 微信公众号 ID
app_id = os.environ["APP_ID"]
# 微信公众号 app_secret
app_secret = os.environ["APP_SECRET"]
semester = '2022-2023-1'  # 学期
firstDay = '2022-08-29'  # 学期开始日期
# 用户ID
user_id_1 = os.environ["USER_ID_1"]
user_id_2 = os.environ["USER_ID_2"]
template_id_class = os.environ["TEMPLATE_ID_CLASS"]
template_id_noclass = os.environ["TEMPLATE_ID_NOCLASS"]


# "jsxm": "老师", // 教师姓名
# "jsmc": "一教101", // 教室名称
# "jssj": "9:35", // 结束时间
# "kssj": "08:00", // 开始时间
# "kkzc": "1", // 开课周次，有三种已知格式1)a - b、2)a, b, c、3)a - b, c - d
# "kcsj": "10102", // 课程时间，格式x0a0b，意为星期x的第a, b节上课
# "kcmc": "大学英语", // 课程名称
# "sjbz": "0" // 具体意义未知，据观察值为1时本课单周上，2时双周上

user_id_list = [
    {'user_id': user_id_1, "name": 'Orange', "date": "2021-04-02", "birthday": "05-28",
     'city': '110108'}
    ,{'user_id': user_id_2, "name": 'Orange', "date": "2021-04-02", "birthday": "05-28",
     'city': '110108'}
]

week = '6'
table = [[{'jsxm': '无', 'jsmc': '无', 'jssj': '00:00', 'kssj': '00:00', 'kkzc': '0', 'kcsj': '00000', 'kcmc': '本节无课',
              'sjbz': '0'} for i in range(1, 100)] for j in range(1, 100)]


# 获取当前日期
def getNowDate():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d')


# 判断当前日期所在周数
def getWeek():
    # 获取现在时间
    now = datetime.datetime.now()
    # 第一周
    firstWeek = datetime.datetime.strptime(firstDay, '%Y-%m-%d')
    # 当前周数
    week = (now - firstWeek).days // 7 + 1
    print("第" + str(week) + "周")
    return week


# 判断今天星期几
def getWeekDay():
    d = datetime.datetime.now()
    weekd = d.weekday() + 1
    print("星期" + str(weekd))
    return int(weekd)

# 判断当前所在第几节课
def getNowClass():
    # 获取现在时间
    now = datetime.datetime.now()
    # 获取现在时间的小时和分钟
    year = now.year
    hour = now.hour
    minute = now.minute + 20
    second = now.second
    # 如果分钟大于60，小时加1，分钟减60
    if minute >= 60:
        hour += 1
        minute -= 60
    # 拼接为时间格式
    if hour<=10:
        nowTime = '0' + str(hour) + ':' + str(minute) + ':' + str(second)
    else :
        nowTime = str(hour) + ':' + str(minute) + ':' + str(second)

    if hour==24:
        nowTime = '00' + ':' + str(minute) + ':' + str(second)
    print("现在时间：" + nowTime)
    # 判断当前时间所在第几节课
    # 如果当前时间位于 8:00 到 9:35 之间，返回 1
    # Github采用UTC时间，北京时间比UTC时间早8小时
    dt1 = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    dt2 = datetime.datetime.strptime('01:50:00', '%H:%M:%S')
    dt3 = datetime.datetime.strptime('05:30:00', '%H:%M:%S')
    dt4 = datetime.datetime.strptime('07:20:00', '%H:%M:%S')
    dt5 = datetime.datetime.strptime('10:30:00', '%H:%M:%S')
    dtNow = datetime.datetime.strptime(nowTime, '%H:%M:%S')
    # print((dtNow - dt1).seconds)
    if 0 <= (dtNow - dt1).seconds < 5700:
        return 1
    elif 0 <= (dtNow - dt2).seconds < 8700:
        return 3
    elif 0 <= (dtNow - dt3).seconds < 5700:
        return 6
    elif 0 <= (dtNow - dt4).seconds < 5700:
        return 8
    elif 0 <= (dtNow - dt5).seconds < 8700:
        return 10
    else:
        return -1

def Crawl():
    loginLink = "http://newjwxt.bjfu.edu.cn/app.do?method=authUser&xh=" + id + "&pwd=" + pwd
    rep = requests.get(loginLink)
    res = json.loads(rep.text)
    # 使用账号密码换取网站 token
    token = res["token"]
    tableUrl = "http://newjwxt.bjfu.edu.cn/app.do?method=getKbcxAzc&xh=" + id + "&xnxqid=" + semester + "&zc=" + week
    header = {
        "token": token  # 传入 token ，鉴权
    }
    res = requests.get(url=tableUrl, headers=header)
    schedule = json.loads(res.text)  # 读取课表 json
    # nowClass = getNowClass()  # 获取当前所在第几节课
    # print("当前第" + str(nowClass) + "节课")
    # 显示 schedule 中第 nowClass 节课的课程
    # print(schedule[nowClass - 1]['kcmc'])
    # print(schedule)  # 打印课表 json
    # 初始化二维列表

    # 将 schedule 中的课程信息赋值给 table
    for i in schedule:
        classNum = int(i['kcsj'][1] + i['kcsj'][2])
        # 将课程信息写入列表
        wd = int(i['kcsj'][0])
        table[wd][classNum] = i


def QueryClass():
    nowClass = getNowClass()
    nowWd = getWeekDay()
    if nowClass == -1:
        print("当前无课")
    else:
        print("当前第" + str(nowClass) + "节课")
    print(table[nowWd][nowClass])
    return table[nowWd][nowClass]

# 随机文字颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

# 发送消息 支持批量用户
def send_message():
    for user in user_id_list:
        user_id = user.get('user_id')
        lesson=QueryClass()
        client = WeChatClient(app_id, app_secret)
        wm = WeChatMessage(client)
        # 获取今天日期
        # Date=today.strftime("%Y-%m-%d")
        print(lesson['kcmc'])
        ks=lesson['kcsj'][1] + lesson['kcsj'][2]+'~'+lesson['kcsj'][3] + lesson['kcsj'][4]
        data = {
            "kcmc": {"value": str(lesson['kcmc']), "color": get_random_color()},
            "sksj": {"value": str(ks), "color": get_random_color()},
            "jsmc": {"value": str(lesson['jsmc']), "color": get_random_color()},
            "jsxm": {"value": str(lesson['jsxm']), "color": get_random_color()},
        }

        if (lesson['kcmc']=='本节无课'):
            res = wm.send_template(user_id, template_id_noclass, data)
        else:
            res = wm.send_template(user_id, template_id_class, data)
        print(res)

if __name__ == "__main__":
    week = str(getWeek())
    Crawl()
    # QueryClass()
    send_message()