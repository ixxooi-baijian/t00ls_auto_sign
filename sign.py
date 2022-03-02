from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import random
import json

login_url = 'https://www.t00ls.cc/login.json'
sign_url = 'https://www.t00ls.cc/ajax-sign.json'

login_post_params = {
    'username': '账号',
    'password': 'md5(密码)',
    'questionid': '问题序号',
    'answer': '问题答案',
    'action': 'login',
    'redirect': 'https://www.t00ls.cc/',
    'cookietime': '2592000',
}

# 问题序号如下：
# 0 = 没有安全提问
# 1 = 母亲的名字
# 2 = 爷爷的名字
# 3 = 父亲出生的城市
# 4 = 您其中一位老师的名字
# 5 = 您个人计算机的型号
# 6 = 您最喜欢的餐馆名称
# 7 = 驾驶执照的最后四位数字

login_header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
}

scheduler = BlockingScheduler()


def tools_auto_sign():
    # 模拟登陆
    login_response = requests.post(login_url, headers=login_header, data=login_post_params, allow_redirects=False,
                                   timeout=5)
    login_response_json = json.loads(login_response.text)

    # 获取cookie
    cookie = requests.utils.dict_from_cookiejar(login_response.cookies)

    # 获取表单哈希值
    form_hash = login_response_json['formhash']

    # 构建签到表单
    sign_post_params = {
        'formhash': form_hash,
        'signsubmit': 'apply'
    }

    if login_response_json['status'] == 'success':
        print('成功登陆')
        # 签到模块
        sign_response = requests.post(sign_url, headers=login_header, cookies=cookie, data=sign_post_params).json()
        print(sign_response)

        if sign_response["status"] == "success":
            print("签到成功")
        elif sign_response["message"] == "alreadysign":
            print("已经签到过了")
        else:
            tools_auto_sign()
    else:
        tools_auto_sign()


def random_time_function():
    global last_day_sign_time
    now_datetime = datetime.datetime.now()
    if last_day_sign_time:
        if (now_datetime.date() - last_day_sign_time.date()).days == 1:
            _hour_random = random.randrange(24)
            _minute_random = random.randrange(60)
            _second_random = random.randrange(60)
            scheduler.add_job(tools_auto_sign, 'cron', year=now_datetime.year, month=now_datetime.month,
                              day=now_datetime.day, hour=_hour_random, minute=_minute_random, second=_second_random)
            scheduler.start()
            last_day_sign_time = datetime.datetime(year=now_datetime.year, month=now_datetime.month,
                                                   day=now_datetime.day, hour=_hour_random, minute=_minute_random,
                                                   second=_second_random)
        else:
            last_day_sign_time = now_datetime
            tools_auto_sign()
    else:
        last_day_sign_time = now_datetime
        tools_auto_sign()


if __name__ == '__main__':
    scheduler.add_job(random_time_function, 'cron', year='*', month='*', day='*', hour=0,
                      minute=0, second=0)
    scheduler.start()
