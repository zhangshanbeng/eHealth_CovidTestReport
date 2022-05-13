import datetime
import json
import time
import requests
from sendmail import send_email

headers_jsstm = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
headers_jshscx = {'Content-Type': 'application/json;charset=UTF-8'}


def get_abc() -> str:
    data = {
        'token': 'YOUR_SKM_TOKEN',
        'uuid': 'YOUR_SKM_UUID',
    }
    user_auth_token = 'https://jsstm.jszwfw.gov.cn/jkm/2/userAuth_token'
    with requests.post(user_auth_token, headers=headers_jsstm, data=data) as res:
        return res.json()['res']['userdetail']['abc']


def get_secret(abc: str) -> str:
    query_drhs = 'https://jsstm.jszwfw.gov.cn/jkm/2/queryDrHs'
    data = {'idType': '1', 'abc': abc}
    with requests.post(query_drhs, headers=headers_jsstm, data=data) as res:
        url = str(res.json()['res']['url'])
        return url.split('?secret=')[-1]


def auth_secret(secret: str) -> dict:
    rna_auth = 'https://jshscx.jsehealth.com:8002/app-backend/rna/authentication'
    data = {'secret': secret}
    with requests.post(rna_auth, headers=headers_jshscx, data=json.dumps(data)) as res:
        id_type = res.json()['data']['idType']
        id_card = res.json()['data']['idCard']
        headers_jshscx['secret'] = secret
        return {'idType': id_type, 'idCard': id_card}


def query_report(data: dict) -> list:
    query_rna_report = 'https://jshscx.jsehealth.com:8002/app-backend/rna/queryRnaReport'
    with requests.post(query_rna_report, headers=headers_jshscx, data=json.dumps(data)) as res:
        report_list = res.json()['data']['reportList']
        return report_list


def get_report() -> list:
    abc = get_abc()
    secret = get_secret(abc)
    auth_info = auth_secret(secret)
    report = query_report(auth_info)
    return report


def judge_report(report: list, dateFlag: int):
    if report[0]['timeFlag'] >= dateFlag:
        # 可选项，发送邮件，当然你也可以选择Server酱or企业微信BOT等
        send_email('核酸结果已出', str(report[0]), 'YOUR_EMAIL_ADDRESS')
        return True
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{now} 核酸结果未出')
        return False


if __name__ == '__main__':
    my_report = get_report()
    # my_dateFlag可以设置为你核酸采集那天的0点
    # 例如：我在2022年1月1日的15时20分做了一次核酸
    # 那么my_dateFlag就可以设置为202201010000
    my_dateFlag = 202201010000
    
    while True:
        if judge_report(my_report, my_dateFlag):
            break
        time.sleep(60)
        my_report = get_report()
    print('核酸结果已出')
