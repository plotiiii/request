"""
-- coding: utf-8 --
@Time : 2020/4/15 23:56
@Author : jcoool
@Site : 
@File : test_create_login.py
@Software: PyCharm
"""
import jsonpath
from requests import request

from jiekoucs.common.handle_config import conf
from jiekoucs.common.handle_docker import EnvData


class TestBase:

    @staticmethod
    def login():
        """用例执行的前置条件：登录"""
        # 准备登录的相关数据
        url = conf.get("login", "url")
        data = {
            "username": conf.get("login", "username"),
            "password": conf.get("login", "password")
        }
        post = conf.get('login', 'post')
        response = request(method=post, url=url, json=data)
        res = response.json()
        token = "JWT" + " " + jsonpath.jsonpath(res, "$..token")[0]
        # 将提取出来的数据保存为EnvData这个类的属性（环境变量）
        setattr(EnvData, "token", token)
if __name__ == '__main__':
    a = TestBase.login()
    print(a)