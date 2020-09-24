from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import re
import random

login_url = 'https://www.t00ls.net/login.html'

login_header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Cookie': 'UTH_cookietime=2592000; ',
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
    'formhash': 'b7112f2b',
    'loginsubmit': '登陆',
    'redirect': 'https://www.t00ls.net/',
    'cookietime': '2592000',
}

sched = BlockingScheduler()

def tools_auto_sigin():
    get_formhash_url = 'https://www.t00ls.net/checklogin.html'

    get_formhash_response = requests.post(get_formhash_url, headers=login_header)
    formhash = re.findall('formhash=(.*?)"', get_formhash_response.text)[0]

    sigin_url = 'https://www.t00ls.net/ajax-sign.json'

    sigin_post_params = {
        'formhash': formhash,
        'signsubmit': 'apply'
    }

    # 模拟登陆
    login_response = requests.post(login_url, headers=login_header, data=login_post_params, allow_redirects=False, timeout=5)
    # 获取返回的cookie
    if login_response.status_code == 302:
        print('成功登陆')
        response_cookie_str = login_response.headers['Set-Cookie']
        reg = re.compile('(.*?(?:UTH_sid=|UTH_auth=|).*?)[, ;]', re.S)
        content = re.findall(reg, response_cookie_str)
        set_cookie_params_dict = {one.split('=')[0]:one.split('=')[1] for one in content if len(one.split('='))==2 }

        # 插入cookie
        login_header['Cookie'] += 'UTH_sid=' + set_cookie_params_dict['UTH_sid'] + '; '
        login_header['Cookie'] += 'UTH_auth=' + set_cookie_params_dict['UTH_auth'] + '; '

        # 签到模块
        sigin_response = requests.post(sigin_url, headers=login_header, data= sigin_post_params)
        print(sigin_response.text)
    else:
        tools_auto_sigin()
    
    
if __name__ == '__main__':
    sched.add_job(tools_auto_sigin, 'cron', year='*', month='*', day='*', hour=str(random.randrange(24)), minute='00', second='00')
    sched.start()
