from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import random
import json

login_url = 'https://www.t00ls.net/login.json'
sigin_url = 'https://www.t00ls.net/ajax-sign.json'

login_header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
}

login_post_params = {
    'username': 账号,
    'password': md5(密码),
    'questionid': 问题序号,
    'answer': 问题答案,
    'action': 'login',
    'redirect': 'https://www.t00ls.net/',
    'cookietime': '2592000',
}

sched = BlockingScheduler()

def tools_auto_sigin():
    # 模拟登陆
    login_response = requests.post(login_url, headers=login_header, data=login_post_params, allow_redirects=False, timeout=5)
    login_response_json = json.loads(login_response.text)
    
    # 获取cookie
    cookie = requests.utils.dict_from_cookiejar(login_response.cookies)

    # 获取表单哈希值
    formhash = login_response_json['formhash']
    
    # 构建签到表单
    sigin_post_params = {
        'formhash': formhash,
        'signsubmit': 'apply'
    }

    if login_response_json['status'] == 'success':
        print('成功登陆')
        # 签到模块
        sigin_response = requests.post(sigin_url, headers=login_header, cookies=cookie, data= sigin_post_params)
        if (sigin_response["status"] == "success"):
            print ("签到成功")
        elif (sigin_response["message"] == "alreadysign"):
            print ("已经签到过了")
        else:
            tools_auto_sigin()
    else:
        tools_auto_sigin()
    
    
if __name__ == '__main__':
    sched.add_job(tools_auto_sigin, 'cron', year='*', month='*', day='*', hour=str(random.randrange(24)), minute='00', second='00')
    sched.start()
