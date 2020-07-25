"""
-- coding: utf-8 --
@Time : 2020/4/14 21:37
@Author : jcoool
@Site : 
@File : run_test.py
@Software: PyCharm
"""
import unittest
from BeautifulReport import BeautifulReport
from jiekoucs.common.handle_logging import HandleLogger
from jiekoucs.common.handle_data import HandleData
from jiekoucs.common.handle_path import CASE_DIR,REPORT_DIR
# log = HandleLogger.create_logger()

current_time = HandleData.Current_time()
current_time += '.html'
# log.info("---------------开始执行测试用例-----------------------")
# 创建测试套件
suite =  unittest.TestSuite()

# 加载用例到套件
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASE_DIR))

# 执行用例生成报告
bf = BeautifulReport(suite)

bf.report("注册接口",filename=current_time,report_dir=REPORT_DIR)


# log.info('---------------测试用例执行完毕-----------------------')
