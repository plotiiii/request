"""
-- coding: utf-8 --
@Time : 2020/4/15 23:32
@Author : jcoool
@Site : 
@File : test_user_login.py
@Software: PyCharm
"""
import os
import unittest

from requests import request
from jiekoucs.common.handle_logging import log
from jiekoucs.common.handle_data import HandleData
from jiekoucs.common.handle_db import HandleMysql
from jiekoucs.common.handle_docker import EnvData, replace_data
from jiekoucs.common.handle_excel import HandleExcel
from jiekoucs.common.handle_path import DATA_DIR
from jiekoucs.library.myddt import ddt, data

@ddt
class RegisterTestLogin(unittest.TestCase):
    filename = os.path.join(DATA_DIR, 'apicases.xlsx')
    excel = HandleExcel(filename, "login")
    cases = excel.read_data()
    db = HandleMysql()
    random_data = HandleData()

    @data(*cases)
    def test_login(self, case):
        # 第一步：准备用例数据
        # 请求方法
        method = case["method"]
        # 请求地址
        url = case["url"]
        # 请求参数
        data = eval(case["data"])
        # 预期结果
        expected = eval(case["expected"])
        # 用例所在行
        row = case["case_id"] + 1
        # 第二步：发送请求获取实际结果
        response = request(method=method, url=url, json=data)
        # 获取实际结果
        res = response.json()

        print("预期结果：", expected)
        print("实际结果：", res)
        # 第三步：断言
        try:
            # 若响应中有token则代表登录成功，断言响应的username
            if 'token' in res:
                self.assertEqual(expected["username"], res["username"])
            # 无token代表登录失败，断言失败结果
            else:
                self.assertEqual(expected,res)
        except AssertionError as e:
            # 结果回写excel中
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug("预期结果：{}".format(expected))
            log.debug("实际结果：{}".format(res))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value="未通过")
            raise e
        else:
            # 结果回写excel中
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")

if __name__ == '__main__':
    pass

