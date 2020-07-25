"""
-- coding: utf-8 --
@Time : 2020/4/16 0:48
@Author : jcoool
@Site : 
@File : test_05interface.py
@Software: PyCharm
"""
import os
import unittest
import jsonpath
import decimal
from jiekoucs.library.myddt import ddt, data
from jiekoucs.common.handle_excel import HandleExcel
from jiekoucs.common.handle_path import DATA_DIR
from jiekoucs.common.handle_config import conf
from jiekoucs.common.handle_logging import log
from jiekoucs.common.handle_db import HandleMysql
from requests import request
from jiekoucs.common.handle_data import HandleData
from jiekoucs.common.handle_docker import EnvData,replace_data
from jiekoucs.testcase.test_03create_login import TestBase

@ddt
class TestInterfaces(unittest.TestCase,TestBase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlsx"), "interface")
    cases = excel.read_data()
    random_data = HandleData()
    db = HandleMysql()

    @classmethod
    def setUpClass(cls):
        TestBase.login()

    @data(*cases)
    def test_interfaces(self, case):

        # 第一步：准备用例数据
        url = case['url']
        method = case["method"]
        # 准备用例参数
        # 替换参数中的用户id
        # 准备请求头
        headers = eval(conf.get("interface", "headers"))
        headers["Authorization"] = getattr(EnvData,"token")
        row = case["case_id"] + 1
        if '#interface#' in case['data'] or '#interface#' in case['expected']:
            setattr(EnvData, 'interface', self.random_data.random_name())
            data = eval(replace_data(case["data"]))
            expected = eval(replace_data(case["expected"]))
        else:
            data = eval(case['data'])
            expected = eval(case['expected'])
        # 第二步： 发送请求获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        if 'create_time' in res:
            res_project = res['project']
            setattr(EnvData, "project",res_project)
        print(res)


        # 第三步：断言预期结果和实际结果
        try:
            # 若需要校验数据库则判断数据库提取的id和name与输入数据断言
            if case["check_sql"]:
                expected_sql = replace_data(case["check_sql"])
                project_name = self.db.find_one(expected_sql)["name"]
                self.assertEqual(res['project'], project_name)
                self.assertEqual(expected["tester"], res["tester"])
            # 不需要校验数据库则通过响应和期望断言
            else:
                self.assertEqual(expected, res)
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