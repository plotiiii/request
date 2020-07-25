"""
-- coding: utf-8 --
@Time : 2020/4/4 21:59
@Author : jcoool
@Site : 
@File : handle_phone.py
@Software: PyCharm
"""
import datetime
import random

from jiekoucs.common.handle_db import HandleMysql


class HandleData():
    def random_phone(self):
        """生成一个数据库里面未注册的手机号码"""
        db = HandleMysql()
        while True:
            phone = '13'
            for i in range(9):
                num = str(random.randint(0, 9))
                phone += num
            sql = "SELECT * FROM futureloan.member WHERE mobile_phone={}".format(phone)
            res = db.find_count(sql)
            if res == 0:
                return phone

    def random_name(self):
        """生成一个数据库中允许的随机名字"""
        db = HandleMysql()
        name = 'jcool'
        for i in range(5):
            num = str(random.randint(0, 9))
            name += num
        return name

    def token_jiaoyan(self, user_token):
        return 'Bearer' + ' ' + user_token

    def random_email(self):
        """生成一个随机邮箱"""
        name = 'jcol'
        for i in range(5):
            num = str(random.randint(0, 9))
            name += num
        name += '@qq.com'
        return name

    @classmethod
    def Current_time(cls):
        a = datetime.datetime.now()
        return a.strftime('%Y-%m-%d-%H-%M-%S')


if __name__ == '__main__':
    a = HandleData()
    b = a.Current_time()
    print(b)
