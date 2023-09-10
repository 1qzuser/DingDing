import requests

def checkin_with_push(Email, passwd, SCKEY):
    url = "https://go.runba.cyou/auth/login"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.69'
    }
    data = {
        "email": Email,
        "passwd": passwd
    }
    resp = requests.post(url, headers=headers, data=data)
    to_set_cookie = requests.utils.dict_from_cookiejar(resp.cookies)
    if not (resp.status_code == 200 and resp.json().get('ret') == 1):
        print("登录失败", resp.text)
        exit(0)
    else:
        print('用户==>', to_set_cookie.get('email'), '登录成功')
    checkin_url = "https://go.runba.cyou/user/checkin"
    resp2 = requests.post(checkin_url, headers=headers, cookies=to_set_cookie)
    if resp2.status_code == 200:
        if resp2.json().get("ret") == 1:
            print("*" * 10 + "签到成功" + 10 * "*")
            print("签到获得流量==>", resp2.json().get('msg'))
            print("剩余流量==>", resp2.json().get('trafficInfo').get('unUsedTraffic'))
            print("已经使用==>", resp2.json().get('trafficInfo').get('lastUsedTraffic'))
            print("今日使用==>", resp2.json().get('trafficInfo').get('todayUsedTraffic'))
            # 进行推送
            if SCKEY != '':
                push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, resp2.json().get('msg'))
                requests.post(url=push_url)
                print('推送成功')
        else:
            print(resp2.json().get("msg"))
    return resp2

checkin_with_push('1366565528@qq.com', 'cyx2174324', 'SCT179362T7SSeEEZcUVRSyTxPTt6YiYtS')
