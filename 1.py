# !/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import time
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from email.header import Header

import requests
import datetime

domain = 'https://api19.51yund.com'
form_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    # "content-type": "application/x-www-form-urlencoded",
}

# Email:
EMAIL_USE_TLS = False  # 是否使用TLS安全传输协议
EMAIL_USE_SSL = True  # 是否使用SSL加密，qq企业邮箱要求使用
# SMTP地址
EMAIL_HOST = 'smtp.sina.com'
# SMTP端口
EMAIL_PORT = 465
# 自己的邮箱
EMAIL_HOST_USER = 'lzjpython@sina.com'
# 自己的邮箱授权码，非密码
EMAIL_HOST_PASSWORD = '1991630da76fdd8c'
EMAIL_SUBJECT_PREFIX = '[lzjpython的博客]'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

users_list = {
    289149607: {
        'platform_conf': [{'amount': 200, 'platform': 1}],
        'email': '956573391@qq.com',
        'sub_email': True,
    },
}


def send_mail(to_address_list, subject, message):
    """
    :param message: str 邮件内容
    :param subject: str 邮件主题描述
    :param to_address_list: str 实际收件人
    """
    # 填写真实的发邮件服务器用户名、密码
    # 邮件内容
    msg = MIMEText(message, 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = Header(EMAIL_SUBJECT_PREFIX + subject, charset='utf-8')
    # 发件人显示
    msg["From"] = Header(EMAIL_HOST_USER)
    # 收件人显示
    msg["To"] = Header(to_address_list[0])
    with SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT) as smtp:
        # 登录发邮件服务器
        smtp.login(user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=EMAIL_HOST_USER, to_addrs=to_address_list, msg=msg.as_string())
    print(f'发送邮件完毕：收件人{to_address_list}')


def post(url, data):
    print(url, data)
    user_id = data['user_id']

    user_conf = users_list[user_id]
    data['session_from'] = 1
    data['timestamp'] = time.time()
    raw_data = f', url:{url}, data:{str(data)}'

    sub_email = user_conf.get('sub_email')
    email = user_conf.get('email')
    subject = '悦动圈早起打卡脚本'
    try:
        response = requests.post(url, data=data, headers=form_headers)
        if response.status_code == 200:
            res = response.json()
            if res['code'] != 0:
                msg = f'[正常响应]响应:{res}'
            else:
                msg = f'[异常响应]响应:{res}'

            if email and sub_email:
                send_mail([email], subject, msg + raw_data)
            print(res)

        else:
            msg = f'[状态码异常]status_code:{response.status_code}'
            print(msg)
            send_mail(['956573391@qq.com'], subject, msg + raw_data)
    except Exception as e:
        msg = f'[程序异常]Exception:{str(e)}'
        print(msg)
        send_mail(['956573391@qq.com'], subject, msg + raw_data)
    print('{}==============='.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


def do(users, go_to):
    uri = '/yd_punch_clock/' + go_to

    for user_id, item in users.items():
        platform_conf_list = item['platform_conf']
        for platform_conf in platform_conf_list:
            form_data = {"user_id": user_id}
            if go_to == 'clock_sign_up':
                form_data.update(platform_conf)
                form_data["platform"] = platform_conf['platform']
                form_data["amount"] = platform_conf['amount']
            elif go_to == 'punch_clock':
                form_data["platform"] = platform_conf['platform']
            post(domain + uri, data=form_data)
            time.sleep(random.randint(30, 180))
        time.sleep(get_random_time())


def get_random_time():
    return random.randint(60, 60 * 10)


if __name__ == '__main__':
    argv = sys.argv
    if argv:
        do(users_list, argv[1])
