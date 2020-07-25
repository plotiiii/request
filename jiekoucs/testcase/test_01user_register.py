"""
-- coding: utf-8 --
@Time : 2020/4/14 22:41
@Author : jcoool
@Site : 
@File : test_user_register.py
@Software: PyCharm
"""
import os
import unittest

from requests import request

from jiekoucs.common.handle_data import HandleData
from jiekoucs.common.handle_db import HandleMysql
from jiekoucs.common.handle_docker import EnvData, replace_data
from jiekoucs.common.handle_excel import HandleExcel
from jiekoucs.common.handle_logging import log
from jiekoucs.common.handle_path import DATA_DIR
from jiekoucs.library.myddt import ddt, data


@ddt
class RegisterTestCase(unittest.TestCase):
    filename = os.path.join(DATA_DIR, 'apicases.xlsx')
    excel = HandleExcel(filename, "register")
    cases = excel.read_data()
    db = HandleMysql()
    random_data = HandleData()

    @data(*cases)
    def test_register(self, case):
        # 提取url、method、row、expected
        url = case['url']
        method = case['method']
        row = case["case_id"] + 1
        expected = eval(case['expected'])
        # 生成动态函数 写入随机名字、邮箱
        setattr(EnvData, 'username', self.random_data.random_name())
        setattr(EnvData, 'email', self.random_data.random_email())
        # 若data里面有#username#、#email#
        if '#username#' in case['data'] or '#email#' in case['data']:
            data = eval(replace_data(case["data"]))
        response = request(url=url, method=method, json=data).json()
        try:
            # 判断是否需要进行sql校验
            if case['check_sql']:
                # 替换随机生成的用户名，用于数据库查询
                case['check_sql'] = case['check_sql'].replace('#username#', getattr(EnvData, 'username'))
                sql = self.db.find_one(case['check_sql'])
                # 数据库中提取用户名和邮箱
                sql_username = sql['username']
                sql_email = sql['email']
                # 将随机生成的用户名和邮箱与数据库中创建成功数据进行断言
                self.assertEqual(getattr(EnvData, 'username'), sql_username)
                self.assertEqual(getattr(EnvData, 'email'), sql_email)
                print('创建随机生成的用户名:{}和:邮箱{}'.format(getattr(EnvData, 'username'), getattr(EnvData, 'email')))
                print('根据创建用户名查询数据库得到的用户名:{}和:邮箱{}'.format(sql_username, sql_email))
            else:
                self.assertEqual(response, expected)
                print('期望返回的数据是:{} \n 响应返回的数据是：{}'.format(response, expected))
        except AssertionError as e:
            # 结果回写excel中
            log.error("用例--{}--执行未通过".format(case["title"]))
            log.debug('创建随机生成的用户名{}和邮箱{}'.format(getattr(EnvData, 'username'), getattr(EnvData, 'email')))
            log.debug('根据创建用户名查询数据库得到的用户名{}和邮箱{}'.format(sql_username, sql_email))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value="未通过")
            raise e
        else:
            # 结果回写excel中
            log.info("用例--{}--执行通过".format(case["title"]))
            self.excel.write_data(row=row, column=8, value="通过")


if __name__ == '__main__':
    pass
