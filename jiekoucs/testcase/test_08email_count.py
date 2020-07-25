"""
-- coding: utf-8 --
@Time : 2020/4/16 20:51
@Author : jcoool
@Site : 
@File : test_08user_email.py
@Software: PyCharm
"""
import os
import unittest
from jiekoucs.library.myddt import ddt, data
from jiekoucs.common.handle_excel import HandleExcel
from jiekoucs.common.handle_path import DATA_DIR
from jiekoucs.common.handle_config import conf
from jiekoucs.common.handle_logging import log
from requests import request
from jiekoucs.common.handle_data import HandleData
from jiekoucs.common.handle_docker import EnvData,replace_data
from jiekoucs.common.handle_db import HandleMysql
from jiekoucs.testcase.test_03create_login import TestBase

@ddt
class Test_email_count(unittest.TestCase,TestBase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlsx"), "email_count")
    cases = excel.read_data()
    random_data = HandleData()
    db = HandleMysql()
    @classmethod
    def setUpClass(cls):
        TestBase.login()

    @data(*cases)
    def test_testcases(self, case):
        # 第一步：准备用例数据
        # if判断数据中是否需要替换数据
        if '#email#' in case['url'] or '#email#' in case['expected']:
            setattr(EnvData, 'email', self.random_data.random_email())
            expected = eval(replace_data(case["expected"]))
            url = replace_data(case["url"])
        else:
            # 若没有则正常提取
            url = case['url']
            expected = eval(case["expected"])
        headers = eval(conf.get("create_project", "headers"))
        headers["Authorization"] = getattr(EnvData, "token")
        method = case["method"]
        # 准备用例参数
        # 替换参数中的用户id
        # 准备请求头
        row = case["case_id"] + 1
        # 第二步： 发送请求获取实际结果
        response = request(url=url, method=method,headers=headers)
        res = response.json()
        # 第三步：断言预期结果和实际结果
        try:
                # 将随机生成的用户名和邮箱与数据库中创建成功数据进行断言
                self.assertEqual(expected['count'], res['count'])
                self.assertEqual(expected['email'], res['email'])
                print('期望的数据:{}和:响应的数据:{}'.format(expected ,res))

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