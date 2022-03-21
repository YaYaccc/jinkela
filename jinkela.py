# -*- coding: utf-8 -*
# !/usr/bin/env python
import smtplib
import time
from email.mime.text import MIMEText
# from imp import reload

import requests
import json
import pymysql

# linux专用
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


# 邮件通知
from lxml import etree

import os

# 需要代理才能登入
# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"


def getInformation(s):
    response = s.get("https://v2.jinkela.link/user", headers=header)
    tree = etree.HTML(response.text)
    Hi_name = tree.xpath("//div[@class='d-sm-none d-lg-inline-block']/text()")[0]
    bodyList = tree.xpath("//span[@class='counter']/text()")
    daysRemaining = int(bodyList[0])
    gbRemaining = float(bodyList[1])
    content = "%s\n剩余天数:%s\n剩余流量:%sGB\n每天可以用%sGb哦" % (
        Hi_name, daysRemaining, gbRemaining, int(gbRemaining / daysRemaining))
    return content


def checkin(s):
    try:
        checkinUrl = "https://v2.jinkela.link/user/checkin"
        response = s.post(checkinUrl, headers=header)
        inJson = json.loads(response.text)
        msg = inJson["msg"]
        print(msg)
        if inJson["ret"] == 1:
            return True, msg
        else:
            return False, msg
    except(requests.exceptions.ConnectionError, NameError):
        return False, msg


def login():
    try:
        loginUrl = "https://v2.jinkela.link/auth/login"
        data = {
            "email": "登入邮箱",
            "passwd": "密码"
        }
        s = requests.session()
        s.get("https://v2.jinkela.link/")
        time.sleep(30)
        s.post(loginUrl, headers=header, json=data)
        # s.post(loginUrl, headers=header, json=data)
        checkin(s)

    except(requests.exceptions.ConnectionError, NameError):
        print("连接错误")


if __name__ == '__main__':
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    login()
