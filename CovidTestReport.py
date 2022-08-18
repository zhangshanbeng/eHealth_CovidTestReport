import datetime
import json
import time
import requests
from sendmail import send_email

headers_jsstm = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
headers_jshscx = {'Content-Type': 'application/json;charset=UTF-8'}


class SKM:
    def __init__(self, token: str, uuid: str):
        self.token = token
        self.uuid = uuid
        self.abc = self.get_abc()

    def get_abc(self) -> str:
        user_auth_token = 'https://jsstm.jszwfw.gov.cn/jkm/2/userAuth_token'
        data = {
            'token': self.token,
            'uuid': self.uuid
        }
        with requests.post(user_auth_token, headers=headers_jsstm, data=data) as res:
            res_json = res.json()
            if res_json['resCode'] == 0:
                return res_json['res']['userdetail']['abc']

    # 江苏卫健委接口
    # 通过苏康码abc字段获取卫健委secret令牌，验证后获取最近的核酸数据(多条)
    def query_latest_report_by_jsehealth(self) -> dict:
        """
        :return: {'id': None, 'cardNo': '', 'name': '', 'collectUnit': '', 'collectTime': '2022-07-07 07:07', 'checkUnit': '', 'checkTime': None, 'checkResult': '阴性', 'area': '', 'collectCity': '', 'timeFlag': 202207070707}
        """
        secret = get_secret(self.abc)
        auth_info = auth_secret(secret)
        report = query_report(auth_info)
        return report[0]

    # 苏康码接口
    # 只需要abc字段即可，但是只能获取最近一次核酸数据
    def query_hs_by_jsstm(self) -> dict:
        """
        :return: {'area': '', 'collectTime': '2022-07-07 07:07', 'collectUnit': '', 'collectCity': '', 'checkResult': '阴性', 'checkUnit': ''}
        """
        url = 'https://jsstm.jszwfw.gov.cn/healthCode/queryHs'
        data = {'abc': self.abc}
        with requests.post(url, headers=headers_jsstm, data=data) as res:
            res_json = res.json()
            if res_json['resCode'] == 0:
                return res_json['res']['hs']


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


def read_config() -> dict:
    with open('config.json', 'r') as f:
        return json.load(f)


def str2timestamp(time_str: str) -> int:
    time_struct = time.strptime(time_str, '%Y-%m-%d %H:%M')
    return int(time.mktime(time_struct))


if __name__ == '__main__':
    config = read_config()
    # 苏康码token
    token = config['token']
    # 苏康码uuid
    uuid = config['uuid']
    # 日期
    time_point = str2timestamp(config['time'])
    # 是否发送邮件
    is_send_email = config['need_mail']
    if is_send_email:
        # 邮件接收者
        receiver = config['receiver']
    # 查询间隔
    interval = config['interval']

    user = SKM(token, uuid)
    # 使用苏康码接口
    latest_report = user.query_hs_by_jsstm()

    while True:
        collect_time = str2timestamp(latest_report['collectTime'])
        if collect_time >= time_point:
            print('核酸结果已出')
            print(latest_report)
            if is_send_email:
                send_email('核酸结果已出', str(latest_report), receiver)
            break
        else:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{now} 核酸结果未出')
            latest_report = user.query_hs_by_jsstm()
            time.sleep(interval)
