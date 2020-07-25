"""
-- coding: utf-8 --
@Time : 2020/4/16 1:37
@Author : jcoool
@Site : 
@File : test_06testcase.py
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
class TestRecharge(unittest.TestCase,TestBase):
    excel = HandleExcel(os.path.join(DATA_DIR, "apicases.xlsx"), "testcases")
    cases = excel.read_data()
    random_data = HandleData()
    db = HandleMysql()
    @classmethod
    def setUpClass(cls):
        TestBase.login()

    @data(*cases)
    def test_testcases(self, case):
        # 第一步：准备用例数据
        url = case['url']
        method = case["method"]
        # 准备用例参数
        # 替换参数中的用户id
        # 准备请求头
        headers = eval(conf.get("create_project", "headers"))
        headers["Authorization"] = getattr(EnvData,"token")
        row = case["case_id"] + 1
        # if判断数据中是否需要替换数据
        if '#username#' in case['data'] or '#username#' in case['expected']:
            setattr(EnvData, 'username', self.random_data.random_name())
            expected = eval(replace_data(case["expected"]))
            data = eval(replace_data(case["data"]))
        # 若没有则正常提取
        else:
            data = eval(case['data'])
            expected = eval(case["expected"])
        # 第二步： 发送请求获取实际结果
        response = request(url=url, method=method, json=data, headers=headers)
        res = response.json()
        # 通过id判断是否登录成功 若登录成功则获取
        if 'id' in res:
            response_id = str(res['id'])
        # 第三步：断言预期结果和实际结果
        try:
            # 若需要校验数据库则判断数据库提取的id和name与输入数据断言
            # 判断是否需要进行sql校验
            if case['check_sql']:
                # 替换随机生成的用户名，用于数据库查询
                case['check_sql'] = replace_data(case['check_sql'])
                sql = self.db.find_one(case['check_sql'])
                # 数据库中提取用户名和邮箱
                sql_id = str(sql['id'])
                sql_name = sql['name']
                # 将随机生成的用户名和邮箱与数据库中创建成功数据进行断言
                self.assertEqual(response_id, sql_id)
                self.assertEqual(expected['name'], sql_name)
                print('响应的id:{}和:数据库查询到的id:{}'.format(response_id, sql_id))
                print('根据创建用户名查询数据库得到的用户名:{}和:邮箱{}'.format(expected['name'], sql_name))
                # 不需要校验数据库则通过响应和期望断言
            else:
                self.assertEqual(res, expected)
                print('期望返回的数据是:{} \n 响应返回的数据是：{}'.format(res, expected))

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
